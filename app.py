import streamlit as st
from components.sidebar import sidebar_navigation
from modules import (
    supermercado,
    distribuicao,
    atacado,
    serv_financeiros,
    farmacia,
    logistica,
    turismo,
    restaurante
)

# Configuração da página
st.set_page_config(page_title="Universal System", layout="wide")

# Sidebar de navegação
pagina = sidebar_navigation()

# Roteamento de páginas
if pagina == "🏠 Início":
    st.title("Bem-vindo ao Universal System")
    st.write("Selecione um módulo no menu lateral.")

elif pagina == "🛒 Supermercado":
    supermercado.exibir()

elif pagina == "🚚 Distribuição":
    distribuicao.exibir()

elif pagina == "🏬 Atacado":
    atacado.exibir()

elif pagina == "💳 Serviços Financeiros":
    serv_financeiros.exibir()

elif pagina == "💊 Farmácia":
    farmacia.exibir()

elif pagina == "🚛 Logística":
    logistica.exibir()

elif pagina == "✈️ Turismo":
    turismo.exibir()

elif pagina == "🍽️ Restaurante":
    restaurante.exibir()

