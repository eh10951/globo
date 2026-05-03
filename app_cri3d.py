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
    .main { background: #05070a; color: #f8fafc; font-family: 'Outfit', sans-serif; }
    .stApp { background: #05070a; }
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
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem !important;}
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
    .st-emotion-cache-1v469f6 {display: none !important;}
    .st-emotion-cache-v698uo {display: none !important;}
    .st-emotion-cache-6q9sum {display: none !important;}
    .st-emotion-cache-1vt4y6f {display: none !important;}
    footer {display: none !important;}
</style>
""", unsafe_allow_html=True)

# Datos maestros
@st.cache_data
def get_data():
    base = [
        {"country": "México", "name": "Sonora", "lat": 29.3, "lon": -110.3, "risk": 94.2},
        {"country": "México", "name": "Chihuahua", "lat": 28.6, "lon": -106.1, "risk": 88.5},
        {"country": "México", "name": "Coahuila", "lat": 27.3, "lon": -101.7, "risk": 86.1},
        {"country": "México", "name": "Nuevo León", "lat": 25.7, "lon": -100.3, "risk": 82.3},
        {"country": "México", "name": "Jalisco", "lat": 20.7, "lon": -103.3, "risk": 55.2},
        {"country": "México", "name": "Veracruz", "lat": 19.2, "lon": -96.1, "risk": 41.5},
        {"country": "México", "name": "Chiapas", "lat": 16.8, "lon": -93.1, "risk": 35.1},
        {"country": "USA", "name": "Texas", "lat": 31.9, "lon": -99.9, "risk": 85.0},
        {"country": "Brasil", "name": "Mato Grosso", "lat": -12.6, "lon": -55.4, "risk": 91.4},
        {"country": "Australia", "name": "Queensland", "lat": -20.9, "lon": 142.7, "risk": 96.8}
    ]
    return pd.DataFrame(base).sort_values("name")

df = get_data()

if 'selected_state' not in st.session_state: st.session_state.selected_state = "Sonora"
if 'selected_country' not in st.session_state: st.session_state.selected_country = "México"

# Ajuste de columnas para balance profesional (Proporción 2:1)
col_map, col_side = st.columns([2, 1], gap="large", vertical_alignment="center")

with col_side:
    # Contenedor principal con efecto Glassmorphism
    st.markdown(f"""
        <div style="
            background: rgba(10, 14, 20, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 30px;
            border: 1px solid rgba(232, 181, 71, 0.2);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        ">
            <div style='text-align: center; margin-bottom: 25px;'>
                <p style='margin:0; font-size:0.9rem; color:#E8B547; letter-spacing: 4px; font-weight: 800; text-transform: uppercase;'>VISIÓN INTELIGENTE</p>
                <div style='height: 2px; width: 40px; background: #E8B547; margin: 10px auto;'></div>
            </div>
    """, unsafe_allow_html=True)
    
    countries = df['country'].unique().tolist()
    country_choice = st.selectbox("PAÍS DE ORIGEN", countries, index=countries.index(st.session_state.selected_country))
    
    if country_choice != st.session_state.selected_country:
        st.session_state.selected_country = country_choice
        st.session_state.selected_state = df[df['country'] == country_choice]['name'].iloc[0]
        st.rerun()

    states = df[df['country'] == st.session_state.selected_country]['name'].tolist()
    state_choice = st.selectbox("ESTADO / REGIÓN", states, index=states.index(st.session_state.selected_state))
    st.session_state.selected_state = state_choice

    data = df[df['name'] == st.session_state.selected_state].iloc[0]
    risk = data['risk']
    color = "#ff4b4b" if risk > 85 else ("#E8B547" if risk > 50 else "#4caf50")
    status = "NIVEL CRÍTICO" if risk > 85 else ("ALERTA" if risk > 50 else "ÓPTIMO")

    # Visualización de Riesgo Premium
    st.markdown(f"""
        <div style="margin: 25px 0;">
            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 8px;">
                <span style="font-size: 0.75rem; color: #94a3b8; font-weight: 600;">RIESGO ITH</span>
                <span style="font-size: 1.8rem; font-weight: 800; color: #fff;">{risk:.1f}%</span>
            </div>
            <div style="height: 6px; width: 100%; background: rgba(255,255,255,0.05); border-radius: 10px; overflow: hidden;">
                <div style="height: 100%; width: {risk}%; background: {color}; box-shadow: 0 0 10px {color}88;"></div>
            </div>
            <p style="font-size: 0.7rem; color: {color}; font-weight: 700; margin-top: 8px; letter-spacing: 1px;">{status}</p>
        </div>
        
        <div style="
            background: rgba(232, 181, 71, 0.05);
            border-left: 3px solid {color};
            padding: 15px;
            border-radius: 12px;
            margin-top: 20px;
        ">
            <p style="font-size: 0.65rem; color: #E8B547; font-weight: 800; margin-bottom: 5px; text-transform: uppercase;">Protocolo IA</p>
            <p style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.5; margin: 0;">
                { "Activar enfriamiento forzado y aspersores de inmediato." if risk > 85 else 
                  ("Preparar zonas de sombra y aumentar flujo de hidratación." if risk > 65 else 
                  "Condiciones estables. Monitoreo rutinario activo.") }
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_map:
    # GLOBO AZUL REAL (Más grande y centrado para profesionalismo)
    fig = go.Figure()
    
    fig.add_trace(go.Scattergeo(
        lon = df['lon'], lat = df['lat'], text = df['name'],
        mode = 'markers+text', textposition = 'top center', name = "",
        marker = dict(size = 14, color = df['risk'], colorscale = [[0, '#4caf50'], [0.5, '#E8B547'], [1, '#ff4b4b']], line = dict(width=1, color='white'), opacity = 0.9),
        showlegend = False, customdata = df['name'],
        hovertemplate = "<b>%{text}</b><br>Riesgo: %{marker.color}%<extra></extra>"
    ))

    fig.add_trace(go.Scattergeo(
        lon = [data['lon']], lat = [data['lat']], mode = 'markers',
        marker = dict(size = 40, symbol = 'circle-open', line = dict(width=3, color=color)),
        showlegend = False, hoverinfo = 'none'
    ))

    fig.update_layout(
        height = 500, margin = {"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor = "rgba(0,0,0,0)", plot_bgcolor = "rgba(0,0,0,0)",
        geo = dict(
            projection_type = "orthographic",
            showcoastlines = True, coastlinecolor = "#3498DB",
            showland = True, landcolor = "#1F2F45", 
            showocean = True, oceancolor = "#121926", 
            showcountries = True, countrycolor = "rgba(255,255,255,0.2)",
            bgcolor = "rgba(0,0,0,0)",
            projection_scale = 0.9, # Ajuste de distancia pedido por el usuario
            projection_rotation = dict(lon=data['lon'], lat=data['lat'], roll=0)
        )
    )

    selection = st.plotly_chart(fig, use_container_width=True, on_select="rerun", config={'displayModeBar': False})

    if selection and "selection" in selection and selection["selection"]["points"]:
        clicked_name = selection["selection"]["points"][0]["text"]
        if clicked_name != st.session_state.selected_state:
            st.session_state.selected_state = clicked_name
            st.session_state.selected_country = df[df['name'] == clicked_name]['country'].iloc[0]
            st.rerun()
