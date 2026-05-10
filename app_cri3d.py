import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random
import numpy as np
import os
import base64
from PIL import Image

# Configuración de página
st.set_page_config(
    page_title="CRI 3D Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilos CSS - Estética Escudo Ganadero
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    .main, .stApp { 
        background-color: #05070a !important;
        background-image: 
            radial-gradient(circle at 10% 15%, rgba(255, 255, 255, 0.07) 0%, transparent 35%),
            radial-gradient(circle at 85% 25%, rgba(255, 255, 255, 0.04) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.03) 0%, transparent 60%),
            radial-gradient(circle at 20% 85%, rgba(255, 255, 255, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.06) 0%, transparent 45%),
            linear-gradient(rgba(232, 181, 71, 0.015) 1px, transparent 1px),
            linear-gradient(90deg, rgba(232, 181, 71, 0.015) 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 100%, 100% 100%, 100% 100%, 100% 100%, 50px 50px, 50px 50px !important;
        background-attachment: fixed !important;
        color: #f8fafc; 
        font-family: 'Outfit', sans-serif; 
        overflow: hidden !important;
        touch-action: none !important;
        overscroll-behavior: none !important;
    }
    .sidebar-section {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(232, 181, 71, 0.15);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }
    .title-panel { 
        padding: 0 0 10px 0;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(232, 181, 71, 0.2);
        text-align: center;
    }
    .ai-protocol-card {
        background: linear-gradient(135deg, rgba(232, 181, 71, 0.08) 0%, rgba(0,0,0,0.2) 100%);
        border-radius: 16px;
        padding: 18px;
        margin-top: 15px;
        border: 1px solid rgba(232, 181, 71, 0.2);
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .ai-protocol-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: #E8B547;
    }
    .protocol-header {
        color: #E8B547;
        font-weight: 800;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .protocol-body { 
        font-size: 0.85rem; 
        line-height: 1.5; 
        color: #e2e8f0; 
        font-weight: 400;
    }
    .ai-badge {
        background: rgba(232, 181, 71, 0.15);
        color: #E8B547;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.6rem;
        font-weight: 900;
        border: 1px solid rgba(232, 181, 71, 0.3);
    }
    #MainMenu {visibility: hidden;}
    footer {display: none !important; visibility: hidden !important;}
    header {display: none !important; visibility: hidden !important;}
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
    .stAppDeployButton {display: none !important;}
    /* Ocultar elementos de control de Streamlit y marca de agua */
    [data-testid="stStatusWidget"], [data-testid="stFooter"], [data-testid="stHeader"], .st-emotion-cache-1vt4y6f, .viewerBadge_container__1QSob, .stToolbar, .stStatusWidget {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        opacity: 0 !important;
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
            border-radius: 16px;
        }
        .scenario-overlay h1 {
            font-size: 1.8rem !important;
        }
        .scenario-overlay p {
            font-size: 0.9rem !important;
        }
        .scenario-badge {
            font-size: 0.6rem !important;
            padding: 3px 10px;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
        }
    }

    @media (max-width: 480px) {
        .scenario-container {
            height: 300px !important;
        }
        .scenario-overlay {
            padding: 20px 15px !important;
        }
        .scenario-overlay h1 {
            font-size: 1.5rem !important;
        }
    }
    /* Scenario Viewer Styles */
    .scenario-container {
        position: relative;
        width: 100%;
        height: 600px;
        border-radius: 24px;
        overflow: hidden;
        border: 1px solid rgba(232, 181, 71, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    .scenario-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: all 0.5s ease;
    }
    .scenario-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 40px 30px;
        background: linear-gradient(to top, rgba(5, 7, 10, 0.9) 0%, rgba(5, 7, 10, 0) 100%);
        color: white;
    }
    .scenario-badge {
        background: rgba(232, 181, 71, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(232, 181, 71, 0.3);
        padding: 5px 15px;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Función para convertir imagen a base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Función para calcular ITH (Índice de Temperatura y Humedad)
def calculate_ith(temp, rh):
    # Fórmula de Thom (1959)
    return (1.8 * temp + 32) - (0.55 - 0.55 * (rh / 100)) * (1.8 * temp - 26)

# Datos maestros dinámicos con caché para evitar cambios aleatorios al interactuar
@st.cache_data(ttl=1800)
def get_data():
    seed_time = int(time.time() / 1800)
    random.seed(seed_time)
    
    base = [
        {"country": "México", "name": "Sonora", "lat": 29.3, "lon": -110.3, "temp": 31.0, "hum": 15.0, "weather": "Mucho Sol"},
        {"country": "México", "name": "Chihuahua", "lat": 28.6, "lon": -106.1, "temp": 29.0, "hum": 20.0, "weather": "Mucho Sol"},
        {"country": "México", "name": "Coahuila", "lat": 27.3, "lon": -101.7, "temp": 33.0, "hum": 25.0, "weather": "Mucho Sol"},
        {"country": "México", "name": "Nuevo León", "lat": 25.7, "lon": -100.3, "temp": 34.0, "hum": 45.0, "weather": "Normal"},
        {"country": "México", "name": "Jalisco", "lat": 20.7, "lon": -103.3, "temp": 32.0, "hum": 50.0, "weather": "Nublado"},
        {"country": "México", "name": "Veracruz", "lat": 19.2, "lon": -96.1, "temp": 38.0, "hum": 85.0, "weather": "Lluvias Fuertes"},
        {"country": "México", "name": "Chiapas", "lat": 16.8, "lon": -93.1, "temp": 39.0, "hum": 90.0, "weather": "Tormenta Eléctrica"},
        {"country": "USA", "name": "Texas", "lat": 31.9, "lon": -99.9, "temp": 34.0, "hum": 30.0, "weather": "Mucho Sol"},
        {"country": "Brasil", "name": "Mato Grosso", "lat": -12.6, "lon": -55.4, "temp": 31.0, "hum": 70.0, "weather": "Normal"},
        {"country": "Australia", "name": "Queensland", "lat": -20.9, "lon": 142.7, "temp": 36.0, "hum": 10.0, "weather": "Mucho Sol"}
    ]
    
    # Aplicar fluctuación dinámica y calcular ITH inicial
    for item in base:
        item['temp'] += random.uniform(-2, 3)
        item['hum'] = max(5, min(100, item['hum'] + random.uniform(-5, 5)))
        item['ith'] = calculate_ith(item['temp'], item['hum'])
        
        # Ajustar clima inicial según ITH/Humedad (Lógica unificada)
        if item['hum'] > 85: 
            item['weather'] = "Tormenta Eléctrica" if item['temp'] > 30 else "Lluvias Fuertes"
        elif item['hum'] > 65: 
            item['weather'] = "Nublado"
        elif item['temp'] > 36: 
            item['weather'] = "Mucho Sol"
        elif item['temp'] < 15: 
            item['weather'] = "Viento Fuerte"
        else: 
            item['weather'] = "Normal"

    return pd.DataFrame(base).sort_values("name")

# Cargar datos base (congelados por el caché)
df_base = get_data()
# Crear una copia para la visualización que sí pueda ser modificada por el simulador
df = df_base.copy()

if 'selected_state' not in st.session_state: st.session_state.selected_state = "Sonora"
if 'selected_country' not in st.session_state: st.session_state.selected_country = "México"

# UI con centrado vertical absoluto y balance de márgenes
col_map, col_side, col_spacer = st.columns([3.5, 1.5, 0.3], gap="large", vertical_alignment="center")

with col_side:
    # Gestión de estado de simulación
    
    # Gestión de estado de simulación
    data = df[df['name'] == st.session_state.selected_state].iloc[0]
    
    # Gestión de estado de simulación
    if 'temp_slider' not in st.session_state or st.session_state.last_state != st.session_state.selected_state:
        st.session_state.temp_slider = float(data['temp'])
        st.session_state.hum_slider = float(data['hum'])
        st.session_state.last_state = st.session_state.selected_state

    # SIMULADOR DE ESCENARIOS PREVENTIVOS (WHAT-IF)
    st.markdown("<p style='font-size:0.85rem; color:#E8B547; margin:10px 0 5px 0; text-transform: uppercase; letter-spacing:1px; font-weight:700;'>Simulador de Escenarios (What-If)</p>", unsafe_allow_html=True)
    
    sim_temp = st.slider("Temperatura (°C)", 10.0, 50.0, key="temp_slider", step=0.5)
    sim_hum = st.slider("Humedad (%)", 5.0, 100.0, key="hum_slider", step=1.0)

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
    # Esto permite que el punto en el mapa cambie de color en tiempo real
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

    # Lógica de Color, Estado, Protocolos e Imágenes (Inteligencia Unificada)
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

    # Intervención Especial por Clima
    if weather == "Tormenta Eléctrica":
        scenario_img = "cow_storm.png"
        scenario_label = "RIESGO: TORMENTA ELÉCTRICA"
        if ith < 89:
            status = "RIESGO CLIMÁTICO"
            color = "#ff4b4b"
            protocol = f"⛈️ <b style='color:#ff4b4b'>ALERTA DE RAYOS</b>: Tormenta detectada. Resguardar al hato inmediatamente bajo techo."
        else:
            protocol = f"🆘 <b style='color:#ff4b4b'>RIESGO DOBLE</b>: Emergencia por Calor (ITH {ith:.1f}) + Tormenta Eléctrica. Resguardar en establos con ventilación forzada."

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
<p style="font-size:1.1rem; font-weight:700; margin:0; color: #FFFFFF;">{data['name']}</p>
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
    # para asegurar sincronización total respetando la estructura visual de globo.

    # Ruta de la imagen y conversión a base64 para CSS
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "assets", scenario_img)
    
    try:
        # Verificamos si la imagen existe antes de intentar cargarla
        if os.path.exists(img_path):
            img_base64 = get_base64(img_path)
            bg_style = f"background-image: url('data:image/png;base64,{img_base64}');"
            title_text = "Visualización del<br>Entorno de la Vaca"
            subtitle_text = f"Visualización predictiva para el estado de <b>{st.session_state.selected_state}</b>"
        else:
            # Fallback elegante si no se encuentran las imágenes (común en despliegue cloud sin assets)
            bg_style = "background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);"
            title_text = "Escenario Visual<br>No Disponible"
            subtitle_text = "Por favor, asegúrate de subir la carpeta <b>assets</b> a tu repositorio de GitHub para habilitar las imágenes dinámicas."
            st.info("💡 **Tip**: Se han generado imágenes locales en la carpeta `simulador/assets/`. Súbelas a tu servidor para activar la vista completa.")

        # Contenedor para el Escenario Visual
        st.markdown(f"""
            <div class="scenario-container" style="
                {bg_style}
                background-size: cover;
                background-position: center;
                height: 700px;
            ">
                <div class="scenario-overlay">
                    <div class="scenario-badge">{scenario_label}</div>
                    <h1 style="margin:0; font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; line-height: 1.1;">
                        {title_text}
                    </h1>
                    <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.8); font-size: 1.1rem; font-weight: 400;">
                        {subtitle_text}
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error al cargar el escenario visual: {e}")
