
# Universal System 🚀

**Universal System** é uma plataforma modular e reutilizável desenvolvida em Python e Streamlit, voltada para análise de dados e integração com inteligência artificial. Seu objetivo principal é atender empresas com múltiplos setores de operação, oferecendo módulos analíticos independentes e personalizáveis.

## 🎯 Objetivo do Projeto

Criar um sistema robusto, escalável e reutilizável, com:
- Estrutura modular com navegação via páginas nativas do Streamlit.
- Dashboard interativo por setor (Ex: Supermercado, Logística, Turismo etc).
- Integração futura com RAG (Retrieval-Augmented Generation) para uso de LLMs com dados específicos por módulo.
- Possibilidade de reutilização por outras empresas de segmentos diversos.

## 🗂️ Estrutura Inicial

```
universal_system/
├── app.py                      # Ponto de entrada do app (controla login e redirecionamento)
├── .streamlit/
│   └── config.toml             # Configurações do layout Streamlit
│   └── secrets.toml            
├── pages/
│   └── 1_Home.py               # Página inicial com miniaturas dos módulos
│   └── (futuras páginas)       # Ex: 2_Farmacia.py, 3_Logistica.py etc.
├── components/
│   └── sidebar.py              # Componente do sidebar modular e condicional
├── auth/
│   └── login.py                # Função de autenticação segura
├── data/                       # (futuramente) dados locais ou datasets fictícios
├── utils/
│   └── helpers.py              # Funções auxiliares e genéricas
└── requirements.txt            # Dependências do projeto
```

## ⚙️ Tecnologias Utilizadas

- **Python 3.12+**
- **Streamlit 1.45+**
- **Pandas 2.3+**
- (Futuramente: FAISS ou Pinecone, LangChain, LLM APIs)


## 🔢 Módulos e Gráficos Sugeridos

### 🛒 1. Supermercado
**Dataset fictício:** `contratos_fornecedores_comida.parquet`  
**Gráficos sugeridos:**
- 📊 Top 10 fornecedores por volume de entrega  
- 📅 Distribuição dos prazos de validade exigidos  
- 🧾 Tipos de contratos por fornecedor (exclusivo / não exclusivo)  
- 📈 Evolução dos contratos assinados por mês  
- 💰 Comparativo de valores contratados por categoria (carnes, hortifruti, padaria)  

### 🚚 2. Distribuição
**Dataset fictício:** `contratos_distribuicao.csv`, `SLA_entregas.pdf`  
**Gráficos sugeridos:**
- 📦 Distribuição geográfica dos clientes atendidos  
- ⏱️ Cumprimento de SLA por região  
- 🧾 Tipos de contratos por segmento de comércio  
- 📈 Evolução do número de entregas por mês  
- 📊 Ranking de produtos mais distribuídos  

### 🏬 3. Atacado
**Dataset fictício:** `contratos_locacao_lojas.parquet`, `planos_expansao.csv`  
**Gráficos sugeridos:**
- 🗺️ Mapa das lojas por estado  
- 💸 Valores de aluguel por loja e por metro quadrado  
- 📅 Prazo de vigência dos contratos de locação  
- 📈 Histórico de inaugurações por ano  
- 🧾 Índice de correção mais utilizado (IGP-M, IPCA, etc.)  

### 💳 4. Serviços Financeiros
**Dataset fictício:** `contratos_credito.csv`, `seguros_termos.pdf`  
**Gráficos sugeridos:**
- 💳 Número de cartões emitidos por estado  
- 📊 Parcelamentos médios por cliente  
- 💰 Valor total contratado por tipo de crédito (compra, seguro, odontológico)  
- 📅 Evolução do inadimplemento mensal  
- 📈 Uso de funcionalidades por cliente (cartão, seguro, odonto)  

### 💊 5. Farmácias
**Dataset fictício:** `fornecedores_medicamentos.csv`, `registros_anvisa.pdf`  
**Gráficos sugeridos:**
- 🧪 Quantidade de medicamentos por categoria (genéricos, controlados, etc.)  
- 📦 Fornecedores com maior volume de entrega  
- 📈 Variação de preço médio por categoria de produto  
- ⚠️ Medicamentos com maior volume de devoluções  
- 📊 Prazo médio de aprovação da ANVISA  

### 🚛 6. Logística
**Dataset fictício:** `contratos_frete.csv`, `licencas_antt.pdf`  
**Gráficos sugeridos:**
- 🚚 Custo médio de frete por rota  
- 📍 Mapa interativo das rotas mais utilizadas  
- 📈 Evolução de entregas por mês  
- ⏱️ Tempo médio de entrega por estado  
- 🧾 Tipos de contrato logístico por modalidade (FTL, LTL, etc.)  

### ✈️ 7. Turismo
**Dataset fictício:** `parcerias_hotel.pdf`, `condicoes_cancelamento.csv`  
**Gráficos sugeridos:**
- 🌍 Top destinos mais vendidos  
- 📊 Taxa de cancelamento por fornecedor  
- 🧾 Média de reembolso por tipo de serviço (aéreo, terrestre, hospedagem)  
- 📈 Evolução de reservas por colaborador/mês  
- 💬 Motivos de cancelamento mais recorrentes (texto categorizado)  

### 🍽️ 8. Restaurante
**Dataset fictício:** `contratos_terceirizacao_alimentos.pdf`, `colaboradores_clt.csv`  
**Gráficos sugeridos:**
- 🍽️ Pratos mais vendidos por dia da semana  
- 📊 Custo médio por prato (baseado em contratos com fornecedores)  
- 🧾 Número de contratos terceirizados ativos  
- 📈 Evolução de refeições servidas por mês  
- 🧑‍🍳 Distribuição de funções dos colaboradores  

---

### 🧠 Extras para Todos os Setores (Dashboard Principal)
- 🔎 Documentos carregados por setor  
- ⏱️ Tempo médio de resposta do RAG por setor  
- 💬 Consultas mais frequentes  
- 📈 Uso por dia / semana / mês  
- 👥 Colaboradores mais ativos (se login for usado)  

## 🔐 Segurança e Escopo Futuro

- Página de login com autenticação (sem estar no diretório `pages/`).
- Controle de acesso por usuário e setor.
- Dashboard dinâmico com filtros pelo `sidebar.py`.
- Integração com RAG para respostas inteligentes por setor.
- Personalização do tema para cada empresa cliente.

## 🚀 Execução Local

```bash
# Ativando ambiente virtual
source .venv/bin/activate  # (Linux/macOS)
.venv\Scripts\activate   # (Windows)

# Instalando dependências
pip install -r requirements.txt

# Executando o app
streamlit run app.py
```

## 📄 Licença

Projeto open-source. Licença a ser definida conforme cliente ou repositório corporativo.

---

Desenvolvido com foco em **clean code**, **escalabilidade** e **reutilização**, como um desenvolvedor sênior faria. 😉
