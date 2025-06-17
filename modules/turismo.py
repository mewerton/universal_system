# modules/turismo.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from rag_section import rag_section

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

    # ---------- WIDGET RAG (Turismo) ----------
    rag_section(
        titulo     = "Assistente inteligente de Turismo & Agência de Viagens",
        index_name = "turismo",                          # namespace exclusivo
        pasta_docs = Path("data/documentos/turismo")     # onde salvar os PDFs
    )

    # ------------------------------------------------------------------
    # ⬇️  NOVO BLOCO: tabela de “Tipos de Documentos” recomendados
    # ------------------------------------------------------------------
    st.divider()
    if st.button("📑 Tipos de Documentos"):
        dados = [
            {
                "Categoria": "Pacotes & Contratos de Viagem",
                "Exemplos de PDF": "Contrato de pacote turístico, termos de adesão",
                "Por que ajudam": "Regras de reembolso, cláusulas de cancelamento",
                "Exemplo de pergunta": "Qual a multa por cancelamento 10 dias antes do embarque?"
            },
            {
                "Categoria": "Roteiros e Guias de Destino",
                "Exemplos de PDF": "Roteiro dia-a-dia, guia cultural",
                "Por que ajudam": "Detalhes de visitas, horários e logística",
                "Exemplo de pergunta": "Que atrações estão incluídas no 3º dia do roteiro Europa Clássica?"
            },
            {
                "Categoria": "Políticas Tarifárias & Tarifas Aéreas",
                "Exemplos de PDF": "Tabela de tarifas GDS, política de YR/YQ",
                "Por que ajudam": "Comparar classes, franquia de bagagem, regras tarifárias",
                "Exemplo de pergunta": "Qual franquia de bagagem para a tarifa Economy Light da LATAM?"
            },
            {
                "Categoria": "Vouchers e Confirmações de Reserva",
                "Exemplos de PDF": "Voucher hotel, bilhete eletrônico (e-ticket)",
                "Por que ajudam": "Checar códigos de reserva e condições",
                "Exemplo de pergunta": "Qual é o código localizador do hotel em Paris?"
            },
            {
                "Categoria": "Condições Gerais de Viagem / Termos ANAC",
                "Exemplos de PDF": "Cond. gerais de transporte aéreo (ANAC Res. 400)",
                "Por que ajudam": "Garantir compliance e defender o cliente",
                "Exemplo de pergunta": "Qual o prazo de reembolso segundo a Resolução 400?"
            },
            {
                "Categoria": "Seguros-Viagem & Coberturas",
                "Exemplos de PDF": "Apolice, manual de coberturas",
                "Por que ajudam": "Cobertura médica, extravio, cancelamento",
                "Exemplo de pergunta": "Qual o valor de cobertura médica para viagens aos EUA?"
            },
            {
                "Categoria": "Relatórios de Ocupação & Demanda",
                "Exemplos de PDF": "Relatório de room-nights, ADR, demanda sazonal",
                "Por que ajudam": "Planejar allotments e negociações hoteleiras",
                "Exemplo de pergunta": "Qual foi o ADR médio em Salvador no verão 2024?"
            },
            {
                "Categoria": "Documentos de Compliance & Vistos",
                "Exemplos de PDF": "Regras de vistos, exigências sanitárias (ex.: vacina febre-amarela)",
                "Por que ajudam": "Orientar viajantes e evitar impedimentos",
                "Exemplo de pergunta": "Brasileiros precisam de visto para viajar ao México a turismo?"
            },
        ]

        st.markdown("### 📂 Documentos recomendados para indexação")
        st.dataframe(pd.DataFrame(dados), use_container_width=True)
