# ============================================================
# TRIAI COACH - Streamlit
# modulos/modulo5.py - Biomecanica y Analisis de Video
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
import os
import tempfile
from datetime import datetime

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor']   = '#f8f8f8'
plt.rcParams['axes.spines.top']  = False
plt.rcParams['axes.spines.right']= False

COLORES = {
    'ok'      : '#1D9E75',
    'advertir': '#EF9F27',
    'error'   : '#D85A30',
    'neutro'  : '#888780',
}

PUNTOS = {
    'nariz':0,'ojo_izq':1,'ojo_der':2,'oreja_izq':3,'oreja_der':4,
    'hombro_izq':5,'hombro_der':6,'codo_izq':7,'codo_der':8,
    'muneca_izq':9,'muneca_der':10,'cadera_izq':11,'cadera_der':12,
    'rodilla_izq':13,'rodilla_der':14,'tobillo_izq':15,'tobillo_der':16,
}

RANGOS = {
    'Ciclismo': {
        'rodilla_extension': {
            'min_ok':140,'max_ok':150,'ideal':145,
            'error_bajo':'Rodilla demasiado flexionada — sillon muy bajo',
            'error_alto':'Rodilla sobreextendida — sillon muy alto',
            'correccion_bajo':'Sube el sillon 0.5-1cm y vuelve a analizar',
            'correccion_alto':'Baja el sillon 0.5-1cm y vuelve a analizar',
        },
        'inclinacion_tronco': {
            'min_ok':35,'max_ok':55,'ideal':45,
            'error_bajo':'Tronco demasiado vertical — posicion poco aerodinamica',
            'error_alto':'Tronco demasiado horizontal — puede causar dolor lumbar',
            'correccion_bajo':'Inclina el tronco hacia adelante, ajusta el manubrio',
            'correccion_alto':'Levanta el manubrio o acorta el potenciometro',
        },
        'angulo_codo': {
            'min_ok':150,'max_ok':165,'ideal':158,
            'error_bajo':'Codos muy flexionados — tension en hombros',
            'error_alto':'Brazos completamente extendidos — menos absorcion',
            'correccion_bajo':'Relaja los brazos sobre el manubrio',
            'correccion_alto':'Flexiona levemente los codos',
        },
    },
    'Carrera': {
        'inclinacion_tronco': {
            'min_ok':5,'max_ok':15,'ideal':10,
            'error_bajo':'Tronco muy vertical — falta inclinacion hacia adelante',
            'error_alto':'Tronco demasiado inclinado — sobrecarga lumbar',
            'correccion_bajo':'Inclina levemente el tronco desde los tobillos',
            'correccion_alto':'Activa el core y reduce la inclinacion',
        },
        'angulo_rodilla': {
            'min_ok':160,'max_ok':175,'ideal':168,
            'error_bajo':'Rodilla muy flexionada al impactar — frenado excesivo',
            'error_alto':'Rodilla casi recta — riesgo de lesion',
            'correccion_bajo':'Aumenta la cadencia y acorta la zancada',
            'correccion_alto':'Aterriza con el pie bajo el centro de gravedad',
        },
        'angulo_brazo': {
            'min_ok':85,'max_ok':100,'ideal':90,
            'error_bajo':'Brazos muy cerrados — limitan la respiracion',
            'error_alto':'Brazos muy abiertos — gasto energetico extra',
            'correccion_bajo':'Abre los codos a 90 grados, relaja hombros',
            'correccion_alto':'Cierra los codos hacia el cuerpo',
        },
    },
    'Natacion': {
        'entrada_brazo': {
            'min_ok':170,'max_ok':185,'ideal':178,
            'error_bajo':'Brazo entra demasiado cruzado — reduce propulsion',
            'error_alto':'Brazo entra muy abierto — mas resistencia',
            'correccion_bajo':'Entra el brazo en linea con el hombro',
            'correccion_alto':'Cierra la entrada hacia la linea central',
        },
        'rotacion_tronco': {
            'min_ok':40,'max_ok':60,'ideal':50,
            'error_bajo':'Poca rotacion — limita la amplitud de brazada',
            'error_alto':'Demasiada rotacion — pierde estabilidad',
            'correccion_bajo':'Rota mas el tronco al tirar del brazo atras',
            'correccion_alto':'Reduce la rotacion, caderas mas planas',
        },
        'posicion_cadera': {
            'min_ok':170,'max_ok':185,'ideal':178,
            'error_bajo':'Caderas hundidas — mas resistencia del agua',
            'error_alto':'Caderas muy elevadas — inestabilidad',
            'correccion_bajo':'Presiona el pecho abajo para elevar caderas',
            'correccion_alto':'Relaja la patada y mantien el cuerpo horizontal',
        },
    },
}


