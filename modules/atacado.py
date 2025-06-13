import streamlit as st
import pandas as pd
import plotly.express as px

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
