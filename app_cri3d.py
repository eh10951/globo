import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
        background: rgba(232, 181, 71, 0.03);
        border-radius: 14px;
        padding: 15px;
        margin-top: 10px;
        border: 1px solid rgba(232, 181, 71, 0.25);
    }
    .protocol-header {
        color: #E8B547;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .protocol-body { font-size: 0.8rem; line-height: 1.4; color: #cbd5e1; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden; display: none !important;}
    header {visibility: hidden; display: none !important;}
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
    .stAppDeployButton {display: none !important;}
    .st-emotion-cache-1kyy7id {display: none !important;}
    .st-emotion-cache-zq5wmm {display: none !important;}
    button[title="View fullscreen"] {display: none !important;}
    .block-container { padding: 0.5rem 2rem !important; }
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem !important;}
    /* Ocultar scrollbar para vista limpia */
    .stApp { overflow: hidden !important; }
    ::-webkit-scrollbar { display: none; }
    /* Eliminación total de marca de agua de Streamlit */
    div[data-testid="stFooter"] {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .stAppToolbar {display: none !important;}
    .st-emotion-cache-1vt4y6f {display: none !important;}
    
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
</style>
""", unsafe_allow_html=True)

# Datos maestros
@st.cache_data
def get_data():
    base = [
        {"country": "México", "name": "Sonora", "lat": 29.3, "lon": -110.3, "risk": 94.2, "weather": "Mucho Sol"},
        {"country": "México", "name": "Chihuahua", "lat": 28.6, "lon": -106.1, "risk": 88.5, "weather": "Mucho Sol"},
        {"country": "México", "name": "Coahuila", "lat": 27.3, "lon": -101.7, "risk": 86.1, "weather": "Normal"},
        {"country": "México", "name": "Nuevo León", "lat": 25.7, "lon": -100.3, "risk": 82.3, "weather": "Viento Fuerte"},
        {"country": "México", "name": "Jalisco", "lat": 20.7, "lon": -103.3, "risk": 55.2, "weather": "Nublado"},
        {"country": "México", "name": "Veracruz", "lat": 19.2, "lon": -96.1, "risk": 41.5, "weather": "Lluvias Fuertes"},
        {"country": "México", "name": "Chiapas", "lat": 16.8, "lon": -93.1, "risk": 35.1, "weather": "Tormenta Eléctrica"},
        {"country": "USA", "name": "Texas", "lat": 31.9, "lon": -99.9, "risk": 85.0, "weather": "Mucho Sol"},
        {"country": "Brasil", "name": "Mato Grosso", "lat": -12.6, "lon": -55.4, "risk": 91.4, "weather": "Nublado"},
        {"country": "Australia", "name": "Queensland", "lat": -20.9, "lon": 142.7, "risk": 96.8, "weather": "Mucho Sol"}
    ]
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
    status = "CRÍTICO" if risk > 85 else ("ALERTA" if risk > 50 else "ÓPTIMO")

    st.markdown(f"""
        <div class="sidebar-section" style="border-top: 4px solid {color}; text-align: center; padding: 20px 15px;">
            <p style="font-size:0.7rem; color:#94a3b8; margin:0; text-transform: uppercase; letter-spacing: 1px;">ESTADO ACTUAL: <b style="color:{color}">{status}</b></p>
            
            <div style="margin: 15px 0;">
                <span style="font-size: 3rem; display: block; filter: drop-shadow(0 0 15px {color}44);" title="{weather}">{w_icon}</span>
                <p style="font-size: 0.8rem; color: #fff; margin: 5px 0 0 0; font-weight: 600;">{weather}</p>
            </div>

            <p style="font-size:1.3rem; font-weight:700; margin:0; color: #E8B547;">{data['name']}</p>
            <p style="font-size:3.5rem; font-weight:800; color:#fff; margin:0; line-height: 1.1;">{risk:.1f}%</p>
            <p style="font-size:0.7rem; color:#94a3b8; margin:0; text-transform: uppercase; letter-spacing: 2px;">RIESGO TÉRMICO</p>
        </div>
    """, unsafe_allow_html=True)

    if risk > 85: protocol = "🚨 **ALERTA CRÍTICA**: Estrés térmico extremo. Activar aspersores cada 15 min, agua a <20°C."
    elif risk > 65: protocol = "⚠️ **AVISO PREVENTIVO**: ITH elevado. Garantizar sombra total para el hato."
    elif risk > 40: protocol = "⚖️ **MODERADO**: Condiciones estables. Monitorear hidratación."
    else: protocol = "✅ **ÓPTIMO**: Condiciones ideales. Autorizado pastoreo intensivo."

    st.markdown(f"""
        <div class="ai-protocol-card">
            <div class="protocol-header">Sugerencias IA</div>
            <div class="protocol-body">{protocol}</div>
        </div>
    """, unsafe_allow_html=True)

with col_map:
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
            projection_rotation = dict(lon=data['lon'], lat=data['lat'], roll=0)
        )
    )

    # Contenedor para el mapa con Sol y Luna superpuestos mediante CSS
    map_container = st.container()
    with map_container:
        st.markdown("""
            <div style="position: relative; touch-action: none;">
                <!-- SOL PROFESIONAL (Resplandor Intenso) -->
                <div style="
                    position: absolute; 
                    top: 10%; left: 8%; 
                    width: 30px; height: 30px; 
                    background: #fff; 
                    border-radius: 50%; 
                    box-shadow: 0 0 15px #fff, 0 0 40px #E8B547, 0 0 70px #E8B547;
                    z-index: 10;
                    pointer-events: none;
                "></div>
                <!-- LUNA PROFESIONAL (Ligeramente más baja que el sol) -->
                <div style="
                    position: absolute; 
                    top: 22%; right: 10%; 
                    width: 22px; height: 22px; 
                    background: #E2E8F0; 
                    border-radius: 50%; 
                    box-shadow: 0 0 8px #fff, 0 0 25px rgba(148, 163, 184, 0.4); 
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
