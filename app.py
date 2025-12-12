# =========================================================
# ZAGAZ · Dashboard Estratégico GNV — Versión Premium
# Arquitectura visual modular + diseño corporativo
# =========================================================

import os
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN INICIAL DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="ZAGAZ · Dashboard Estratégico GNV",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar colapsado por defecto (mejor para móvil)
)

# ---------------------------------------------------------
# INYECCIÓN DE CSS PREMIUM (no sobrescribir si ya existe)
# ---------------------------------------------------------
assets_dir = Path("assets")
assets_dir.mkdir(parents=True, exist_ok=True)
css_path = assets_dir / "style.css"

default_css = """
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
"""

if not css_path.exists():
    css_path.write_text(default_css)

with open(css_path) as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# CSS para bordes verdes en gráficos de Plotly y responsive design
st.markdown("""
<style>
    /* Borde verde para todos los gráficos de Plotly */
    [data-testid="stPlotlyChart"] {
        border: 3px solid #10b981;
        border-radius: 14px;
        padding: 15px;
        background: white;
    }
    
    /* Colores verdes vibrantes para controles del sidebar */
    /* Multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #22c55e !important;
    }
    .stMultiSelect [data-baseweb="select"] > div {
        border-color: #22c55e !important;
    }
    .stMultiSelect [data-baseweb="select"] > div:focus-within {
        border-color: #34d399 !important;
        box-shadow: 0 0 0 2px rgba(52, 211, 153, 0.2) !important;
    }
    
    /* Slider */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #22c55e !important;
    }
    .stSlider [data-baseweb="slider"] > div > div {
        background-color: #22c55e !important;
    }
    .stSlider [data-baseweb="slider"] > div > div > div {
        background-color: rgba(52, 211, 153, 0.3) !important;
    }
    /* Track del slider (barra completa) */
    .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] > div {
        background-color: #22c55e !important;
    }
    /* Thumb (círculo que se mueve) */
    .stSlider [data-baseweb="slider"] [role="slider"]:before {
        background-color: #22c55e !important;
        border-color: #22c55e !important;
    }
    
    /* Date Input */
    .stDateInput [data-baseweb="input"] {
        border-color: #22c55e !important;
    }
    .stDateInput [data-baseweb="input"]:focus-within {
        border-color: #34d399 !important;
        box-shadow: 0 0 0 2px rgba(52, 211, 153, 0.2) !important;
    }
    .stDateInput button {
        color: #22c55e !important;
    }
    
    /* ========================================
       RESPONSIVE DESIGN PARA MÓVIL Y TABLET
       ======================================== */
    
    /* Media query para tablets (768px - 1024px) */
    @media (max-width: 1024px) {
        /* Reducir tamaño de títulos principales */
        h2 {
            font-size: 1.4rem !important;
        }
        
        /* Ajustar header */
        .zg-header .zg-title {
            font-size: 1.8rem !important;
        }
        .zg-header .zg-subtitle {
            font-size: 0.9rem !important;
        }
        
        /* Reducir padding en gráficos */
        [data-testid="stPlotlyChart"] {
            padding: 10px !important;
        }
        
        /* KPIs más compactos */
        .zg-card {
            padding: 15px 18px !important;
        }
    }
    
    /* Media query para móviles (menos de 768px) */
    @media (max-width: 768px) {
        /* Sidebar colapsado por defecto */
        section[data-testid="stSidebar"] {
            width: 0px !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            width: 280px !important;
        }
        
        /* Reducir títulos principales */
        h2 {
            font-size: 1.2rem !important;
            margin-top: 20px !important;
            margin-bottom: 15px !important;
        }
        
        h3 {
            font-size: 1rem !important;
        }
        
        /* Header más compacto */
        .zg-header {
            padding: 20px 20px !important;
        }
        .zg-header .zg-title {
            font-size: 1.5rem !important;
        }
        .zg-header .zg-subtitle {
            font-size: 0.85rem !important;
        }
        
        /* Ocultar imagen del header en móvil */
        .zg-header img {
            display: none !important;
        }
        
        /* KPIs más compactos */
        .zg-card {
            padding: 12px 15px !important;
            margin-bottom: 15px !important;
        }
        .zg-card div[style*="font-size:2.2rem"] {
            font-size: 1.8rem !important;
        }
        .zg-card div[style*="font-size:4rem"] {
            font-size: 2.5rem !important;
        }
        
        /* Gráficos más pequeños */
        [data-testid="stPlotlyChart"] {
            padding: 8px !important;
            border-width: 2px !important;
        }
        
        /* Footer más compacto */
        .zg-header + div {
            padding: 20px 15px !important;
        }
        
        /* Reducir márgenes generales */
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* Botones de descarga apilados */
        .stDownloadButton {
            margin-bottom: 10px !important;
        }
        
        /* Expander más compacto */
        .stExpander {
            font-size: 0.9rem !important;
        }
    }
    
    /* Media query para móviles muy pequeños (menos de 480px) */
    @media (max-width: 480px) {
        h2 {
            font-size: 1.1rem !important;
        }
        
        .zg-header .zg-title {
            font-size: 1.3rem !important;
        }
        
        .zg-header .zg-subtitle {
            font-size: 0.75rem !important;
            line-height: 1.4 !important;
        }
        
        /* KPIs aún más compactos */
        .zg-card div[style*="font-size:2.2rem"] {
            font-size: 1.5rem !important;
        }
        .zg-card div[style*="font-size:4rem"] {
            font-size: 2rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ENCABEZADO PRINCIPAL
# ---------------------------------------------------------
import base64
from pathlib import Path
header_img_path = Path("assets/uploads/8.png")
if header_img_path.exists():
    with open(header_img_path, "rb") as img_file:
        header_img_base64 = base64.b64encode(img_file.read()).decode()
    header_img_html = f"<img src='data:image/png;base64,{header_img_base64}' style='position:absolute; right:30px; top:50%; transform:translateY(-50%); width:350px; height:auto; object-fit:contain;'>"
else:
    header_img_html = ""

st.markdown(f"""
<div class="zg-header" style="display:flex; justify-content:space-between; align-items:center; position:relative;">
    <div>
        <div class="zg-title">Dashboard Estratégico GNV</div>
        <div class="zg-subtitle">
            Decisiones basadas en datos · segmentos · adopción · riesgos y oportunidades
        </div>
    </div>
    {header_img_html}
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CARGA DE DATOS
# ---------------------------------------------------------
@st.cache_data
def load_data():
    data_path = Path("data/dataset_valores.xlsx")
    if not data_path.exists():
        return pd.DataFrame()
    try:
        return pd.read_excel(data_path)
    except Exception:
        return pd.DataFrame()

df = load_data()

# ---------------------------------------------------------
# CARGA DE DATOS
# ---------------------------------------------------------
df = load_data()
if df.empty:
    st.warning("No se encontró `data/dataset_valores.xlsx` o el archivo está vacío. Sube un archivo en la barra lateral o coloca el dataset en `data/`.")

# ---------------------------------------------------------
# DEFINICIÓN DE KPIs (valores seguros por defecto)
# ---------------------------------------------------------
KPI_TAXIS = 0
KPI_UBER_DIDI = 0
KPI_VAGONETAS = 0
KPI_URBANOS_TOTALES = 0

# Si el dataframe tiene columnas esperadas, intentar calcular KPIs mínimos
if not df.empty:
    KPI_REGISTROS_ESTUDIO = len(df)
    # intentos seguros de obtener conteos por tipo si existe una columna 'tipo' o 'categoria'
    if "tipo" in df.columns:
        counts = df["tipo"].value_counts()
        KPI_TAXIS = int(counts.get("Taxis", 0))
        KPI_UBER_DIDI = int(counts.get("Uber/Didi", 0))
        KPI_VAGONETAS = int(counts.get("Vagonetas", 0))
    else:
        KPI_REGISTROS_ESTUDIO = len(df)
else:
    KPI_REGISTROS_ESTUDIO = 0

KPI_UNIVERSO_TOTAL = KPI_TAXIS + KPI_UBER_DIDI + KPI_VAGONETAS + KPI_URBANOS_TOTALES
KPI_RUTAS_TOTALES = 0

# ---------------------------------------------------------
# NUEVO DISEÑO: filtros, KPIs, gráficos e insights
# ---------------------------------------------------------

def detect_date_column(df):
    for col in df.columns:
        if "fecha" in col.lower() or "date" in col.lower():
            return col
    return None


def find_col(df, keywords):
    """Buscar primer nombre de columna que contenga alguna de las palabras clave (case-insensitive)."""
    for col in df.columns:
        low = col.lower()
        for k in keywords:
            if k.lower() in low:
                return col
    return None


def sidebar_filters(df):
    st.sidebar.header("Filtros")
    filters = {}
    if df.empty:
        return filters

    # --- Filtros solicitados explícitamente por el usuario ---
    # 1) Tipo de unidad
    tipo_col = find_col(df, ["tipo de unidad", "tipo unidad", "tipo"]) 
    if tipo_col:
        vals = sorted(df[tipo_col].dropna().unique().tolist())
        if vals:
            sel = st.sidebar.multiselect("Tipo de unidad", options=vals, default=vals)
            filters[tipo_col] = sel

    # 2) Perfil de adopción
    perfil_col = find_col(df, ["perfil adop", "perfil", "adopción", "adopcion"]) 
    if perfil_col:
        vals = sorted(df[perfil_col].dropna().unique().tolist())
        if vals:
            sel = st.sidebar.multiselect("Perfil de adopción", options=vals, default=vals)
            filters[perfil_col] = sel

    # 3) Rango generacional -> usar columna 'Edad' o similar
    edad_col = find_col(df, ["edad", "generaci", "age"]) 
    if edad_col:
        try:
            min_v = int(pd.to_numeric(df[edad_col], errors='coerce').min())
            max_v = int(pd.to_numeric(df[edad_col], errors='coerce').max())
            if pd.notna(min_v) and pd.notna(max_v):
                sel = st.sidebar.slider("Rango edad", min_value=min_v, max_value=max_v, value=(min_v, max_v))
                filters[edad_col] = sel
        except Exception:
            pass

    # 4) Dueño / Operador
    duenio_col = find_col(df, ["dueño", "dueno", "operador", "propietario", "dueño/operador"]) 
    if duenio_col:
        vals = sorted(df[duenio_col].dropna().unique().tolist())
        if vals:
            sel = st.sidebar.multiselect("Dueño / Operador", options=vals, default=vals)
            filters[duenio_col] = sel

    # Mantener también rango de fecha si existe
    date_col = detect_date_column(df)
    if date_col:
        try:
            df[date_col] = pd.to_datetime(df[date_col])
            min_date = df[date_col].min().date()
            max_date = df[date_col].max().date()
            dr = st.sidebar.date_input("Rango fecha", value=(min_date, max_date))
            filters[date_col] = dr
        except Exception:
            pass

    return filters


def apply_filters(df, filters):
    if df.empty or not filters:
        return df
    out = df.copy()
    for col, sel in filters.items():
        if col not in out.columns:
            continue
        # Date range (tuple from date_input)
        if pd.api.types.is_datetime64_any_dtype(out[col]) and isinstance(sel, tuple) and len(sel) == 2:
            try:
                start, end = sel
                out = out[(pd.to_datetime(out[col]).dt.date >= start) & (pd.to_datetime(out[col]).dt.date <= end)]
            except Exception:
                continue
        # Numeric range (Edad slider returns tuple of two ints)
        elif (isinstance(sel, tuple) and len(sel) == 2) and pd.api.types.is_numeric_dtype(out[col]):
            try:
                start, end = sel
                out = out[(pd.to_numeric(out[col], errors='coerce') >= start) & (pd.to_numeric(out[col], errors='coerce') <= end)]
            except Exception:
                continue
        elif isinstance(sel, list):
            if len(sel) == 0:
                out = out.iloc[0:0]
            else:
                out = out[out[col].isin(sel)]
    return out


def compute_kpis(df, df_total):
    k = {}
    k["total_registros"] = len(df_total)
    k["registros_filtrados"] = len(df)
    k["pct_filtrados"] = (len(df) / len(df_total) * 100) if len(df_total) > 0 else 0
    # tipo dominante
    if "tipo" in df.columns:
        top = df["tipo"].value_counts(normalize=True)
        if not top.empty:
            k["top_tipo"] = top.index[0]
            k["top_tipo_share"] = float(top.iloc[0])
        else:
            k["top_tipo"] = None
            k["top_tipo_share"] = 0
    else:
        k["top_tipo"] = None
        k["top_tipo_share"] = 0
    return k


def make_charts(df):
    charts = {}
    if df.empty:
        return charts
    if "tipo" in df.columns:
        df_tipo = df["tipo"].value_counts().reset_index()
        df_tipo.columns = ["tipo", "count"]
        fig = px.pie(df_tipo, names="tipo", values="count", hole=0.5, title="Distribución por tipo")
        charts["donut_tipo"] = fig

    # top rutas
    if "ruta" in df.columns:
        top_rutas = df["ruta"].value_counts().head(10).reset_index()
        top_rutas.columns = ["ruta", "count"]
        fig2 = px.bar(top_rutas, x="ruta", y="count", title="Top rutas (10)", labels={"count":"Registros","ruta":"Ruta"})
        charts["bar_rutas"] = fig2

    # time series if date
    date_col = detect_date_column(df)
    if date_col:
        try:
            df[date_col] = pd.to_datetime(df[date_col])
            series = df.groupby(pd.Grouper(key=date_col, freq='W'))[date_col].count().reset_index(name='count')
            fig3 = px.line(series, x=date_col, y='count', title='Registros por semana')
            charts["ts_registros"] = fig3
        except Exception:
            pass

    return charts


def generate_insights(kpis, df, df_total):
    insights = []
    if kpis["registros_filtrados"] == 0:
        insights.append("No hay registros con los filtros seleccionados.")
        return insights

    if kpis.get("top_tipo") and kpis.get("top_tipo_share", 0) > 0.6:
        insights.append(f"Predominancia de '{kpis['top_tipo']}' en la muestra filtrada ({kpis['top_tipo_share']:.0%}).")

    # comparar proporción filtrada vs total por tipo si posible
    if "tipo" in df.columns and len(df_total) > 0:
        global_top = df_total["tipo"].value_counts(normalize=True)
        local_top = df["tipo"].value_counts(normalize=True)
        if not global_top.empty and not local_top.empty:
            gt = global_top.index[0]
            lt = local_top.index[0]
            if gt != lt:
                insights.append(f"El tipo dominante a nivel global es '{gt}', pero en la selección actual domina '{lt}'.")

    # tendencia temporal simple
    date_col = detect_date_column(df)
    if date_col and len(df) > 5:
        try:
            df[date_col] = pd.to_datetime(df[date_col])
            weekly = df.groupby(pd.Grouper(key=date_col, freq='W'))[date_col].count()
            if len(weekly) >= 4:
                last = weekly.iloc[-1]
                prev = weekly.iloc[-4:-1].mean()
                if prev > 0 and (last / prev) > 1.25:
                    insights.append("Aumento reciente en registros (última semana >25% promedio previo).")
                elif prev > 0 and (last / prev) < 0.8:
                    insights.append("Disminución reciente en registros (última semana <80% promedio previo).")
        except Exception:
            pass

    if not insights:
        insights.append("No se detectaron insights automáticos relevantes; revisar filtros o criterios de segmentación.")

    return insights


# -------------------------
# Render principal
# -------------------------

# Crear placeholder para KPI dinámico en sidebar (se actualiza después de filtros)
kpi_placeholder = st.sidebar.empty()
kpi_porcentaje_placeholder = st.sidebar.empty()
kpi_universo_placeholder = st.sidebar.empty()

filters = sidebar_filters(df)
df_filtered = apply_filters(df, filters) if not df.empty else df

# Actualizar KPIs dinámicos en los placeholders (arriba de filtros)
registros_filtrados = len(df_filtered) if not df_filtered.empty else 0
total_muestra = len(df) if not df.empty else 1  # Evitar división por cero
porcentaje_filtrado = (registros_filtrados / total_muestra) * 100
universo_proyectado = int(round((registros_filtrados / total_muestra) * KPI_UNIVERSO_TOTAL))

kpi_html = f"""
<div class='zg-card' style='margin-bottom:20px; border:3px solid #10b981;'>
    <div style='font-size:0.85rem; color:#475569; text-transform:uppercase;'>Registros validados</div>
    <div style='font-size:2.2rem; font-weight:900; color:#0f172a;'>{registros_filtrados:,}</div>
    <div style='font-size:0.85rem; color:#10b981;'>Muestra representativa</div>
</div>
"""
kpi_placeholder.markdown(kpi_html, unsafe_allow_html=True)

# KPI 2: Porcentaje de la muestra
kpi_porcentaje_html = f"""
<div class='zg-card' style='margin-bottom:20px; border:3px solid #10b981;'>
    <div style='font-size:0.85rem; color:#475569; text-transform:uppercase;'>Porcentaje de muestra</div>
    <div style='font-size:2.2rem; font-weight:900; color:#0f172a;'>{porcentaje_filtrado:.1f}%</div>
    <div style='font-size:0.85rem; color:#10b981;'>De {total_muestra:,} registros totales</div>
</div>
"""
kpi_porcentaje_placeholder.markdown(kpi_porcentaje_html, unsafe_allow_html=True)

# KPI 3: Proyección al universo
kpi_universo_html = f"""
<div class='zg-card' style='margin-bottom:20px; border:3px solid #10b981;'>
    <div style='font-size:0.85rem; color:#475569; text-transform:uppercase;'>Proyección universo</div>
    <div style='font-size:2.2rem; font-weight:900; color:#0f172a;'>{universo_proyectado:,}</div>
    <div style='font-size:0.85rem; color:#10b981;'>Unidades del universo total</div>
</div>
"""
kpi_universo_placeholder.markdown(kpi_universo_html, unsafe_allow_html=True)

# KPIs
kpis = compute_kpis(df_filtered, df)

# -------------------------
# TOP LAYOUT — KPIs FIJOS + GRÁFICOS + INSIGHT
# -------------------------
# Valores fijos del universo (según solicitud)
KPI_TAXIS = 1739
KPI_UBER_DIDI = 1331
KPI_URBANOS_TOTALES = 640
KPI_VAGONETAS = 530

KPI_UNIVERSO_TOTAL = KPI_TAXIS + KPI_UBER_DIDI + KPI_URBANOS_TOTALES + KPI_VAGONETAS

st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)

