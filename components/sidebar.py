import streamlit as st

def sidebar_navigation():
    st.sidebar.title("📋 Navegação")
    menu = st.sidebar.radio(
        "Ir para:",
        (
            "🏠 Início",
            "🛒 Supermercado",
            "🚚 Distribuição",
            "🏬 Atacado",
            "💳 Serviços Financeiros",
            "💊 Farmácia",
            "🚛 Logística",
            "✈️ Turismo",
            "🍽️ Restaurante"

        )
    )
    return menu
