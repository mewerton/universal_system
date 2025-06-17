from __future__ import annotations

from pathlib import Path
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from rag_pipeline import create_rag_chain, process_document

EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large"


def rag_section(titulo: str, index_name: str, pasta_docs: Path) -> None:
    """Widget de Q&A + upload de PDFs isolado por módulo."""
    st.markdown(f"## {titulo}")

    INDEX_PATH = Path("data/indexes") / f"{index_name}_faiss_index"

    # ────────────────────────────────────────────────────────────
    # 1) Carrega índice existente (cachê separado por caminho)
    # ────────────────────────────────────────────────────────────
    @st.cache_resource(show_spinner="🔄 Carregando índice…")
    def _load_existing(index_path_str: str):
        path = Path(index_path_str)
        if not (path / "index.faiss").exists() or not (path / "index.pkl").exists():
            return None
        emb = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        vs  = FAISS.load_local(
            index_path_str,
            emb,
            allow_dangerous_deserialization=True,
        )
        return create_rag_chain(vs)

    # cache em session_state, independente de outros módulos
    key_rag = f"rag_{index_name}"
    if key_rag not in st.session_state:
        st.session_state[key_rag] = _load_existing(str(INDEX_PATH))

    rag = st.session_state[key_rag]

    # ───────────────────────── 2) Caixa de perguntas ─────────────────────────
    if rag is not None:
        pergunta = st.text_input(
            "Pergunte sobre os PDFs indexados:",
            key=f"ask_{index_name}",
        )
        if pergunta:
            resp = rag({"input": pergunta}).get("answer", "")
            st.markdown("### Resposta:")
            st.write(resp or "Não foi possível responder.")

    st.divider()

    # ───────────────────────── 3) Upload + processamento ────────────────────
    uploaded = st.file_uploader(
        "📎 Envie um novo PDF:",
        type="pdf",
        key=f"upload_{index_name}",
    )

    if uploaded:
        pasta_docs.mkdir(parents=True, exist_ok=True)
        destino = pasta_docs / uploaded.name
        with open(destino, "wb") as f:
            f.write(uploaded.read())
        st.success(f"📄 '{uploaded.name}' salvo!")

        if st.button("🔍 Processar documento", key=f"btn_proc_{index_name}"):
            with st.spinner("Gerando embeddings…"):
                new_rag = process_document(str(destino), index_name)

            if new_rag:
                st.success("✅ Índice criado/atualizado!")
                st.session_state[key_rag] = new_rag        # substitui ↓
                rag = new_rag                              # mostra Q&A já
            else:
                st.error("Falha ao criar o índice.")
