import streamlit as st
import pandas as pd
import plotly.express as px

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