# Valor mostrado ajustado por petición: excluir autobuses y vagonetas => 3070
KPI_UNIVERSO_DISPLAY = KPI_TAXIS + KPI_UBER_DIDI

# Título de sección
st.markdown("<h2 style='color:#003d82; font-size:1.8rem; font-weight:800; margin-top:30px; margin-bottom:20px;'>Alcance Real del Mercado Convertible a GNV</h2>", unsafe_allow_html=True)

# Primera fila: 5 KPI fijos (Universo total destacado en verde)
cols_kpi = st.columns(5)
with cols_kpi[0]:
    # Universo Total — tarjeta destacada en verde con texto blanco (valor ajustado)
    st.markdown(f"""
    <div style='background:linear-gradient(90deg,#0b8a3b,#16a34a); border-radius:14px; padding:18px; color:white; border:3px solid #10b981;'>
        <div style='font-size:0.85rem; text-transform:uppercase; opacity:0.95;'>Universo Total</div>
        <div style='font-size:2.2rem; font-weight:900;'>{KPI_UNIVERSO_DISPLAY:,}</div>
        <div style='font-size:0.85rem; opacity:0.95;'><em>Enlace de fuentes</em></div>
    </div>
    """, unsafe_allow_html=True)
with cols_kpi[1]:
    st.markdown(f"""
    <div class='zg-card' style='border:3px solid #10b981;'>
        <div style='font-size:0.85rem; color:#475569; text-transform:uppercase;'>Taxis</div>
        <div style='font-size:2.2rem; font-weight:900; color:#0f172a;'>{KPI_TAXIS:,}</div>
        <div style='font-size:0.85rem; color:#10b981;'>Unidades Taxis</div>
    </div>
    """, unsafe_allow_html=True)
