import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random
import numpy as np

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

    /* Animaciones Premium */
    @keyframes glow-sun {
        0% { box-shadow: 0 0 15px #fff, 0 0 40px #E8B547, 0 0 70px #E8B547; transform: scale(1); }
        50% { box-shadow: 0 0 25px #fff, 0 0 60px #E8B547, 0 0 100px #E8B547; transform: scale(1.05); }
        100% { box-shadow: 0 0 15px #fff, 0 0 40px #E8B547, 0 0 70px #E8B547; transform: scale(1); }
    }
    .sun-glow { animation: glow-sun 4s infinite ease-in-out; }
    
    @keyframes glow-moon {
        0% { box-shadow: 0 0 8px #fff, 0 0 20px rgba(148, 163, 184, 0.4); transform: scale(1); }
        50% { box-shadow: 0 0 15px #fff, 0 0 35px rgba(148, 163, 184, 0.6); transform: scale(1.03); }
        100% { box-shadow: 0 0 8px #fff, 0 0 20px rgba(148, 163, 184, 0.4); transform: scale(1); }
    }
    .moon-glow { animation: glow-moon 6s infinite ease-in-out; }
</style>
""", unsafe_allow_html=True)

# Datos maestros dinámicos
def get_data():
    # Usamos la hora actual para crear un "seed" que cambie cada 30 minutos (1800 segundos)
    # Esto hace que los datos sean "dinámicos" pero consistentes durante ese periodo
    seed_time = int(time.time() / 1800)
    random.seed(seed_time)
    
    base = [
        {"country": "México", "name": "Sonora", "lat": 29.3, "lon": -110.3, "risk": 92.0, "weather": "Mucho Sol"},
        {"country": "México", "name": "Chihuahua", "lat": 28.6, "lon": -106.1, "risk": 87.0, "weather": "Mucho Sol"},
        {"country": "México", "name": "Coahuila", "lat": 27.3, "lon": -101.7, "risk": 84.0, "weather": "Mucho Sol"},
        {"country": "México", "name": "Nuevo León", "lat": 25.7, "lon": -100.3, "risk": 78.0, "weather": "Mucho Sol"},
        {"country": "México", "name": "Jalisco", "lat": 20.7, "lon": -103.3, "risk": 52.0, "weather": "Nublado"},
        {"country": "México", "name": "Veracruz", "lat": 19.2, "lon": -96.1, "risk": 40.0, "weather": "Normal"},
        {"country": "México", "name": "Chiapas", "lat": 16.8, "lon": -93.1, "risk": 32.0, "weather": "Lluvias Fuertes"},
        {"country": "USA", "name": "Texas", "lat": 31.9, "lon": -99.9, "risk": 82.0, "weather": "Mucho Sol"},
        {"country": "Brasil", "name": "Mato Grosso", "lat": -12.6, "lon": -55.4, "risk": 89.0, "weather": "Mucho Sol"},
        {"country": "Australia", "name": "Queensland", "lat": -20.9, "lon": 142.7, "risk": 94.0, "weather": "Mucho Sol"}
    ]
    
    # Aplicar fluctuación dinámica
    for item in base:
        # Variación de +/- 5% según el tiempo
        variation = random.uniform(-5.0, 8.0)
        item['risk'] = max(0, min(100, item['risk'] + variation))
        
        # Cambiar clima dinámicamente según el riesgo actual
        if item['risk'] > 85:
            item['weather'] = "Mucho Sol"
        elif item['risk'] > 70:
            item['weather'] = random.choice(["Mucho Sol", "Viento Fuerte", "Normal"])
        elif item['risk'] > 50:
            item['weather'] = random.choice(["Nublado", "Normal", "Lluvias Fuertes"])
        elif item['risk'] < 35:
            item['weather'] = random.choice(["Lluvias Fuertes", "Tormenta Eléctrica"])

    return pd.DataFrame(base).sort_values("name")

df = get_data()

if 'selected_state' not in st.session_state: st.session_state.selected_state = "Sonora"
if 'selected_country' not in st.session_state: st.session_state.selected_country = "México"

# UI con centrado vertical absoluto y balance de márgenes
col_map, col_side, col_spacer = st.columns([3.5, 1.5, 0.3], gap="large", vertical_alignment="center")

with col_side:
    st.markdown("<div class='title-panel'><p style='margin:0; font-size:0.9rem; color:#E8B547; letter-spacing: 3px; font-weight: 700; text-transform: uppercase;'>VISIÓN INTELIGENTE</p></div>", unsafe_allow_html=True)
    
    countries = df['country'].unique().tolist()
    country_choice = st.selectbox("País", countries, index=countries.index(st.session_state.selected_country))
    
    if country_choice != st.session_state.selected_country:
        st.session_state.selected_country = country_choice
        st.session_state.selected_state = df[df['country'] == country_choice]['name'].iloc[0]
        st.rerun()

    states = df[df['country'] == st.session_state.selected_country]['name'].tolist()
    state_choice = st.selectbox("Estado", states, index=states.index(st.session_state.selected_state))
    st.session_state.selected_state = state_choice

    data = df[df['name'] == st.session_state.selected_state].iloc[0]
    risk = data['risk']
    weather = data['weather']
    
    weather_icons = {
        "Mucho Sol": "☀️",
        "Lluvias Fuertes": "🌧️",
        "Normal": "🌤️",
        "Nublado": "☁️",
        "Tormenta Eléctrica": "⛈️",
        "Viento Fuerte": "🌬️"
    }
    w_icon = weather_icons.get(weather, "🌡️")

    color = "#ff4b4b" if risk > 85 else ("#E8B547" if risk > 50 else "#4caf50")
    status = "PELIGRO" if weather == "Tormenta Eléctrica" else ("CRÍTICO" if risk > 85 else ("ALERTA" if risk > 50 or weather == "Lluvias Fuertes" else "ÓPTIMO"))

    st.markdown(f"""
<div class="sidebar-section" style="border-top: 4px solid {color}; padding: 15px;">
<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0px;">
<p style="font-size:0.7rem; color:#94a3b8; margin:0; text-transform: uppercase;">ESTADO ACTUAL: <b style="color:{color}">{status}</b></p>
<div style="text-align: right;">
<span style="font-size: 2.2rem; filter: drop-shadow(0 0 10px rgba(255,255,255,0.2));" title="{weather}">{w_icon}</span>
<p style="font-size: 0.6rem; color: #94a3b8; margin: 0; font-weight: 600;">{weather}</p>
</div>
</div>
<div style="text-align: center; margin-top: -15px;">
<p style="font-size:1.2rem; font-weight:700; margin:0; color: #E8B547;">{data['name']}</p>
<p style="font-size:3.5rem; font-weight:800; color:#fff; margin:0; line-height: 1;">{risk:.1f}%</p>
<p style="font-size:0.7rem; color:#94a3b8; margin:5px 0 0 0; text-transform: uppercase; letter-spacing: 2px;">RIESGO TÉRMICO</p>
</div>
</div>
""", unsafe_allow_html=True)

    if weather == "Tormenta Eléctrica":
        protocol = "⛈️ <b style='color:#ff4b4b'>PELIGRO</b>: Tormenta eléctrica activa. <b>PROHIBIDO</b> el pastoreo en áreas abiertas. Resguardar al hato en establos protegidos por riesgo de rayos."
    elif weather == "Lluvias Fuertes":
        protocol = "🌧️ <b style='color:#E8B547'>AVISO</b>: Lluvias intensas. Riesgo de lodo y estrés por humedad. Se recomienda resguardar en áreas cubiertas y monitorear salud podal."
    elif risk > 85:
        protocol = "🚨 <b style='color:#ff4b4b'>ALERTA CRÍTICA</b>: Estrés térmico extremo detectado. Se requiere activar aspersores cada 15 min y asegurar agua a <20°C inmediatamente."
    elif risk > 65:
        protocol = "⚠️ <b style='color:#E8B547'>AVISO PREVENTIVO</b>: Índice térmico elevado. Es imperativo garantizar sombra total y ventilación para el hato."
    elif weather == "Viento Fuerte":
        protocol = "🌬️ <b style='color:#3498DB'>AVISO POR VIENTO</b>: Vientos fuertes detectados. Asegurar estructuras ligeras y monitorear posible irritación ocular en el hato."
    elif risk > 40:
        protocol = "⚖️ <b style='color:#3498DB'>MODERADO</b>: Condiciones ambientales estables. Mantener monitoreo preventivo de hidratación."
    else:
        protocol = "✅ <b style='color:#4caf50'>ESTADO ÓPTIMO</b>: Condiciones ideales para la producción. Autorizado pastoreo intensivo sin restricciones."

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
    # Lógica de Rotación Suave
    if 'rotation_lon' not in st.session_state:
        st.session_state.rotation_lon = data['lon']
    
    # Efecto de inercia/seguimiento suave: la cámara se mueve hacia el punto seleccionado
    # pero mantiene un desplazamiento constante para el efecto de rotación
    target_lon = data['lon']
    diff = target_lon - st.session_state.rotation_lon
    
    # Si la diferencia es muy grande (ej. cambio de país), saltamos un poco más rápido
    step = 0.05 if abs(diff) < 30 else 0.1
    st.session_state.rotation_lon += diff * step + 0.15 # 0.15 es el drift constante

    # GLOBO AZUL REAL (No negro)
    fig = go.Figure()
    
    fig.add_trace(go.Scattergeo(
        lon = df['lon'], lat = df['lat'], text = df['name'],
        mode = 'markers+text', textposition = 'top center', name = "",
        marker = dict(size = 14, color = df['risk'], colorscale = [[0, '#4caf50'], [0.5, '#E8B547'], [1, '#ff4b4b']], line = dict(width=1, color='white'), opacity = 0.9),
        showlegend = False, customdata = df[['name', 'weather', 'risk']],
        hovertemplate = "<b>%{customdata[0]}</b><br>Clima: %{customdata[1]}<br>Riesgo: %{customdata[2]}%<extra></extra>"
    ))

    fig.add_trace(go.Scattergeo(
        lon = [data['lon']], lat = [data['lat']], mode = 'markers',
        marker = dict(size = 40, symbol = 'circle-open', line = dict(width=3, color=color)),
        showlegend = False, hoverinfo = 'none'
    ))

    fig.update_layout(
        height = 700, margin = {"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor = "rgba(0,0,0,0)", plot_bgcolor = "rgba(0,0,0,0)",
        geo = dict(
            projection_type = "orthographic",
            showcoastlines = True, coastlinecolor = "#3498DB",
            showland = True, landcolor = "#1F2F45", # Azul Grisáceo elegante
            showocean = True, oceancolor = "#121926", # Azul Profundo (no negro)
            showcountries = True, countrycolor = "rgba(255,255,255,0.2)",
            bgcolor = "rgba(0,0,0,0)",
            projection_scale = 0.92, 
            projection_rotation = dict(lon=st.session_state.rotation_lon, lat=data['lat'], roll=0)
        ),
        transition = {'duration': 0, 'easing': 'linear'} # La suavidad la da nuestro loop
    )

    # Contenedor para el mapa con Sol y Luna superpuestos mediante CSS
    map_container = st.container()
    with map_container:
        st.markdown("""
            <div style="position: relative; touch-action: none;">
                <!-- SOL PROFESIONAL (Resplandor Intenso) -->
                <div class="sun-glow" style="
                    position: absolute; 
                    top: 10%; left: 8%; 
                    width: 30px; height: 30px; 
                    background: #fff; 
                    border-radius: 50%; 
                    z-index: 10;
                    pointer-events: none;
                "></div>
                <!-- LUNA PROFESIONAL -->
                <div class="moon-glow" style="
                    position: absolute; 
                    top: 22%; right: 10%; 
                    width: 22px; height: 22px; 
                    background: #E2E8F0; 
                    border-radius: 50%; 
                    z-index: 10;
                    pointer-events: none;
                "></div>
            </div>
        """, unsafe_allow_html=True)
        
        selection = st.plotly_chart(fig, use_container_width=True, on_select="rerun", config={'displayModeBar': False})

    if selection and "selection" in selection and selection["selection"]["points"]:
        clicked_name = selection["selection"]["points"][0]["text"]
        if clicked_name != st.session_state.selected_state:
            st.session_state.selected_state = clicked_name
            st.session_state.selected_country = df[df['name'] == clicked_name]['country'].iloc[0]
            st.rerun()

# Forzar actualización para la animación (Rotación Suave)
time.sleep(0.01)
st.rerun()
