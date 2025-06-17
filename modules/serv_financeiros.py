import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path
from rag_section import rag_section

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


    # ---------- WIDGET RAG (Serviços Financeiros) ----------
    rag_section(
        titulo     = "Assistente inteligente de Serviços Financeiros",
        index_name = "servicos_financeiros",              # namespace exclusivo
        pasta_docs = Path("data/documentos/servicos_financeiros")
    )

    # ------------------------------------------------------------------
    # ⬇️  Tabela de “Tipos de Documentos” recomendados
    # ------------------------------------------------------------------
    st.divider()
    if st.button("📑 Tipos de Documentos"):
        dados = [
            {
                "Categoria": "Contrato & Regulamento do Cartão",
                "Exemplos de PDF": "Contrato de adesão, regulamento VUON CARD",
                "Por que ajudam": "Regras de tarifas, juros, cancelamento",
                "Exemplo de pergunta": "Qual a taxa de juros por atraso?"
            },
            {
                "Categoria": "Tabelas de Tarifas e Taxas",
                "Exemplos de PDF": "Tabela de tarifas vigente, CET",
                "Por que ajudam": "Consultas rápidas de custos",
                "Exemplo de pergunta": "Há cobrança de anuidade?"
            },
            {
                "Categoria": "Política de Cashback & Cupons",
                "Exemplos de PDF": "Manual Clube VUON, política de cupons",
                "Por que ajudam": "Regras de resgate, prazos de crédito",
                "Exemplo de pergunta": "Em quantos dias recebo o cashback?"
            },
            {
                "Categoria": "Apólices de Seguros & Assistências",
                "Exemplos de PDF": "Vuon Vida, Vuon Casa Protegida, Vuon Odonto",
                "Por que ajudam": "Cobertura, carência, prêmio",
                "Exemplo de pergunta": "Qual a cobertura médica do Vuon Odonto?"
            },
            {
                "Categoria": "Guia de Emissão & Crédito",
                "Exemplos de PDF": "Manual de análise de crédito",
                "Por que ajudam": "Padronizar onboarding em loja",
                "Exemplo de pergunta": "Quais documentos o cliente apresenta?"
            },
            {
                "Categoria": "Relatórios de Desempenho da Carteira",
                "Exemplos de PDF": "Relatório de inadimplência, participação nas vendas",
                "Por que ajudam": "Gestão de risco e metas",
                "Exemplo de pergunta": "Qual a inadimplência no último trimestre?"
            },
            {
                "Categoria": "Documentos de Compliance (Bacen / LGPD)",
                "Exemplos de PDF": "Política de privacidade, normas Bacen",
                "Por que ajudam": "Respostas corretas a obrigações regulatórias",
                "Exemplo de pergunta": "O VUON CARD compartilha dados com terceiros?"
            },
            {
                "Categoria": "Acordos com Lojas Parceiras",
                "Exemplos de PDF": "Termos de parceria, SLA de cashback",
                "Por que ajudam": "Negociação e suporte comercial",
                "Exemplo de pergunta": "Qual percentual de cashback na parceira Y?"
            },
            {
                "Categoria": "Scripts de Atendimento & FAQ",
                "Exemplos de PDF": "Manual de suporte, FAQ interno",
                "Por que ajudam": "Uniformizar respostas ao cliente",
                "Exemplo de pergunta": "Como solicitar a 2ª via do cartão?"
            },
        ]

        st.markdown("### 📂 Documentos recomendados para indexação")
        st.dataframe(pd.DataFrame(dados), use_container_width=True)