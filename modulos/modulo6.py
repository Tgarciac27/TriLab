# ============================================================
# TRIAI COACH - Streamlit
# modulos/modulo6.py - Fuerza, Calentamiento y Enfriamiento
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor']   = '#f8f8f8'
plt.rcParams['axes.spines.top']  = False
plt.rcParams['axes.spines.right']= False

COLORES = {
    'base'      : '#1D9E75',
    'volumen'   : '#378ADD',
    'intensidad': '#EF9F27',
    'tapering'  : '#888780',
    'fuerza'    : '#D4537E',
}

CALENTAMIENTO = {
    'Ciclismo': [
        {'ejercicio':'Pedaleo suave sin resistencia','duracion_seg':120,
         'descripcion':'Cadencia alta (90-100 rpm), resistencia minima'},
        {'ejercicio':'Rotaciones de cadera en el sitio','duracion_seg':30,
         'descripcion':'10 rotaciones por lado, amplitud maxima'},
        {'ejercicio':'Activacion de gluteos (sentadilla parcial)','duracion_seg':30,
         'descripcion':'15 repeticiones lentas, enfocate en activar el gluteo'},
        {'ejercicio':'Movilidad de tobillo','duracion_seg':30,
         'descripcion':'Circulos con el pie, 10 por lado'},
        {'ejercicio':'Pedaleo progresivo','duracion_seg':150,
         'descripcion':'Aumenta la resistencia gradualmente hasta ritmo de entreno'},
    ],
    'Natacion': [
        {'ejercicio':'Rotaciones de hombro hacia adelante','duracion_seg':30,
         'descripcion':'15 rotaciones por brazo, amplitud completa'},
        {'ejercicio':'Rotaciones de hombro hacia atras','duracion_seg':30,
         'descripcion':'15 rotaciones por brazo, amplitud completa'},
        {'ejercicio':'Apertura de pecho','duracion_seg':30,
         'descripcion':'Manos entrelazadas atras, mantiene 3 seg x 10 veces'},
        {'ejercicio':'Movilidad de cuello','duracion_seg':30,
         'descripcion':'Inclinaciones laterales y rotaciones suaves'},
        {'ejercicio':'Brazada en seco','duracion_seg':120,
         'descripcion':'Simula la brazada de pie, enfocate en la entrada del brazo'},
        {'ejercicio':'Series suaves en agua','duracion_seg':180,
         'descripcion':'2x50m muy suave, enfocate en la tecnica'},
    ],
    'Carrera': [
        {'ejercicio':'Trote suave','duracion_seg':120,
         'descripcion':'Ritmo muy suave, FC menor a 130 bpm'},
        {'ejercicio':'Skipping bajo','duracion_seg':30,
         'descripcion':'2x20m levantando apenas las rodillas, cadencia alta'},
        {'ejercicio':'Talones al gluteo','duracion_seg':30,
         'descripcion':'2x20m llevando el talon hacia el gluteo'},
        {'ejercicio':'Zancadas laterales','duracion_seg':30,
         'descripcion':'10 por lado, activa la cadera y los aductores'},
        {'ejercicio':'Progresion de ritmo','duracion_seg':180,
         'descripcion':'3x100m aumentando el ritmo hasta el pace de entreno'},
    ],
    'Fuerza': [
        {'ejercicio':'Movilidad articular general','duracion_seg':60,
         'descripcion':'Tobillos, rodillas, caderas, hombros — 10 circulos cada uno'},
        {'ejercicio':'Sentadilla con peso corporal','duracion_seg':45,
         'descripcion':'15 repeticiones lentas, activa el gluteo en la subida'},
        {'ejercicio':'Plank frontal','duracion_seg':30,
         'descripcion':'Mantiene 30 seg, core activado, no arqueyes la espalda'},
        {'ejercicio':'Rotaciones de tronco','duracion_seg':45,
         'descripcion':'10 rotaciones por lado, lento y controlado'},
        {'ejercicio':'Saltos suaves en el sitio','duracion_seg':60,
         'descripcion':'Activa el sistema nervioso, aterrizaje suave'},
        {'ejercicio':'Respiracion diafragmatica','duracion_seg':40,
         'descripcion':'5 respiraciones profundas, inhala 4 seg, exhala 6 seg'},
    ],
}