with cols_kpi[2]:
    st.markdown(f"""
    <div class='zg-card' style='border:3px solid #10b981;'>
        <div style='font-size:0.85rem; color:#475569; text-transform:uppercase;'>Plataforma</div>
        <div style='font-size:2.2rem; font-weight:900; color:#0f172a;'>{KPI_UBER_DIDI:,}</div>
        <div style='font-size:0.85rem; color:#10b981;'>Uber / Didi estimado</div>
    </div>
    """, unsafe_allow_html=True)
with cols_kpi[3]:
    st.markdown(f"""
    <div class='zg-card' style='border:3px solid #10b981;'>
        <div style='font-size:0.85rem; color:#475569; text-transform:uppercase;'>Autobuses Diesel</div>
        <div style='font-size:2.2rem; font-weight:900; color:#0f172a;'>{KPI_URBANOS_TOTALES:,}</div>
        <div style='font-size:0.85rem; color:#10b981;'>240 ya usan GNV</div>
    </div>
    """, unsafe_allow_html=True)
with cols_kpi[4]:
    st.markdown(f"""
    <div class='zg-card' style='border:3px solid #10b981;'>
        <div style='font-size:0.85rem; color:#475569; text-transform:uppercase;'>Vagonetas</div>
        <div style='font-size:2.2rem; font-weight:900; color:#0f172a;'>{KPI_VAGONETAS:,}</div>
        <div style='font-size:0.85rem; color:#10b981;'>Vagonetas estimadas</div>
    </div>
    """, unsafe_allow_html=True)

# Segunda fila: 3 gráficos (contenedores más amplios)
g1, g2, g3 = st.columns([1.3, 1.3, 1.3])

# Donut universo (usar paleta verde)
with g1:
    df_universo = pd.DataFrame({
        "Tipo": ["Taxis", "Plataforma", "Autobuses", "Vagonetas"],
        "Total": [KPI_TAXIS, KPI_UBER_DIDI, KPI_URBANOS_TOTALES, KPI_VAGONETAS]
    })
    fig_univ = px.pie(
        df_universo,
        names='Tipo',
        values='Total',
        hole=0.5,
        color_discrete_sequence=["#0b8a3b", "#16a34a", "#10b981", "#0f766e"],
    )
    fig_univ.update_traces(textinfo='percent+label')
    fig_univ.update_layout(title={'text':'Universo por tipo de vehículo','x':0.5,'xanchor':'center','font':{'size':16}}, height=380, margin=dict(t=50, b=20, l=10, r=10))
    st.plotly_chart(fig_univ, use_container_width=True)

# Pie por Marca (participación por marca)
with g2:
    if 'Marca' in df.columns:
        df_marca = df['Marca'].dropna().value_counts().reset_index()
        df_marca.columns = ['Marca','count']
        # colores más vivos para marcas
        vivid_colors = px.colors.qualitative.Bold
        fig_marca = px.pie(
            df_marca,
            names='Marca',
            values='count',
            hole=0.45,
            color_discrete_sequence=vivid_colors
        )
        fig_marca.update_layout(title={'text':'Participación por marca','x':0.5,'xanchor':'center','font':{'size':16}}, height=380, margin=dict(t=50, b=20, l=10, r=10))
        st.plotly_chart(fig_marca, use_container_width=True)
    else:
        st.info('Columna "Marca" no encontrada para gráfico de marca.')

# Barras por año de vehículo
with g3:
    year_col = None
    if 'Año_Vehículo' in df.columns:
        year_col = 'Año_Vehículo'
    else:
        year_col = find_col(df, ['año', 'ano', 'year'])
    if year_col and year_col in df.columns:
        try:
            df_year = pd.to_numeric(df[year_col], errors='coerce').dropna().astype(int)
            counts = df_year.value_counts().reset_index()
            counts.columns = [year_col, 'count']
            # seleccionar top 12 por conteo, ordenar por año para mostrar
            top12 = counts.nlargest(12, 'count').sort_values(year_col).reset_index(drop=True)
            # identificar top 3 años que sobresalen (por count)
            top3_years = counts.nlargest(3, 'count')[year_col].tolist()
            # asignar colores: azul para top3, gris claro para el resto
            colors = [('#1f77b4' if int(y) in top3_years else '#9ca3af') for y in top12[year_col]]
            fig_year = px.bar(top12, x=year_col, y='count', title='Distribución por año')
            fig_year.update_traces(marker_color=colors)
            fig_year.update_layout(title={'text':'Distribución por año','x':0.5,'xanchor':'center','font':{'size':16}}, height=380, margin=dict(t=50, b=40, l=40, r=10))
            st.plotly_chart(fig_year, use_container_width=True)
        except Exception:
            st.info('No fue posible graficar años.')
    else:
        st.info('Columna año no encontrada.')

# Insight: caja alargada debajo de los 3 gráficos, borde verde marcado
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
total_base = KPI_UNIVERSO_TOTAL
trucks_using_gnv = 240
camionetas_no_cargaran = 530
diesel_buses = 400
# remaining refleja el universo después de excluir UNIBUS, vagonetas de Nayarit y autobuses diésel
remaining = total_base - trucks_using_gnv - camionetas_no_cargaran - diesel_buses
insight_html = f"""
<div class='zg-card' style='border:3px solid #10b981;'>
    <div style='font-size:0.85rem; color:#475569; text-transform:uppercase; margin-bottom:12px;'>Ajuste real del mercado convertible</div>
    <div style='font-size:0.9rem; color:#374151; line-height:1.5;'>El valor mostrado en el KPI <strong>Universo Total</strong> excluye:<br>
    &middot; <strong style='color:#0f172a;'>{trucks_using_gnv:,}</strong> autobuses de <em>UNIBUS</em>, que operan con su propia estación de autoconsumo;<br>
    &middot; <strong style='color:#0f172a;'>{camionetas_no_cargaran:,}</strong> vagonetas de Nayarit, que por dinámicas operativas y geopolíticas no participarían en el sistema local;<br>
    &middot; <strong style='color:#0f172a;'>400</strong> autobuses que conforman el resto del parque vehicular y que actualmente operan con diésel.<br><br>
    El KPI refleja únicamente el mercado directamente convertible a GNV, mientras que el segmento diésel requiere una estrategia específica de sustitución que detallaremos en el informe ejecutivo.
    </div>
</div>
"""
# Convertir en expander colapsable
with st.expander("📊 Ajuste real del mercado convertible", expanded=False):
    st.markdown(insight_html, unsafe_allow_html=True)


# -------------------------
# SECCIÓN DINÁMICA — KPIs GRANDES + DONUT PERFIL DE ADOPCIÓN
# -------------------------
st.markdown("---")
st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

# compute dynamic KPIs
registros_filtrados = kpis.get('registros_filtrados', 0)
visionarios_pct = 0.0
if 'Perfil_Adopción' in df_filtered.columns:
    try:
        # detectar valores que indiquen 'visionario'
        values = df_filtered['Perfil_Adopción'].dropna().astype(str)
        mask = values.str.lower().str.contains('vision')
        if len(values) > 0:
            visionarios_pct = mask.sum() / len(values)
    except Exception:
        visionarios_pct = 0.0

consumo_promedio = 0.0
if 'Consumo_Diario_Lts' in df_filtered.columns:
    try:
        consumo_promedio = float(pd.to_numeric(df_filtered['Consumo_Diario_Lts'], errors='coerce').mean() or 0)
    except Exception:
        consumo_promedio = 0.0

# Título de sección
st.markdown("<h2 style='color:#003d82; font-size:1.8rem; font-weight:800; margin-top:40px; margin-bottom:20px;'>El Segmento Visionario: Punto de Entrada para el Mercado GNV</h2>", unsafe_allow_html=True)