# ── Funciones de calculo ──

def calcular_angulo(a, b, c):
    if a is None or b is None or c is None:
        return None
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc  = a - b, c - b
    coseno  = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return round(math.degrees(math.acos(np.clip(coseno, -1.0, 1.0))), 1)


def evaluar_angulo(nombre, angulo, rango):
    if rango['min_ok'] <= angulo <= rango['max_ok']:
        return {'nombre':nombre,'angulo':angulo,'ideal':rango['ideal'],
                'estado':'ok','mensaje':'Dentro del rango optimo',
                'correccion':'Mantiene esta posicion'}
    elif angulo < rango['min_ok']:
        dif    = round(rango['min_ok'] - angulo, 1)
        estado = 'advertir' if dif <= 10 else 'error'
        return {'nombre':nombre,'angulo':angulo,'ideal':rango['ideal'],
                'estado':estado,'mensaje':rango['error_bajo'],
                'correccion':rango['correccion_bajo']}
    else:
        dif    = round(angulo - rango['max_ok'], 1)
        estado = 'advertir' if dif <= 10 else 'error'
        return {'nombre':nombre,'angulo':angulo,'ideal':rango['ideal'],
                'estado':estado,'mensaje':rango['error_alto'],
                'correccion':rango['correccion_alto']}


