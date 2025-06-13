# modules/turismo.py
import streamlit as st
import pandas as pd
import plotly.express as px

def exibir():
    st.title("✈️ Módulo Turismo")
    st.markdown("Análise das viagens e reservas.")

    # Carregar dados
    df = pd.read_csv("data/turismo/viagens.csv")

    # Forçar conversão correta para datetime
    df["Data_Reserva"] = pd.to_datetime(df["Data_Reserva"], errors="coerce")



    col1, col2 = st.columns(2)

    with col1:
        # 🌍 Top destinos mais vendidos
        st.subheader(" Destinos mais visitados")
        destinos = df[df["Status"] == "Efetivada"]["Destino"].value_counts().reset_index()
        destinos.columns = ["Destino", "Reservas"]
        fig1 = px.bar(destinos, x="Destino", y="Reservas", color="Destino", text="Reservas")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # 📊 Taxa de cancelamento por fornecedor
        st.subheader(" Cancelamentos por fornecedor")
        cancelamentos = df[df["Status"] == "Cancelada"]["Fornecedor"].value_counts().reset_index()
        cancelamentos.columns = ["Fornecedor", "Cancelamentos"]
        fig2 = px.pie(cancelamentos, names="Fornecedor", values="Cancelamentos", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # 🧾 Média de reembolso por tipo de serviço
        st.subheader(" Reembolso médio por tipo de serviço")
        media_reembolso = df[df["Status"] == "Cancelada"].groupby("Tipo_Servico")["Valor_Reembolso"].mean().reset_index()
        fig3 = px.bar(media_reembolso, x="Tipo_Servico", y="Valor_Reembolso", color="Tipo_Servico", text_auto=".2s")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        # 📈 Evolução de reservas por tipo de serviço (mês a mês)
        st.subheader("📈 Evolução de reservas por tipo de serviço (mês a mês)")
        df["AnoMes"] = pd.to_datetime(df["Data_Reserva"]).dt.to_period("M").astype(str)
        evolucao_servico = df.groupby(["AnoMes", "Tipo_Servico"]).size().reset_index(name="Reservas")
        fig5 = px.line(
            evolucao_servico,
            x="AnoMes",
            y="Reservas",
            color="Tipo_Servico",
            markers=True,
            line_shape="spline"  # <- suavização aqui
        )
        st.plotly_chart(fig5, use_container_width=True)


    # 💬 Motivos de cancelamento mais recorrentes
    st.subheader(" Motivos de cancelamento mais recorrentes")
    motivos = df[df["Status"] == "Cancelada"]["Motivo_Cancelamento"].value_counts().reset_index()
    motivos.columns = ["Motivo", "Ocorrências"]
    fig5 = px.bar(motivos, x="Motivo", y="Ocorrências", color="Motivo", text="Ocorrências")
    st.plotly_chart(fig5, use_container_width=True)