# KPIs grandes: redistribuir en 3 columnas (Registros validados ahora está en sidebar)
kcols = st.columns([1,1,1])
with kcols[0]:
        # Cargar imagen para el KPI
        import base64
        from pathlib import Path
        img_path = Path("assets/uploads/obre nosotros.png")
        if img_path.exists():
            with open(img_path, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode()
            img_html = f"<img src='data:image/png;base64,{img_base64}' style='position:absolute; right:0px; top:50%; transform:translateY(-50%); width:160px; height:auto; object-fit:contain;'>"
        else:
            img_html = ""
        
        st.markdown(f"""
        <div class='zg-card' style='border:3px solid #10b981; position:relative;'>
            <div>
                <div style='font-size:0.85rem; color:#475569; text-transform:uppercase;'>Visionarios detectados</div>
                <div style='font-size:2.2rem; font-weight:900; color:#0f172a;'>{visionarios_pct:.1%}</div>
                <div style='font-size:0.85rem; color:#10b981;'>Segmento listo para adoptar</div>
            </div>
            {img_html}
        </div>
        """, unsafe_allow_html=True)
with kcols[1]:
        # Cargar imagen para el KPI
        img_path_consumo = Path("assets/uploads/7.png")
        if img_path_consumo.exists():
            with open(img_path_consumo, "rb") as img_file:
                img_base64_consumo = base64.b64encode(img_file.read()).decode()
            img_html_consumo = f"<img src='data:image/png;base64,{img_base64_consumo}' style='position:absolute; right:0px; top:50%; transform:translateY(-50%); width:160px; height:auto; object-fit:contain;'>"
        else:
            img_html_consumo = ""
        
        st.markdown(f"""
        <div class='zg-card' style='border:3px solid #10b981; position:relative;'>
            <div>
                <div style='font-size:0.85rem; color:#475569; text-transform:uppercase;'>Consumo promedio diario (L)</div>
                <div style='font-size:2.2rem; font-weight:900; color:#0f172a;'>{consumo_promedio:.1f}</div>
                <div style='font-size:0.85rem; color:#10b981;'>Por unidad activa</div>
            </div>
            {img_html_consumo}
        </div>
        """, unsafe_allow_html=True)
with kcols[2]:
        # KPI dinámico de conversiones basado en el universo real restante (remaining = 3470)
        conversions = int(round(visionarios_pct * remaining)) if 'remaining' in globals() else int(round(visionarios_pct * KPI_UNIVERSO_TOTAL))
        
        # Cargar imagen para el KPI
        img_path_conversiones = Path("assets/uploads/5.png")
        if img_path_conversiones.exists():
            with open(img_path_conversiones, "rb") as img_file:
                img_base64_conversiones = base64.b64encode(img_file.read()).decode()
            img_html_conversiones = f"<img src='data:image/png;base64,{img_base64_conversiones}' style='position:absolute; right:0px; top:50%; transform:translateY(-50%); width:160px; height:auto; object-fit:contain;'>"
        else:
            img_html_conversiones = ""
        
        st.markdown(f"""
        <div style='background:linear-gradient(90deg,#0b8a3b,#16a34a); border-radius:14px; padding:18px; color:white; border:3px solid #10b981; position:relative;'>
            <div>
                <div style='font-size:0.85rem; text-transform:uppercase; opacity:0.95;'>Número de Conversiones</div>
                <div style='font-size:2.2rem; font-weight:900;'>{conversions:,}</div>
                <div style='font-size:0.85rem; opacity:0.95;'>Early Adopters</div>
            </div>
            {img_html_conversiones}
        </div>
        """, unsafe_allow_html=True)

# KPI dinámico: litros generados si convertimos visionarios (se calculará para usar después del gráfico)
litros_generados = visionarios_pct * consumo_promedio * 26 * registros_filtrados

# Curva de Gauss: Adopción de Innovaciones con datos reales del mercado
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
if 'Perfil_Adopción' in df_filtered.columns:
    try:
        import numpy as np
        import plotly.graph_objects as go
        
        # Calcular distribución real del mercado
        df_perfil = df_filtered['Perfil_Adopción'].dropna().value_counts()
        total_muestra = len(df_filtered['Perfil_Adopción'].dropna())
        
        # Contar cada perfil
        visionarios = df_perfil.get('Visionario', 0)
        pragmaticos = df_perfil.get('Pragmático', 0)
        rezagados = df_perfil.get('Rezagado', 0)
        
        # Calcular porcentajes
        pct_visionarios = (visionarios / total_muestra * 100) if total_muestra > 0 else 0
        pct_pragmaticos = (pragmaticos / total_muestra * 100) if total_muestra > 0 else 0
        pct_rezagados = (rezagados / total_muestra * 100) if total_muestra > 0 else 0
        
        # Extrapolación al universo total (3070)
        universo_total = 3070
        unidades_visionarios = int(universo_total * pct_visionarios / 100)
        unidades_pragmaticos = int(universo_total * pct_pragmaticos / 100)
        unidades_rezagados = int(universo_total * pct_rezagados / 100)
        
        # Crear curva de Gauss (distribución normal)
        x = np.linspace(-4, 4, 1000)
        y = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)
        
        # Normalizar para que sea más visual
        y = y / y.max() * 100
        
        fig_gauss = go.Figure()
        
        # Áreas coloreadas según adopción - ORDEN: Visionarios (izq), Pragmáticos (centro), Rezagados (der)
        # Visionarios (izquierda) - #2563EB
        mask_visionarios = x <= -1.5
        fig_gauss.add_trace(go.Scatter(
            x=x[mask_visionarios],
            y=y[mask_visionarios],
            fill='tozeroy',
            fillcolor='rgba(37, 99, 235, 0.95)',  # #2563EB
            line=dict(color='rgba(0, 123, 255, 0)', width=0),
            name=f'Visionarios: {pct_visionarios:.1f}%',
            hovertemplate=f'<b>Visionarios</b><br>{pct_visionarios:.1f}% ({unidades_visionarios:,} unidades)<extra></extra>',
            showlegend=True
        ))
        
        # Pragmáticos (centro) - Gris medio
        mask_pragmaticos = (x > -1.5) & (x <= 1.5)
        fig_gauss.add_trace(go.Scatter(
            x=x[mask_pragmaticos],
            y=y[mask_pragmaticos],
            fill='tozeroy',
            fillcolor='rgba(107, 114, 128, 0.6)',  # Gris medio
            line=dict(color='rgba(168, 213, 172, 0)', width=0),
            name=f'Pragmáticos: {pct_pragmaticos:.1f}%',
            hovertemplate=f'<b>Pragmáticos</b><br>{pct_pragmaticos:.1f}% ({unidades_pragmaticos:,} unidades)<extra></extra>',
            showlegend=True
        ))
        
        # Rezagados (derecha) - Gris claro
        mask_rezagados = x > 1.5
        fig_gauss.add_trace(go.Scatter(
            x=x[mask_rezagados],
            y=y[mask_rezagados],
            fill='tozeroy',
            fillcolor='rgba(156, 163, 175, 0.4)',  # Gris claro
            line=dict(color='rgba(217, 230, 211, 0)', width=0),
            name=f'Rezagados: {pct_rezagados:.1f}%',
            hovertemplate=f'<b>Rezagados</b><br>{pct_rezagados:.1f}% ({unidades_rezagados:,} unidades)<extra></extra>',
            showlegend=True
        ))
        
        # Línea de la curva
        fig_gauss.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color='#0f172a', width=2),
            name='Curva de Adopción',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Anotaciones con porcentajes y unidades - reordenadas según nuevo layout
        annotations = [
            dict(x=-2.5, y=20, text=f"<b>Visionarios</b><br>{pct_visionarios:.1f}%<br>{unidades_visionarios:,} unidades", 
                 showarrow=False, font=dict(size=11, color="#2563EB")),
            dict(x=0, y=85, text=f"<b>Pragmáticos</b><br>{pct_pragmaticos:.1f}%<br>{unidades_pragmaticos:,} unidades", 
                 showarrow=False, font=dict(size=12, color="#6B7280")),
            dict(x=2.5, y=20, text=f"<b>Rezagados</b><br>{pct_rezagados:.1f}%<br>{unidades_rezagados:,} unidades", 
                 showarrow=False, font=dict(size=11, color="#9CA3AF"))
        ]
        
        fig_gauss.update_layout(
            title={'text': 'Distribución Real de Perfiles de Adopción en Puerto Vallarta', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 16}},
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0, 110]),
            height=520,
            margin=dict(t=60, b=20, l=20, r=20),
            plot_bgcolor='white',
            annotations=annotations,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig_gauss, use_container_width=True)
    except Exception as e:
        st.warning(f'No fue posible generar la curva de adopción: {e}')
else:
    st.info('Columna "Perfil_Adopción" no encontrada.')

# Layout 2x2: Primera fila con insights, segunda fila con notas
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# Primera fila: Potencial mensual + Proyección anual (mismo ancho)
col_mensual, col_anual = st.columns([1, 1])

litros_anuales = litros_generados * 12

with col_mensual:
    # Cargar imagen para el KPI
    img_path_mensual = Path("assets/uploads/4.png")
    if img_path_mensual.exists():
        with open(img_path_mensual, "rb") as img_file:
            img_base64_mensual = base64.b64encode(img_file.read()).decode()
        img_html_mensual = f"<img src='data:image/png;base64,{img_base64_mensual}' style='position:absolute; right:0px; top:50%; transform:translateY(-50%); width:160px; height:auto; object-fit:contain;'>"
    else:
        img_html_mensual = ""
    
    mensual_html = f"""
    <div class='zg-card' style='border:3px solid #10b981; position:relative;'>
        <div>
            <div style='font-size:0.85rem; color:#475569; text-transform:uppercase;'>Potencial mensual</div>
            <div style='font-size:2.2rem; font-weight:900; color:#0f172a; margin-top:8px;'>{litros_generados:,.0f} L</div>
            <div style='font-size:0.85rem; color:#10b981;'>Mercado visionario</div>
        </div>
        {img_html_mensual}
    </div>
    """
    st.markdown(mensual_html, unsafe_allow_html=True)

with col_anual:
    # Cargar imagen para el KPI
    img_path_anual = Path("assets/uploads/3.png")
    if img_path_anual.exists():
        with open(img_path_anual, "rb") as img_file:
            img_base64_anual = base64.b64encode(img_file.read()).decode()
        img_html_anual = f"<img src='data:image/png;base64,{img_base64_anual}' style='position:absolute; right:0px; top:50%; transform:translateY(-50%); width:160px; height:auto; object-fit:contain;'>"
    else:
        img_html_anual = ""
    
    anual_html = f"""
    <div class='zg-card' style='border:3px solid #10b981; position:relative;'>
        <div>
            <div style='font-size:0.85rem; color:#475569; text-transform:uppercase;'>Proyección anual</div>
            <div style='font-size:2.2rem; font-weight:900; color:#0f172a; margin-top:8px;'>{litros_anuales:,.0f} L</div>
            <div style='font-size:0.85rem; color:#10b981;'>Mercado visionario</div>
        </div>
        {img_html_anual}
    </div>
    """
    st.markdown(anual_html, unsafe_allow_html=True)

# Segunda fila: Notas metodológicas (ancho completo) - AHORA EN EXPANDER
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
notas_html = """
<div class='zg-card' style='border:3px solid #10b981;'>
    <div style='font-size:0.85rem; color:#475569; text-transform:uppercase; margin-bottom:12px;'>Notas metodológicas</div>
    <div style='font-size:0.9rem; color:#374151; line-height:1.5;'>
    &middot; Esta cifra NO corresponde a convertir únicamente a los visionarios detectados en las 273 encuestas.<br>
    &middot; La muestra es estadísticamente suficiente para extrapolar con precisión el comportamiento al universo total de operadores en Vallarta.<br>
    &middot; El cálculo estima el consumo mensual del segmento visionario completo del mercado (visionarios del universo × consumo diario × 26 días).<br>
    &middot; Este escenario muestra el potencial bruto; a la cifra final habría que aplicarle el proceso natural de decantación propio del negocio GNV, evaluación técnica, elegibilidad de crédito y filtros operativos, para obtener el volumen neto real.<br>
    &middot; Todo este embudo será analizado a profundidad en el informe ejecutivo.
    </div>
</div>
"""
with st.expander("📓 Notas metodológicas", expanded=False):
    st.markdown(notas_html, unsafe_allow_html=True)

# -------------------------
# SECCIÓN: GRÁFICO DE BURBUJAS + TOP 3 RUTAS + IMAGEN MAPEO
# -------------------------
st.markdown("---")
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

