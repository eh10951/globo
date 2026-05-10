import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64
import os
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="OITIZ - Inteligencia Ganadera",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS Premium (Minimalismo Absoluto)
st.markdown("""
    <style>
    /* Reset total de márgenes y paddings */
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Tema Oscuro Elegante */
    .stApp {
        background-color: #05070a;
        color: #ffffff;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    
    /* Panel Lateral (Visión Inteligente) */
    .sidebar-section {
        background: rgba(17, 21, 30, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Tarjetas de Protocolo AI */
    .ai-protocol-card {
        background: linear-gradient(145deg, rgba(232, 181, 71, 0.05) 0%, rgba(13, 17, 23, 0.8) 100%);
        border-left: 3px solid #E8B547;
        padding: 15px;
        border-radius: 12px;
        margin-top: 15px;
    }
    .protocol-header {
        font-size: 0.7rem;
        font-weight: 900;
        letter-spacing: 1.5px;
        color: #E8B547;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .ai-badge {
        background: #E8B547;
        color: black;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.6rem;
    }
    .protocol-body {
        font-size: 0.8rem;
        color: #cbd5e0;
        line-height: 1.4;
    }

    /* Contenedor del Simulador (Mapa 3D) */
    .scenario-container {
        position: relative;
        width: 100%;
        height: 650px;
        border-radius: 24px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 40px;
    }
    .scenario-overlay {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(0deg, rgba(5,7,10,0.9) 0%, rgba(5,7,10,0) 50%);
    }
    .scenario-content {
        position: relative;
        z-index: 2;
    }
    
    /* Sliders Estilizados */
    .stSlider > div [data-baseweb="slider"] {
        height: 6px;
    }
    .stSlider > div [data-baseweb="slider"] > div {
        background-color: #E8B547;
    }
    
    /* Disable click pointer events on background */
    .stApp > div {
        pointer-events: none !important;
        background: transparent !important;
    }
    /* Ocultar botón de pantalla completa y decoración superior */
    button[title="View fullscreen"], [data-testid="stDecoration"], .stAppToolbar, .stFullScreenFrame {
        display: none !important;
    }
    .block-container { 
        padding-top: 5vh !important;
        padding-bottom: 5vh !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 95% !important;
    }
    [data-testid="stAppViewContainer"] {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh !important;
        overflow: auto !important;
    }
    [data-testid="stVerticalBlock"] {
        gap: 2rem !important;
    }
    .stHorizontalBlock {
        align-items: center !important;
        gap: 3rem !important;
    }
    /* Ocultar scrollbar para vista limpia */
    .stApp { overflow: hidden !important; height: 100vh !important; }
    ::-webkit-scrollbar { display: none; }
    
    /* Responsive Design - Full Screen Optimization */
    @media (max-width: 1200px) {
        [data-testid="stAppViewContainer"] {
            height: auto !important;
            min-height: 100vh;
            overflow: auto !important;
            padding: 20px 0;
        }
        .block-container {
            max-width: 100% !important;
            padding: 10px !important;
        }
        .scenario-container {
            height: 450px !important;
        }
    }

    @media (max-width: 768px) {
        .scenario-container {
            height: 350px !important;
            padding: 20px !important;
        }
        .scenario-content h1 {
            font-size: 1.8rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# LÓGICA DE DATOS
# ==========================================

def calculate_ith(temp, hum):
    """Cálculo del Índice de Temperatura y Humedad (ITH)"""
    return (1.8 * temp + 32) - (0.55 - 0.0055 * hum) * (1.8 * temp - 26)

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return ""

# Datos ficticios de estados para la simulación
data_states = {
    "Sonora": {"temp": 32, "hum": 15, "weather": "Despejado"},
    "Jalisco": {"temp": 24, "hum": 60, "weather": "Nublado"},
    "Chihuahua": {"temp": 38, "hum": 10, "weather": "Mucho Sol"},
    "Veracruz": {"temp": 30, "hum": 85, "weather": "Lluvioso"},
}

df = pd.DataFrame([
    {"name": k, "temp": v["temp"], "hum": v["hum"], "weather": v["weather"], 
     "ith": calculate_ith(v["temp"], v["hum"])} 
    for k, v in data_states.items()
])

# ==========================================
# INTERFAZ PRINCIPAL
# ==========================================

col_map, col_side = st.columns([0.65, 0.35])

with col_side:
    st.markdown("<p style='font-size:0.8rem; font-weight:900; letter-spacing:1px; color:#E8B547; margin-bottom:10px;'>SIMULADOR DE ESCENARIOS (WHAT-IF)</p>", unsafe_allow_html=True)
    
    # Selector de Estado
    if 'selected_state' not in st.session_state:
        st.session_state.selected_state = "Sonora"
    
    data = data_states[st.session_state.selected_state]
    
    sim_temp = st.slider("Temperatura (°C)", 10.0, 50.0, value=float(data["temp"]), key="temp_slider", step=0.5)
    sim_hum = st.slider("Humedad (%)", 5.0, 100.0, value=float(data["hum"]), key="hum_slider", step=1.0)
    
    # Cálculo ITH dinámico basado en sliders (Científico)
    ith = calculate_ith(sim_temp, sim_hum)
    
    # Cálculo CRI (0-100%) sincronizado con ITH
    # 72 es el umbral de alerta, 89 es emergencia.
    if ith < 72:
        cri_risk = (ith / 72) * 50
    else:
        cri_risk = 50 + ((ith - 72) / (95 - 72)) * 50
    cri_risk = max(0, min(100, cri_risk))

    # ACTUALIZAR EL DATAFRAME GLOBAL CON LOS DATOS SIMULADOS
    df.loc[df['name'] == st.session_state.selected_state, 'ith'] = ith
    df.loc[df['name'] == st.session_state.selected_state, 'temp'] = sim_temp
    df.loc[df['name'] == st.session_state.selected_state, 'hum'] = sim_hum
    
    # Lógica dinámica de clima basado en simulación
    if sim_hum > 85:
        weather = "Tormenta Eléctrica" if sim_temp > 28 else "Lluvias Fuertes"
    elif sim_hum > 65:
        weather = "Húmedo / Nublado"
    elif sim_temp > 38:
        weather = "Calor Extremo"
    elif sim_temp > 32:
        weather = "Despejado / Cálido"
    elif sim_temp < 15:
        weather = "Clima Frío"
    else:
        weather = "Clima Templado"
    
    weather_icons = {
        "Calor Extremo": "☀️",
        "Despejado / Cálido": "🌤️",
        "Lluvias Fuertes": "🌧️",
        "Clima Templado": "🌤️",
        "Húmedo / Nublado": "☁️",
        "Tormenta Eléctrica": "⛈️",
        "Clima Frío": "🌬️"
    }
    w_icon = weather_icons.get(weather, "🌡️")

    # Lógica de Color, Estado y Protocolos (Inteligencia Integrada)
    if ith >= 89:
        color = "#ff4b4b" # Rojo Emergencia
        status = "EMERGENCIA"
        protocol = "🆘 <b style='color:#ff4b4b'>CRÍTICO - ITH EXTREMO</b>: Riesgo inminente de muerte por golpe de calor. Activar aspersores continuos, ventilación máxima y agua helada."
        scenario_img = "cow_heat_emergency.png"
        scenario_label = "EMERGENCIA: CALOR EXTREMO"
    elif ith >= 79:
        color = "#ff9800" # Naranja Peligro
        status = "PELIGRO"
        protocol = "🚨 <b style='color:#ff9800'>PELIGRO DETECTADO</b>: Estrés térmico severo. Reducir densidad, sombra total y refrescamiento por pulsos obligatorio."
        scenario_img = "cow_heat_alert.png"
        scenario_label = "PELIGRO: ESTRÉS TÉRMICO"
    elif ith >= 72:
        color = "#E8B547" # Amarillo Alerta
        status = "ALERTA"
        protocol = "⚠️ <b style='color:#E8B547'>AVISO PREVENTIVO</b>: Inicio de estrés térmico. Monitorear frecuencia respiratoria y asegurar agua fresca."
        scenario_img = "cow_heat_alert.png"
        scenario_label = "ALERTA: INICIO DE ESTRÉS"
    elif sim_temp < 15:
        color = "#3498DB" # Azul Frío
        status = "FRÍO"
        protocol = "❄️ <b style='color:#3498DB'>ESTRÉS POR FRÍO</b>: Proteger de vientos, asegurar camas secas y aumentar aporte calórico en dieta."
        scenario_img = "cow_cold.png"
        scenario_label = "ALERTA: ESTRÉS POR FRÍO"
    else:
        color = "#4caf50" # Verde Óptimo
        status = "ÓPTIMO"
        protocol = "✅ <b style='color:#4caf50'>CONFORT TÉRMICO</b>: El hato se encuentra en su zona de bienestar. Condiciones ideales para máxima productividad."
        scenario_img = "cow_optimal.png"
        scenario_label = "ZONA DE CONFORT TÉRMICO"

    # Sobreescribir por Clima si es necesario
    if weather == "Tormenta Eléctrica":
        scenario_img = "cow_storm.png"
        scenario_label = "RIESGO: TORMENTA ELÉCTRICA"
        if ith < 89:
            status = "RIESGO CLIMÁTICO"
            color = "#ff4b4b"
            protocol = "⛈️ <b style='color:#ff4b4b'>ALERTA DE RAYOS</b>: Tormenta detectada. Resguardar al hato inmediatamente bajo techo."

    st.markdown(f"""
<div class="sidebar-section" style="border-top: 4px solid {color}; padding: 15px;">
<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0px;">
<p style="font-size:0.7rem; color:#94a3b8; margin:0; text-transform: uppercase;">ESTADO: <b style="color:{color}">{status}</b></p>
<div style="text-align: right;">
<span style="font-size: 2.2rem; filter: drop-shadow(0 0 10px rgba(255,255,255,0.2));" title="{weather}">{w_icon}</span>
<p style="font-size: 0.6rem; color: #94a3b8; margin: 0; font-weight: 600;">{weather}</p>
</div>
</div>
<div style="text-align: center; margin-top: -15px;">
<p style="font-size:1.1rem; font-weight:700; margin:0; color: #FFFFFF;">{st.session_state.selected_state}</p>
<div style="display: flex; justify-content: center; align-items: baseline; gap: 10px; margin-top: 5px;">
    <div style="text-align: center;">
        <p style="font-size:3.5rem; font-weight:800; color: #FFFFFF; margin:0; line-height: 1;">{cri_risk:.0f}%</p>
        <p style="font-size:0.6rem; color:#E8B547; margin:0; text-transform: uppercase; letter-spacing: 2px; font-weight: 700;">RIESGO CRI</p>
    </div>
</div>
</div>
<div style="display: flex; justify-content: center; margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px;">
    <div style="text-align: center;">
        <p style="margin:0; font-size:0.75rem; color:#E8B547; text-transform:uppercase; letter-spacing: 1px;">DATOS SIMULADOS</p>
        <p style="margin:0; font-size:1.4rem; font-weight:700; color:#FFFFFF;">{sim_temp:.1f}°C / {sim_hum:.1f}%</p>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
        <div class="ai-protocol-card">
            <div class="protocol-header">
                <span class="ai-badge">AI</span>
                SUGERENCIAS DE PROTOCOLO
            </div>
            <div class="protocol-body">{protocol}</div>
        </div>
    """, unsafe_allow_html=True)

with col_map:
    # La imagen y el label ya fueron seleccionados en el bloque de inteligencia superior
    # para asegurar sincronización total.

    # Ruta de la imagen y conversión a base64 para CSS
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "assets", scenario_img)
    img_b64 = get_image_base64(img_path)
    
    st.markdown(f"""
        <div class="scenario-container" style="background-image: url('data:image/png;base64,{img_b64}');">
            <div class="scenario-overlay"></div>
            <div class="scenario-content">
                <div style="background: rgba(232, 181, 71, 0.2); backdrop-filter: blur(5px); padding: 4px 12px; border-radius: 8px; border: 1px solid rgba(232, 181, 71, 0.3); display: inline-block; margin-bottom: 20px;">
                    <p style="color: #E8B547; font-size: 0.7rem; font-weight: 900; margin: 0; letter-spacing: 1px;">{scenario_label}</p>
                </div>
                <h1 style="color: white; font-size: 2.8rem; font-weight: 900; margin-bottom: 10px; line-height: 1.1;">Visualización del<br>Entorno de la Vaca</h1>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-bottom: 0;">Visualización predictiva para el estado de {st.session_state.selected_state}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
