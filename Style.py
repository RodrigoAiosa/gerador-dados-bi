import streamlit as st


def aplicar_design():
    """
    Aplica o CSS premium DataHub ao app Streamlit.
    Chame esta função logo após st.set_page_config().
    """
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ══════════════════════════════════════
   RESET & BASE
══════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html,
body,
.main,
[data-testid="stAppViewContainer"] {
    background-color: #060912 !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #060912 !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0,180,216,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 80% 60%,  rgba(0,100,180,0.07) 0%, transparent 50%);
}

/* dot-grid overlay */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background-image: radial-gradient(rgba(0,180,216,0.07) 1px, transparent 1px);
    background-size: 28px 28px;
    mask-image: radial-gradient(ellipse 90% 90% at 50% 50%, black 10%, transparent 100%);
}

[data-testid="stHeader"] { background: transparent !important; }

/* ══════════════════════════════════════
   TIPOGRAFIA
══════════════════════════════════════ */
.main h1, .main h2, .main h3, .main h4,
.main p,  .main a,  .main li,
[data-testid="stAppViewContainer"] div:not([data-testid="stSidebar"]) {
    font-family: 'DM Sans', sans-serif !important;
}

h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    color: #f0f4ff !important;
}

/* ══════════════════════════════════════
   LAYOUT
══════════════════════════════════════ */
[data-testid="stMarkdownContainer"] { width: 100% !important; }

.block-container {
    max-width: 100% !important;
    padding-left:  4rem !important;
    padding-right: 4rem !important;
    padding-top:   2rem !important;
}

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background-color: #0d1120 !important;
    border-right: 1px solid rgba(0,180,216,0.12) !important;
}

section[data-testid="stSidebar"] .stMarkdown p {
    color: #7b8ba8 !important;
    font-size: 0.82rem !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    color: #f0f4ff !important;
    font-family: 'Syne', sans-serif !important;
}

/* sidebar selectbox / inputs */
section[data-testid="stSidebar"] [data-testid="stSelectbox"] > div,
section[data-testid="stSidebar"] [data-testid="stDateInput"]  > div input {
    background: rgba(0,180,216,0.06) !important;
    border: 1px solid rgba(0,180,216,0.18) !important;
    border-radius: 8px !important;
    color: #e8edf8 !important;
}

/* slider */
section[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {
    background: #00b4d8 !important;
    box-shadow: 0 0 12px rgba(0,180,216,0.5) !important;
}
section[data-testid="stSidebar"] [data-testid="stSlider"] div[data-baseweb="slider"] > div:first-child {
    background: rgba(0,180,216,0.2) !important;
}
section[data-testid="stSidebar"] [data-testid="stSlider"] div[data-baseweb="slider"] > div:nth-child(2) {
    background: linear-gradient(90deg, #00b4d8, #0096c7) !important;
}

/* ══════════════════════════════════════
   BOTAO GERAR (sidebar)
══════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #00b4d8 0%, #0077b6 100%) !important;
    color: #001a24 !important;
    border-radius: 12px !important;
    height: 3em !important;
    width: 100% !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.92rem !important;
    border: none !important;
    letter-spacing: 0.02em !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(0,180,216,0.35) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #48cae4 0%, #00b4d8 100%) !important;
    box-shadow: 0 8px 32px rgba(0,180,216,0.5) !important;
    transform: translateY(-2px) !important;
}

/* ══════════════════════════════════════
   BOTAO DOWNLOAD
══════════════════════════════════════ */
.stDownloadButton > button {
    background: linear-gradient(135deg, #00b4d8 0%, #0077b6 100%) !important;
    color: #001a24 !important;
    border-radius: 12px !important;
    height: 3em !important;
    width: 100% !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.92rem !important;
    border: none !important;
    letter-spacing: 0.02em !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(0,180,216,0.35) !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #48cae4 0%, #00b4d8 100%) !important;
    box-shadow: 0 8px 32px rgba(0,180,216,0.5) !important;
    transform: translateY(-2px) !important;
}

/* ══════════════════════════════════════
   STATUS MESSAGES
══════════════════════════════════════ */
.stSuccess {
    background-color: rgba(0,180,216,0.08) !important;
    color: #00b4d8 !important;
    border-left: 3px solid #00b4d8 !important;
    border-radius: 10px !important;
}

.stInfo {
    background-color: rgba(0,180,216,0.05) !important;
    color: #7b8ba8 !important;
    border-left: 3px solid rgba(0,180,216,0.4) !important;
    border-radius: 10px !important;
}

/* ══════════════════════════════════════
   METRICS
══════════════════════════════════════ */
[data-testid="stMetricLabel"] {
    color: #7b8ba8 !important;
    font-size: 0.82rem !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.02em !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    color: #00b4d8 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: unset !important;
    font-size: clamp(0.85rem, 1.4vw, 1.6rem) !important;
}

/* metric container card */
[data-testid="stMetric"] {
    background: rgba(0,180,216,0.04) !important;
    border: 1px solid rgba(0,180,216,0.12) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

/* ══════════════════════════════════════
   DIVIDER
══════════════════════════════════════ */
hr {
    border: 0 !important;
    height: 1px !important;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(0,180,216,0.3),
        transparent
    ) !important;
    margin: 2rem 0 !important;
}

/* ══════════════════════════════════════
   EXPANDER
══════════════════════════════════════ */
[data-testid="stExpander"] {
    border: 1px solid rgba(0,180,216,0.15) !important;
    border-radius: 12px !important;
    background: rgba(0,180,216,0.02) !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stExpander"]:hover {
    border-color: rgba(0,180,216,0.3) !important;
}
[data-testid="stExpanderDetails"] {
    background: rgba(0,180,216,0.02) !important;
}

/* expander header text */
[data-testid="stExpander"] summary span p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    color: #8fa0bb !important;
}
[data-testid="stExpander"]:hover summary span p {
    color: #00b4d8 !important;
}

/* ══════════════════════════════════════
   DATAFRAME
══════════════════════════════════════ */
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid rgba(0,180,216,0.12) !important;
}

/* ══════════════════════════════════════
   CAPTION
══════════════════════════════════════ */
.stCaption {
    color: #7b8ba8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
}

/* ══════════════════════════════════════
   SPINNER
══════════════════════════════════════ */
[data-testid="stSpinner"] {
    color: #00b4d8 !important;
}

/* ══════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════ */
::-webkit-scrollbar       { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #060912; }
::-webkit-scrollbar-thumb {
    background: rgba(0,180,216,0.2);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(0,180,216,0.45); }

/* ══════════════════════════════════════
   BADGE PERSONALIZADO (uso no app.py)
   Exemplo: st.markdown('<span class="badge-cyan">texto</span>', True)
══════════════════════════════════════ */
.badge-cyan {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,180,216,0.08);
    border: 1px solid rgba(0,180,216,0.25);
    border-radius: 100px;
    padding: 4px 14px;
    font-size: 0.72rem;
    color: #00b4d8;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
</style>
        """,
        unsafe_allow_html=True,
    )