# Título de sección
st.markdown("<h2 style='color:#003d82; font-size:1.8rem; font-weight:800; margin-top:30px; margin-bottom:20px;'>Análisis Geoestratégico de Adopción por Rutas y Bases Operativas</h2>", unsafe_allow_html=True)

# Gráfico scatter horizontal (arriba, ancho completo)
if 'Organización_Ruta' in df_filtered.columns and 'Perfil_Adopción' in df_filtered.columns:
    try:
        import plotly.graph_objects as go
        
        # Preparar datos para scatter
        df_scatter = df_filtered[['Organización_Ruta', 'Perfil_Adopción']].dropna().copy()
        
        if not df_scatter.empty:
            # Definir orden de perfiles (Y axis de abajo hacia arriba) - nombres exactos del Excel
            perfiles_orden = ['Rezagado', 'Pragmático', 'Visionario']
            
            # Crear diccionario de colores
            color_map = {
                'Visionario': '#3b82f6',  # azul
                'Pragmático': '#10b981',  # verde vibrante
                'Rezagado': '#ef4444'     # rojo
            }
            
            # Obtener lista única de rutas ordenadas
            rutas_unicas = sorted(df_scatter['Organización_Ruta'].unique().tolist())
            
            fig_scatter = go.Figure()
            
            # Agregar líneas punteadas verticales para separar rutas
            for i, ruta in enumerate(rutas_unicas):
                fig_scatter.add_vline(
                    x=i, 
                    line_dash="dot", 
                    line_color="#d1d5db",
                    opacity=0.5
                )
            
            # Agregar trace por cada perfil
            for perfil in perfiles_orden:
                # Filtrar datos por perfil exacto
                df_perfil = df_scatter[df_scatter['Perfil_Adopción'] == perfil]
                
                if not df_perfil.empty:
                    # Contar ocurrencias por ruta
                    counts = df_perfil['Organización_Ruta'].value_counts()
                    
                    # Mapear rutas a índices numéricos
                    x_values = [rutas_unicas.index(ruta) for ruta in counts.index]
                    
                    fig_scatter.add_trace(go.Scatter(
                        x=x_values,
                        y=[perfil] * len(x_values),
                        mode='markers',
                        marker=dict(
                            size=counts.values * 4,  # tamaño proporcional a cantidad
                            color=color_map.get(perfil, '#666666'),
                            opacity=0.75,
                            line=dict(width=2, color='white')
                        ),
                        name=perfil,
                        text=[f"{ruta}<br>{count}" for ruta, count in zip(counts.index, counts.values)],
                        customdata=counts.values,
                        hovertemplate='<b>%{text}</b><br>%{y}<extra></extra>'
                    ))
            
            fig_scatter.update_layout(
                title={
                    'text': 'Distribución de Perfiles de Adopción por Ruta — Detección de Focos Visionarios',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#0f172a', 'family': 'Arial, sans-serif'}
                },
                xaxis=dict(
                    tickmode='linear',
                    tick0=0,
                    dtick=1,
                    ticktext=rutas_unicas,
                    tickvals=list(range(len(rutas_unicas))),
                    tickangle=-45,
                ),
                yaxis=dict(categoryorder='array', categoryarray=perfiles_orden),
                height=450,
                margin=dict(l=20, r=20, t=60, b=150),
                font=dict(size=11),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode='closest',
                plot_bgcolor='white',
                yaxis_title="Perfil de Adopción",
                xaxis_title="Organización / Ruta"
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No hay datos suficientes para generar el gráfico")
    except Exception as e:
        st.warning(f"No se pudo generar el gráfico: {e}")
else:
    st.info("Columnas 'Organización_Ruta' y/o 'Perfil_Adopción' no encontradas")

# Espacio
st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)

# Dos columnas: Imagen izquierda + Contenido derecha
col_left, col_right = st.columns([1, 1])

with col_left:
    # Título de la imagen
    st.markdown("<h3 style='color:#0f172a; font-size:1rem; font-weight:700; text-align:center; margin-bottom:15px;'>Puntos Críticos con Mayor Concentración de Unidades</h3>", unsafe_allow_html=True)
    
    from pathlib import Path
    uploads_dir = Path("assets/uploads")
    
    if uploads_dir.exists():
        img_files = [f for f in uploads_dir.iterdir() if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.webp']]
        if img_files:
            latest_img = max(img_files, key=lambda p: p.stat().st_mtime)
            st.markdown(f"<div style='border:3px solid #10b981; border-radius:8px; overflow:hidden;'><img src='data:image/png;base64,{__import__('base64').b64encode(open(str(latest_img), 'rb').read()).decode()}' style='width:100%; display:block;'></div>", unsafe_allow_html=True)
        else:
            st.info("📤 Sube una imagen en el sidebar")
    else:
        st.info("📤 Sube una imagen en el sidebar")

with col_right:
    # Agregar margen superior para alinear con la imagen
    st.markdown("<div style='margin-top:60px;'></div>", unsafe_allow_html=True)
    
    # KPI 1: Top 3 rutas con más visionarios
    top3_html = "<div class='zg-card' style='border:3px solid #10b981; padding:12px; margin-bottom:75px; min-height:220px; max-height:220px; overflow:hidden;'>"
    top3_html += "<div style='font-size:0.75rem; color:#475569; text-transform:uppercase; margin-bottom:8px; font-weight:600;'>Top 3 Rutas con más Visionarios</div>"
    
    if 'Organización_Ruta' in df_filtered.columns and 'Perfil_Adopción' in df_filtered.columns:
        try:
            df_visionarios = df_filtered[df_filtered['Perfil_Adopción'] == 'Visionario']
            if not df_visionarios.empty:
                top3_rutas = df_visionarios['Organización_Ruta'].value_counts().head(3)
                for i, (ruta, count) in enumerate(top3_rutas.items(), 1):
                    top3_html += f"""<div style='margin-bottom:8px;'>
<div style='font-size:0.7rem; color:#64748b; text-transform:uppercase;'>#{i} RUTA</div>
<div style='font-size:1rem; font-weight:700; color:#0f172a; margin-top:2px;'>{ruta}</div>
</div>"""
            else:
                top3_html += "<div style='color:#94a3b8; font-size:0.9rem;'>No hay visionarios detectados</div>"
        except Exception as e:
            top3_html += f"<div style='color:#ef4444; font-size:0.85rem;'>Error: {e}</div>"
    else:
        top3_html += "<div style='color:#94a3b8; font-size:0.9rem;'>Datos no disponibles</div>"
    
    top3_html += "</div>"
    st.markdown(top3_html, unsafe_allow_html=True)
    
    # KPI 2: Desconocimiento del GNV
    gnv_html = "<div class='zg-card' style='border:3px solid #10b981; padding:18px; height:54%; display:flex; flex-direction:column; justify-content:center;'>"
    gnv_html += "<div style='font-size:0.8rem; color:#475569; text-transform:uppercase; margin-bottom:10px; font-weight:600;'>Desconocimiento del GNV</div>"
    
    if 'Conocimiento_GNV' in df_filtered.columns:
        try:
            conocimiento_series = df_filtered['Conocimiento_GNV'].dropna().astype(str)
            total_respuestas = len(conocimiento_series)
            
            if total_respuestas > 0:
                bajo_conocimiento = conocimiento_series.str.lower().str.strip().str.contains('bajo', na=False).sum()
                porcentaje_bajo = (bajo_conocimiento / total_respuestas) * 100
                
                gnv_html += f"""
<div style='font-size:2.8rem; font-weight:900; color:#0f172a; margin-top:8px;'>{porcentaje_bajo:.1f}%</div>
<div style='font-size:0.85rem; color:#10b981; margin-top:6px; font-weight:600;'>dijeron no saber nada del GNV</div>
<div style='font-size:0.75rem; color:#94a3b8; margin-top:4px;'>{bajo_conocimiento} de {total_respuestas} encuestados</div>
"""
            else:
                gnv_html += "<div style='color:#94a3b8; font-size:0.9rem;'>Sin respuestas disponibles</div>"
        except Exception as e:
            gnv_html += f"<div style='color:#ef4444; font-size:0.85rem;'>Error: {e}</div>"
    else:
        gnv_html += "<div style='color:#94a3b8; font-size:0.9rem;'>Columna 'Conocimiento_GNV' no encontrada</div>"
    
    gnv_html += "</div>"
    st.markdown(gnv_html, unsafe_allow_html=True)

# =====================================================================
# NUEVA SECCIÓN: Análisis de Modelos y Antigüedad del Parque Vehicular
# =====================================================================
st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#003d82; font-size:1.8rem; font-weight:800; margin-top:40px; margin-bottom:20px;'>Diagnóstico del Parque Actual y Potencial de Sustitución Early Adopter</h2>", unsafe_allow_html=True)

col_graf, col_kpi1, col_kpi2 = st.columns([1.5, 1, 1])

# COLUMNA 1: Gráfico de Modelos predominantes
with col_graf:
    if 'Modelo' in df_filtered.columns:
        # Obtener top 10 modelos
        df_modelo = df_filtered['Modelo'].dropna().value_counts().reset_index()
        df_modelo.columns = ['Modelo', 'count']
        top10_modelos = df_modelo.head(10)
        
        # Calcular factor de expansión
        n_muestra = len(df_filtered)
        n_universo = KPI_UNIVERSO_TOTAL if KPI_UNIVERSO_TOTAL > 0 else n_muestra
        factor = n_universo / n_muestra if n_muestra > 0 else 1
        
        # Aplicar factor de expansión
        top10_modelos['count_universo'] = (top10_modelos['count'] * factor).round().astype(int)
        
        # Crear gráfico de barras horizontales
        import plotly.graph_objects as go
        fig_modelo = go.Figure(go.Bar(
            y=top10_modelos['Modelo'],
            x=top10_modelos['count_universo'],
            orientation='h',
            marker=dict(color='#10b981'),
            text=top10_modelos['count_universo'],
            textposition='outside',
            texttemplate='%{text:,}'
        ))
        
        fig_modelo.update_layout(
            title={'text': 'Top 10 Modelos Predominantes en el Mercado', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 16}},
            height=450,
            margin=dict(t=50, b=40, l=150, r=40),
            xaxis_title="Unidades (universo)",
            yaxis=dict(autorange="reversed"),
            showlegend=False
        )
        
        st.plotly_chart(fig_modelo, use_container_width=True)
    else:
        st.info('Columna "Modelo" no encontrada.')

