import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from rag_section import rag_section

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


    # ---------- WIDGET RAG (Restaurante) ----------
    rag_section(
        titulo     = "Assistente inteligente de Restaurante",
        index_name = "restaurante",                       # namespace exclusivo
        pasta_docs = Path("data/documentos/restaurante")  # onde salvar os PDFs
    )

    # ------------------------------------------------------------------
    # ⬇️  NOVO BLOCO: tabela de “Tipos de Documentos” recomendados
    # ------------------------------------------------------------------
    st.divider()
    if st.button("📑 Tipos de Documentos"):
        dados = [
            {
                "Categoria": "Cardápios & Fichas Técnicas",
                "Exemplos de PDF": "Menu sazonal, ficha de receita (BOM)",
                "Por que ajudam": "Custo de prato, alergênicos, padronização",
                "Exemplo de pergunta": "Quais ingredientes e custos do prato Spaghetti Carbonara?"
            },
            {
                "Categoria": "Contratos com Fornecedores",
                "Exemplos de PDF": "Acordo de fornecimento de carnes, hortifruti",
                "Por que ajudam": "Condições de preço, prazo de entrega e SLA",
                "Exemplo de pergunta": "Qual o prazo de pagamento negociado com o fornecedor de peixes?"
            },
            {
                "Categoria": "Laudos & Licenças Sanitárias",
                "Exemplos de PDF": "Vigilância sanitária, AVCB, alvará",
                "Por que ajudam": "Compliance e auditorias",
                "Exemplo de pergunta": "Quando vence o alvará sanitário da unidade centro?"
            },
            {
                "Categoria": "Relatórios de Vendas & CMV",
                "Exemplos de PDF": "Relatório POS diário, CMV mensal",
                "Por que ajudam": "Análise de performance e margem",
                "Exemplo de pergunta": "Qual foi o CMV (%) em maio de 2024?"
            },
            {
                "Categoria": "Escalas & Folhas de Ponto",
                "Exemplos de PDF": "Escala de garçom/cozinha, banco de horas",
                "Por que ajudam": "Gestão de pessoal e custos de mão de obra",
                "Exemplo de pergunta": "Quantas horas extras o garçom João fez na última semana?"
            },
            {
                "Categoria": "Procedimentos Operacionais (POP)",
                "Exemplos de PDF": "Higienização de utensílios, boas práticas",
                "Por que ajudam": "Treinamento e padronização de qualidade",
                "Exemplo de pergunta": "Qual a temperatura mínima de cozimento para frango indicada no POP?"
            },
            {
                "Categoria": "Inventário de Estoque",
                "Exemplos de PDF": "Inventário quinzenal, planilha de perdas",
                "Por que ajudam": "Controle de desperdício e reordem",
                "Exemplo de pergunta": "Qual o estoque atual de óleo de cozinha?"
            },
            {
                "Categoria": "Planos de Marketing & Promoções",
                "Exemplos de PDF": "Calendário de eventos, campanhas delivery",
                "Por que ajudam": "Avaliar ROI e programar ações futuras",
                "Exemplo de pergunta": "Quando inicia a promoção de rodízio a R$ 59,90?"
            },
        ]

        st.markdown("### 📂 Documentos recomendados para indexação")
        st.dataframe(pd.DataFrame(dados), use_container_width=True)