def analizar_video_movenet(ruta_video, disciplina, max_segundos=15):
    """
    Analiza el video con MoveNet de TensorFlow.
    Retorna los promedios de angulos y el acumulador por frame.
    """
    try:
        import tensorflow as tf
        import tensorflow_hub as hub

        # Cargamos el modelo (se cachea despues de la primera vez)
        if 'movenet_model' not in st.session_state:
            with st.spinner('Cargando modelo MoveNet... (solo la primera vez)'):
                modelo = hub.load(
                    'https://tfhub.dev/google/movenet/singlepose/lightning/4'
                )
                st.session_state.movenet_model = modelo.signatures['serving_default']

        movenet_fn = st.session_state.movenet_model

    except Exception as e:
        st.error(f'Error cargando MoveNet: {e}')
        return None

    cap = cv2.VideoCapture(ruta_video)
    if not cap.isOpened():
        st.error('No se pudo abrir el video.')
        return None

    fps        = cap.get(cv2.CAP_PROP_FPS)
    ancho      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto       = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    max_frames = int(fps * max_segundos)

    acumulador = {}
    frames_ok  = 0
    frame_num  = 0
    progreso   = st.progress(0, text='Procesando video...')

    while cap.isOpened() and frame_num < max_frames:
        ok, frame = cap.read()
        if not ok:
            break

        frame_num += 1
        frame_rgb  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        try:
            import tensorflow as tf
            img = tf.image.resize_with_pad(
                tf.expand_dims(frame_rgb, axis=0), 192, 192
            )
            img       = tf.cast(img, dtype=tf.int32)
            resultado = movenet_fn(img)
            keypoints = resultado['output_0'].numpy()[0][0]

            def p(nombre):
                idx        = PUNTOS[nombre]
                y_n, x_n, conf = keypoints[idx]
                if conf < 0.3: return None
                return (int(x_n * ancho), int(y_n * alto))

            angulos = {}
            if disciplina == 'Ciclismo':
                val = calcular_angulo(p('cadera_izq'), p('rodilla_izq'), p('tobillo_izq'))
                if val: angulos['rodilla_extension'] = val
                cadera = p('cadera_izq')
                hombro = p('hombro_izq')
                if cadera and hombro:
                    ref = (cadera[0], cadera[1] - 100)
                    val = calcular_angulo(hombro, cadera, ref)
                    if val: angulos['inclinacion_tronco'] = val
                val = calcular_angulo(p('hombro_izq'), p('codo_izq'), p('muneca_izq'))
                if val: angulos['angulo_codo'] = val

            elif disciplina == 'Carrera':
                cadera = p('cadera_izq')
                hombro = p('hombro_izq')
                if cadera and hombro:
                    ref = (cadera[0], cadera[1] - 100)
                    val = calcular_angulo(hombro, cadera, ref)
                    if val: angulos['inclinacion_tronco'] = val
                val = calcular_angulo(p('cadera_izq'), p('rodilla_izq'), p('tobillo_izq'))
                if val: angulos['angulo_rodilla'] = val
                val = calcular_angulo(p('hombro_izq'), p('codo_izq'), p('muneca_izq'))
                if val: angulos['angulo_brazo'] = val

            elif disciplina == 'Natacion':
                val = calcular_angulo(p('hombro_izq'), p('codo_izq'), p('muneca_izq'))
                if val: angulos['entrada_brazo'] = val
                val = calcular_angulo(p('hombro_izq'), p('cadera_izq'), p('hombro_der'))
                if val: angulos['rotacion_tronco'] = val
                val = calcular_angulo(p('hombro_izq'), p('cadera_izq'), p('tobillo_izq'))
                if val: angulos['posicion_cadera'] = val

            if angulos:
                frames_ok += 1
                for nombre, valor in angulos.items():
                    if nombre not in acumulador:
                        acumulador[nombre] = []
                    acumulador[nombre].append(valor)

        except Exception:
            pass

        progreso.progress(
            min(frame_num / max_frames, 1.0),
            text=f'Frame {frame_num}/{max_frames} procesado...'
        )

    cap.release()
    progreso.empty()

    if frames_ok == 0:
        st.error('No se detectaron poses en el video. '
                 'Asegurate de que el atleta sea visible de cuerpo completo.')
        return None

    promedios = {n: round(np.mean(v), 1) for n, v in acumulador.items()}
    st.success(f'OK — {frames_ok}/{frame_num} frames analizados')
    return promedios, acumulador