# COLUMNA 2: KPI Unidades menores a 2016
with col_kpi1:
    kpi1_html = """
<div style='background:white; border:2px solid #10b981; border-radius:12px; padding:20px; height:450px; display:flex; flex-direction:column; justify-content:center;'>
    <div style='font-size:0.9rem; color:#64748b; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:15px;'>Antigüedad del Parque</div>
    <div style='font-size:1.3rem; font-weight:700; color:#0f172a; margin-bottom:20px;'>Unidades Anteriores a 2016</div>
"""
    
    # Buscar columna de año
    year_col = None
    if 'Año_Vehículo' in df_filtered.columns:
        year_col = 'Año_Vehículo'
    else:
        year_col = find_col(df_filtered, ['año', 'ano', 'year'])
    
    if year_col and year_col in df_filtered.columns:
        try:
            df_year_clean = pd.to_numeric(df_filtered[year_col], errors='coerce').dropna()
            unidades_antiguas = (df_year_clean < 2016).sum()
            
            # Expandir al universo
            n_muestra = len(df_filtered)
            n_universo = KPI_UNIVERSO_TOTAL if KPI_UNIVERSO_TOTAL > 0 else n_muestra
            factor = n_universo / n_muestra if n_muestra > 0 else 1
            unidades_antiguas_universo = int(unidades_antiguas * factor)
            
            # Aplicar porcentaje de visionarios
            unidades_antiguas_visionarios = int(unidades_antiguas_universo * visionarios_pct)
            
            porcentaje_antiguas = (unidades_antiguas / len(df_year_clean) * 100) if len(df_year_clean) > 0 else 0
            
            kpi1_html += f"""
<div style='font-size:4rem; font-weight:900; color:#0f172a; margin-top:15px;'>{unidades_antiguas_visionarios:,}</div>
<div style='font-size:1.1rem; color:#10b981; margin-top:12px; font-weight:600;'>unidades visionarias (fase sustitución)</div>
<div style='font-size:0.95rem; color:#94a3b8; margin-top:10px;'>{visionarios_pct*100:.1f}% de {unidades_antiguas_universo:,} unidades antiguas</div>
<div style='font-size:0.85rem; color:#cbd5e1; margin-top:12px;'>Base: {len(df_year_clean)} vehículos en muestra</div>
"""
        except Exception as e:
            kpi1_html += f"<div style='color:#ef4444; font-size:0.85rem;'>Error calculando antigüedad: {e}</div>"
    else:
        kpi1_html += "<div style='color:#94a3b8; font-size:0.9rem;'>Columna de año no encontrada</div>"
    
    kpi1_html += "</div>"
    st.markdown(kpi1_html, unsafe_allow_html=True)

# COLUMNA 3: KPI Volumen de litros mensuales (unidades < 2016)
with col_kpi2:
    kpi2_html = """
<div style='background:white; border:2px solid #10b981; border-radius:12px; padding:20px; height:450px; display:flex; flex-direction:column; justify-content:center;'>
    <div style='font-size:0.9rem; color:#64748b; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:15px;'>Potencial de Sustitución</div>
    <div style='font-size:1.3rem; font-weight:700; color:#0f172a; margin-bottom:20px;'>Volumen Mensual (< 2016)</div>
"""
    
    # Buscar columnas necesarias
    year_col = None
    if 'Año_Vehículo' in df_filtered.columns:
        year_col = 'Año_Vehículo'
    else:
        year_col = find_col(df_filtered, ['año', 'ano', 'year'])
    
    consumo_col = 'Consumo_Diario_Lts' if 'Consumo_Diario_Lts' in df_filtered.columns else find_col(df_filtered, ['consumo', 'litros', 'lts'])
    
    if year_col and consumo_col and year_col in df_filtered.columns and consumo_col in df_filtered.columns:
        try:
            # Filtrar unidades < 2016
            df_temp = df_filtered.copy()
            df_temp[year_col] = pd.to_numeric(df_temp[year_col], errors='coerce')
            df_temp[consumo_col] = pd.to_numeric(df_temp[consumo_col], errors='coerce')
            df_antiguas = df_temp[df_temp[year_col] < 2016].dropna(subset=[consumo_col])
            
            if len(df_antiguas) > 0:
                # Calcular consumo diario promedio
                consumo_diario_promedio = df_antiguas[consumo_col].mean()
                
                # Expandir al universo
                n_muestra = len(df_filtered)
                n_universo = KPI_UNIVERSO_TOTAL if KPI_UNIVERSO_TOTAL > 0 else n_muestra
                factor = n_universo / n_muestra if n_muestra > 0 else 1
                
                unidades_antiguas_universo = int(len(df_antiguas) * factor)
                
                # Aplicar porcentaje de visionarios
                unidades_antiguas_visionarios = int(unidades_antiguas_universo * visionarios_pct)
                
                # Calcular volumen mensual total (solo visionarios)
                litros_mensuales_visionarios = consumo_diario_promedio * unidades_antiguas_visionarios * 30
                
                kpi2_html += f"""
<div style='font-size:4rem; font-weight:900; color:#0f172a; margin-top:15px;'>{litros_mensuales_visionarios:,.0f}</div>
<div style='font-size:1.1rem; color:#10b981; margin-top:12px; font-weight:600;'>litros mensuales (segmento visionario)</div>
<div style='font-size:0.95rem; color:#94a3b8; margin-top:10px;'>{visionarios_pct*100:.1f}% de {unidades_antiguas_universo:,} unidades antiguas</div>
<div style='font-size:0.85rem; color:#cbd5e1; margin-top:12px;'>Promedio: {consumo_diario_promedio:.1f} lts/día por unidad</div>
"""
            else:
                kpi2_html += "<div style='color:#94a3b8; font-size:0.9rem;'>Sin datos de consumo para unidades < 2016</div>"
        except Exception as e:
            kpi2_html += f"<div style='color:#ef4444; font-size:0.85rem;'>Error calculando volumen: {e}</div>"
    else:
        kpi2_html += "<div style='color:#94a3b8; font-size:0.9rem;'>Columnas de año o consumo no encontradas</div>"
    
    kpi2_html += "</div>"
    st.markdown(kpi2_html, unsafe_allow_html=True)

# Nota explicativa sobre esta sección - Expander colapsable
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
nota_html = """
<div class='zg-card' style='border:3px solid #10b981;'>
    <div style='font-size:0.85rem; color:#475569; text-transform:uppercase; margin-bottom:12px;'>Notas sobre esta sección</div>
    <div style='font-size:0.9rem; color:#374151; line-height:1.5;'>
    &middot; Los KPI mostrados no se calculan sobre el universo total ni sobre las 273 encuestas, sino sobre el <strong>porcentaje de visionarios detectado</strong> y su proyección al parque completo.<br>
    &middot; Se incluyen únicamente <strong>unidades anteriores a 2016</strong>, por ser las que están fuera de norma y representan el potencial inmediato de sustitución.<br>
    &middot; La <strong>fase de sustitución</strong> iniciará después de los primeros seis meses de activar y consolidar a los early adopters.<br>
    &middot; El volumen estimado deberá pasar por un <strong>embudo de elegibilidad crediticia</strong>, cuyo detalle se desarrollará en el Resumen Ejecutivo.
    </div>
</div>
"""
with st.expander("📝 Notas sobre esta sección", expanded=False):
    st.markdown(nota_html, unsafe_allow_html=True)

# =====================================================================
# NUEVA SECCIÓN: Retos y Barreras para la Adopción del GNV
# =====================================================================
st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#003d82; font-size:1.8rem; font-weight:800; margin-top:40px; margin-bottom:20px;'>Retos y Barreras para la Adopción del GNV en Puerto Vallarta</h2>", unsafe_allow_html=True)

col_zona, col_miedos, col_edad_kpi = st.columns([1.3, 1.3, 1])

# COLUMNA 1: Gráfico de Zona vs Tipo de Unidad (excluye vagonetas)
with col_zona:
    zona_col = None
    tipo_col = None
    
    if 'Zona' in df_filtered.columns:
        zona_col = 'Zona'
    else:
        zona_col = find_col(df_filtered, ['zona', 'zone'])
    
    if 'Tipo_Unidad' in df_filtered.columns:
        tipo_col = 'Tipo_Unidad'
    else:
        tipo_col = find_col(df_filtered, ['tipo unidad', 'tipo de unidad', 'tipo'])
    
    if zona_col and tipo_col and zona_col in df_filtered.columns and tipo_col in df_filtered.columns:
        try:
            # Excluir vagonetas explícitamente
            df_zona_sin_vagonetas = df_filtered[~df_filtered[tipo_col].astype(str).str.lower().str.contains('vagoneta', na=False)].copy()
            
            # Crear tabla cruzada usando df sin vagonetas
            df_zona_tipo = df_zona_sin_vagonetas.groupby([zona_col, tipo_col]).size().reset_index(name='count')
            
            # Calcular totales por zona
            zona_totales = df_zona_tipo.groupby(zona_col)['count'].sum().reset_index()
            zona_totales.columns = [zona_col, 'total_zona']
            
            # Merge para calcular porcentajes
            df_zona_tipo = df_zona_tipo.merge(zona_totales, on=zona_col)
            df_zona_tipo['porcentaje'] = (df_zona_tipo['count'] / df_zona_tipo['total_zona'] * 100).round(1)
            
            # Crear gráfico de barras agrupadas
            fig_zona = px.bar(
                df_zona_tipo,
                x=zona_col,
                y='count',
                color=tipo_col,
                text='porcentaje',
                barmode='group',
                color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
            )
            
            fig_zona.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside'
            )
            
            fig_zona.update_layout(
                title={'text': 'Distribución por Zona y Tipo de Unidad', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 16}},
                height=450,
                margin=dict(t=50, b=60, l=40, r=10),
                xaxis_title="Zona",
                yaxis_title="Unidades",
                legend_title="Tipo de Unidad",
                showlegend=True
            )
            
            st.plotly_chart(fig_zona, use_container_width=True)
        except Exception as e:
            st.info(f'Error al generar gráfico: {e}')
    else:
        st.info('Columnas "Zona" o "Tipo_Unidad" no encontradas.')

