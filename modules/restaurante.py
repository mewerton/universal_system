import streamlit as st
import pandas as pd
import plotly.express as px

def exibir():
    st.title("🍽️ Módulo Restaurante")
    st.markdown("Análises de consumo no restaurante.")

    # Carregar dados
    df = pd.read_csv("data/restaurante/restaurante.csv", encoding="utf-8-sig")
    df["Data"] = pd.to_datetime(df["Data"])
    df["AnoMes"] = df["Data"].dt.to_period("M").astype(str)

    # Traduzir dias da semana para português
    dias_semana_pt = {
        "Monday": "Segunda",
        "Tuesday": "Terça",
        "Wednesday": "Quarta",
        "Thursday": "Quinta",
        "Friday": "Sexta",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    df["Dia_Semana"] = df["Dia_Semana"].replace(dias_semana_pt)
    ordem_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    df["Dia_Semana"] = pd.Categorical(df["Dia_Semana"], categories=ordem_dias, ordered=True)

    # 🍽️ Gráfico 1: Pratos mais vendidos por dia da semana
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🍽️ Pratos mais vendidos por dia da semana")
        top_pratos = df.groupby(["Dia_Semana", "Prato"], observed=False)["Qtd_Refeicoes_Servidas"].sum().reset_index()
        fig1 = px.bar(top_pratos, x="Dia_Semana", y="Qtd_Refeicoes_Servidas", color="Prato", barmode="stack")
        st.plotly_chart(fig1, use_container_width=True)

    # 📊 Gráfico 2: Custo médio por prato
    with col2:
        st.subheader("📊 Custo médio por prato")
        custo_prato = df.groupby("Prato")["Custo_Total_Prato"].mean().reset_index()
        fig2 = px.bar(custo_prato, x="Prato", y="Custo_Total_Prato", labels={"Custo_Total_Prato": "Custo Médio (R$)"})
        st.plotly_chart(fig2, use_container_width=True)

    # 🧾 Gráfico 3: Fornecimentos por fornecedor
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("🧾 Fornecimentos por fornecedor")
        contratos = df["Fornecedor"].value_counts().reset_index()
        contratos.columns = ["Fornecedor", "Qtd_Contratos"]
        fig3 = px.pie(contratos, values="Qtd_Contratos", names="Fornecedor", title="Distribuição por Fornecedor")
        st.plotly_chart(fig3, use_container_width=True)

    # 📈 Gráfico 4: Evolução de refeições por mês
    with col4:
        st.subheader("📈 Evolução de refeições por mês")
        evolucao = df.groupby("AnoMes")["Qtd_Refeicoes_Servidas"].sum().reset_index()
        fig4 = px.line(evolucao, x="AnoMes", y="Qtd_Refeicoes_Servidas", markers=True)
        st.plotly_chart(fig4, use_container_width=True)

    # 🍽️ Gráfico 5: Arrecadação por tipo de serviço
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("🍽️ Arrecadação por tipo de serviço")
        comparativo = df.groupby("Tipo_Servico")["Valor_Total_Arrecadado"].sum().reset_index()
        fig5 = px.bar(comparativo, x="Tipo_Servico", y="Valor_Total_Arrecadado", color="Tipo_Servico")
        st.plotly_chart(fig5, use_container_width=True)

    # 🕐 Gráfico 6: Refeições por turno
    with col6:
        st.subheader("🕐 Distribuição de refeições por turno")
        turnos = df.groupby("Turno")["Qtd_Refeicoes_Servidas"].sum().reset_index()
        fig6 = px.pie(turnos, values="Qtd_Refeicoes_Servidas", names="Turno", title="Refeições por Turno")
        st.plotly_chart(fig6, use_container_width=True)
