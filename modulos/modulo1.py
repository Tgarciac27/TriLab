# ============================================================
# TRIAI COACH - Streamlit
# modulos/modulo1.py - Registro y Analisis de Entrenamientos
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor']   = '#f8f8f8'
plt.rcParams['axes.spines.top']  = False
plt.rcParams['axes.spines.right']= False

COLORES = {
    'Natacion': '#1D9E75',
    'Ciclismo': '#378ADD',
    'Carrera' : '#BA7517',
    'Fuerza'  : '#D4537E',
    'Descanso': '#888780',
}


# ── Funciones de calculo ──

def calcular_pace_natacion(distancia_m, tiempo_min):
    if distancia_m == 0: return 'N/A'
    pace = (tiempo_min / distancia_m) * 100
    return f'{int(pace)}:{int((pace - int(pace)) * 60):02d}'

def calcular_velocidad_ciclismo(distancia_m, tiempo_min):
    if tiempo_min == 0: return 0.0
    return round((distancia_m / 1000) / (tiempo_min / 60), 1)

def calcular_pace_carrera(distancia_m, tiempo_min):
    if distancia_m == 0: return 'N/A'
    pace = tiempo_min / (distancia_m / 1000)
    return f'{int(pace)}:{int((pace - int(pace)) * 60):02d}'

def calcular_zona_fc(fc_promedio, fc_max=185):
    pct = (fc_promedio / fc_max) * 100
    if pct < 60:   return 'Z1 Recuperacion'
    elif pct < 70: return 'Z2 Base aerobica'
    elif pct < 80: return 'Z3 Umbral aerobico'
    elif pct < 90: return 'Z4 Umbral anaerobico'
    else:          return 'Z5 VO2 maximo'

def calcular_carga(tiempo_min, fc_promedio, fc_reposo=55, fc_max=185):
    if fc_promedio <= fc_reposo: return 0.0
    hrr   = (fc_promedio - fc_reposo) / (fc_max - fc_reposo)
    trimp = tiempo_min * hrr * 0.64 * (2.718 ** (1.92 * hrr))
    return round(trimp, 1)

def enriquecer_registro(df):
    df             = df.copy()
    df['zona_fc']      = df.apply(lambda r: calcular_zona_fc(r['fc_promedio']), axis=1)
    df['carga']        = df.apply(lambda r: calcular_carga(r['tiempo_min'], r['fc_promedio']), axis=1)
    df['distancia_km'] = (df['distancia_m'] / 1000).round(2)
    df['semana']       = df['fecha'].dt.isocalendar().week
    return df


# ── Datos de ejemplo ──

