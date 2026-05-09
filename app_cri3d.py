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
        background: 
            radial-gradient(1px 1px at 5% 5%, #fff, transparent),
            radial-gradient(1.5px 1.5px at 15% 25%, #3498DB, transparent),
            radial-gradient(0.8px 0.8px at 25% 10%, #fff, transparent),
            radial-gradient(1.2px 1.2px at 35% 45%, #E8B547, transparent),
            radial-gradient(1px 1px at 45% 85%, #fff, transparent),
            radial-gradient(2px 2px at 55% 15%, #3498DB, transparent),
            radial-gradient(1px 1px at 65% 65%, #fff, transparent),
            radial-gradient(1.5px 1.5px at 75% 35%, #E8B547, transparent),
            radial-gradient(0.5px 0.5px at 85% 75%, #fff, transparent),
            radial-gradient(1px 1px at 95% 20%, #3498DB, transparent),
            radial-gradient(1.2px 1.2px at 10% 80%, #fff, transparent),
            radial-gradient(1px 1px at 30% 90%, #E8B547, transparent),
            radial-gradient(1.5px 1.5px at 50% 50%, #fff, transparent),
            radial-gradient(0.8px 0.8px at 70% 10%, #3498DB, transparent),
            radial-gradient(1px 1px at 90% 40%, #fff, transparent),
            radial-gradient(circle at 30% 30%, rgba(52, 152, 219, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 70% 70%, rgba(52, 152, 219, 0.1) 0%, transparent 60%),
            radial-gradient(ellipse at 50% 50%, rgba(20, 30, 48, 0.6) 0%, #05070a 100%) !important;
        background-attachment: fixed !important;
        color: #f8fafc; 
        font-family: 'Outfit', sans-serif; 
        overflow: hidden !important;
        touch-action: none !important;
        overscroll-behavior: none !important;
    }
    .sidebar-section {
        background: rgba(26, 31, 46, 0.4);
        border: 1px solid rgba(232, 181, 71, 0.15);
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 10px;
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
    .block-container { padding: 0.5rem 2rem !important; }
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem !important;}
    /* Ocultar scrollbar para vista limpia */
    .stApp { overflow: hidden !important; height: 100vh !important; }
    ::-webkit-scrollbar { display: none; }
    
    /* Responsividad para Móviles */
    @media (max-width: 600px) {
        .block-container { padding: 0.5rem 0.5rem !important; }
        .sidebar-section { padding: 10px !important; margin-bottom: 5px !important; }
        .sidebar-section p { font-size: 0.6rem !important; }
        .sidebar-section h3 { font-size: 1rem !important; }
        .sidebar-section span { font-size: 2rem !important; }
        .title-panel p { font-size: 0.7rem !important; letter-spacing: 1px !important; }
        .ai-protocol-card { padding: 10px !important; }
        .protocol-body { font-size: 0.7rem !important; }
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
    st.markdown("<div class='title-panel'><p style='margin:0; font-size:1.1rem; color:#E8B547; letter-spacing: 3px; font-weight: 700; text-transform: uppercase;'>VISIÓN INTELIGENTE</p></div>", unsafe_allow_html=True)
    
    countries = df['country'].unique().tolist()
    country_choice = st.selectbox("País", countries, index=countries.index(st.session_state.selected_country))
    
    if country_choice != st.session_state.selected_country:
        st.session_state.selected_country = country_choice
        st.session_state.selected_state = df[df['country'] == country_choice]['name'].iloc[0]
        st.rerun()

    states = df[df['country'] == st.session_state.selected_country]['name'].tolist()
    state_choice = st.selectbox("Estado", states, index=states.index(st.session_state.selected_state))
    st.session_state.selected_state = state_choice

    # Cargar datos base del estado
    data = df[df['name'] == st.session_state.selected_state].iloc[0]
    
    # Gestión de estado de simulación
    if 'temp_slider' not in st.session_state or st.session_state.last_state != st.session_state.selected_state:
        st.session_state.temp_slider = float(data['temp'])
        st.session_state.hum_slider = float(data['hum'])
        st.session_state.last_state = st.session_state.selected_state

    # SIMULADOR DE ESCENARIOS PREVENTIVOS (WHAT-IF)
    st.markdown("<p style='font-size:0.85rem; color:#E8B547; margin:10px 0 5px 0; text-transform: uppercase; letter-spacing:1px; font-weight:700;'>Simulador de Escenarios (What-If)</p>", unsafe_allow_html=True)
    
    # El botón debe ir ANTES de los sliders para poder actualizar su estado sin errores
    if st.button("🔄 Restablecer a Tiempo Real", use_container_width=True):
        st.session_state.temp_slider = float(data['temp'])
        st.session_state.hum_slider = float(data['hum'])
        st.rerun()

    sim_temp = st.slider("Temperatura (°C)", 10.0, 50.0, key="temp_slider", step=0.5)
    sim_hum = st.slider("Humedad (%)", 5.0, 100.0, key="hum_slider", step=1.0)

    # Cálculo ITH dinámico basado en sliders
    ith = calculate_ith(sim_temp, sim_hum)
    
    # ACTUALIZAR EL DATAFRAME GLOBAL CON LOS DATOS SIMULADOS
    # Esto permite que el punto en el mapa cambie de color en tiempo real
    df.loc[df['name'] == st.session_state.selected_state, 'ith'] = ith
    df.loc[df['name'] == st.session_state.selected_state, 'temp'] = sim_temp
    df.loc[df['name'] == st.session_state.selected_state, 'hum'] = sim_hum
    
    # Lógica dinámica de clima basado en simulación
    if sim_hum > 85:
        weather = "Tormenta Eléctrica" if sim_temp > 30 else "Lluvias Fuertes"
    elif sim_hum > 65:
        weather = "Nublado"
    elif sim_temp > 36:
        weather = "Mucho Sol"
    elif sim_temp < 15:
        weather = "Viento Fuerte"
    else:
        weather = "Normal"
    
    weather_icons = {
        "Mucho Sol": "☀️",
        "Lluvias Fuertes": "🌧️",
        "Normal": "🌤️",
        "Nublado": "☁️",
        "Tormenta Eléctrica": "⛈️",
        "Viento Fuerte": "🌬️"
    }
    w_icon = weather_icons.get(weather, "🌡️")

    # Lógica de Color y Estado basada en ITH Científico (Jerarquía de Alerta)
    if ith >= 89:
        color = "#ff4b4b" # Rojo Emergencia
        status = "EMERGENCIA"
        protocol = "🆘 <b style='color:#ff4b4b'>CRÍTICO - ITH EXTREMO</b>: Riesgo inminente de muerte. Activar aspersores continuos, ventilación máxima y suministro de agua helada. Suspender todo movimiento de ganado."
    elif ith >= 79:
        color = "#ff9800" # Naranja Peligro
        status = "PELIGRO"
        protocol = "🚨 <b style='color:#ff9800'>PELIGRO DETECTADO</b>: Estrés térmico severo. Reducir densidad en corrales, asegurar sombra total y activar protocolos de refrescamiento por pulsos."
    elif ith >= 72:
        color = "#E8B547" # Amarillo Alerta
        status = "ALERTA"
        protocol = "⚠️ <b style='color:#E8B547'>AVISO PREVENTIVO</b>: Inicio de estrés térmico. Monitorear frecuencia respiratoria y asegurar disponibilidad de agua fresca y limpia."
    else:
        color = "#4caf50" # Verde Óptimo
        status = "ÓPTIMO"
        protocol = "✅ <b style='color:#4caf50'>CONFORT TÉRMICO</b>: El hato se encuentra en su zona de bienestar. Condiciones ideales para máxima productividad."

    # Intervención por clima extremo (Solo sobrepone si el ITH no es ya una Emergencia)
    if weather == "Tormenta Eléctrica":
        if ith < 89:
            status = "RIESGO CLIMÁTICO"
            color = "#ff4b4b"
            protocol = f"⛈️ <b style='color:#ff4b4b'>ALERTA DE RAYOS</b>: Tormenta detectada. <b>PROHIBIDO</b> el pastoreo en áreas abiertas. Resguardar al hato inmediatamente bajo techo."
        else:
            # Si hay calor extremo Y tormenta
            protocol = f"🆘 <b style='color:#ff4b4b'>RIESGO DOBLE</b>: Emergencia por Calor (ITH {ith:.1f}) + Tormenta Eléctrica. Resguardar en establos con ventilación forzada. <b>NO usar aspersores en exterior</b>."

    elif weather == "Lluvias Fuertes" and ith < 79:
        protocol = "🌧️ <b style='color:#3498DB'>LLUVIAS INTENSAS</b>: Monitorear salud podal y evitar zonas de encharcamiento para prevenir infecciones."

    # Cálculo del Riesgo CRI (%) basado en el ITH
    # Mapeamos el ITH (aprox 60-95) a una escala de 0-100%
    if ith < 72:
        cri_risk = (ith / 72) * 50
    else:
        cri_risk = 50 + ((ith - 72) / (95 - 72)) * 50
    cri_risk = max(0, min(100, cri_risk))

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
<p style="font-size:1.1rem; font-weight:700; margin:0; color: #E8B547;">{data['name']}</p>
<div style="display: flex; justify-content: center; align-items: baseline; gap: 10px; margin-top: 5px;">
    <div style="text-align: center;">
        <p style="font-size:2.8rem; font-weight:800; color:#fff; margin:0; line-height: 1;">{ith:.1f}</p>
        <p style="font-size:0.55rem; color:#94a3b8; margin:0; text-transform: uppercase; letter-spacing: 1px;">ÍNDICE ITH</p>
    </div>
    <div style="width: 1px; height: 30px; background: rgba(255,255,255,0.1); align-self: center;"></div>
    <div style="text-align: center;">
        <p style="font-size:1.8rem; font-weight:700; color:{color}; margin:0; line-height: 1;">{cri_risk:.0f}%</p>
        <p style="font-size:0.55rem; color:#94a3b8; margin:0; text-transform: uppercase; letter-spacing: 1px;">RIESGO CRI</p>
    </div>
</div>
</div>
<div style="display: flex; justify-content: space-around; margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px;">
    <div style="text-align: center;">
        <p style="margin:0; font-size:0.7rem; color:#94a3b8; text-transform:uppercase; letter-spacing: 0.5px;">Real (Actual)</p>
        <p style="margin:0; font-size:1.1rem; font-weight:700; color:#3498DB;">{data['temp']:.1f}°C / {data['hum']:.1f}%</p>
    </div>
    <div style="width: 1px; height: 30px; background: rgba(255,255,255,0.05); align-self: center;"></div>
    <div style="text-align: center;">
        <p style="margin:0; font-size:0.7rem; color:#94a3b8; text-transform:uppercase; letter-spacing: 0.5px;">Simulado</p>
        <p style="margin:0; font-size:1.1rem; font-weight:700; color:#E8B547;">{sim_temp:.1f}°C / {sim_hum:.1f}%</p>
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
    # Selección de imagen de escenario basada en simulación
    if weather in ["Tormenta Eléctrica", "Lluvias Fuertes"]:
        scenario_img = "cow_storm.png"
        scenario_label = "RIESGO CLIMÁTICO: TORMENTA"
    elif sim_temp < 15:
        scenario_img = "cow_cold.png"
        scenario_label = "ESTRÉS POR FRÍO"
    elif ith >= 89:
        scenario_img = "cow_heat_emergency.png"
        scenario_label = "EMERGENCIA: CALOR EXTREMO"
    elif ith >= 79:
        scenario_img = "cow_heat_alert.png"
        scenario_label = "PELIGRO: ESTRÉS TÉRMICO"
    elif ith >= 72:
        scenario_img = "cow_heat_alert.png"
        scenario_label = "ALERTA: INICIO DE ESTRÉS"
    else:
        scenario_img = "cow_optimal.png"
        scenario_label = "ZONA DE CONFORT TÉRMICO"

    # Ruta de la imagen y conversión a base64 para CSS
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "assets", scenario_img)
    try:
        img_base64 = get_base64(img_path)
        
        # Contenedor para el Escenario Visual con fondo dinámico
        st.markdown(f"""
            <div class="scenario-container" style="
                background-image: url('data:image/png;base64,{img_base64}');
                background-size: cover;
                background-position: center;
                height: 700px;
            ">
                <div class="scenario-overlay">
                    <div class="scenario-badge">{scenario_label}</div>
                    <h1 style="margin:0; font-size: 2.8rem; font-weight: 800; letter-spacing: -1.5px; line-height: 1.1;">
                        Simulación de<br>Entorno Animal
                    </h1>
                    <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.8); font-size: 1.1rem; font-weight: 400;">
                        Visualización predictiva para el estado de <b>{st.session_state.selected_state}</b>
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error al cargar el escenario visual: {e}")