ENFRIAMIENTO = {
    'Ciclismo': [
        {'ejercicio':'Pedaleo muy suave sin resistencia','duracion_seg':120,
         'descripcion':'Cadencia libre, resistencia cero — baja la FC gradualmente'},
        {'ejercicio':'Estiramiento de cuadriceps de pie','duracion_seg':60,
         'descripcion':'30 seg por pierna, pie hacia el gluteo'},
        {'ejercicio':'Estiramiento de isquiotibiales','duracion_seg':60,
         'descripcion':'30 seg por pierna, pierna extendida sobre una superficie'},
        {'ejercicio':'Estiramiento de cadera (figura 4)','duracion_seg':60,
         'descripcion':'30 seg por lado, tumbado en el suelo'},
        {'ejercicio':'Postura del nino','duracion_seg':60,
         'descripcion':'Mantiene 60 seg, brazos extendidos al frente'},
        {'ejercicio':'Respiracion de recuperacion','duracion_seg':60,
         'descripcion':'5 respiraciones profundas, cierra los ojos'},
    ],
    'Natacion': [
        {'ejercicio':'Series de recuperacion','duracion_seg':120,
         'descripcion':'2x50m a ritmo muy suave, enfocate en la tecnica'},
        {'ejercicio':'Estiramiento de hombro cruzado','duracion_seg':60,
         'descripcion':'30 seg por brazo, lleva el brazo al pecho'},
        {'ejercicio':'Estiramiento de triceps','duracion_seg':60,
         'descripcion':'30 seg por brazo, brazo detras de la cabeza'},
        {'ejercicio':'Estiramiento de espalda','duracion_seg':40,
         'descripcion':'Abraza tus rodillas tumbado, rueda suavemente'},
        {'ejercicio':'Estiramiento de cuello','duracion_seg':60,
         'descripcion':'30 seg por lado, oreja hacia el hombro'},
        {'ejercicio':'Respiracion de recuperacion','duracion_seg':60,
         'descripcion':'5 respiraciones profundas, relaja los hombros'},
    ],
    'Carrera': [
        {'ejercicio':'Trote suave bajando a caminar','duracion_seg':120,
         'descripcion':'2 min de trote suave hasta detener completamente'},
        {'ejercicio':'Estiramiento de pantorrilla','duracion_seg':60,
         'descripcion':'30 seg por pierna, pie contra la pared'},
        {'ejercicio':'Estiramiento de cuadriceps','duracion_seg':60,
         'descripcion':'30 seg por pierna, de pie o tumbado'},
        {'ejercicio':'Estiramiento de isquiotibiales','duracion_seg':60,
         'descripcion':'30 seg por pierna, pierna extendida en el suelo'},
        {'ejercicio':'Estiramiento de cadera flexor','duracion_seg':60,
         'descripcion':'30 seg por lado, posicion de caballero'},
        {'ejercicio':'Respiracion de recuperacion','duracion_seg':60,
         'descripcion':'5 respiraciones profundas, manos en las rodillas'},
    ],
    'Fuerza': [
        {'ejercicio':'Caminata suave','duracion_seg':60,
         'descripcion':'1 min de caminata lenta para bajar la FC'},
        {'ejercicio':'Estiramiento de gluteo (figura 4)','duracion_seg':60,
         'descripcion':'30 seg por lado — Lunes'},
        {'ejercicio':'Estiramiento de cuadriceps','duracion_seg':60,
         'descripcion':'30 seg por pierna — Lunes'},
        {'ejercicio':'Estiramiento de hombro cruzado','duracion_seg':60,
         'descripcion':'30 seg por brazo — Jueves'},
        {'ejercicio':'Gato-vaca','duracion_seg':60,
         'descripcion':'10 repeticiones lentas en cuatro puntos — Jueves'},
        {'ejercicio':'Postura del nino extendida','duracion_seg':60,
         'descripcion':'60 seg, brazos extendidos al frente, respira profundo'},
        {'ejercicio':'Respiracion de recuperacion','duracion_seg':60,
         'descripcion':'5 respiraciones profundas tumbado boca arriba'},
    ],
}

