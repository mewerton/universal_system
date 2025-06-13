import streamlit as st
import pandas as pd
import plotly.express as px

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