def cargar_datos_ejemplo():
    datos = [
        {'fecha':'2025-04-14','disciplina':'Ciclismo','tipo_sesion':'Fondo Z2',
         'distancia_m':45000,'tiempo_min':82,'fc_promedio':135,'fc_maxima':152,'cadencia':88,'notas':''},
        {'fecha':'2025-04-14','disciplina':'Fuerza','tipo_sesion':'Acondicionamiento',
         'distancia_m':0,'tiempo_min':40,'fc_promedio':128,'fc_maxima':145,'cadencia':0,'notas':''},
        {'fecha':'2025-04-15','disciplina':'Natacion','tipo_sesion':'Tecnica',
         'distancia_m':2000,'tiempo_min':42,'fc_promedio':132,'fc_maxima':148,'cadencia':28,'notas':''},
        {'fecha':'2025-04-16','disciplina':'Carrera','tipo_sesion':'Z2 suave',
         'distancia_m':8000,'tiempo_min':44,'fc_promedio':138,'fc_maxima':152,'cadencia':170,'notas':''},
        {'fecha':'2025-04-17','disciplina':'Natacion','tipo_sesion':'Fondo',
         'distancia_m':2500,'tiempo_min':50,'fc_promedio':138,'fc_maxima':155,'cadencia':30,'notas':''},
        {'fecha':'2025-04-17','disciplina':'Fuerza','tipo_sesion':'Acondicionamiento',
         'distancia_m':0,'tiempo_min':40,'fc_promedio':125,'fc_maxima':140,'cadencia':0,'notas':''},
        {'fecha':'2025-04-18','disciplina':'Ciclismo','tipo_sesion':'Umbral',
         'distancia_m':38000,'tiempo_min':68,'fc_promedio':162,'fc_maxima':178,'cadencia':92,'notas':''},
        {'fecha':'2025-04-19','disciplina':'Carrera','tipo_sesion':'Fondo',
         'distancia_m':12000,'tiempo_min':62,'fc_promedio':145,'fc_maxima':162,'cadencia':172,'notas':''},
        {'fecha':'2025-04-21','disciplina':'Ciclismo','tipo_sesion':'Fondo Z2',
         'distancia_m':50000,'tiempo_min':90,'fc_promedio':137,'fc_maxima':155,'cadencia':89,'notas':''},
        {'fecha':'2025-04-21','disciplina':'Fuerza','tipo_sesion':'Acondicionamiento',
         'distancia_m':0,'tiempo_min':40,'fc_promedio':128,'fc_maxima':142,'cadencia':0,'notas':''},
        {'fecha':'2025-04-22','disciplina':'Natacion','tipo_sesion':'Series',
         'distancia_m':3000,'tiempo_min':55,'fc_promedio':158,'fc_maxima':174,'cadencia':34,'notas':''},
        {'fecha':'2025-04-23','disciplina':'Carrera','tipo_sesion':'Umbral',
         'distancia_m':10000,'tiempo_min':48,'fc_promedio':164,'fc_maxima':180,'cadencia':178,'notas':''},
        {'fecha':'2025-04-25','disciplina':'Descanso','tipo_sesion':'Descanso activo',
         'distancia_m':0,'tiempo_min':30,'fc_promedio':105,'fc_maxima':115,'cadencia':0,'notas':''},
        {'fecha':'2025-04-26','disciplina':'Ciclismo','tipo_sesion':'Brick',
         'distancia_m':30000,'tiempo_min':55,'fc_promedio':155,'fc_maxima':172,'cadencia':90,'notas':'Brick T2'},
        {'fecha':'2025-04-26','disciplina':'Carrera','tipo_sesion':'Brick',
         'distancia_m':5000,'tiempo_min':26,'fc_promedio':168,'fc_maxima':182,'cadencia':180,'notas':'Brick T2'},
        {'fecha':'2025-05-05','disciplina':'Ciclismo','tipo_sesion':'Fondo Z2',
         'distancia_m':48000,'tiempo_min':86,'fc_promedio':136,'fc_maxima':154,'cadencia':88,'notas':''},
        {'fecha':'2025-05-05','disciplina':'Fuerza','tipo_sesion':'Acondicionamiento',
         'distancia_m':0,'tiempo_min':40,'fc_promedio':128,'fc_maxima':143,'cadencia':0,'notas':''},
        {'fecha':'2025-05-06','disciplina':'Natacion','tipo_sesion':'Fondo',
         'distancia_m':4000,'tiempo_min':74,'fc_promedio':141,'fc_maxima':158,'cadencia':31,'notas':''},
        {'fecha':'2025-05-07','disciplina':'Carrera','tipo_sesion':'Umbral',
         'distancia_m':10000,'tiempo_min':46,'fc_promedio':165,'fc_maxima':181,'cadencia':180,'notas':''},
        {'fecha':'2025-05-08','disciplina':'Natacion','tipo_sesion':'Tecnica',
         'distancia_m':2000,'tiempo_min':40,'fc_promedio':130,'fc_maxima':146,'cadencia':29,'notas':''},
        {'fecha':'2025-05-09','disciplina':'Descanso','tipo_sesion':'Descanso activo',
         'distancia_m':0,'tiempo_min':30,'fc_promedio':105,'fc_maxima':115,'cadencia':0,'notas':''},
        {'fecha':'2025-05-10','disciplina':'Ciclismo','tipo_sesion':'Brick',
         'distancia_m':32000,'tiempo_min':58,'fc_promedio':157,'fc_maxima':173,'cadencia':91,'notas':'Brick T2'},
        {'fecha':'2025-05-10','disciplina':'Carrera','tipo_sesion':'Brick',
         'distancia_m':5000,'tiempo_min':25,'fc_promedio':170,'fc_maxima':183,'cadencia':182,'notas':'Brick T2'},
    ]
    df = pd.DataFrame(datos)
    df['fecha'] = pd.to_datetime(df['fecha'])
    return enriquecer_registro(df)


# ── Funcion principal del modulo ──

