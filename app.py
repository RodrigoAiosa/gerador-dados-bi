import streamlit as st
from datetime import date
import pandas as pd

from services.data_generator import gerar_base_completa
from utils.zip_exporter import gerar_zip
from style import aplicar_design

# --------------------------------------------------
# CONFIGURACAO
# --------------------------------------------------
st.set_page_config(
    page_title="BI Data Generator PRO",
    page_icon="📊",
    layout="wide",
)

aplicar_design()

# --------------------------------------------------
# FUNCAO: gerar dCalendario
# --------------------------------------------------
def gerar_dCalendario(data_inicio: date, data_fim: date) -> pd.DataFrame:
    """
    Gera dCalendario equivalente ao script Power Query.

    Colunas:
        Data      -> date
        Ano       -> int64   (Date.Year)
        Mes       -> int64   (Date.Month)
        MesAno    -> str     (Text.Proper MMM/yy  ex: Jan/23)
        IdMesAno  -> int64   (Ano*100 + Mes        ex: 202301)
    """
    lista_datas = pd.date_range(start=data_inicio, end=data_fim, freq="D")
    df = pd.DataFrame({"Data": lista_datas.date})

    df["Ano"]      = pd.to_datetime(df["Data"]).dt.year.astype("int64")
    df["Mes"]      = pd.to_datetime(df["Data"]).dt.month.astype("int64")
    df["MesAno"]   = pd.to_datetime(df["Data"]).dt.strftime("%b/%y").str.title()
    df["IdMesAno"] = (df["Ano"] * 100 + df["Mes"]).astype("int64")

    return df[["Data", "Ano", "Mes", "MesAno", "IdMesAno"]]


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("Parametros")
st.sidebar.markdown("Configure sua base de dados:")

setor = st.sidebar.selectbox(
    "Setor",
    [
        "Varejo", "Financeiro", "Saude", "Tecnologia",
        "Educacao", "Logistica", "Energia",
        "Telecom", "Industria", "Agronegocio",
    ],
)

data_inicio = st.sidebar.date_input(
    "Data Inicio",
    value=date(2023, 1, 1),
)
data_fim = st.sidebar.date_input(
    "Data Fim",
    value=date(2023, 12, 31),
    min_value=data_inicio,
)

linhas = st.sidebar.slider(
    "Quantidade de linhas",
    min_value=1000,
    max_value=10000,
    value=5000,
    step=1000,
)

gerar = st.sidebar.button("Gerar Base")

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("BI Data Generator")
st.caption(
    "Geracao profissional de dados no modelo estrela "
    "para projetos de Business Intelligence"
)
st.divider()

# --------------------------------------------------
# AREA PRINCIPAL
# --------------------------------------------------
if gerar:
    with st.spinner("Gerando base de dados..."):
        dataframes = gerar_base_completa(setor, data_inicio, data_fim, linhas)
        df_calendario = gerar_dCalendario(data_inicio, data_fim)
        dataframes["dCalendario"] = df_calendario
        zip_file = gerar_zip(dataframes)

    # ---- Status ----
    st.success("Base gerada com sucesso!")

    total_dias = (data_fim - data_inicio).days + 1

    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
    col1.metric("Setor",           setor)
    col2.metric("Periodo",         f"{data_inicio}  ->  {data_fim}")
    col3.metric("Linhas Fato",     f"{linhas:,}")
    col4.metric("Dias Calendario", f"{total_dias:,}")

    st.divider()

    # ---- Preview ----
    st.subheader("Preview das Tabelas")
    for nome, df in dataframes.items():
        with st.expander(f"{nome} - {len(df):,} linhas", expanded=False):
            st.dataframe(df.head(20), use_container_width=True)

    st.divider()

    # ---- Download ----
    st.download_button(
        label="Baixar Base Completa com dCalendario (.zip)",
        data=zip_file,
        file_name=f"Base_BI_{setor}.zip",
        mime="application/zip",
        use_container_width=True,
    )

else:
    st.info("Configure os parametros no menu lateral e clique em **Gerar Base**.")