# COLUMNA 2: Gráfico de Barras Horizontales de Miedos
with col_miedos:
    if 'Miedo_GNV' in df_filtered.columns:
        df_miedos = df_filtered['Miedo_GNV'].dropna().value_counts().reset_index()
        df_miedos.columns = ['Miedo', 'count']
        
        # Calcular factor de expansión al universo
        n_muestra = len(df_filtered)
        n_universo = KPI_UNIVERSO_TOTAL if KPI_UNIVERSO_TOTAL > 0 else n_muestra
        factor = n_universo / n_muestra if n_muestra > 0 else 1
        
        # Aplicar factor de expansión
        df_miedos['count_universo'] = (df_miedos['count'] * factor).round().astype(int)
        
        # Ordenar de mayor a menor (ya viene ordenado por value_counts)
        # Tomar top 8 para no saturar
        df_miedos = df_miedos.head(8)
        
        # Identificar top 3
        top3_indices = [0, 1, 2]
        
        # Crear paleta de colores: verde para top 3, gris para el resto
        colores = ['#10b981' if i in top3_indices else '#cbd5e1' for i in range(len(df_miedos))]
        
        # Invertir orden para que el más importante quede arriba
        df_miedos = df_miedos.iloc[::-1].reset_index(drop=True)
        colores = colores[::-1]
        
        # Crear gráfico de barras horizontales
        import plotly.graph_objects as go
        fig_miedos = go.Figure(go.Bar(
            y=df_miedos['Miedo'],
            x=df_miedos['count_universo'],
            orientation='h',
            marker=dict(color=colores),
            text=df_miedos['count_universo'],
            textposition='outside',
            texttemplate='%{text}'
        ))
        
        fig_miedos.update_layout(
            title={'text': 'Principales Miedos Detectados frente al GNV', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 16}},
            height=450,
            margin=dict(t=50, b=40, l=180, r=40),
            xaxis_title="Respuestas",
            yaxis=dict(autorange="reversed"),
            showlegend=False
        )
        
        st.plotly_chart(fig_miedos, use_container_width=True)
    else:
        st.info('Columna "Miedo_GNV" no encontrada.')

# COLUMNA 3: KPI Restricción Crediticia (Edad > 60 + Inestabilidad laboral)
with col_edad_kpi:
    kpi_edad_html = """
<div style='background:white; border:2px solid #ef4444; border-radius:12px; padding:20px; height:450px; display:flex; flex-direction:column; justify-content:center;'>
    <div style='font-size:0.9rem; color:#64748b; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:15px;'>Restricción Crediticia</div>
    <div style='font-size:1.3rem; font-weight:700; color:#0f172a; margin-bottom:20px;'>Inelegibles por Edad o Empleo</div>
"""
    
    # Buscar columnas de edad y miedo personal
    edad_col = None
    if 'Edad' in df_filtered.columns:
        edad_col = 'Edad'
    else:
        edad_col = find_col(df_filtered, ['edad', 'age'])
    
    miedo_personal_col = None
    if 'Miedo_Personal' in df_filtered.columns:
        miedo_personal_col = 'Miedo_Personal'
    else:
        miedo_personal_col = find_col(df_filtered, ['miedo personal', 'miedo_personal'])
    
    if edad_col and edad_col in df_filtered.columns:
        try:
            # Calcular mayores de 60
            df_edad_clean = pd.to_numeric(df_filtered[edad_col], errors='coerce').dropna()
            mayores_60 = (df_edad_clean > 60).sum()
            
            # Calcular inestabilidad laboral
            inestabilidad = 0
            if miedo_personal_col and miedo_personal_col in df_filtered.columns:
                miedo_series = df_filtered[miedo_personal_col].astype(str).str.lower().str.strip()
                inestabilidad = miedo_series.str.contains('inestabilidad', na=False).sum()
            
            # Total de registros únicos (algunos pueden tener ambas condiciones)
            # Crear máscaras para cada condición
            mask_edad = pd.to_numeric(df_filtered[edad_col], errors='coerce') > 60
            mask_inestabilidad = pd.Series([False] * len(df_filtered), index=df_filtered.index)
            
            if miedo_personal_col and miedo_personal_col in df_filtered.columns:
                mask_inestabilidad = df_filtered[miedo_personal_col].astype(str).str.lower().str.strip().str.contains('inestabilidad', na=False)
            
            # Operadores con al menos una condición (OR lógico)
            total_inelegibles = (mask_edad | mask_inestabilidad).sum()
            total_operadores = len(df_filtered)
            
            # Expandir al universo
            n_muestra = len(df_filtered)
            n_universo = KPI_UNIVERSO_TOTAL if KPI_UNIVERSO_TOTAL > 0 else n_muestra
            factor = n_universo / n_muestra if n_muestra > 0 else 1
            inelegibles_universo = int(total_inelegibles * factor)
            
            porcentaje_inelegibles = (total_inelegibles / total_operadores * 100) if total_operadores > 0 else 0
            
            kpi_edad_html += f"""
<div style='font-size:4rem; font-weight:900; color:#ef4444; margin-top:15px;'>{porcentaje_inelegibles:.1f}%</div>
<div style='font-size:1.1rem; color:#ef4444; margin-top:12px; font-weight:600;'>no elegibles para crédito</div>
<div style='font-size:0.95rem; color:#94a3b8; margin-top:10px;'>{inelegibles_universo:,} operadores por edad o empleo</div>
<div style='font-size:0.85rem; color:#cbd5e1; margin-top:12px;'>Edad >60: {mayores_60} | Inestabilidad: {inestabilidad}</div>
"""
        except Exception as e:
            kpi_edad_html += f"<div style='color:#ef4444; font-size:0.85rem;'>Error calculando restricciones: {e}</div>"
    else:
        kpi_edad_html += "<div style='color:#94a3b8; font-size:0.9rem;'>Columna de edad no encontrada</div>"
    
    kpi_edad_html += "</div>"
    st.markdown(kpi_edad_html, unsafe_allow_html=True)

# Debug: Notas sobre esta sección
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
notas_retos_html = """
<div class='zg-card' style='border:3px solid #10b981;'>
    <div style='font-size:0.85rem; color:#475569; text-transform:uppercase; margin-bottom:12px;'>Notas sobre esta sección</div>
    <div style='font-size:0.9rem; color:#374151; line-height:1.5;'>
    &middot; Todas las métricas presentadas se proyectan del muestreo de 273 operadores hacia el universo total, manteniendo un nivel de confiabilidad suficiente para orientar decisiones estratégicas.<br>
    &middot; El análisis de restricción crediticia cruza dos variables críticas: edad del operador e inestabilidad laboral.<br>
    &middot; Las personas que reportaron inestabilidad laboral reflejan falta de continuidad en el oficio, lo que afecta directamente la predictibilidad de ingresos, un factor clave en cualquier evaluación de crédito.<br>
    &middot; Este filtrado no busca alarmar, sino dimensionar con realismo el porcentaje de operadores que, aun deseando adoptar GNV, requieren acompañamiento adicional para ser sujetos de financiamiento.
    </div>
</div>
"""
with st.expander("📝 Notas sobre esta sección", expanded=False):
    st.markdown(notas_retos_html, unsafe_allow_html=True)

# =====================================================================
# NUEVA SECCIÓN: Identidad Horizontal del Operador
# =====================================================================
st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#003d82; font-size:1.8rem; font-weight:800; margin-top:40px; margin-bottom:20px;'>Perfil Psicográfico y Aspiracional del Transportista en Puerto Vallarta</h2>", unsafe_allow_html=True)

# Primera fila: 3 columnas [1.5, 1, 1]
col_heatmap, col_redes, col_hobbies = st.columns([1.5, 1, 1])

# COLUMNA 1: Heatmap Edad × Miedo Personal
with col_heatmap:
    edad_col = 'Edad' if 'Edad' in df_filtered.columns else find_col(df_filtered, ['edad', 'age'])
    miedo_personal_col = 'Miedo_Personal' if 'Miedo_Personal' in df_filtered.columns else find_col(df_filtered, ['miedo personal', 'miedo_personal'])
    
    if edad_col and miedo_personal_col and edad_col in df_filtered.columns and miedo_personal_col in df_filtered.columns:
        try:
            # Crear rangos de edad
            df_temp = df_filtered[[edad_col, miedo_personal_col]].dropna().copy()
            df_temp[edad_col] = pd.to_numeric(df_temp[edad_col], errors='coerce')
            df_temp = df_temp.dropna()
            
            # Definir rangos de edad
            bins = [0, 30, 40, 50, 60, 100]
            labels = ['18-30', '31-40', '41-50', '51-60', '60+']
            df_temp['Rango_Edad'] = pd.cut(df_temp[edad_col], bins=bins, labels=labels)
            
            # Crear tabla cruzada
            ct = pd.crosstab(df_temp['Rango_Edad'], df_temp[miedo_personal_col], normalize='index') * 100
            
            # Crear heatmap
            import plotly.graph_objects as go
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=ct.values,
                x=ct.columns,
                y=ct.index,
                colorscale='Greens',
                text=ct.values.round(1),
                texttemplate='%{text:.1f}%',
                textfont={"size": 10},
                colorbar=dict(title="% Respuestas")
            ))
            
            fig_heatmap.update_layout(
                title={'text': 'Miedos Personales por Rango de Edad', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 16}},
                height=450,
                margin=dict(t=50, b=80, l=60, r=40),
                xaxis_title="Miedo Personal",
                yaxis_title="Rango de Edad"
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
        except Exception as e:
            st.info(f'Error generando heatmap: {e}')
    else:
        st.info('Columnas "Edad" o "Miedo_Personal" no encontradas.')

