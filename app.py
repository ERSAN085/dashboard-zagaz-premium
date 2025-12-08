# =========================================================
# ZAGAZ · Dashboard Estratégico GNV — Versión Premium
# Arquitectura visual modular + diseño corporativo
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN INICIAL DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="ZAGAZ · Dashboard Estratégico",
    page_icon="💠",
    layout="wide"
)

# ---------------------------------------------------------
# INYECCIÓN DE CSS PREMIUM
# ---------------------------------------------------------
with open("assets/style.css", "w") as f:
    f.write("""
/* ====================== */
/* ESTILO PREMIUM GLOBAL  */
/* ====================== */

body, .stApp {
    background-color: #f6f7f9 !important;
    font-family: 'Inter', sans-serif;
}

/* Encabezado */
.zg-header {
    background: linear-gradient(90deg, #0b8a3b, #21c06b);
    padding: 30px 40px;
    border-radius: 16px;
    margin-bottom: 30px;
    color: white;
}

.zg-title {
    font-size: 2.5rem;
    font-weight: 900;
}

.zg-subtitle {
    font-size: 1.1rem;
    margin-top: -6px;
    opacity: 0.95;
}

/* Tarjetas Premium */
.zg-card {
    background: white;
    border-radius: 14px;
    padding: 20px 26px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

.zg-section-title {
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 8px;
    color: #0a2a18;
}

.zg-section-sub {
    font-size: 0.95rem;
    color: #58746a;
    margin-bottom: 20px;
}
    """)

# Inyectamos CSS
with open("assets/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


# ---------------------------------------------------------
# CARGA DE DATOS
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("data/dataset_valores.xlsx")

df = load_data()


# ---------------------------------------------------------
# ENCABEZADO PRINCIPAL DEL DASHBOARD
# ---------------------------------------------------------
st.markdown("""
<div class="zg-header">
    <div class="zg-title">ZAGAZ · Dashboard Estratégico GNV</div>
    <div class="zg-subtitle">
        Decisiones basadas en datos · segmentos · adopción · riesgos y oportunidades
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SECCIÓN 1 · BLOQUE PREMIUM (Aquí insertaremos KPIs + gráfico)
# ---------------------------------------------------------
st.markdown("""
<div class='zg-section-title'>Bloque Premium Inicial</div>
<div class='zg-section-sub'>Aquí colocaremos el primer bloque visual: KPIs principales + gráfico principal.</div>
""", unsafe_allow_html=True)

st.markdown("<div class='zg-card'>[ Bloque Premium #1 irá aquí ]</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# SECCIÓN 2 · KPI A (Versión Premium)
# ---------------------------------------------------------
st.markdown("""
<div class='zg-section-title'>KPI A · Panorama del Mercado</div>
<div class='zg-section-sub'>Valores estructurales del ecosistema de transporte.</div>
""", unsafe_allow_html=True)

st.markdown("<div class='zg-card'>[ Aquí insertaremos KPI A premium ]</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# SECCIÓN 3 · KPI B (Dinámica filtrada)
# ---------------------------------------------------------
st.markdown("""
<div class='zg-section-title'>KPI B · Dinámica de la Muestra</div>
<div class='zg-section-sub'>Valores condicionados por filtros o criterios dinámicos.</div>
""", unsafe_allow_html=True)

st.markdown("<div class='zg-card'>[ KPI B premium irá aquí ]</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# SECCIÓN 4 · INSIGHTS (al final)
# ---------------------------------------------------------
st.markdown("""
<div class='zg-section-title'>Insights Críticos</div>
<div class='zg-section-sub'>Interpretaciones basadas en patrones del dataset.</div>
""", unsafe_allow_html=True)

st.markdown("<div class='zg-card'>[ Insights premium irán aquí ]</div>", unsafe_allow_html=True)

