import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from rag_section import rag_section

def exibir():
    st.title(" Módulo Distribuição")
    st.markdown("Análise dos contratos de distribuição e desempenho logístico")

    # Carrega o dataset
    try:
        df = pd.read_csv("data/distribuicao/contratos_distribuicao.csv")
    except FileNotFoundError:
        st.error("Arquivo contratos_distribuicao.csv não encontrado.")
        return

    # Pré-processamento
    df["Data_Entrega"] = pd.to_datetime(df["Data_Entrega"], errors="coerce")
    df = df.dropna(subset=["Data_Entrega"])
    df["AnoMes"] = df["Data_Entrega"].dt.to_period("M").astype(str)

    # Gráfico 1 - Distribuição geográfica dos clientes atendidos
    st.subheader(" Distribuição geográfica dos clientes atendidos")
    clientes_estado = df["Estado"].value_counts().reset_index()
    clientes_estado.columns = ["Estado", "Quantidade"]
    fig1 = px.bar(clientes_estado, x="Estado", y="Quantidade", title="Clientes Atendidos por Estado")
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2 - Cumprimento de SLA por região (Estado)
    st.subheader(" Cumprimento de SLA por Estado")
    sla_estado = df.groupby("Estado")["Cumprimento_SLA"].apply(lambda x: (x == "Sim").mean() * 100).reset_index()
    sla_estado.columns = ["Estado", "Cumprimento_SLA (%)"]
    fig2 = px.bar(sla_estado, x="Estado", y="Cumprimento_SLA (%)", title="Cumprimento de SLA (%) por Estado")
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3 - Tipos de contratos por segmento de comércio
    st.subheader(" Tipos de contratos por segmento de comércio")
    contratos_segmento = df.groupby(["Segmento_Comercio", "Tipo_Contrato"]).size().reset_index(name="Quantidade")
    fig3 = px.bar(contratos_segmento, x="Segmento_Comercio", y="Quantidade", color="Tipo_Contrato",
                  barmode="group", title="Tipos de Contrato por Segmento")
    st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4 - Evolução do número de entregas por mês
    st.subheader(" Evolução do número de entregas por mês")
    entregas_mes = df.groupby("AnoMes").size().reset_index(name="Entregas")
    fig4 = px.line(entregas_mes, x="AnoMes", y="Entregas", markers=True, title="Entregas por Mês")
    st.plotly_chart(fig4, use_container_width=True)

    # Gráfico 5 - Ranking de produtos mais distribuídos
    st.subheader(" Produtos mais distribuídos")
    produtos_top = df["Produto"].value_counts().reset_index()
    produtos_top.columns = ["Produto", "Quantidade"]
    fig5 = px.bar(produtos_top.head(10), x="Quantidade", y="Produto", orientation="h",
                  title="Top 10 Produtos Distribuídos")
    st.plotly_chart(fig5, use_container_width=True)

   # ---------- WIDGET RAG (Distribuição) ----------
    rag_section(
        titulo     = "Assistente inteligente de Distribuição",
        index_name = "distribuicao",                     # ← muda o namespace
        pasta_docs = Path("data/documentos/distribuicao")  # ← onde salvar PDFs
    )

    # ------------------------------------------------------------------
    # ⬇️  NOVO BLOCO: tabela de “Tipos de Documentos” recomendados
    # ------------------------------------------------------------------
    st.divider()
    if st.button("📑 Tipos de Documentos"):
        dados = [
            {
                "Categoria": "Contratos de Distribuição & SLA",
                "Exemplos de PDF": "Contrato logístico, aditivos de SLA, ANS",
                "Por que ajudam": "Prazos, multas, níveis de serviço acordados",
                "Exemplo de pergunta": "Qual a multa estipulada para atraso acima de 24 h?"
            },
            {
                "Categoria": "Mapas de Rotas & Janelas de Doca",
                "Exemplos de PDF": "Plano mestre de rotas, booking de docas",
                "Por que ajudam": "Otimização de roteirização e slots de carregamento",
                "Exemplo de pergunta": "Qual a janela de doca do cliente XPTO às segundas-feiras?"
            },
            {
                "Categoria": "Relatórios de Nível de Serviço",
                "Exemplos de PDF": "Relatório OTIF, KPI mensal de entrega",
                "Por que ajudam": "Medição de performance por região/transportadora",
                "Exemplo de pergunta": "Qual foi o OTIF do Nordeste em março?"
            },
            {
                "Categoria": "Inventário & Capacidade de CDs",
                "Exemplos de PDF": "Inventário mensal, layout de armazenagem",
                "Por que ajudam": "Consultas rápidas de saldo e ocupação",
                "Exemplo de pergunta": "Qual o estoque disponível do SKU 123 no CD Recife?"
            },
            {
                "Categoria": "Tabelas de Frete e Custos",
                "Exemplos de PDF": "Tabela de frete por faixa de km, acordo de combustível",
                "Por que ajudam": "Simulações de custo e negociação de transportadoras",
                "Exemplo de pergunta": "Quanto custa o frete por kg para 500 km na região Sul?"
            },
            {
                "Categoria": "Documentos Regulatórios & Sanitários",
                "Exemplos de PDF": "Autorização ANTT, licenças ANVISA",
                "Por que ajudam": "Compliance e auditorias",
                "Exemplo de pergunta": "Quando expira a licença ANVISA do CD Curitiba?"
            },
            {
                "Categoria": "Manuais de Operação & Segurança",
                "Exemplos de PDF": "Procedimento de carga/descarga, NR-11",
                "Por que ajudam": "Consulta a padrões operacionais e EHS",
                "Exemplo de pergunta": "Qual o procedimento para amarração de carga paletizada?"
            },
            {
                "Categoria": "Ocorrências & Logs de Transporte",
                "Exemplos de PDF": "Relatório de avarias, registro de atrasos",
                "Por que ajudam": "Análise de falhas e melhoria contínua",
                "Exemplo de pergunta": "Quantas avarias ocorreram na rota SP-RJ em 2024?"
            },
        ]

        st.markdown("### 📂 Documentos recomendados para indexação")
        st.dataframe(pd.DataFrame(dados), use_container_width=True)