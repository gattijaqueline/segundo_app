import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Simulador de Custos e Orçamento",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 1. Base de Dados Interna
# -----------------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    dados = [
        {"Item": "Chapa de Aço Inox", "Categoria": "Matéria-Prima", "Valor (R$)": 4500.00, "Prioridade": "Alta"},
        {"Item": "Componentes Eletrônicos", "Categoria": "Matéria-Prima", "Valor (R$)": 3200.00, "Prioridade": "Alta"},
        {"Item": "Desenvolvimento de Software", "Categoria": "Mão de Obra", "Valor (R$)": 8000.00, "Prioridade": "Alta"},
        {"Item": "Operadores de Máquina", "Categoria": "Mão de Obra", "Valor (R$)": 4200.00, "Prioridade": "Média"},
        {"Item": "Frete de Entrega Regional", "Categoria": "Logística", "Valor (R$)": 1800.00, "Prioridade": "Média"},
        {"Item": "Embalagens Sustentáveis", "Categoria": "Logística", "Valor (R$)": 950.00, "Prioridade": "Baixa"},
        {"Item": "Consumo Elétrico Industrial", "Categoria": "Energia", "Valor (R$)": 2300.00, "Prioridade": "Alta"},
        {"Item": "Combustível Gerador", "Categoria": "Energia", "Valor (R$)": 1100.00, "Prioridade": "Baixa"},
        {"Item": "Licença de Softwares CAD", "Categoria": "Ferramentas", "Valor (R$)": 2500.00, "Prioridade": "Média"},
        {"Item": "Manutenção de Impressora 3D", "Categoria": "Ferramentas", "Valor (R$)": 850.00, "Prioridade": "Baixa"}
    ]
    return pd.DataFrame(dados)

df_base = carregar_dados()

# -----------------------------------------------------------------------------
# 2. Barra Lateral (Sidebar)
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Configurações & Filtros")

# Slider de Orçamento
orcamento_disponivel = st.sidebar.slider(
    label="Orçamento Total Disponível (R$)",
    min_value=5000.0,
    max_value=50000.0,
    value=20000.0,
    step=500.0,
    format="R$ %.2f"
)

# Filtro por Categoria
categorias_disponiveis = df_base["Categoria"].unique().tolist()
categorias_selecionadas = st.sidebar.multiselect(
    label="Categorias a Exibir",
    options=categorias_disponiveis,
    default=categorias_disponiveis
)

# Filtragem do DataFrame
if categorias_selecionadas:
    df_filtrado = df_base[df_base["Categoria"].isin(categorias_selecionadas)]
else:
    df_filtrado = df_base.iloc[0:0]  # DataFrame vazio caso nada esteja selecionado

# -----------------------------------------------------------------------------
# 3. Área Principal
# -----------------------------------------------------------------------------
st.title("📊 Simulador de Custos e Orçamento")
st.markdown("Gerencie despesas simuladas, analise o impacto no orçamento e monitore os saldos em tempo real.")

st.markdown("---")

# Métricas Calculadas
gasto_filtrado = df_filtrado["Valor (R$)"].sum() if not df_filtrado.empty else 0.0
saldo_restante = orcamento_disponivel - gasto_filtrado

# Painel de 3 Métricas
col1, col2, col3 = st.columns(3)

col1.metric(
    label="Orçamento Definido",
    value=f"R$ {orcamento_disponivel:,.2f}"
)

col2.metric(
    label="Gasto Filtrado",
    value=f"R$ {gasto_filtrado:,.2f}"
)

col3.metric(
    label="Saldo Restante",
    value=f"R$ {saldo_restante:,.2f}",
    delta=f"R$ {saldo_restante:,.2f}",
    delta_color="normal"
)

st.markdown("<br>", unsafe_allow_html=True)

# Alert Visual Condicional
if gasto_filtrado <= orcamento_disponivel:
    st.success(f"✅ **Projeto dentro da meta!** Você ainda possui **R$ {saldo_restante:,.2f}** de margem orçamentária.")
else:
    excedente = abs(saldo_restante)
    st.error(f"⚠️ **Orçamento Excedido!** Os custos selecionados ultrapassam o limite em **R$ {excedente:,.2f}**.")

st.markdown("---")

# Visualização de Dados (Gráfico de Barras Nativos e Tabela)
col_grafico, col_tabela = st.columns([1, 1])

with col_grafico:
    st.subheader("📌 Gastos por Categoria")
    if not df_filtrado.empty:
        gastos_por_categoria = df_filtrado.groupby("Categoria")["Valor (R$)"].sum()
        st.bar_chart(gastos_por_categoria)
    else:
        st.info("Nenhuma categoria selecionada para exibir o gráfico.")

with col_tabela:
    st.subheader("📋 Detalhamento dos Itens")
    if not df_filtrado.empty:
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("Selecione ao menos uma categoria na barra lateral para visualizar a tabela.")
