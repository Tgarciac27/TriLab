# ============================================================
# TRIAI COACH - Streamlit
# modulos/perfil.py - Perfil del atleta
# ============================================================

import streamlit as st
from datetime import date, datetime
from PIL import Image
import io
import base64


def calcular_edad(fecha_nacimiento):
    """Calcula la edad del atleta a partir de su fecha de nacimiento."""
    hoy  = date.today()
    edad = hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )
    return edad


def calcular_imc(peso_kg, altura_cm):
    """
    Calcula el Indice de Masa Corporal (IMC).
    IMC = peso (kg) / altura (m)^2
    """
    altura_m = altura_cm / 100
    imc      = peso_kg / (altura_m ** 2)
    return round(imc, 1)


def clasificar_imc(imc):
    """Clasifica el IMC segun los rangos de la OMS."""
    if imc < 18.5:   return 'Bajo peso'
    elif imc < 25.0: return 'Normal'
    elif imc < 30.0: return 'Sobrepeso'
    else:            return 'Obesidad'


def imagen_a_base64(imagen_bytes):
    """Convierte una imagen a base64 para guardarla en session_state."""
    return base64.b64encode(imagen_bytes).decode('utf-8')


def mostrar_formulario_bienvenida():
    """
    Muestra el formulario de bienvenida para crear el perfil del atleta.
    Se llama solo la primera vez que el atleta abre la app.
    Retorna True cuando el perfil ha sido guardado correctamente.
    """
    st.markdown('''
    <div style="text-align:center;padding:2rem 0 1rem;">
        <div style="font-size:48px;margin-bottom:8px;">🏅</div>
        <h1 style="font-size:28px;font-weight:600;margin-bottom:4px;">
            Bienvenido a TriAI Coach
        </h1>
        <p style="color:#888780;font-size:15px;">
            Completa tu perfil para comenzar tu entrenamiento personalizado
        </p>
    </div>
    ''', unsafe_allow_html=True)

    st.divider()

    # ── Foto de perfil ──
    st.subheader('📸 Foto de perfil')
    foto = st.file_uploader(
        'Sube tu foto (jpg, png)',
        type=['jpg','jpeg','png'],
        help='Opcional — puedes agregarla despues'
    )
    if foto:
        imagen = Image.open(foto)
        col_img = st.columns([1,2,1])[1]
        with col_img:
            st.image(imagen, width=150, caption='Tu foto de perfil')

    st.divider()

    # ── Datos personales ──
    st.subheader('👤 Datos personales')

    col1, col2 = st.columns(2)
    with col1:
        nombre    = st.text_input('Nombre *', placeholder='Tu nombre')
        sexo      = st.selectbox('Sexo *', ['Masculino','Femenino','Prefiero no decir'])
        ubicacion = st.text_input('Ubicacion', placeholder='Ciudad, Pais')
    with col2:
        apellidos = st.text_input('Apellidos *', placeholder='Tus apellidos')
        correo    = st.text_input('Correo electronico', placeholder='correo@ejemplo.com')
        fecha_nac = st.date_input(
            'Fecha de nacimiento *',
            value=date(1990, 1, 1),
            min_value=date(1940, 1, 1),
            max_value=date.today()
        )

    biografia = st.text_area(
        'Biografia',
        placeholder='Cuentanos sobre ti — cuanto tiempo llevas en el triatlon, tus logros...',
        max_chars=300,
        help='Maximo 300 caracteres'
    )

    st.divider()

    # ── Datos fisicos ──
    st.subheader('⚖️ Datos fisicos')

    col3, col4 = st.columns(2)
    with col3:
        altura = st.number_input('Altura (cm) *',
                                  min_value=140, max_value=220, value=175, step=1)
    with col4:
        peso   = st.number_input('Peso (kg) *',
                                  min_value=40, max_value=150, value=72, step=1)

    if altura > 0 and peso > 0:
        imc     = calcular_imc(peso, altura)
        clasif  = clasificar_imc(imc)
        st.caption(f'IMC: {imc} — {clasif}')

    st.divider()

    # ── Datos deportivos ──
    st.subheader('🏅 Perfil deportivo')

    col5, col6 = st.columns(2)
    with col5:
        modalidad  = st.selectbox('Modalidad de triatlon *',
                     ['Sprint (750m/20km/5km)',
                      'Olimpico (1.5km/40km/10km)',
                      'Media distancia (1.9km/90km/21km)',
                      'Ironman (3.8km/180km/42km)'])
        nivel      = st.selectbox('Nivel *',
                     ['Principiante','Intermedio','Avanzado'])
        disc_debil = st.selectbox('Disciplina debil',
                     ['Natacion','Ciclismo','Carrera'])
    with col6:
        objetivo      = st.text_input('Objetivo (tiempo meta)',
                                       placeholder='Ej: Sub 2:30, Terminar, Mejorar marca')
        horas_semana  = st.slider('Horas disponibles por semana *',
                                   min_value=4, max_value=20, value=10, step=1)
        fecha_comp    = st.date_input('Fecha de competencia',
                                       value=date.today(),
                                       min_value=date.today())

    st.divider()

    # ── Datos fisiologicos ──
    st.subheader('❤️ Datos fisiologicos')
    st.caption('Si no los conoces, puedes dejar los valores por defecto')

    col7, col8 = st.columns(2)
    with col7:
        fc_max    = st.slider('FC maxima (bpm)', 150, 220, 185, step=1)
    with col8:
        fc_reposo = st.slider('FC reposo (bpm)', 35, 80, 55, step=1)

    # Formula de FC maxima estimada
    if fecha_nac:
        edad_atleta = calcular_edad(fecha_nac)
        fc_estimada = 220 - edad_atleta
        st.caption(f'FC maxima estimada para tu edad ({edad_atleta} anos): {fc_estimada} bpm')

    st.divider()

    # ── Boton de guardar ──
    col_btn = st.columns([1, 2, 1])[1]
    with col_btn:
        guardar = st.button('Crear mi perfil y comenzar →',
                            type='primary',
                            use_container_width=True)

    if guardar:
        # Validamos campos obligatorios
        if not nombre:
            st.error('El nombre es obligatorio.')
            return False
        if not apellidos:
            st.error('Los apellidos son obligatorios.')
            return False

        # Extraemos la modalidad sin las distancias
        modalidad_limpia = modalidad.split(' ')[0].lower()

        # Guardamos el perfil en session_state
        st.session_state.perfil = {
            'nombre'      : nombre,
            'apellidos'   : apellidos,
            'nombre_completo': f'{nombre} {apellidos}',
            'biografia'   : biografia,
            'sexo'        : sexo,
            'correo'      : correo,
            'ubicacion'   : ubicacion,
            'fecha_nac'   : fecha_nac,
            'edad'        : calcular_edad(fecha_nac),
            'altura_cm'   : altura,
            'peso_kg'     : peso,
            'imc'         : calcular_imc(peso, altura),
            'modalidad'   : modalidad_limpia,
            'modalidad_completa': modalidad,
            'nivel'       : nivel.lower(),
            'disciplina_debil': disc_debil,
            'objetivo'    : objetivo,
            'horas_semana': horas_semana,
            'fecha_comp'  : fecha_comp,
            'fc_maxima'   : fc_max,
            'fc_reposo'   : fc_reposo,
        }

        # Guardamos la foto si se subio
        if foto:
            foto.seek(0)
            st.session_state.perfil['foto_bytes'] = imagen_a_base64(foto.read())
        else:
            st.session_state.perfil['foto_bytes'] = None

        # Marcamos que el perfil ya fue creado
        st.session_state.perfil_creado = True

        st.success(f'Perfil creado exitosamente. Bienvenido, {nombre}!')
        st.balloons()

        import time
        time.sleep(1.5)
        st.rerun()

    return False