def mostrar():
    st.title('🔬 Biomecanica y Analisis de Tecnica')

    if 'historial_bio' not in st.session_state:
        st.session_state.historial_bio = pd.DataFrame(columns=[
            'fecha','disciplina','angulo','valor','ideal','estado'
        ])

    tab1, tab2, tab3 = st.tabs([
        '🎥 Analizar video',
        '📊 Progreso',
        '🤖 Recomendaciones IA',
    ])

    # ── TAB 1: Analizar video ──
    with tab1:
        st.subheader('Analisis biomecanico en video')

        st.info('''
        **Recomendaciones para el video:**
        - Maximo 15 segundos (mp4, avi o mov)
        - Atleta visible de cabeza a pies
        - Grabar de perfil (lado izquierdo preferible)
        - Buena iluminacion, sin contraluz
        - Fondo despejado, sin otras personas
        ''')

        disciplina = st.selectbox('Disciplina',
                     ['Ciclismo', 'Carrera', 'Natacion'])

        video_file = st.file_uploader(
            'Sube tu video (mp4, avi, mov)',
            type=['mp4', 'avi', 'mov']
        )

        if video_file and st.button('Analizar video', type='primary'):
            # Guardamos el video en un archivo temporal
            with tempfile.NamedTemporaryFile(
                delete=False, suffix='.mp4'
            ) as tmp:
                tmp.write(video_file.read())
                tmp_path = tmp.name

            resultado = analizar_video_movenet(tmp_path, disciplina)
            os.unlink(tmp_path)

            if resultado:
                promedios, acumulador = resultado

                st.divider()
                st.subheader('Angulos promedio del video')

                rangos_disc = RANGOS[disciplina]
                resultados  = []

                for nombre, valor in promedios.items():
                    if nombre in rangos_disc:
                        r = evaluar_angulo(nombre, valor, rangos_disc[nombre])
                        resultados.append(r)

                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f'**{nombre}**')
                            st.caption(r['mensaje'])
                        with col2:
                            st.metric('Medido', f'{valor}°')
                        with col3:
                            st.metric('Ideal', f'{r["ideal"]}°')

                        if r['estado'] == 'ok':
                            st.success(f'OK — {r["correccion"]}')
                        elif r['estado'] == 'advertir':
                            st.warning(f'ADVERTENCIA — {r["correccion"]}')
                        else:
                            st.error(f'ERROR — {r["correccion"]}')
                        st.divider()

                # Guardamos en historial
                for r in resultados:
                    st.session_state.historial_bio = pd.concat([
                        st.session_state.historial_bio,
                        pd.DataFrame([{
                            'fecha'     : pd.Timestamp(datetime.today().date()),
                            'disciplina': disciplina,
                            'angulo'    : r['nombre'],
                            'valor'     : r['angulo'],
                            'ideal'     : r['ideal'],
                            'estado'    : r['estado'],
                        }])
                    ], ignore_index=True)

                # Grafica de evolucion por frame
                st.subheader('Evolucion de angulos durante el video')
                rangos_disc = RANGOS[disciplina]
                n = len(acumulador)

                fig, axes = plt.subplots(n, 1,
                                         figsize=(12, 4*n),
                                         squeeze=False)

                for i, (nombre, valores) in enumerate(acumulador.items()):
                    ax    = axes[i][0]
                    rango = rangos_disc.get(nombre, {})
                    x     = range(len(valores))

                    ax.plot(x, valores, linewidth=1.5,
                            color='#7F77DD', alpha=0.8, label='Angulo por frame')
                    promedio = np.mean(valores)
                    ax.axhline(promedio, color='#378ADD', linestyle='-',
                               linewidth=2, label=f'Promedio: {promedio:.1f}°')

                    if rango:
                        ax.fill_between(x, rango['min_ok'], rango['max_ok'],
                                        alpha=0.12, color='#1D9E75',
                                        label=f'Rango optimo ({rango["min_ok"]}-{rango["max_ok"]}°)')
                        ax.axhline(rango['ideal'], color='#1D9E75',
                                   linestyle='-', linewidth=1, alpha=0.5,
                                   label=f'Ideal: {rango["ideal"]}°')

                    ax.set_title(nombre, fontsize=11, fontweight='500')
                    ax.set_xlabel('Frame')
                    ax.set_ylabel('Angulo (grados)')
                    ax.legend(fontsize=8, loc='upper right')

                plt.tight_layout()
                st.pyplot(fig)
                plt.close()

    # ── TAB 2: Progreso ──
    with tab2:
        st.subheader('Progreso biomecanico por sesion')

        historial = st.session_state.historial_bio
        if historial.empty:
            st.info('Sin datos aun. Analiza un video para comenzar.')
            return

        disc_sel = st.selectbox('Disciplina ',
                   ['Ciclismo','Carrera','Natacion'])
        datos_disc = historial[historial['disciplina'] == disc_sel]

        if datos_disc.empty:
            st.info(f'Sin datos para {disc_sel}.')
            return

        angulos_disp = datos_disc['angulo'].unique().tolist()
        angulo_sel   = st.selectbox('Angulo a graficar', angulos_disp)

        datos_ang = datos_disc[datos_disc['angulo'] == angulo_sel]
        if len(datos_ang) < 2:
            st.info('Se necesitan al menos 2 sesiones para graficar el progreso.')
            st.dataframe(datos_ang[['fecha','valor','ideal','estado']],
                         use_container_width=True)
            return

        rango  = RANGOS[disc_sel].get(angulo_sel, {})
        fechas = datos_ang['fecha'].dt.strftime('%d/%m')
        vals   = datos_ang['valor'].values
        col_estado = {'ok':COLORES['ok'],'advertir':COLORES['advertir'],
                      'error':COLORES['error']}
        colores = [col_estado.get(e, '#888780') for e in datos_ang['estado'].values]

        fig, ax = plt.subplots(figsize=(9, 4))
        ax.plot(fechas, vals, 'o-', color='#7F77DD',
                linewidth=2, markersize=8, zorder=3)
        for i, (f, v, c) in enumerate(zip(fechas, vals, colores)):
            ax.scatter(f, v, color=c, s=90, zorder=4)
            ax.annotate(f'{v}°', (f, v),
                        textcoords='offset points',
                        xytext=(0,12), ha='center', fontsize=10)
        if rango:
            ax.fill_between(range(len(fechas)),
                            rango['min_ok'], rango['max_ok'],
                            alpha=0.12, color='#1D9E75',
                            label='Rango optimo')
            ax.axhline(rango['ideal'], color='#1D9E75',
                       linestyle='--', linewidth=1,
                       label=f'Ideal: {rango["ideal"]}°')
        ax.set_ylabel('Angulo (grados)')
        ax.set_xlabel('Fecha')
        ax.legend(fontsize=9)
        ax.set_title(f'{disc_sel} — {angulo_sel}', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.dataframe(
            datos_ang[['fecha','valor','ideal','estado']
                     ].sort_values('fecha', ascending=False).reset_index(drop=True),
            use_container_width=True,
        )

    # ── TAB 3: Recomendaciones IA ──
    with tab3:
        st.subheader('Recomendaciones IA — Biomecanica')

        historial = st.session_state.historial_bio
        if historial.empty:
            st.info('Sin datos aun. Analiza un video para comenzar.')
            return

        disc_rec = st.selectbox('Disciplina  ',
                   ['Ciclismo','Carrera','Natacion'])
        datos    = historial[historial['disciplina'] == disc_rec]

        if datos.empty:
            st.info(f'Sin datos para {disc_rec}.')
            return

        resumen = datos.groupby('angulo')['estado'].agg(
            total        = 'count',
            errores      = lambda x: (x == 'error').sum(),
            advertencias = lambda x: (x == 'advertir').sum(),
            ok           = lambda x: (x == 'ok').sum(),
        ).reset_index()

        errores_p = resumen[resumen['errores'] > 0].sort_values('errores', ascending=False)
        if not errores_p.empty:
            st.error('**PRIORIDAD ALTA — Errores persistentes:**')
            for _, f in errores_p.iterrows():
                rango = RANGOS[disc_rec].get(f['angulo'], {})
                st.write(f'• **{f["angulo"]}** — presente en {f["errores"]}/{f["total"]} sesiones')
                if rango:
                    st.caption(f'Correccion: {rango.get("correccion_bajo","")}')

        adverts = resumen[(resumen['advertencias'] > 0) & (resumen['errores'] == 0)]
        if not adverts.empty:
            st.warning('**PRIORIDAD MEDIA — Advertencias:**')
            for _, f in adverts.iterrows():
                st.write(f'• {f["angulo"]}: {f["advertencias"]} sesiones con advertencia')

        correctos = resumen[resumen['ok'] == resumen['total']]
        if not correctos.empty:
            st.success('**OK — Angulos consistentemente correctos:**')
            for _, f in correctos.iterrows():
                st.write(f'• {f["angulo"]}')

        st.divider()
        consejos = {
            'Ciclismo': [
                'Haz un bike fitting profesional al menos una vez al ano',
                'Graba siempre desde el mismo angulo para comparar bien',
                'Dolor en rodilla casi siempre indica altura de sillon incorrecta',
            ],
            'Carrera': [
                'Trabaja la cadencia — objetivo entre 170-180 pasos por minuto',
                'El fortalecimiento de gluteos mejora la postura de carrera',
                'Graba desde atras tambien para ver la alineacion de caderas',
            ],
            'Natacion': [
                'Graba desde abajo del agua para ver la entrada del brazo',
                'SWOLF bajo indica mejor eficiencia tecnica',
                'Trabaja con un coach de natacion para corregir la brazada',
            ],
        }
        st.subheader(f'Consejos para {disc_rec}')
        for c in consejos.get(disc_rec, []):
            st.write(f'• {c}')
