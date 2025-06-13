import pandas as pd
import plotly.express as px
import streamlit as st

def exibir():
    st.title("💳 Módulo Serviços Financeiros")
    st.markdown("Análise dos contratos de crédito e comportamento financeiro dos clientes.")

    # Carrega o dataset
    df = pd.read_csv("data/financeiro/contratos_credito.csv", parse_dates=["Data_Contrato"])

    col1, col2 = st.columns(2)

    # Gráfico 1: Número de contratos por estado
    with col1:
        st.subheader(" Contratos ativos por estado")
        estado_counts = df['Estado'].value_counts().reset_index()
        estado_counts.columns = ['Estado', 'Quantidade']
        fig1 = px.bar(estado_counts, x='Estado', y='Quantidade', color='Estado')
        st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Parcelamento médio
    with col2:
        st.subheader(" Parcelamento médio")
        fig2 = px.box(df, x="Tipo_Credito", y="Parcelas", color="Tipo_Credito")
        st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Valor total contratado por tipo de crédito
    st.subheader(" Valor contratado por tipo de crédito")
    tipo_valor = df.groupby("Tipo_Credito")["Valor_Contratado"].sum().reset_index()
    fig3 = px.pie(tipo_valor, names="Tipo_Credito", values="Valor_Contratado", hole=0.4)
    st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Inadimplemento ao longo do tempo
    st.subheader(" Evolução do inadimplemento")
    df["AnoMes"] = df["Data_Contrato"].dt.to_period("M").astype(str)
    inad_mensal = df[df["Inadimplente"] == True].groupby("AnoMes").size().reset_index(name="Inadimplentes")
    fig4 = px.line(inad_mensal, x="AnoMes", y="Inadimplentes", markers=True)
    st.plotly_chart(fig4, use_container_width=True)

    # Gráfico 5: Uso de funcionalidades (análise multivalorada)
    st.subheader(" Funcionalidades mais utilizadas pelos clientes")

    # Explodir Uso_Funcionalidade para múltiplas linhas
    funcionalidades_df = df.assign(Funcionalidade=df["Uso_Funcionalidade"].str.split(", ")).explode("Funcionalidade")
    func_counts = funcionalidades_df["Funcionalidade"].value_counts().reset_index()
    func_counts.columns = ["Funcionalidade", "Quantidade"]

    fig5 = px.bar(func_counts, x="Funcionalidade", y="Quantidade", color="Funcionalidade")
    st.plotly_chart(fig5, use_container_width=True)