def mostrar():
    st.title('📊 Registro y Analisis de Entrenamientos')

    # Inicializamos el registro en session_state para que persista
    if 'registro' not in st.session_state:
        st.session_state.registro = cargar_datos_ejemplo()

    registro = st.session_state.registro

    # ── Tabs del modulo ──
    tab1, tab2, tab3, tab4 = st.tabs([
        '📈 Resumen',
        '📋 Historial',
        '➕ Registrar sesion',
        '🤖 Recomendaciones IA',
    ])

    # ── TAB 1: Resumen ──
    with tab1:
        st.subheader('Resumen de entrenamientos')

        col1, col2, col3, col4 = st.columns(4)
        datos_nat = registro[registro['disciplina'] == 'Natacion']
        datos_cic = registro[registro['disciplina'] == 'Ciclismo']
        datos_car = registro[registro['disciplina'] == 'Carrera']

        with col1:
            st.metric('Natacion', f'{datos_nat["distancia_km"].sum():.1f} km',
                      f'{len(datos_nat)} sesiones')
        with col2:
            st.metric('Ciclismo', f'{datos_cic["distancia_km"].sum():.1f} km',
                      f'{len(datos_cic)} sesiones')
        with col3:
            st.metric('Carrera', f'{datos_car["distancia_km"].sum():.1f} km',
                      f'{len(datos_car)} sesiones')
        with col4:
            st.metric('Carga total', f'{registro["carga"].sum():.0f} TRIMP',
                      f'{len(registro)} sesiones')

        st.divider()

        # Grafica de distancia semanal
        st.subheader('Distancia semanal por disciplina')
        fig, axes = plt.subplots(1, 3, figsize=(14, 4))

        for i, disc in enumerate(['Natacion', 'Ciclismo', 'Carrera']):
            ax    = axes[i]
            datos = registro[registro['disciplina'] == disc]
            if datos.empty:
                ax.text(0.5, 0.5, 'Sin datos', ha='center', va='center')
                continue
            por_sem = datos.groupby('semana')['distancia_km'].sum().reset_index()
            barras  = ax.bar(por_sem['semana'].astype(str),
                             por_sem['distancia_km'],
                             color=COLORES[disc], alpha=0.85, width=0.6)
            for b, v in zip(barras, por_sem['distancia_km']):
                ax.text(b.get_x() + b.get_width()/2,
                        b.get_height() + 0.2,
                        f'{v:.1f}', ha='center', fontsize=9, fontweight='bold')
            ax.axhline(por_sem['distancia_km'].mean(), color='gray',
                       linestyle='--', alpha=0.6, linewidth=1)
            ax.set_title(disc, fontsize=11, fontweight='bold')
            ax.set_xlabel('Semana')
            ax.set_ylabel('km')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.divider()

        # Grafica de carga semanal
        st.subheader('Carga semanal (TRIMP)')
        por_sem_carga = registro.groupby(['semana','disciplina'])['carga'].sum().unstack(fill_value=0)
        semanas       = por_sem_carga.index.astype(str)

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        bottom    = np.zeros(len(semanas))
        for disc in ['Natacion','Ciclismo','Carrera','Fuerza']:
            if disc in por_sem_carga.columns:
                vals = por_sem_carga[disc].values
                ax2.bar(semanas, vals, bottom=bottom, label=disc,
                        color=COLORES[disc], alpha=0.85, width=0.6)
                bottom += vals
        for i, total in enumerate(bottom):
            ax2.text(i, total + 3, f'{total:.0f}',
                     ha='center', fontsize=10, fontweight='bold')
        ax2.axhline(300, color='orange', linestyle='--',
                    linewidth=1.5, alpha=0.7, label='Carga moderada')
        ax2.axhline(500, color='red', linestyle='--',
                    linewidth=1.5, alpha=0.7, label='Limite alto')
        ax2.set_ylabel('Carga TRIMP')
        ax2.legend(fontsize=9, loc='upper left')
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    # ── TAB 2: Historial ──
    with tab2:
        st.subheader('Historial de sesiones')

        disc_filtro = st.selectbox(
            'Filtrar por disciplina',
            options=['Todas','Natacion','Ciclismo','Carrera','Fuerza','Descanso']
        )

        df_mostrar = registro.copy()
        if disc_filtro != 'Todas':
            df_mostrar = df_mostrar[df_mostrar['disciplina'] == disc_filtro]

        df_mostrar = df_mostrar.sort_values('fecha', ascending=False)
        st.dataframe(
            df_mostrar[['fecha','disciplina','tipo_sesion',
                        'distancia_km','tiempo_min','fc_promedio',
                        'zona_fc','carga','notas']].reset_index(drop=True),
            use_container_width=True,
        )

    # ── TAB 3: Registrar sesion ──
    with tab3:
        st.subheader('Registrar nueva sesion')

        col_a, col_b = st.columns(2)

        with col_a:
            fecha       = st.date_input('Fecha', value=datetime.today())
            disciplina  = st.selectbox('Disciplina',
                          ['Natacion','Ciclismo','Carrera','Fuerza','Descanso'])
            tipo_sesion = st.selectbox('Tipo de sesion',
                          ['Tecnica','Fondo','Series','Umbral','Z2 suave',
                           'Recuperacion','Acondicionamiento','Descanso activo','Brick'])
            distancia   = st.number_input('Distancia (m)', min_value=0, value=2000)

        with col_b:
            tiempo      = st.number_input('Tiempo (min)', min_value=0, value=40)
            fc_promedio = st.slider('FC promedio (bpm)', 100, 200, 140)
            fc_maxima   = st.slider('FC maxima (bpm)', 110, 220, 165)
            cadencia    = st.number_input('Cadencia', min_value=0, value=0)

        notas = st.text_area('Notas', placeholder='Observaciones del entrenamiento...')

        if st.button('Guardar sesion', type='primary'):
            nueva = {
                'fecha'      : pd.Timestamp(fecha),
                'disciplina' : disciplina,
                'tipo_sesion': tipo_sesion,
                'distancia_m': distancia,
                'tiempo_min' : tiempo,
                'fc_promedio': fc_promedio,
                'fc_maxima'  : fc_maxima,
                'cadencia'   : cadencia,
                'notas'      : notas,
            }
            st.session_state.registro = pd.concat(
                [st.session_state.registro, pd.DataFrame([nueva])],
                ignore_index=True
            )
            st.session_state.registro = enriquecer_registro(st.session_state.registro)

            zona  = calcular_zona_fc(fc_promedio)
            carga = calcular_carga(tiempo, fc_promedio)

            if disciplina == 'Natacion':
                metrica = f'Pace: {calcular_pace_natacion(distancia, tiempo)} /100m'
            elif disciplina == 'Ciclismo':
                metrica = f'Velocidad: {calcular_velocidad_ciclismo(distancia, tiempo)} km/h'
            elif disciplina == 'Carrera':
                metrica = f'Pace: {calcular_pace_carrera(distancia, tiempo)} /km'
            else:
                metrica = f'Duracion: {tiempo} min'

            st.success(f'Sesion guardada — {metrica} | {zona} | Carga: {carga} TRIMP')

    # ── TAB 4: Recomendaciones IA ──
    with tab4:
        st.subheader('Recomendaciones IA')

        ultima_semana  = registro['semana'].max()
        carga_reciente = registro[registro['semana'] == ultima_semana]['carga'].sum()

        st.metric('Carga ultima semana', f'{carga_reciente:.0f} TRIMP')

        if carga_reciente > 500:
            st.error('Carga muy alta. Considera una semana de recuperacion.')
        elif carga_reciente < 150:
            st.warning('Carga baja. Puedes aumentar volumen o intensidad.')
        else:
            st.success('Carga en rango optimo. Mantiene la progresion actual.')

        st.divider()

        # Tendencias
        st.subheader('Tendencias por disciplina')
        for disc in ['Natacion', 'Ciclismo', 'Carrera']:
            datos = registro[
                (registro['disciplina'] == disc) &
                (registro['tipo_sesion'] != 'Brick')
            ].copy().sort_values('fecha')

            if len(datos) < 3:
                st.info(f'{disc}: se necesitan al menos 3 sesiones para analizar.')
                continue

            if disc == 'Natacion':
                datos['metrica'] = (datos['tiempo_min'] / datos['distancia_m']) * 100 * 60
                nombre   = 'Pace (seg/100m)'
                mejor_si = 'baja'
            elif disc == 'Ciclismo':
                datos['metrica'] = (datos['distancia_m'] / 1000) / (datos['tiempo_min'] / 60)
                nombre   = 'Velocidad (km/h)'
                mejor_si = 'sube'
            else:
                datos['metrica'] = (datos['tiempo_min'] / (datos['distancia_m'] / 1000)) * 60
                nombre   = 'Pace (seg/km)'
                mejor_si = 'baja'

            x    = np.arange(len(datos))
            y    = datos['metrica'].values
            m, b = np.polyfit(x, y, 1)

            if mejor_si == 'baja':
                estado = 'MEJORANDO' if m < -0.5 else ('EMPEORANDO' if m > 0.5 else 'ESTABLE')
            else:
                estado = 'MEJORANDO' if m > 0.1 else ('EMPEORANDO' if m < -0.1 else 'ESTABLE')

            if estado == 'MEJORANDO':
                st.success(f'{disc}: {estado} — {nombre}')
            elif estado == 'EMPEORANDO':
                st.error(f'{disc}: {estado} — {nombre}')
            else:
                st.info(f'{disc}: {estado} — {nombre}')

        st.divider()

        # Distribucion de zonas
        st.subheader('Distribucion de zonas FC')
        zonas   = registro['zona_fc'].value_counts(normalize=True) * 100
        pct_z2  = zonas.get('Z2 Base aerobica', 0)
        pct_alt = zonas.get('Z4 Umbral anaerobico', 0) + zonas.get('Z5 VO2 maximo', 0)

        col1, col2 = st.columns(2)
        with col1:
            st.metric('Z2 Base aerobica', f'{pct_z2:.0f}%', 'objetivo ~80%')
        with col2:
            st.metric('Z4-Z5 Intensidad', f'{pct_alt:.0f}%', 'objetivo ~20%')

        if pct_z2 < 50:
            st.warning('Poco trabajo de base aerobica. Agrega sesiones Z2.')
        elif pct_alt < 10:
            st.warning('Poca intensidad alta. Incluye series o umbrales.')
        else:
            st.success('Buena distribucion de zonas (modelo 80/20).')