RUTINAS_FUERZA = {
    'Lunes': {
        'grupos': 'Gluteos + Cuadriceps y Pantorrillas',
        'descripcion': 'Potencia para ciclismo y carrera',
        'bloques': [
            {'nombre':'Bloque 1 — Activacion de gluteo','ejercicios':[
                {'nombre':'Hip thrust con peso corporal',
                 'descripcion':'Tumbado, empuja las caderas hacia arriba. Aprieta el gluteo arriba.',
                 'musculo':'Gluteo mayor'},
                {'nombre':'Clamshell con banda elastica',
                 'descripcion':'De lado, abre y cierra la rodilla como almeja.',
                 'musculo':'Gluteo medio'},
            ]},
            {'nombre':'Bloque 2 — Fuerza de piernas','ejercicios':[
                {'nombre':'Sentadilla bulgara (split squat)',
                 'descripcion':'Pie trasero elevado, baja controlado. Rodilla no pasa el pie.',
                 'musculo':'Cuadriceps y gluteo'},
                {'nombre':'Peso muerto rumano a una pierna',
                 'descripcion':'Inclina el tronco con espalda recta. Siente el isquiotibial.',
                 'musculo':'Isquiotibiales y gluteo'},
            ]},
            {'nombre':'Bloque 3 — Potencia de piernas','ejercicios':[
                {'nombre':'Saltos al cajon (box jump)',
                 'descripcion':'Salta con ambos pies, aterriza suave. Simula la pedalada explosiva.',
                 'musculo':'Cuadriceps, gluteo y pantorrilla'},
                {'nombre':'Zancadas con mancuernas',
                 'descripcion':'Paso largo, rodilla trasera casi toca el suelo.',
                 'musculo':'Cuadriceps y gluteo'},
            ]},
            {'nombre':'Bloque 4 — Pantorrillas y tobillo','ejercicios':[
                {'nombre':'Elevacion de pantorrilla de pie',
                 'descripcion':'Sube en dos tiempos, baja en cuatro. Maximo recorrido.',
                 'musculo':'Gastrocnemio y soleo'},
                {'nombre':'Saltos en punta de pie',
                 'descripcion':'Saltos rapidos y bajos, solo mueve el tobillo.',
                 'musculo':'Pantorrilla y tobillo'},
            ]},
            {'nombre':'Bloque 5 — Estabilidad de rodilla y cadera','ejercicios':[
                {'nombre':'Monster walk con banda elastica',
                 'descripcion':'Pasos laterales con banda en los tobillos, rodillas semiflexionadas.',
                 'musculo':'Gluteo medio y estabilizadores de rodilla'},
                {'nombre':'Step up con rodilla elevada',
                 'descripcion':'Sube al cajon y eleva la rodilla al frente. Baja controlado.',
                 'musculo':'Cuadriceps, gluteo y equilibrio'},
            ]},
        ],
    },
    'Jueves': {
        'grupos': 'Core + Hombros y Espalda',
        'descripcion': 'Estabilidad para las 3 disciplinas y fuerza de brazada',
        'bloques': [
            {'nombre':'Bloque 1 — Activacion de core','ejercicios':[
                {'nombre':'Dead bug',
                 'descripcion':'Tumbado, baja brazo y pierna contraria sin arquear la espalda.',
                 'musculo':'Core profundo y transverso abdominal'},
                {'nombre':'Pallof press con banda',
                 'descripcion':'Empuja la banda al frente sin rotar el tronco.',
                 'musculo':'Core lateral y oblicuos'},
            ]},
            {'nombre':'Bloque 2 — Core dinamico','ejercicios':[
                {'nombre':'Plank con toque de hombro',
                 'descripcion':'En plank, toca el hombro contrario sin mover las caderas.',
                 'musculo':'Core, hombros y estabilidad'},
                {'nombre':'Russian twist con peso',
                 'descripcion':'Rota el tronco de lado a lado. Pies levantados para mas dificultad.',
                 'musculo':'Oblicuos y core rotacional'},
            ]},
            {'nombre':'Bloque 3 — Espalda alta y remo','ejercicios':[
                {'nombre':'Remo con mancuerna a una mano',
                 'descripcion':'Codo cerca del cuerpo, lleva la mancuerna a la cadera.',
                 'musculo':'Dorsal y romboides'},
                {'nombre':'Face pull con banda elastica',
                 'descripcion':'Jala la banda hacia la cara, codos a la altura de los hombros.',
                 'musculo':'Deltoides posterior y manguito rotador'},
            ]},
            {'nombre':'Bloque 4 — Hombros funcionales','ejercicios':[
                {'nombre':'Press de hombro con mancuernas',
                 'descripcion':'Empuja hacia arriba sin bloquear los codos. Espalda neutra.',
                 'musculo':'Deltoides anterior y medio'},
                {'nombre':'Elevacion lateral con banda',
                 'descripcion':'Levanta los brazos hasta la altura del hombro, lento y controlado.',
                 'musculo':'Deltoides medio'},
            ]},
            {'nombre':'Bloque 5 — Cadena posterior superior','ejercicios':[
                {'nombre':'Superman en el suelo',
                 'descripcion':'Tumbado boca abajo, levanta brazos y piernas. Mantiene 2 seg.',
                 'musculo':'Espalda baja, gluteo y espalda alta'},
                {'nombre':'Remo invertido en barra o anillas',
                 'descripcion':'Cuerpo recto, jala el pecho hacia la barra.',
                 'musculo':'Espalda, biceps y core'},
            ]},
        ],
    },
}

