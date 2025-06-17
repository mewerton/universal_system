import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from rag_section import rag_section

def exibir():
    st.title("🛒 Módulo Supermercado")
    st.markdown("Análise de contratos com fornecedores de comida")

    # Carrega o dataset
    try:
        df = pd.read_parquet("data/supermercado/contratos_fornecedores_comida.parquet")
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado. Verifique se o arquivo está na pasta `data`.")
        return

    # Criar duas colunas lado a lado
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(" Top 10 fornecedores por valor contratado")
        top_fornecedores = df.groupby("Fornecedor")["Valor_Contrato"].sum().nlargest(10).reset_index()
        fig1 = px.bar(top_fornecedores, x="Fornecedor", y="Valor_Contrato", title="Top 10 Fornecedores")
        fig1.update_layout(xaxis_tickangle=-45)  # Gira os rótulos
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader(" Distribuição dos prazos de validade exigidos")
        fig2 = px.histogram(df, x="Prazo_Validade_Dias", nbins=10, title="Distribuição dos Prazos de Validade")
        st.plotly_chart(fig2, use_container_width=True)

    # Tipos de contrato por fornecedor
    st.subheader(" Tipos de contratos por fornecedor")
    tipo_contrato = df.groupby(["Fornecedor", "Tipo_Contrato"]).size().reset_index(name="Quantidade")
    fig3 = px.bar(tipo_contrato, x="Fornecedor", y="Quantidade", color="Tipo_Contrato", barmode="group")
    st.plotly_chart(fig3, use_container_width=True)

    # Criar duas colunas lado a lado
    col1, col2 = st.columns(2)
    with col1:
        # Evolução dos contratos por mês
        st.subheader(" Evolução dos contratos assinados por mês")
        df["Data_Assinatura"] = pd.to_datetime(df["Data_Assinatura"])
        df["AnoMes"] = df["Data_Assinatura"].dt.to_period("M").astype(str)
        contratos_por_mes = df.groupby("AnoMes")["Valor_Contrato"].sum().reset_index()
        fig4 = px.line(contratos_por_mes, x="AnoMes", y="Valor_Contrato", markers=True)
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        # Comparativo de valores por categoria
        st.subheader(" Comparativo de valores contratados por categoria")
        categoria_valores = df.groupby("Categoria")["Valor_Contrato"].sum().reset_index()
        fig5 = px.pie(categoria_valores, values="Valor_Contrato", names="Categoria", title="Distribuição por Categoria")
        st.plotly_chart(fig5, use_container_width=True)

    # ---------- WIDGET RAG (Supermercado) ----------
    rag_section(
        titulo     = "Assistente inteligente de Supermercado",
        index_name = "supermercado",                      # namespace isolado
        pasta_docs = Path("data/documentos/supermercado") # onde salvar/encontrar PDFs
    )

    # ------------------------------------------------------------------
    # ⬇️  NOVO BLOCO: tabela de “Tipos de Documentos” recomendados
    # ------------------------------------------------------------------
    st.divider()
    if st.button("📑 Tipos de Documentos"):
        dados = [
            {
                "Categoria": "Relatórios de Vendas & Mix",
                "Exemplos de PDF": "Curva ABC, sell-out mensal, painel de categorias",
                "Por que ajudam": "Consultas rápidas a volume, margem e giro por SKU/categoria",
                "Exemplo de pergunta": "Qual foi o faturamento da categoria Laticínios em abril?"
            },
            {
                "Categoria": "Planogramas & Layout de Gôndola",
                "Exemplos de PDF": "Planograma de prateleira, guia de exposição",
                "Por que ajudam": "Verificar facings, espaço linear e regras de merchandising",
                "Exemplo de pergunta": "Quantos facings o café Premium ocupa no planograma 2024?"
            },
            {
                "Categoria": "Contratos de Fornecimento & Merchandising",
                "Exemplos de PDF": "Acordo anual de compra, contrato de verba promocional",
                "Por que ajudam": "Condições de preço, bonificação, verba de gôndola",
                "Exemplo de pergunta": "Qual o desconto de volume acordado com o fornecedor XYZ?"
            },
            {
                "Categoria": "Política de Preços & Promoções",
                "Exemplos de PDF": "Tabela de preços, calendário promocional",
                "Por que ajudam": "Referência de preço base e mecânicas de oferta",
                "Exemplo de pergunta": "Quando está prevista a próxima promoção de arroz 5 kg?"
            },
            {
                "Categoria": "Relatórios de Perdas & Quebras",
                "Exemplos de PDF": "Inventário de perdas, análise de desperdício",
                "Por que ajudam": "Acompanhar shrinkage e definir ações corretivas",
                "Exemplo de pergunta": "Qual foi a taxa de quebra em FLV no último trimestre?"
            },
            {
                "Categoria": "Licenças Sanitárias & Certificados",
                "Exemplos de PDF": "Alvará da vigilância sanitária, ISO 22000",
                "Por que ajudam": "Compliance em inspeções e auditorias",
                "Exemplo de pergunta": "Quando vence a licença sanitária da loja Centro?"
            },
            {
                "Categoria": "Procedimentos de Segurança Alimentar",
                "Exemplos de PDF": "POP de higienização, manual APPCC",
                "Por que ajudam": "Consulta a padrões obrigatórios de manipulação",
                "Exemplo de pergunta": "Qual a temperatura mínima de conservação de carnes frescas?"
            },
            {
                "Categoria": "Pesquisas de Satisfação & NPS",
                "Exemplos de PDF": "Relatório NPS, survey de experiência",
                "Por que ajudam": "Insights para melhoria de atendimento e sortimento",
                "Exemplo de pergunta": "Qual foi o NPS médio das lojas no 2º semestre?"
            },
        ]

        st.markdown("### 📂 Documentos recomendados para indexação")
        st.dataframe(pd.DataFrame(dados), use_container_width=True)