from __future__ import annotations

from typing import List, Dict, Any
from pathlib import Path
import hashlib, json, shutil

import streamlit as st
import faiss                              
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document as LCDocument
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_anthropic import ChatAnthropic  
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
import pandas as pd, json, io

from utils import (
    log_time,
    prefix_documents_for_e5,
    count_tokens,
    #extract_metadata,
    format_response,
)

# ═══════════ CONFIG ═══════════
DATA_FOLDER      = Path("data")
DOCUMENTS_FOLDER = DATA_FOLDER / "documentos"
INDEX_FOLDER     = DATA_FOLDER / "indexes"
INDEX_FOLDER.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large"
LLM_MODEL_NAME = "claude-sonnet-4-20250514"
TOKEN_LIMIT          = 7000


# ═════ Wrapper de saída ═════
class RagChainWrapper:
    def __init__(self, chain, template: str):
        self._chain    = chain
        self._template = template

    def invoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        approx = count_tokens(
            self._template.format(context="", input=inputs.get("input", "")),
            model_name=EMBEDDING_MODEL_NAME,
        )
        if approx > TOKEN_LIMIT:
            st.warning(f"⚠️ Prompt estimado em {approx} tokens (limite {TOKEN_LIMIT}).")

        output = self._chain.invoke(inputs)

      
        # if "context" in output:
        #     st.write("🔍 Documentos recuperados:")
        #     for doc in output["context"]:
        #         st.write(f"{extract_metadata(doc)} — {doc.page_content}")

        if "answer" in output:
            output["answer"] = format_response(output["answer"])
        return output

    __call__ = invoke


# ═════ Utilidades ═════
def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _new_empty_index(embeddings: HuggingFaceEmbeddings) -> faiss.Index:
    """Cria um IndexFlatL2 vazio com a dimensão correta."""
    dim = len(embeddings.embed_query(""))
    return faiss.IndexFlatL2(dim)


# ═════ Carregar PDF ═════
@log_time
def load_documents_with_docling(
    file_path: str,
    export_type: ExportType = ExportType.DOC_CHUNKS,
) -> List[LCDocument]:
    return DoclingLoader(file_path=file_path, export_type=export_type).load()


# ═════ Criar / Carregar Vectorstore ═════
@log_time
def create_or_load_vectorstore(
    documents : List[LCDocument],
    embeddings: HuggingFaceEmbeddings,
    index_name: str,
    file_path : str | None = None,
) -> FAISS | None:
    """
    • Carrega o índice se todos os arquivos existirem.
    • Se faltar index.faiss ou index.pkl → recria a partir dos documentos.
    • Dedup de arquivo (hash) e de chunk (md5).
    """
    index_path  = INDEX_FOLDER / f"{index_name}_faiss_index"
    index_file  = index_path / "index.faiss"
    pkl_file    = index_path / "index.pkl"
    meta_path   = index_path / "metadata.json"

    # ───────── criar diretório, se necessário
    index_path.mkdir(parents=True, exist_ok=True)

    # ───────── existe um índice VÁLIDO?
    has_full_index = index_file.exists() and pkl_file.exists()

    if has_full_index:
        try:
            vs = FAISS.load_local(
                str(index_path), embeddings,
                allow_dangerous_deserialization=True,
            )
        except Exception:
            st.warning("🛠️ Índice corrompido — recriando.")
            shutil.rmtree(index_path, ignore_errors=True)
            index_path.mkdir(parents=True, exist_ok=True)
            has_full_index = False

    # ───────── se não existe índice, precisamos de documentos
    if not has_full_index:
        if not documents:
            st.error("Nenhum chunk disponível para criar o índice.")
            return None
        vs = FAISS.from_documents(documents, embeddings)
        vs.save_local(str(index_path))
        # registra hash do primeiro PDF
        if file_path:
            meta_path.write_text(json.dumps([_sha256_file(Path(file_path))]))
        return vs                # índice criado → nada mais a fazer

    # ───────── deduplicação (arquivo e chunk)
    pdf_hash = _sha256_file(Path(file_path)) if file_path else None
    processed = (
        set(json.loads(meta_path.read_text())) if meta_path.exists() else set()
    )

    if pdf_hash and pdf_hash in processed:
        st.info("📄 Documento já indexado — pulando.")
        return vs

    existing_ids = set(vs.docstore._dict.keys())
    new_docs: list[LCDocument] = []

    for d in documents:
        cid = hashlib.md5(d.page_content.encode()).hexdigest()
        if cid not in existing_ids:
            d.metadata["chunk_id"] = cid
            new_docs.append(d)

    if new_docs:
        vs.add_documents(new_docs)
        vs.save_local(str(index_path))
        st.success(f"✅ {len(new_docs)} novos chunks adicionados.")
        if pdf_hash:
            processed.add(pdf_hash)
            meta_path.write_text(json.dumps(list(processed)))

    return vs


