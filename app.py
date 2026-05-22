# ============================================================
# TRIAI COACH
# app.py - Archivo principal de la aplicacion Streamlit
# ============================================================

import streamlit as st

# Configuracion de la pagina
st.set_page_config(
    page_title='TriAI Coach',
    page_icon='🏅',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ── Estilos personalizados ──
st.markdown('''
<style>
    /* Fondo y fuente general */
    .main { background-color: #FAFAF8; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1A1A18;
    }
    [data-testid="stSidebar"] * {
        color: #E8E8E4 !important;
    }

    /* Tarjetas de modulo */
    .modulo-card {
        background: white;
        border: 1px solid #E8E8E4;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
        cursor: pointer;
        transition: box-shadow 0.2s;
    }
    .modulo-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    /* Badge de estado */
    .badge-ok {
        background: #E1F5EE;
        color: #085041;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }
    .badge-nuevo {
        background: #EEEDFE;
        color: #3C3489;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }

    /* Metricas */
    .metrica-card {
        background: #F4F4F0;
        border-radius: 10px;
        padding: 14px 16px;
        text-align: center;
    }
    .metrica-valor {
        font-size: 28px;
        font-weight: 600;
        color: #1A1A18;
    }
    .metrica-label {
        font-size: 12px;
        color: #888780;
        margin-top: 2px;
    }

    /* Botones principales */
    .stButton > button {
        background-color: #1D9E75;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #0F6E56;
    }

    /* Titulos de seccion */
    .seccion-titulo {
        font-size: 13px;
        font-weight: 600;
        color: #888780;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 10px;
    }

    /* Ocultar el menu de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
''', unsafe_allow_html=True)


# ── Importamos los modulos ──
from modulos import modulo1, modulo2, modulo3, modulo4, modulo5, modulo6


# ── Sidebar: navegacion principal ──
with st.sidebar:
    st.markdown('''
    <div style="padding: 8px 0 20px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <span style="font-size:28px;">🏅</span>
            <div>
                <div style="font-size:18px;font-weight:600;color:white;">TriAI Coach</div>
                <div style="font-size:12px;color:#888780;">Entrenamiento inteligente</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.divider()

    # Menu de navegacion
    modulo_seleccionado = st.radio(
        'Navegacion',
        options=[
            '🏠  Inicio',
            '📊  Registro y Analisis',
            '📅  Plan de Entrenamiento',
            '⏱   Transiciones T1 y T2',
            '🍎  Nutricion e Hidratacion',
            '🔬  Biomecanica',
            '💪  Fuerza y Acondicionamiento',
        ],
        label_visibility='collapsed',
    )

    st.divider()

    # Perfil del atleta en sidebar
    st.markdown('<div style="font-size:12px;color:#888780;margin-bottom:8px;">PERFIL</div>',
                unsafe_allow_html=True)
    st.markdown('''
    <div style="background:#2A2A28;border-radius:10px;padding:12px;">
        <div style="font-size:14px;font-weight:500;color:white;">Atleta</div>
        <div style="font-size:12px;color:#888780;margin-top:2px;">Triatlon olimpico</div>
        <div style="margin-top:10px;display:flex;justify-content:space-between;">
            <div style="text-align:center;">
                <div style="font-size:16px;font-weight:600;color:#1D9E75;">23</div>
                <div style="font-size:10px;color:#888780;">dias</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:16px;font-weight:600;color:#378ADD;">10h</div>
                <div style="font-size:10px;color:#888780;">semana</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:16px;font-weight:600;color:#BA7517;">6</div>
                <div style="font-size:10px;color:#888780;">modulos</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


# ── Contenido principal segun el modulo seleccionado ──

if '🏠' in modulo_seleccionado:

    # ── PANTALLA DE INICIO ──
    st.markdown('### Buenos dias 👋')
    st.markdown('#### Bienvenido a TriAI Coach')
    st.markdown('---')

    # Metricas de la semana
    st.markdown('<div class="seccion-titulo">Resumen de la semana</div>',
                unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Natacion', '12.4 km', '+2.1 km')
    with col2:
        st.metric('Ciclismo', '87 km', '+12 km')
    with col3:
        st.metric('Carrera', '34 km', '+4 km')
    with col4:
        st.metric('Carga TRIMP', '423', '+38')

    st.markdown('---')

    # Proxima competencia
    st.markdown('<div class="seccion-titulo">Proxima competencia</div>',
                unsafe_allow_html=True)

    col_comp, col_dias = st.columns([3, 1])
    with col_comp:
        st.info('🏁 **Triatlon Olimpico** — Quedan 23 dias para competir')
    with col_dias:
        st.metric('Semana actual', '4 de 8', 'Intensidad')

    st.markdown('---')

    # Modulos
    st.markdown('<div class="seccion-titulo">Modulos de entrenamiento</div>',
                unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        with st.container(border=True):
            st.markdown('📊 **Registro y Analisis**')
            st.caption('Registra y analiza natacion, ciclismo y carrera')
            st.markdown('<span class="badge-ok">Activo</span>',
                        unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('⏱ **Transiciones T1 y T2**')
            st.caption('Historial y recomendaciones de transiciones')
            st.markdown('<span class="badge-ok">Activo</span>',
                        unsafe_allow_html=True)

    with col_b:
        with st.container(border=True):
            st.markdown('📅 **Plan de Entrenamiento**')
            st.caption('Plan personalizado con IA segun tu perfil')
            st.markdown('<span class="badge-ok">Activo</span>',
                        unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('🍎 **Nutricion e Hidratacion**')
            st.caption('Plan nutricional y control de hidratacion')
            st.markdown('<span class="badge-ok">Activo</span>',
                        unsafe_allow_html=True)

    with col_c:
        with st.container(border=True):
            st.markdown('🔬 **Biomecanica**')
            st.caption('Analisis de tecnica con video e IA')
            st.markdown('<span class="badge-nuevo">IA</span>',
                        unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('💪 **Fuerza y Acondicionamiento**')
            st.caption('Rutinas de fuerza, calentamiento y enfriamiento')
            st.markdown('<span class="badge-ok">Activo</span>',
                        unsafe_allow_html=True)

    st.markdown('---')

    # Entrenamiento de hoy
    st.markdown('<div class="seccion-titulo">Entrenamiento de hoy</div>',
                unsafe_allow_html=True)

    col_hoy1, col_hoy2 = st.columns(2)
    with col_hoy1:
        with st.container(border=True):
            st.markdown('🚴 **Ciclismo** — Fondo Z2')
            st.caption('45 km · Zona 2 · FC objetivo: 135 bpm · 82 min')
    with col_hoy2:
        with st.container(border=True):
            st.markdown('💪 **Fuerza** — Gluteos y piernas')
            st.caption('40 min · Semana base · RPE objetivo: 6-7')


elif '📊' in modulo_seleccionado:
    modulo1.mostrar()

elif '📅' in modulo_seleccionado:
    modulo2.mostrar()

elif '⏱' in modulo_seleccionado:
    modulo3.mostrar()

elif '🍎' in modulo_seleccionado:
    modulo4.mostrar()

elif '🔬' in modulo_seleccionado:
    modulo5.mostrar()

elif '💪' in modulo_seleccionado:
    modulo6.mostrar()
