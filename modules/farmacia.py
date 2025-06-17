import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from rag_section import rag_section

def exibir():
    st.title("💊 Módulo Farmácia")
    st.markdown("Análise de fornecimento, controle de estoque e desempenho de medicamentos.")

    # Carregamento de dados
    df = pd.read_csv("data/farmacia/fornecedores_medicamentos.csv", parse_dates=["Data_Aprovacao_ANVISA", "Validade"])

    # Gráfico 1 e 2 lado a lado
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(" Quantidade de medicamentos por categoria")
        cat_count = df["Categoria"].value_counts().reset_index()
        cat_count.columns = ["Categoria", "Quantidade"]
        fig1 = px.bar(cat_count, x="Categoria", y="Quantidade", color="Categoria", text="Quantidade")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader(" Fornecedores com maior volume de entrega")
        fornecedor_vol = df.groupby("Fornecedor")["Volume_Entregue"].sum().reset_index()
        fig2 = px.bar(fornecedor_vol, x="Fornecedor", y="Volume_Entregue", color="Fornecedor", text="Volume_Entregue")
        st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3 e 4 lado a lado
    col3, col4 = st.columns(2)

    with col3:
        st.subheader(" Preço médio por categoria de medicamento")
        preco_categoria = df.groupby("Categoria")["Preco_Unitario"].mean().reset_index()
        fig3 = px.line(preco_categoria, x="Categoria", y="Preco_Unitario", markers=True)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader(" Top 10 medicamentos com mais devoluções")
        top_devolucoes = df.nlargest(10, "Volume_Devolvido")
        fig4 = px.bar(top_devolucoes, x="Medicamento", y="Volume_Devolvido", color="Fornecedor", text="Volume_Devolvido")
        st.plotly_chart(fig4, use_container_width=True)

    # Gráfico 5: Prazo médio de aprovação da ANVISA por categoria
    st.subheader(" Prazo médio de aprovação ANVISA por categoria")
    df["Prazo_Aprovacao"] = (df["Validade"] - df["Data_Aprovacao_ANVISA"]).dt.days
    prazo_aprov = df.groupby("Categoria")["Prazo_Aprovacao"].mean().reset_index()
    fig5 = px.bar(prazo_aprov, x="Categoria", y="Prazo_Aprovacao", color="Categoria", text="Prazo_Aprovacao")
    st.plotly_chart(fig5, use_container_width=True)

    # Gráfico 6: Giro de estoque (vendas vs devoluções)
    st.subheader(" Giro de estoque por medicamento")
    giro = df[["Medicamento", "Vendas", "Volume_Devolvido"]].melt(id_vars="Medicamento",
        value_vars=["Vendas", "Volume_Devolvido"], var_name="Tipo", value_name="Quantidade")
    fig6 = px.bar(giro, x="Medicamento", y="Quantidade", color="Tipo", barmode="group")
    st.plotly_chart(fig6, use_container_width=True)

    # Gráfico 1 e 2 lado a lado
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico 7: Média de dias até vencimento (análise de validade)
        st.subheader(" Dias até vencimento por categoria")
        df["Dias_Para_Vencer"] = (df["Validade"] - pd.Timestamp.today()).dt.days
        vencimento = df.groupby("Categoria")["Dias_Para_Vencer"].mean().reset_index()
        fig7 = px.bar(vencimento, x="Categoria", y="Dias_Para_Vencer", color="Categoria", text="Dias_Para_Vencer")
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        # Gráfico 8: Distribuição geográfica por estado
        st.subheader(" Distribuição de medicamentos por estado")
        estado_dist = df["Estado"].value_counts().reset_index()
        estado_dist.columns = ["Estado", "Quantidade"]
        fig8 = px.pie(estado_dist, names="Estado", values="Quantidade", hole=0.4)
        st.plotly_chart(fig8, use_container_width=True)

    # Gráfico 9: Medicamentos em falta (status estoque)
    st.subheader("🚨 Medicamentos em falta")
    em_falta = df[df["Status_Estoque"] == "Em falta"]
    if not em_falta.empty:
        st.dataframe(em_falta[["Medicamento", "Fornecedor", "Estado", "Cidade", "Volume_Entregue"]])
    else:
        st.success("Nenhum medicamento em falta no momento.")


    # ---------- WIDGET RAG (Farmácia) ----------
    rag_section(
        titulo     = "Assistente inteligente de Farmácia",
        index_name = "farmacia",                          # namespace isolado
        pasta_docs = Path("data/documentos/farmacia")     # onde salvar PDFs
    )

    # ------------------------------------------------------------------
    # ⬇️  NOVO BLOCO: tabela de “Tipos de Documentos” recomendados
    # ------------------------------------------------------------------
    st.divider()
    if st.button("📑 Tipos de Documentos"):
        dados = [
            {
                "Categoria": "Bulas & Dossiês de Medicamentos",
                "Exemplos de PDF": "Bulas RDC 47, dossiê de registro",
                "Por que ajudam": "Informações de posologia, indicações e efeitos adversos",
                "Exemplo de pergunta": "Qual a dose máxima diária de ibuprofeno para adultos?"
            },
            {
                "Categoria": "Protocolos de Dispensação & POPs",
                "Exemplos de PDF": "POP de venda de antimicrobianos, Guia de atenção farmacêutica",
                "Por que ajudam": "Garantir conformidade na dispensação e orientação ao paciente",
                "Exemplo de pergunta": "Quais documentos devo arquivar ao vender psicotrópicos classe B?"
            },
            {
                "Categoria": "Relatórios de Controle Especial (Portaria 344)",
                "Exemplos de PDF": "Livro de psicotrópicos, Mapa de balanceamento mensal",
                "Por que ajudam": "Auditorias sanitárias e conferência de estoque controlado",
                "Exemplo de pergunta": "Quantos comprimidos de clonazepam foram vendidos em maio?"
            },
            {
                "Categoria": "Contratos & Condições Comerciais com Laboratórios",
                "Exemplos de PDF": "Acordo de compra, rebate trimestral",
                "Por que ajudam": "Negociação de preço, bonificações e prazos",
                "Exemplo de pergunta": "Qual rebate firmado com o laboratório XYZ para o medicamento Genérico A?"
            },
            {
                "Categoria": "Relatórios de Vendas & Giro de Estoque",
                "Exemplos de PDF": "Top 100 SKUs, ruptura por categoria",
                "Por que ajudam": "Decisão de compra e reposição",
                "Exemplo de pergunta": "Qual foi o giro médio de analgésicos na última quinzena?"
            },
            {
                "Categoria": "Licenças & Certificados Sanitários",
                "Exemplos de PDF": "Alvará sanitário, Autorização de funcionamento ANVISA",
                "Por que ajudam": "Exigidos em inspeções e renovações",
                "Exemplo de pergunta": "Quando vence o alvará sanitário da loja Matriz?"
            },
            {
                "Categoria": "Política de Descarte de Medicamentos",
                "Exemplos de PDF": "POP de descarte, contrato com incineradora",
                "Por que ajudam": "Compliance ambiental e sanitário",
                "Exemplo de pergunta": "Qual o procedimento para descarte de medicamentos vencidos?"
            },
            {
                "Categoria": "Programas de Benefício / PBM",
                "Exemplos de PDF": "Manual PBM, contratos de copagamento",
                "Por que ajudam": "Orientar equipe sobre elegibilidade e reembolso",
                "Exemplo de pergunta": "Quais documentos o cliente precisa para aderir ao PBM do laboratório ABC?"
            },
        ]

        st.markdown("### 📂 Documentos recomendados para indexação")
        st.dataframe(pd.DataFrame(dados), use_container_width=True)