# ═════ Construir cadeia RAG ═════
def create_rag_chain(vectorstore: FAISS) -> RagChainWrapper:
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 20, "fetch_k": 100, "lambda_mult": 0.8},
    )

    llm = ChatAnthropic(
        temperature=0.1,
        model_name=LLM_MODEL_NAME,
        api_key=st.secrets["ANTHROPIC_API_KEY"],       # 👈 usa a chave adicionada em .streamlit/secrets.toml
        max_tokens=1000,
    )

    template = """
Você é um assistente jurídico especializado.
Analise cuidadosamente o contexto e responda de forma objetiva.
Resposta sempre em Português Brasil.
Não responda em inglês.
Responda sempre com uma formatação de texto única, com seperação e espaços corretos entre as palavras.

Se não souber, diga: "Não encontrei informações suficientes no documento."

<context>
{context}
</context>

Pergunta: {input}

Resposta:
"""
    prompt          = ChatPromptTemplate.from_template(template)
    doc_chain       = create_stuff_documents_chain(llm=llm, prompt=prompt)
    retrieval_chain = create_retrieval_chain(retriever, doc_chain)
    return RagChainWrapper(retrieval_chain, template)


# ═════ Pipeline público ═════
# rag_pipeline.py  –  somente a função process_document() atualizada
# (o restante do arquivo permanece igual)

@log_time
def process_document(file_path: str, index_name: str) -> RagChainWrapper:
    # 1 ───── Texto normal (DOC_CHUNKS)
    docs_texto = load_documents_with_docling(
        file_path,
        export_type=ExportType.DOC_CHUNKS
    )

    # 2 ───── Tabelas em JSON (se a versão do Docling permitir)
    TABLES_JSON = getattr(ExportType, "TABLES_AS_JSON", None)

    if TABLES_JSON:
        docs_tabelas = load_documents_with_docling(
            file_path,
            export_type=TABLES_JSON
        )
    else:
        # fallback para versões antigas  ➜ converte cada tabela “na mão”
        docs_tabelas = []
        for d in docs_texto:
            if d.metadata.get("subtype") == "table":
        
                df = pd.read_csv(io.StringIO(d.page_content))
                d_json = LCDocument(
                    page_content=json.dumps(
                        df.to_dict(orient="records"),
                        ensure_ascii=False
                    ),
                    metadata=d.metadata | {"note": "converted_to_json"}
                )
                docs_tabelas.append(d_json)

        # remove as tabelas originais duplicadas do bloco de texto
        docs_texto = [
            d for d in docs_texto
            if d.metadata.get("subtype") != "table"
        ]

    # 3 ───── Combina texto + tabelas
    docs = docs_texto + docs_tabelas

    # 4 ───── Prefixa para embeddings E5
    docs = prefix_documents_for_e5(docs)

    # 5 ───── Embeddings + vectorstore
    embeddings = HuggingFaceEmbeddings(
        model_name   = EMBEDDING_MODEL_NAME,
        encode_kwargs={"batch_size": 32},
    )
    vs = create_or_load_vectorstore(docs, embeddings, index_name, file_path)

    # 6 ───── Cadeia RAG pronta
    return create_rag_chain(vs)