CONFIG_SEMANA = {
    'base'      : {'series':3,'reps':15,'descanso_seg':45,
                   'descripcion':'Fuerza resistencia — mas reps, menos peso'},
    'volumen'   : {'series':3,'reps':12,'descanso_seg':60,
                   'descripcion':'Fuerza funcional — peso moderado, movimientos compuestos'},
    'intensidad': {'series':4,'reps':8, 'descanso_seg':90,
                   'descripcion':'Potencia — menos reps, mas explosividad'},
    'tapering'  : {'series':2,'reps':10,'descanso_seg':30,
                   'descripcion':'Activacion suave — sin fatiga, llegar fresco a competir'},
}


def cargar_historial_ejemplo():
    df = pd.DataFrame([
        {'fecha':'2025-04-14','dia':'Lunes','tipo_semana':'base',
         'completado':True,'rpe':7,'notas':'Gluteos bien activados'},
        {'fecha':'2025-04-17','dia':'Jueves','tipo_semana':'base',
         'completado':True,'rpe':6,'notas':'Core bien'},
        {'fecha':'2025-04-21','dia':'Lunes','tipo_semana':'volumen',
         'completado':True,'rpe':8,'notas':'Sentadilla bulgara exigente'},
        {'fecha':'2025-04-24','dia':'Jueves','tipo_semana':'volumen',
         'completado':True,'rpe':7,'notas':''},
        {'fecha':'2025-04-28','dia':'Lunes','tipo_semana':'intensidad',
         'completado':True,'rpe':9,'notas':'Box jump muy intenso'},
        {'fecha':'2025-05-01','dia':'Jueves','tipo_semana':'intensidad',
         'completado':True,'rpe':8,'notas':'Remo invertido muy bien'},
        {'fecha':'2025-05-05','dia':'Lunes','tipo_semana':'tapering',
         'completado':True,'rpe':5,'notas':'Sesion suave'},
        {'fecha':'2025-05-08','dia':'Jueves','tipo_semana':'tapering',
         'completado':True,'rpe':4,'notas':'Activacion perfecta'},
    ])
    df['fecha'] = pd.to_datetime(df['fecha'])
    return df


