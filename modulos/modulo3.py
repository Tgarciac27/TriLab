# ============================================================
# TRIAI COACH - Streamlit
# modulos/modulo3.py - Transiciones T1 y T2
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
    'T1'     : '#7F77DD',
    'T2'     : '#D4537E',
    'ok'     : '#1D9E75',
    'revisar': '#EF9F27',
    'critico': '#D85A30',
}

PASOS_T1 = [
    {'paso':'Salir del agua con calma',
     'consejo':'Respira y no te apresures — una caida cuesta mas tiempo',
     'seg_obj':10},
    {'paso':'Quitarse gorro y gafas',
     'consejo':'Hazlo corriendo hacia la zona de transicion',
     'seg_obj':8},
    {'paso':'Bajar el neopreno hasta la cintura',
     'consejo':'Practica esto en casa hasta hacerlo en menos de 10 seg',
     'seg_obj':15},
    {'paso':'Terminar de quitar el neopreno en el rack',
     'consejo':'Pisalo con un pie para ayudarte a sacar el otro',
     'seg_obj':20},
    {'paso':'Ponerse el casco y abrocharlo',
     'consejo':'OBLIGATORIO antes de tocar la bici — hay penalizacion',
     'seg_obj':8},
    {'paso':'Ponerse gafas de ciclismo si aplica',
     'consejo':'Dejala dentro del casco para encontrarla rapido',
     'seg_obj':5},
    {'paso':'Tomar la bici del rack',
     'consejo':'Agarra el manubrio, no el asiento — mas control',
     'seg_obj':5},
    {'paso':'Correr hasta la linea de mount y montar',
     'consejo':'No montes dentro de la zona de transicion — es reglamento',
     'seg_obj':15},
]

PASOS_T2 = [
    {'paso':'Llegar al area de transicion',
     'consejo':'Desmonta la bici antes de la linea de dismount',
     'seg_obj':10},
    {'paso':'Desmontar la bicicleta',
     'consejo':'Practica el dismount volante para ganar segundos',
     'seg_obj':5},
    {'paso':'Dejar la bici en el rack',
     'consejo':'Memoriza tu numero de rack antes de la carrera',
     'seg_obj':8},
    {'paso':'Quitarse el casco',
     'consejo':'Solo puedes quitarlo despues de dejar la bici en el rack',
     'seg_obj':5},
    {'paso':'Cambiar zapatillas',
     'consejo':'Usa cordones elasticos — ahorras hasta 15s',
     'seg_obj':25},
    {'paso':'Ponerse gorra o visera',
     'consejo':'Tenla lista junto a las zapatillas de carrera',
     'seg_obj':5},
    {'paso':'Tomar numero de corredor si aplica',
     'consejo':'Usalo en cinturon elastico para no perder tiempo',
     'seg_obj':5},
    {'paso':'Salir del area de transicion corriendo',
     'consejo':'Empieza a correr antes de llegar a la linea de salida',
     'seg_obj':10},
]

tiempo_obj_t1 = sum(p['seg_obj'] for p in PASOS_T1)
tiempo_obj_t2 = sum(p['seg_obj'] for p in PASOS_T2)


def cargar_historial_ejemplo():
    df = pd.DataFrame([
        {'fecha':'2025-04-26','tiempo_seg':118,'tipo':'Brick',
         'notas':'Primer brick, zapatillas lentas'},
        {'fecha':'2025-05-10','tiempo_seg':102,'tipo':'Brick',
         'notas':'Mejora con cordones elasticos'},
    ])
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['tiempo_fmt']  = df['tiempo_seg'].apply(lambda s: f'{s//60}:{s%60:02d}')
    df['diferencia']  = df['tiempo_seg'] - tiempo_obj_t2
    df['dif_fmt']     = df['diferencia'].apply(lambda d: f'+{d}s' if d > 0 else f'{d}s')
    df['estado']      = df['tiempo_seg'].apply(
        lambda s: 'OK' if s <= tiempo_obj_t2 else 'Por mejorar'
    )
    return df


