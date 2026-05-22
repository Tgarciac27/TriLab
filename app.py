# ============================================================
# TRIAI COACH
# app.py - Archivo principal de la aplicacion Streamlit
# ============================================================

import streamlit as st
from datetime import date

st.set_page_config(
    page_title='TriAI Coach',
    page_icon='🏅',
    layout='wide',
    initial_sidebar_state='expanded',
)

# Estilos personalizados
st.markdown('''
<style>
    .main { background-color: #FAFAF8; }
    [data-testid="stSidebar"] { background-color: #1A1A18; }
    [data-testid="stSidebar"] * { color: #E8E8E4 !important; }
    .stButton > button {
        background-color: #1D9E75;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
    }
    .stButton > button:hover { background-color: #0F6E56; }
    .badge-ok {
        background: #E1F5EE; color: #085041;
        padding: 3px 10px; border-radius: 20px;
        font-size: 12px; font-weight: 500;
    }
    .badge-nuevo {
        background: #EEEDFE; color: #3C3489;
        padding: 3px 10px; border-radius: 20px;
        font-size: 12px; font-weight: 500;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# Importamos los modulos
from modulos import modulo1, modulo2, modulo3, modulo4, modulo5, modulo6
from modulos import perfil as modulo_perfil

# ── Verificamos si el perfil ya fue creado ──
perfil_creado = st.session_state.get('perfil_creado', False)

# ── Si no hay perfil, mostramos el formulario de bienvenida ──
if not perfil_creado:
    modulo_perfil.mostrar_formulario_bienvenida()
    st.stop()

# ── Si hay perfil, mostramos la app completa ──
perfil = st.session_state.get('perfil', {})

# ── Sidebar ──
with st.sidebar:
    st.markdown('''
    <div style="padding:8px 0 12px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
            <span style="font-size:26px;">🏅</span>
            <div>
                <div style="font-size:17px;font-weight:600;color:white;">TriAI Coach</div>
                <div style="font-size:11px;color:#888780;">Entrenamiento inteligente</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Perfil del atleta en sidebar
    modulo_perfil.mostrar_perfil_sidebar()

    st.divider()

    # Menu de navegacion
    modulo_seleccionado = st.radio(
        'Navegacion',
        options=[
            '🏠  Inicio',
            '👤  Mi perfil',
            '📊  Registro y Analisis',
            '📅  Plan de Entrenamiento',
            '⏱   Transiciones T1 y T2',
            '🍎  Nutricion e Hidratacion',
            '🔬  Biomecanica',
            '💪  Fuerza y Acondicionamiento',
        ],
        label_visibility='collapsed',
    )

# ── Contenido principal ──

if '🏠' in modulo_seleccionado:

    nombre = perfil.get('nombre', 'Atleta')
    hora   = date.today()
    st.markdown(f'### Hola, {nombre} 👋')
    st.markdown('#### Bienvenido a tu entrenamiento de hoy')
    st.divider()

    # Metricas principales
    dias_comp = max(0, (perfil.get('fecha_comp', date.today()) - date.today()).days)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Dias para competir', dias_comp)
    with col2:
        st.metric('Modalidad',
                  perfil.get('modalidad_completa','').split('(')[0].strip())
    with col3:
        st.metric('Nivel', perfil.get('nivel','').capitalize())
    with col4:
        st.metric('Objetivo', perfil.get('objetivo','-'))

    st.divider()

    # Modulos
    st.markdown('##### Modulos de entrenamiento')

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        with st.container(border=True):
            st.markdown('📊 **Registro y Analisis**')
            st.caption('Registra y analiza natacion, ciclismo y carrera')
            st.markdown('<span class="badge-ok">Activo</span>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('⏱ **Transiciones T1 y T2**')
            st.caption('Historial y recomendaciones de transiciones')
            st.markdown('<span class="badge-ok">Activo</span>', unsafe_allow_html=True)
    with col_b:
        with st.container(border=True):
            st.markdown('📅 **Plan de Entrenamiento**')
            st.caption('Plan personalizado con IA segun tu perfil')
            st.markdown('<span class="badge-ok">Activo</span>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('🍎 **Nutricion e Hidratacion**')
            st.caption('Plan nutricional y control de hidratacion')
            st.markdown('<span class="badge-ok">Activo</span>', unsafe_allow_html=True)
    with col_c:
        with st.container(border=True):
            st.markdown('🔬 **Biomecanica**')
            st.caption('Analisis de tecnica con video e IA')
            st.markdown('<span class="badge-nuevo">IA</span>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('💪 **Fuerza y Acondicionamiento**')
            st.caption('Rutinas de fuerza, calentamiento y enfriamiento')
            st.markdown('<span class="badge-ok">Activo</span>', unsafe_allow_html=True)

elif '👤' in modulo_seleccionado:
    modulo_perfil.mostrar_pagina_perfil()

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