def mostrar_perfil_sidebar():
    """
    Muestra un resumen compacto del perfil en el sidebar.
    Se llama desde app.py para mostrar el perfil del atleta
    en el menu lateral de navegacion.
    """
    perfil = st.session_state.get('perfil', {})
    if not perfil:
        return

    # Foto de perfil
    if perfil.get('foto_bytes'):
        img_data = base64.b64decode(perfil['foto_bytes'])
        imagen   = Image.open(io.BytesIO(img_data))
        st.image(imagen, width=80)
    else:
        st.markdown('''
        <div style="width:70px;height:70px;border-radius:50%;
                    background:#1D9E75;display:flex;align-items:center;
                    justify-content:center;margin-bottom:8px;">
            <span style="font-size:28px;color:white;">
        ''' + perfil.get('nombre','A')[0].upper() + '''
            </span>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown(f'''
    <div style="margin-bottom:4px;">
        <div style="font-size:15px;font-weight:600;color:white;">
            {perfil.get("nombre_completo","Atleta")}
        </div>
        <div style="font-size:12px;color:#888780;">
            {perfil.get("modalidad_completa","").split("(")[0].strip()}
        </div>
        <div style="font-size:12px;color:#888780;">
            {perfil.get("ubicacion","")}
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Metricas del perfil
    dias_comp = (perfil.get('fecha_comp', date.today()) - date.today()).days
    dias_comp = max(0, dias_comp)

    st.markdown(f'''
    <div style="background:#2A2A28;border-radius:10px;padding:10px;margin-top:8px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
            <div style="text-align:center;flex:1;">
                <div style="font-size:16px;font-weight:600;color:#1D9E75;">
                    {dias_comp}
                </div>
                <div style="font-size:10px;color:#888780;">dias</div>
            </div>
            <div style="text-align:center;flex:1;">
                <div style="font-size:16px;font-weight:600;color:#378ADD;">
                    {perfil.get("horas_semana",10)}h
                </div>
                <div style="font-size:10px;color:#888780;">semana</div>
            </div>
            <div style="text-align:center;flex:1;">
                <div style="font-size:16px;font-weight:600;color:#BA7517;">
                    {perfil.get("edad","-")}
                </div>
                <div style="font-size:10px;color:#888780;">anos</div>
            </div>
        </div>
        <div style="font-size:11px;color:#888780;text-align:center;">
            {perfil.get("objetivo","Sin objetivo definido")}
        </div>
    </div>
    ''', unsafe_allow_html=True)


def mostrar_pagina_perfil():
    """
    Muestra la pagina completa del perfil del atleta
    donde puede ver y editar sus datos.
    """
    perfil = st.session_state.get('perfil', {})

    st.title('👤 Mi perfil')

    tab1, tab2 = st.tabs(['📋 Ver perfil', '✏️ Editar perfil'])

    # ── TAB 1: Ver perfil ──
    with tab1:
        col_foto, col_info = st.columns([1, 3])

        with col_foto:
            if perfil.get('foto_bytes'):
                img_data = base64.b64decode(perfil['foto_bytes'])
                imagen   = Image.open(io.BytesIO(img_data))
                st.image(imagen, width=150)
            else:
                st.markdown(f'''
                <div style="width:120px;height:120px;border-radius:50%;
                            background:#1D9E75;display:flex;align-items:center;
                            justify-content:center;margin-bottom:8px;">
                    <span style="font-size:48px;color:white;">
                        {perfil.get("nombre","A")[0].upper()}
                    </span>
                </div>
                ''', unsafe_allow_html=True)

        with col_info:
            st.markdown(f'## {perfil.get("nombre_completo","Atleta")}')
            if perfil.get('biografia'):
                st.caption(perfil['biografia'])
            st.markdown(f'''
            📍 {perfil.get("ubicacion","Sin ubicacion")} &nbsp;|&nbsp;
            ✉️ {perfil.get("correo","Sin correo")} &nbsp;|&nbsp;
            {perfil.get("sexo","")}
            ''')

        st.divider()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Edad', f'{perfil.get("edad","-")} anos')
        with col2:
            st.metric('Peso', f'{perfil.get("peso_kg","-")} kg')
        with col3:
            st.metric('Altura', f'{perfil.get("altura_cm","-")} cm')
        with col4:
            st.metric('IMC', f'{perfil.get("imc","-")}')

        st.divider()

        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.metric('Modalidad',
                      perfil.get("modalidad_completa","").split("(")[0].strip())
        with col6:
            st.metric('Nivel', perfil.get("nivel","").capitalize())
        with col7:
            st.metric('Horas/semana', f'{perfil.get("horas_semana","-")} h')
        with col8:
            dias = (perfil.get('fecha_comp', date.today()) - date.today()).days
            st.metric('Dias para competir', max(0, dias))

        st.divider()

        col9, col10, col11 = st.columns(3)
        with col9:
            st.metric('FC maxima', f'{perfil.get("fc_maxima","-")} bpm')
        with col10:
            st.metric('FC reposo', f'{perfil.get("fc_reposo","-")} bpm')
        with col11:
            st.metric('Disciplina debil', perfil.get("disciplina_debil","-"))

    # ── TAB 2: Editar perfil ──
    with tab2:
        st.info('Actualiza tus datos y guarda los cambios.')

        col_a, col_b = st.columns(2)
        with col_a:
            nuevo_nombre    = st.text_input('Nombre', value=perfil.get('nombre',''))
            nuevo_apellido  = st.text_input('Apellidos', value=perfil.get('apellidos',''))
            nueva_ubicacion = st.text_input('Ubicacion', value=perfil.get('ubicacion',''))
            nuevo_correo    = st.text_input('Correo', value=perfil.get('correo',''))
        with col_b:
            nuevo_peso   = st.number_input('Peso (kg)', min_value=40, max_value=150,
                                           value=perfil.get('peso_kg', 72))
            nueva_altura = st.number_input('Altura (cm)', min_value=140, max_value=220,
                                           value=perfil.get('altura_cm', 175))
            nuevas_horas = st.slider('Horas/semana', 4, 20,
                                     value=perfil.get('horas_semana', 10))
            nuevo_obj    = st.text_input('Objetivo', value=perfil.get('objetivo',''))

        nueva_bio = st.text_area('Biografia', value=perfil.get('biografia',''),
                                  max_chars=300)

        nueva_foto = st.file_uploader('Cambiar foto de perfil',
                                       type=['jpg','jpeg','png'])

        col_btn2 = st.columns([1, 2, 1])[1]
        with col_btn2:
            if st.button('Guardar cambios', type='primary',
                         use_container_width=True):
                st.session_state.perfil['nombre']         = nuevo_nombre
                st.session_state.perfil['apellidos']      = nuevo_apellido
                st.session_state.perfil['nombre_completo']= f'{nuevo_nombre} {nuevo_apellido}'
                st.session_state.perfil['ubicacion']      = nueva_ubicacion
                st.session_state.perfil['correo']         = nuevo_correo
                st.session_state.perfil['peso_kg']        = nuevo_peso
                st.session_state.perfil['altura_cm']      = nueva_altura
                st.session_state.perfil['imc']            = calcular_imc(nuevo_peso, nueva_altura)
                st.session_state.perfil['horas_semana']   = nuevas_horas
                st.session_state.perfil['objetivo']       = nuevo_obj
                st.session_state.perfil['biografia']      = nueva_bio

                if nueva_foto:
                    nueva_foto.seek(0)
                    st.session_state.perfil['foto_bytes'] = imagen_a_base64(nueva_foto.read())

                st.success('Perfil actualizado correctamente.')
                st.rerun()
