import streamlit as st
import pandas as pd
import plotly.express as px

def exibir():
    st.title("🚛 Módulo Logística")
    st.write("Análise de contratos logísticos e entregas.")

    # Carregamento do dataset
    df = pd.read_csv("data/logistica/contratos_frete.csv", parse_dates=["Data_Entrega"])

    # Gráfico 1: Custo médio de frete por rota
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(" Custo médio de frete por rota")
        rota_custo = df.groupby(["UF_Origem", "UF_Destino"])["Custo_Frete"].mean().reset_index()
        rota_custo["Rota"] = rota_custo["UF_Origem"] + " → " + rota_custo["UF_Destino"]
        fig1 = px.bar(rota_custo, x="Rota", y="Custo_Frete", color="UF_Origem", text_auto=True)
        st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Tipos de contrato por modalidade
    with col2:
        st.subheader(" Distribuição por modalidade logística")
        modalidade_count = df["Modalidade"].value_counts().reset_index()
        modalidade_count.columns = ["Modalidade", "Quantidade"]
        fig2 = px.pie(modalidade_count, names="Modalidade", values="Quantidade", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Mapa interativo das rotas mais utilizadas
    st.subheader(" Mapa de rotas mais utilizadas (interativo)")
    top_rotas = df.nlargest(100, "Quantidade_Entregas")

    # Criando DataFrame para origem e destino separadamente
    origem_df = top_rotas[["ID_Contrato", "Latitude_Origem", "Longitude_Origem"]].copy()
    origem_df.columns = ["ID_Contrato", "Latitude", "Longitude"]
    origem_df["Tipo"] = "Origem"

    destino_df = top_rotas[["ID_Contrato", "Latitude_Destino", "Longitude_Destino"]].copy()
    destino_df.columns = ["ID_Contrato", "Latitude", "Longitude"]
    destino_df["Tipo"] = "Destino"

    # Unindo origem e destino para formar pares de rotas
    rota_df = pd.concat([origem_df, destino_df], ignore_index=True)

    # Plotando com line_mapbox
    fig3 = px.line_mapbox(
        rota_df,
        lat="Latitude",
        lon="Longitude",
        color="ID_Contrato",
        hover_name="ID_Contrato",
        zoom=3,
        height=500
    )
    fig3.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Evolução de entregas por mês
    st.subheader(" Evolução de entregas por mês")
    df["AnoMes"] = df["Data_Entrega"].dt.to_period("M").astype(str)
    entregas_mes = df.groupby("AnoMes")["Quantidade_Entregas"].sum().reset_index()
    fig4 = px.line(entregas_mes, x="AnoMes", y="Quantidade_Entregas", markers=True)
    st.plotly_chart(fig4, use_container_width=True)

    # Gráfico 5: Tempo médio de entrega por estado
    st.subheader(" Tempo médio de entrega por estado de destino")
    tempo_estado = df.groupby("UF_Destino")["Tempo_Entrega_Dias"].mean().reset_index()
    fig5 = px.bar(tempo_estado, x="UF_Destino", y="Tempo_Entrega_Dias", color="UF_Destino", text_auto=True)
    st.plotly_chart(fig5, use_container_width=True)