def mostrar():
    st.title('💪 Fuerza, Calentamiento y Enfriamiento')

    if 'historial_fuerza' not in st.session_state:
        st.session_state.historial_fuerza = cargar_historial_ejemplo()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        '🔥 Calentamiento',
        '💪 Rutina de fuerza',
        '❄️ Enfriamiento',
        '📋 Registro',
        '🤖 Recomendaciones IA',
    ])

    # ── TAB 1: Calentamiento ──
    with tab1:
        st.subheader('Rutina de calentamiento')

        disc_cal = st.selectbox('Disciplina del dia',
                   ['Ciclismo','Natacion','Carrera','Fuerza'])

        ejercicios = CALENTAMIENTO[disc_cal]
        total_seg  = sum(e['duracion_seg'] for e in ejercicios)

        st.metric('Duracion total', f'{total_seg//60}:{total_seg%60:02d}',
                  f'{len(ejercicios)} ejercicios')
        st.divider()

        acum = 0
        for i, e in enumerate(ejercicios, 1):
            acum += e['duracion_seg']
            mins = e['duracion_seg'] // 60
            segs = e['duracion_seg'] % 60
            tiempo_str = f'{mins}:{segs:02d}' if mins > 0 else f'{segs}s'

            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.markdown(f'**{i}. {e["ejercicio"]}**')
                st.caption(e['descripcion'])
            with col2:
                st.metric('Tiempo', tiempo_str)
            with col3:
                st.metric('Acumulado', f'{acum}s')
            st.divider()

    # ── TAB 2: Rutina de fuerza ──
    with tab2:
        st.subheader('Rutina de fuerza')

        col_a, col_b = st.columns(2)
        with col_a:
            dia_fuerza = st.selectbox('Dia', ['Lunes','Jueves'])
        with col_b:
            tipo_semana = st.selectbox('Tipo de semana',
                          ['base','volumen','intensidad','tapering'])

        rutina = RUTINAS_FUERZA[dia_fuerza]
        config = CONFIG_SEMANA[tipo_semana]

        st.info(f'**{rutina["grupos"]}** — {rutina["descripcion"]}')
        st.caption(f'{config["descripcion"]} | '
                   f'{config["series"]} series x {config["reps"]} reps | '
                   f'Descanso: {config["descanso_seg"]}s')
        st.divider()

        for bloque in rutina['bloques']:
            with st.expander(f'**{bloque["nombre"]}**'):
                for ej in bloque['ejercicios']:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f'**{ej["nombre"]}**')
                        st.caption(f'Musculo: {ej["musculo"]}')
                        st.write(ej['descripcion'])
                    with col2:
                        st.metric('Series', f'{config["series"]}x{config["reps"]}')
                        st.caption(f'Desc: {config["descanso_seg"]}s')
                    st.divider()

    # ── TAB 3: Enfriamiento ──
    with tab3:
        st.subheader('Rutina de enfriamiento')

        disc_enf = st.selectbox('Disciplina del dia ',
                   ['Ciclismo','Natacion','Carrera','Fuerza'])

        ejercicios_enf = ENFRIAMIENTO[disc_enf]
        total_enf      = sum(e['duracion_seg'] for e in ejercicios_enf)

        st.metric('Duracion total', f'{total_enf//60}:{total_enf%60:02d}',
                  f'{len(ejercicios_enf)} ejercicios')
        st.divider()

        for i, e in enumerate(ejercicios_enf, 1):
            mins = e['duracion_seg'] // 60
            segs = e['duracion_seg'] % 60
            tiempo_str = f'{mins}:{segs:02d}' if mins > 0 else f'{segs}s'

            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f'**{i}. {e["ejercicio"]}**')
                st.caption(e['descripcion'])
            with col2:
                st.metric('Tiempo', tiempo_str)
            st.divider()

    # ── TAB 4: Registro ──
    with tab4:
        st.subheader('Registrar sesion de fuerza')

        col_a, col_b = st.columns(2)
        with col_a:
            fecha_f      = st.date_input('Fecha', value=datetime.today())
            dia_reg      = st.selectbox('Dia ', ['Lunes','Jueves'])
            tipo_reg     = st.selectbox('Tipo de semana ',
                           ['base','volumen','intensidad','tapering'])
            completado_f = st.checkbox('Sesion completada', value=True)
        with col_b:
            rpe_f   = st.slider('RPE (esfuerzo percibido 1-10)',
                                min_value=1, max_value=10, value=7)
            notas_f = st.text_area('Notas ',
                                   placeholder='Como te sentiste, que ejercicio fue mas dificil...')

        rpe_color = {
            range(1, 6) : 'OK — Carga baja',
            range(6, 9) : 'OK — Carga optima',
            range(9, 11): 'ALTO — Asegurate de descansar bien',
        }
        estado_rpe = next((v for k, v in rpe_color.items() if rpe_f in k), '')
        st.caption(f'RPE {rpe_f}/10 — {estado_rpe}')

        if st.button('Guardar sesion de fuerza', type='primary'):
            nueva = {
                'fecha'      : pd.Timestamp(fecha_f),
                'dia'        : dia_reg,
                'tipo_semana': tipo_reg,
                'completado' : completado_f,
                'rpe'        : rpe_f,
                'notas'      : notas_f,
            }
            st.session_state.historial_fuerza = pd.concat(
                [st.session_state.historial_fuerza, pd.DataFrame([nueva])],
                ignore_index=True
            )
            if rpe_f <= 7:
                st.success(f'Sesion guardada — RPE {rpe_f}/10 | Carga optima')
            else:
                st.warning(f'Sesion guardada — RPE {rpe_f}/10 | Carga alta')

        st.divider()
        st.subheader('Historial de sesiones')
        historial = st.session_state.historial_fuerza
        st.dataframe(
            historial[['fecha','dia','tipo_semana','rpe','notas']
                     ].sort_values('fecha', ascending=False).reset_index(drop=True),
            use_container_width=True,
        )

        if len(historial) >= 2:
            st.subheader('RPE por sesion')
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            for i, dia in enumerate(['Lunes','Jueves']):
                ax   = axes[i]
                datos = historial[historial['dia'] == dia]
                if datos.empty:
                    ax.text(0.5, 0.5, f'Sin datos para {dia}',
                            ha='center', va='center')
                    continue
                fechas  = datos['fecha'].dt.strftime('%d/%m')
                rpes    = datos['rpe'].values
                colores = ['#1D9E75' if r <= 7 else '#EF9F27' if r <= 8 else '#D85A30'
                           for r in rpes]
                barras  = ax.bar(fechas, rpes, color=colores, alpha=0.85, width=0.6)
                for b, v in zip(barras, rpes):
                    ax.text(b.get_x() + b.get_width()/2,
                            b.get_height() + 0.1,
                            str(v), ha='center', fontsize=10, fontweight='bold')
                ax.axhline(7, color='gray', linestyle='--',
                           linewidth=1, alpha=0.6, label='RPE optimo (7)')
                rutina_dia = RUTINAS_FUERZA[dia]
                ax.set_title(f'{dia} — {rutina_dia["grupos"]}', fontsize=10, fontweight='bold')
                ax.set_ylabel('RPE (1-10)')
                ax.set_ylim(0, 11)
                ax.legend(fontsize=8)
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=15)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

    # ── TAB 5: Recomendaciones IA ──
    with tab5:
        st.subheader('Recomendaciones IA — Fuerza')

        historial = st.session_state.historial_fuerza
        if historial.empty:
            st.info('Sin datos. Registra tu primera sesion para ver recomendaciones.')
            return

        pct_comp  = historial['completado'].mean() * 100
        rpe_prom  = historial['rpe'].mean()
        rpe_lunes = historial[historial['dia']=='Lunes']['rpe'].mean()
        rpe_jueves= historial[historial['dia']=='Jueves']['rpe'].mean()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Sesiones completadas', f'{pct_comp:.0f}%')
        with col2:
            st.metric('RPE promedio general', f'{rpe_prom:.1f}/10')
        with col3:
            st.metric('Sesiones registradas', len(historial))

        st.divider()

        if pct_comp < 75:
            st.error('Baja consistencia. La fuerza requiere regularidad. '
                     'Intenta no saltarte mas de 1 sesion por semana.')
        else:
            st.success('Buena consistencia en las sesiones de fuerza.')

        if rpe_prom > 8.5:
            st.warning('Esfuerzo muy alto de forma sostenida. '
                       'Reduce el peso o las series para evitar sobreentrenamiento.')
        elif rpe_prom < 5:
            st.warning('Esfuerzo muy bajo. Aumenta la carga progresivamente.')
        else:
            st.success('Esfuerzo dentro del rango adecuado.')

        if not (pd.isna(rpe_lunes) or pd.isna(rpe_jueves)):
            col1, col2 = st.columns(2)
            with col1:
                st.metric('RPE Lunes (gluteos/piernas)', f'{rpe_lunes:.1f}')
            with col2:
                st.metric('RPE Jueves (core/hombros)', f'{rpe_jueves:.1f}')

            if abs(rpe_lunes - rpe_jueves) > 2:
                dia_alto = 'Lunes' if rpe_lunes > rpe_jueves else 'Jueves'
                st.warning(f'Diferencia alta entre dias — el {dia_alto} es mas exigente. '
                           f'Revisa que la carga este bien distribuida.')

        if len(historial) >= 4:
            x    = np.arange(len(historial))
            y    = historial['rpe'].values
            m, _ = np.polyfit(x, y, 1)
            st.divider()
            st.subheader('Tendencia de esfuerzo')
            if m > 0.3:
                st.error(f'El esfuerzo sube {m:.2f} RPE por sesion. '
                         f'Planifica una semana de descarga pronto.')
            elif m < -0.3:
                st.success(f'El esfuerzo baja {abs(m):.2f} RPE por sesion — '
                           f'el cuerpo se adapta bien.')
            else:
                st.info('Carga estable a lo largo de las sesiones.')

        st.divider()
        st.subheader('Consejos generales')
        consejos = [
            'Nunca hagas fuerza de piernas el dia antes de una carrera larga',
            'El dolor muscular (agujetas) es normal los primeros dias',
            'Aumenta la carga maximo un 10% por semana',
            'El calentamiento y enfriamiento son parte de la sesion, no opcionales',
            'Hidratate bien — la fuerza tambien genera sudoracion significativa',
        ]
        for c in consejos:
            st.write(f'• {c}')