def mostrar():
    st.title('⏱ Transiciones T1 y T2')

    if 'historial_t2' not in st.session_state:
        st.session_state.historial_t2 = cargar_historial_ejemplo()

    tab1, tab2, tab3, tab4 = st.tabs([
        '📋 Guia T1',
        '📋 Guia T2',
        '⏱ Registrar tiempo',
        '🤖 Recomendaciones IA',
    ])

    # ── TAB 1: Guia T1 ──
    with tab1:
        st.subheader('Guia T1 — Natacion a Ciclismo')
        st.metric('Tiempo objetivo T1',
                  f'{tiempo_obj_t1//60}:{tiempo_obj_t1%60:02d}',
                  f'{len(PASOS_T1)} pasos')

        st.divider()

        acum = 0
        for i, paso in enumerate(PASOS_T1, 1):
            acum += paso['seg_obj']
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                critico = ' 🔴' if paso['seg_obj'] >= 20 else ''
                st.markdown(f'**{i}. {paso["paso"]}**{critico}')
                st.caption(f'💡 {paso["consejo"]}')
            with col2:
                st.metric('Objetivo', f'{paso["seg_obj"]}s')
            with col3:
                st.metric('Acumulado', f'{acum}s')
            st.divider()

        st.info('T1 es dificil de practicar en entrenamientos regulares. '
                'Estudia la secuencia y practica quitarte el neopreno en seco.')

    # ── TAB 2: Guia T2 ──
    with tab2:
        st.subheader('Guia T2 — Ciclismo a Carrera')
        st.metric('Tiempo objetivo T2',
                  f'{tiempo_obj_t2//60}:{tiempo_obj_t2%60:02d}',
                  f'{len(PASOS_T2)} pasos')

        st.divider()

        acum = 0
        for i, paso in enumerate(PASOS_T2, 1):
            acum += paso['seg_obj']
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                critico = ' 🔴' if paso['seg_obj'] >= 20 else ''
                st.markdown(f'**{i}. {paso["paso"]}**{critico}')
                st.caption(f'💡 {paso["consejo"]}')
            with col2:
                st.metric('Objetivo', f'{paso["seg_obj"]}s')
            with col3:
                st.metric('Acumulado', f'{acum}s')
            st.divider()

        # Desglose grafico
        st.subheader('Desglose por paso')
        nombres = [p['paso'] for p in PASOS_T2]
        tiempos = [p['seg_obj'] for p in PASOS_T2]
        colores = [COLORES['ok'] if t <= 10
                   else COLORES['revisar'] if t <= 20
                   else COLORES['critico'] for t in tiempos]

        fig, ax = plt.subplots(figsize=(9, 5))
        barras  = ax.barh(range(len(nombres)), tiempos,
                          color=colores, alpha=0.85)
        ax.set_yticks(range(len(nombres)))
        ax.set_yticklabels(nombres, fontsize=9)
        ax.set_xlabel('Segundos (objetivo)')
        for b, v in zip(barras, tiempos):
            ax.text(v + 0.3, b.get_y() + b.get_height()/2,
                    f'{v}s', va='center', fontsize=9)
        leyenda = [
            plt.Rectangle((0,0),1,1, color=COLORES['ok'],
                           alpha=0.85, label='Rapido (hasta 10s)'),
            plt.Rectangle((0,0),1,1, color=COLORES['revisar'],
                           alpha=0.85, label='Moderado (11-20s)'),
            plt.Rectangle((0,0),1,1, color=COLORES['critico'],
                           alpha=0.85, label='Critico (mas de 20s)'),
        ]
        ax.legend(handles=leyenda, fontsize=8, loc='lower right')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # ── TAB 3: Registrar tiempo ──
    with tab3:
        st.subheader('Registrar tiempo de T2')

        col_a, col_b = st.columns(2)
        with col_a:
            fecha_t2 = st.date_input('Fecha', value=datetime.today())
            tipo_t2  = st.selectbox('Tipo', ['Brick','Competencia','Simulacro'])
            minutos  = st.number_input('Minutos', min_value=0, max_value=10, value=1)
            segundos = st.number_input('Segundos', min_value=0, max_value=59, value=42)
        with col_b:
            notas_t2 = st.text_area('Notas',
                                     placeholder='Que salio bien, que mejorar...',
                                     height=120)

        seg_total = minutos * 60 + segundos
        dif       = seg_total - tiempo_obj_t2
        dif_str   = f'+{dif}s sobre objetivo' if dif > 0 else f'{abs(dif)}s bajo objetivo'

        st.info(f'Tiempo ingresado: **{minutos}:{segundos:02d}** | {dif_str}')

        if st.button('Guardar tiempo T2', type='primary'):
            nueva = {
                'fecha'      : pd.Timestamp(fecha_t2),
                'tiempo_seg' : seg_total,
                'tipo'       : tipo_t2,
                'notas'      : notas_t2,
                'tiempo_fmt' : f'{seg_total//60}:{seg_total%60:02d}',
                'diferencia' : dif,
                'dif_fmt'    : dif_str,
                'estado'     : 'OK' if dif <= 0 else 'Por mejorar',
            }
            st.session_state.historial_t2 = pd.concat(
                [st.session_state.historial_t2, pd.DataFrame([nueva])],
                ignore_index=True
            )
            if dif <= 0:
                st.success(f'Tiempo guardado — {minutos}:{segundos:02d} | Objetivo logrado!')
            else:
                st.warning(f'Tiempo guardado — {minutos}:{segundos:02d} | {dif_str}')

        st.divider()

        # Historial
        st.subheader('Historial de T2')
        historial = st.session_state.historial_t2
        st.dataframe(
            historial[['fecha','tiempo_fmt','dif_fmt','estado','tipo','notas']
                     ].sort_values('fecha', ascending=False).reset_index(drop=True),
            use_container_width=True,
        )

        # Grafica de progreso
        if len(historial) >= 2:
            st.subheader('Progreso T2')
            fechas  = historial['fecha'].dt.strftime('%d/%m')
            tiempos = historial['tiempo_seg'].values
            colores_barras = [COLORES['ok'] if t <= tiempo_obj_t2
                              else COLORES['critico'] for t in tiempos]

            fig2, ax2 = plt.subplots(figsize=(9, 4))
            ax2.plot(fechas, tiempos, 'o-', color=COLORES['T2'],
                     linewidth=2, markersize=8, zorder=3)
            for i, (f, t) in enumerate(zip(fechas, tiempos)):
                ax2.scatter(f, t, color=colores_barras[i], s=80, zorder=4)
                ax2.annotate(f'{t//60}:{t%60:02d}', (f, t),
                             textcoords='offset points',
                             xytext=(0,12), ha='center', fontsize=10)
            ax2.axhline(tiempo_obj_t2, color='gray', linestyle='--',
                        linewidth=1.5,
                        label=f'Objetivo: {tiempo_obj_t2//60}:{tiempo_obj_t2%60:02d}')
            ax2.fill_between(range(len(fechas)), 0, tiempo_obj_t2,
                             alpha=0.07, color=COLORES['ok'])
            ax2.set_ylabel('Segundos')
            ax2.set_xlabel('Fecha')
            ax2.set_ylim(0, max(tiempos) * 1.35)
            ax2.legend(fontsize=9)
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()

    # ── TAB 4: Recomendaciones IA ──
    with tab4:
        st.subheader('Recomendaciones IA — Transiciones')

        historial = st.session_state.historial_t2

        if historial.empty:
            st.info('Sin datos aun. Registra tu primer tiempo despues del brick.')
            return

        ultimo   = historial.iloc[-1]['tiempo_seg']
        mejor    = historial['tiempo_seg'].min()
        promedio = round(historial['tiempo_seg'].mean())

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Ultimo T2', f'{ultimo//60}:{ultimo%60:02d}')
        with col2:
            st.metric('Mejor T2', f'{mejor//60}:{mejor%60:02d}')
        with col3:
            st.metric('Promedio', f'{promedio//60}:{promedio%60:02d}')
        with col4:
            st.metric('Objetivo', f'{tiempo_obj_t2//60}:{tiempo_obj_t2%60:02d}')

        st.divider()

        dif = ultimo - tiempo_obj_t2
        if dif <= 0:
            st.success(f'Estas {abs(dif)}s bajo el objetivo. Mantiene la consistencia.')
        else:
            st.warning(f'Te faltan {dif}s para alcanzar el objetivo.')

        # Tendencia
        if len(historial) >= 2:
            x    = np.arange(len(historial))
            y    = historial['tiempo_seg'].values
            m, _ = np.polyfit(x, y, 1)

            st.divider()
            st.subheader('Tendencia')
            if m < -2:
                st.success(f'MEJORANDO: {abs(m):.1f}s mas rapido por brick.')
            elif m > 2:
                st.error(f'EMPEORANDO: {m:.1f}s mas lento por brick.')
            else:
                st.info('ESTABLE: sin cambio significativo. '
                        'Intenta optimizar el paso critico.')

        st.divider()
        st.subheader('Paso mas critico')
        paso_critico = max(PASOS_T2, key=lambda p: p['seg_obj'])
        st.error(f'**{paso_critico["paso"]}** — {paso_critico["seg_obj"]}s objetivo')
        st.caption(f'Consejo: {paso_critico["consejo"]}')

        st.divider()
        st.subheader('Consejos generales')
        consejos = [
            'Practica la secuencia T2 en casa 3 veces por semana',
            'Usa cordones elasticos — ahorras hasta 15s en zapatillas',
            'Organiza siempre tu zona de transicion de la misma forma',
            'Coloca la gorra DENTRO de las zapatillas de carrera',
            'Para T1 practica quitarte el neopreno en seco hasta memorizarlo',
        ]
        for c in consejos:
            st.write(f'• {c}')
