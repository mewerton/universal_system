import streamlit as st
import pandas as pd
import plotly.express as px
# from rag_pipeline import process_document, create_rag_chain
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# import os
from pathlib import Path
from rag_section import rag_section

def exibir():
    st.title(" Módulo Atacado")
    st.markdown("Análise dos contratos de locação e planos de expansão de lojas do atacado.")

    # Carrega datasets
    try:
        contratos = pd.read_parquet("data/atacado/contratos_locacao_lojas.parquet")
        expansao = pd.read_csv("data/atacado/planos_expansao.csv", parse_dates=["Data_Inauguracao_Prevista"])
    except FileNotFoundError:
        st.error("Arquivos de dados não encontrados. Verifique se os arquivos estão na pasta `data/atacado`.")
        return

    # Gráfico 1: Mapa das lojas por estado
    st.subheader(" Mapa de distribuição das lojas por estado")
    mapa = contratos.groupby("Estado").size().reset_index(name="Quantidade de Lojas")
    fig_mapa = px.bar(
        mapa.sort_values("Quantidade de Lojas", ascending=True),
        x="Quantidade de Lojas",
        y="Estado",
        orientation="h",
        title="Quantidade de Lojas por Estado",
        color="Quantidade de Lojas",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_mapa, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        # Gráfico 2: Valor de aluguel por loja
        st.subheader(" Valor de aluguel por loja")
        fig_aluguel = px.bar(
            contratos.sort_values("Valor_Aluguel", ascending=False),
            x="Loja",
            y="Valor_Aluguel",
            title="Valor do Aluguel por Loja"
        )
        fig_aluguel.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_aluguel, use_container_width=True)

    with col2:
        # Gráfico 3: Valor por metro quadrado
        st.subheader(" Valor do aluguel por m²")
        fig_scatter = px.scatter(
            contratos,
            x="Area_m2",
            y="Valor_Aluguel",
            color="Estado",
            size="Valor_m2",
            hover_name="Loja",
            title="Valor de Aluguel vs Área por Estado"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Gráfico 4: Prazo de vigência dos contratos
    st.subheader(" Prazo de vigência dos contratos")
    contratos["Data_Inicio"] = pd.to_datetime(contratos["Data_Inicio"])
    contratos["Data_Fim"] = pd.to_datetime(contratos["Data_Fim"])
    contratos["Prazo_meses"] = ((contratos["Data_Fim"] - contratos["Data_Inicio"]) / pd.Timedelta(days=30)).round()
    fig_prazo = px.histogram(
        contratos,
        x="Prazo_meses",
        nbins=10,
        title="Distribuição do Prazo de Contratos (em meses)"
    )
    st.plotly_chart(fig_prazo, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        # Gráfico 5: Histórico de inaugurações por ano
        st.subheader(" Histórico de inaugurações previstas")
        expansao["Ano"] = expansao["Data_Inauguracao_Prevista"].dt.year
        inauguracoes = expansao.groupby("Ano").size().reset_index(name="Quantidade")
        fig_inauguracoes = px.line(
            inauguracoes,
            x="Ano",
            y="Quantidade",
            markers=True,
            title="Número de Inaugurações por Ano"
        )
        st.plotly_chart(fig_inauguracoes, use_container_width=True)

    with col2:
        # Gráfico 6: Índice de correção mais utilizado
        st.subheader(" Índice de correção mais utilizado")
        fig_indice = px.pie(
            contratos,
            names="Indice_Correcao",
            title="Distribuição dos Índices de Correção"
        )
        st.plotly_chart(fig_indice, use_container_width=True)


    # ---------- WIDGET RAG ----------
    rag_section(
        titulo     = "Assistente inteligente do Atacado",
        index_name = "atacado",
        pasta_docs = Path("data/documentos/atacado"),
    )


    # ------------------------------------------------------------------
    # ⬇️  NOVO BLOCO: tabela de “Tipos de Documentos” recomendados
    # ------------------------------------------------------------------
    st.divider()
    if st.button("📑 Tipos de Documentos"):
        # dados-base da tabela
        dados = [
            {
                "Categoria": "Contratos de Fornecimento & Compra",
                "Exemplos de PDF": "Contrato-quadro, aditivos de preço/prazo",
                "Por que ajudam": "Condições de pagamento, SLAs, multas",
                "Exemplo de pergunta": "Qual é a multa por atraso no contrato com o fornecedor X?"
            },
            {
                "Categoria": "Catálogo de Produtos",
                "Exemplos de PDF": "Catálogo comercial, tabela de preços",
                "Por que ajudam": "Busca rápida de SKU, cálculo de margens",
                "Exemplo de pergunta": "Qual o preço de lista do SKU ABC?"
            },
            {
                "Categoria": "Relatórios Operacionais",
                "Exemplos de PDF": "Relatório de vendas, giro de estoque",
                "Por que ajudam": "Perguntas de performance regional",
                "Exemplo de pergunta": "Quais foram os 3 estados com maior faturamento no 1º tri?"
            },
            {
                "Categoria": "Política Comercial",
                "Exemplos de PDF": "Política de descontos, devoluções",
                "Por que ajudam": "Normas claras para time comercial",
                "Exemplo de pergunta": "Qual o desconto máximo para a categoria de bebidas?"
            },
            {
                "Categoria": "Documentos Logísticos",
                "Exemplos de PDF": "Acordos de frete, contratos de transportadoras",
                "Por que ajudam": "SLA de entrega, regiões atendidas",
                "Exemplo de pergunta": "Qual o prazo de entrega para a região Nordeste?"
            },
            {
                "Categoria": "Compliance & Qualidade",
                "Exemplos de PDF": "Certificados ISO, manual de armazenagem",
                "Por que ajudam": "Respostas rápidas em auditorias",
                "Exemplo de pergunta": "Quando expira o ISO 9001 do CD de Campinas?"
            },
            {
                "Categoria": "Notas Técnicas & Regulamentos",
                "Exemplos de PDF": "Instruções fiscais, circulares ICMS-ST",
                "Por que ajudam": "Orientação tributária e sanitária",
                "Exemplo de pergunta": "Qual é a alíquota ICMS-ST para detergentes em SP?"
            },
            {
                "Categoria": "Propostas & Acordos de Parceria",
                "Exemplos de PDF": "Memorandos, condições especiais",
                "Por que ajudam": "Preparar renegociações ou propostas",
                "Exemplo de pergunta": "Quais benefícios de parceria estão previstos para o cliente Y?"
            },
        ]

        # exibe a tabela
        df_docs = pd.DataFrame(dados)
        st.markdown("### 📂 Documentos recomendados para indexação")
        st.dataframe(df_docs, use_container_width=True)