# COLUMNA 2: Barras apiladas Edad × Red Social
with col_redes:
    edad_col = 'Edad' if 'Edad' in df_filtered.columns else find_col(df_filtered, ['edad', 'age'])
    red_social_col = 'Red_Social' if 'Red_Social' in df_filtered.columns else find_col(df_filtered, ['red social', 'red_social', 'redes'])
    
    if edad_col and red_social_col and edad_col in df_filtered.columns and red_social_col in df_filtered.columns:
        try:
            df_temp = df_filtered[[edad_col, red_social_col]].dropna().copy()
            df_temp[edad_col] = pd.to_numeric(df_temp[edad_col], errors='coerce')
            df_temp = df_temp.dropna()
            
            # Definir rangos de edad
            bins = [0, 30, 40, 50, 60, 100]
            labels = ['18-30', '31-40', '41-50', '51-60', '60+']
            df_temp['Rango_Edad'] = pd.cut(df_temp[edad_col], bins=bins, labels=labels)
            
            # Crear tabla cruzada normalizada
            ct = pd.crosstab(df_temp['Rango_Edad'], df_temp[red_social_col], normalize='index') * 100
            ct_reset = ct.reset_index()
            
            # Convertir a formato largo para plotly
            df_long = ct_reset.melt(id_vars='Rango_Edad', var_name='Red Social', value_name='Porcentaje')
            
            fig_redes = px.bar(
                df_long,
                x='Rango_Edad',
                y='Porcentaje',
                color='Red Social',
                text='Porcentaje',
                color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
            )
            
            fig_redes.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='inside'
            )
            
            fig_redes.update_layout(
                title={'text': 'Red Social Preferida por Edad', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 16}},
                height=450,
                margin=dict(t=50, b=60, l=40, r=10),
                xaxis_title="Rango de Edad",
                yaxis_title="Porcentaje (%)",
                barmode='stack',
                showlegend=True,
                legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
            )
            
            st.plotly_chart(fig_redes, use_container_width=True)
        except Exception as e:
            st.info(f'Error generando gráfico de redes: {e}')
    else:
        st.info('Columnas "Edad" o "Red_Social" no encontradas.')

# COLUMNA 3: Barras horizontales Hobbies
with col_hobbies:
    hobby_col = 'Hobby' if 'Hobby' in df_filtered.columns else find_col(df_filtered, ['hobby', 'pasatiempo', 'hobbies'])
    
    if hobby_col and hobby_col in df_filtered.columns:
        df_hobbies = df_filtered[hobby_col].dropna().value_counts().reset_index()
        df_hobbies.columns = ['Hobby', 'count']
        
        # Tomar top 8
        df_hobbies = df_hobbies.head(8)
        
        # Colores: verde para top 3, gris para el resto
        colores = ['#10b981' if i < 3 else '#cbd5e1' for i in range(len(df_hobbies))]
        
        # Invertir para que el más popular quede arriba
        df_hobbies = df_hobbies.iloc[::-1].reset_index(drop=True)
        colores = colores[::-1]
        
        import plotly.graph_objects as go
        fig_hobbies = go.Figure(go.Bar(
            y=df_hobbies['Hobby'],
            x=df_hobbies['count'],
            orientation='h',
            marker=dict(color=colores),
            text=df_hobbies['count'],
            textposition='outside',
            texttemplate='%{text}'
        ))
        
        fig_hobbies.update_layout(
            title={'text': 'Hobbies Predominantes', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 16}},
            height=450,
            margin=dict(t=50, b=40, l=120, r=40),
            xaxis_title="Respuestas",
            showlegend=False
        )
        
        st.plotly_chart(fig_hobbies, use_container_width=True)
    else:
        st.info('Columna "Hobby" no encontrada.')

# Segunda fila: Edad × Aspiración (ancho completo, compacto)
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

edad_col = 'Edad' if 'Edad' in df_filtered.columns else find_col(df_filtered, ['edad', 'age'])
aspiracion_col = 'Aspiración' if 'Aspiración' in df_filtered.columns else find_col(df_filtered, ['aspiracion', 'aspiración'])

if edad_col and aspiracion_col and edad_col in df_filtered.columns and aspiracion_col in df_filtered.columns:
    try:
        df_temp = df_filtered[[edad_col, aspiracion_col]].dropna().copy()
        df_temp[edad_col] = pd.to_numeric(df_temp[edad_col], errors='coerce')
        df_temp = df_temp.dropna()
        
        # Definir rangos de edad
        bins = [0, 30, 40, 50, 60, 100]
        labels = ['18-30', '31-40', '41-50', '51-60', '60+']
        df_temp['Rango_Edad'] = pd.cut(df_temp[edad_col], bins=bins, labels=labels)
        
        # Filtrar solo los que aspiran a "ser su propio jefe"
        df_temp['Es_Propio_Jefe'] = df_temp[aspiracion_col].astype(str).str.lower().str.contains('propio jefe|independiente|emprendedor', na=False, regex=True)
        
        # Calcular porcentaje por rango
        aspiracion_pct = df_temp.groupby('Rango_Edad')['Es_Propio_Jefe'].apply(lambda x: (x.sum() / len(x) * 100)).reset_index()
        aspiracion_pct.columns = ['Rango_Edad', 'Porcentaje']
        
        fig_aspiracion = px.bar(
            aspiracion_pct,
            x='Rango_Edad',
            y='Porcentaje',
            text='Porcentaje',
            color='Porcentaje',
            color_continuous_scale='Greens'
        )
        
        fig_aspiracion.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )
        
        fig_aspiracion.update_layout(
            title={'text': 'Aspiración a Ser Su Propio Jefe por Rango de Edad', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 16}},
            height=300,
            margin=dict(t=50, b=60, l=40, r=40),
            xaxis_title="Rango de Edad",
            yaxis_title="Porcentaje (%)",
            showlegend=False
        )
        
        st.plotly_chart(fig_aspiracion, use_container_width=True)
    except Exception as e:
        st.info(f'Error generando gráfico de aspiración: {e}')
else:
    st.info('Columnas "Edad" o "Aspiración" no encontradas.')

# Mostrar tabla rápida
st.markdown("---")
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#003d82; font-size:1.8rem; font-weight:800; margin-top:40px; margin-bottom:20px;'>Tabla Completa de Registros · Dataset Puerto Vallarta</h2>", unsafe_allow_html=True)
if df_filtered.empty:
    st.info("No hay datos para mostrar. Asegúrate de tener `data/dataset_valores.xlsx` o sube un archivo en la barra lateral.")
else:
    st.dataframe(df_filtered)
    
    # Botones de descarga profesionales
    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#0f172a; font-size:1.2rem; font-weight:700; margin-bottom:15px;'>Exportar Datos y Reportes</h3>", unsafe_allow_html=True)
    
    # CSS para estilizar los botones con color verde
    st.markdown("""
    <style>
    /* Estilo para todos los botones de descarga */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #0b8a3b, #16a34a) !important;
        color: white !important;
        border: 3px solid #10b981 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 12px 20px !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(90deg, #16a34a, #10b981) !important;
        border-color: #34d399 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
    }
    /* Estilo para el expander de PDF */
    .stExpander {
        background: linear-gradient(90deg, #0b8a3b, #16a34a) !important;
        border: 3px solid #10b981 !important;
        border-radius: 10px !important;
    }
    .stExpander summary {
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 12px 20px !important;
    }
    .stExpander:hover {
        background: linear-gradient(90deg, #16a34a, #10b981) !important;
        border-color: #34d399 !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Botón descargar CSV
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV",
            data=csv_data,
            file_name=f"zagaz_dataset_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Botón descargar Excel
        from io import BytesIO
        excel_buffer = BytesIO()
        df_filtered.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button(
            label="Descargar Excel",
            data=excel_buffer.getvalue(),
            file_name=f"zagaz_dataset_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col3:
        # Botón generar resumen ejecutivo
        resumen = f"""
ZAGAZ · RESUMEN EJECUTIVO
Dashboard Estratégico GNV - Puerto Vallarta
Fecha: {pd.Timestamp.now().strftime('%d/%m/%Y')}

═══════════════════════════════════════════════════════

📊 MÉTRICAS PRINCIPALES

• Universo Total Registrado: {KPI_UNIVERSO_TOTAL:,} unidades
• Registros en Dataset: {len(df_filtered):,} encuestas
• Visionarios Detectados: {visionarios_pct:.1%}
• Conversiones Esperadas: {conversions:,} unidades
• Consumo Promedio Diario: {consumo_promedio:.1f} L/unidad

═══════════════════════════════════════════════════════

🎯 SEGMENTACIÓN DE MERCADO

Perfiles de Adopción:
{df_filtered['Perfil_Adopción'].value_counts().to_string()}

Tipos de Unidad:
{df_filtered['Tipo de unidad'].value_counts().to_string() if 'Tipo de unidad' in df_filtered.columns else 'No disponible'}

═══════════════════════════════════════════════════════

💡 POTENCIAL DE MERCADO

• Potencial Mensual: {litros_generados:,.0f} L
• Proyección Anual: {litros_anuales:,.0f} L
• Mercado Objetivo: Visionarios (Early Adopters)

═══════════════════════════════════════════════════════

Generado automáticamente por ZAGAZ Dashboard
        """
        st.download_button(
            label="Resumen Ejecutivo",
            data=resumen,
            file_name=f"zagaz_resumen_{pd.Timestamp.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col4:
        # Expander con instrucciones (se puede cerrar)
        with st.expander("Guardar como PDF", expanded=False):
            st.markdown("""
            **Cómo guardar el dashboard completo como PDF:**
            
            1. Presiona **Ctrl+P** (Windows/Linux) o **⌘+P** (Mac)
            2. En "Destino" selecciona **"Guardar como PDF"**
            3. Ajusta la orientación a **Horizontal** para mejor visualización
            4. Marca **"Gráficos de fondo"** para incluir todos los elementos visuales
            5. Haz clic en **"Guardar"**
            
            ✅ Esto capturará TODO el dashboard con gráficos interactivos incluidos.
            """)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("<div style='margin-top:60px;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='background: linear-gradient(90deg, #0b8a3b, #21c06b); padding: 30px 40px; border-radius: 16px; color: white; text-align: center;'>
    <div style='font-size: 1.4rem; font-weight: 900; margin-bottom: 8px;'>ZAGAZ · Dashboard Estratégico GNV</div>
    <div style='font-size: 0.95rem; opacity: 0.95; line-height: 1.6;'>
        Análisis basado en datos reales de campo · Herramienta para toma de decisiones<br>
        Construido con Streamlit + Pandas + Plotly Express · Versión piloto
    </div>
</div>
""", unsafe_allow_html=True)
