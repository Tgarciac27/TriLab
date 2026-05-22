# ============================================================
# TRIAI COACH - Streamlit
# modulos/modulo2.py - Plan de Entrenamiento con IA
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

DISTANCIAS = {
    'sprint'  : {'natacion':  750, 'ciclismo': 20000, 'carrera':  5000},
    'olimpico': {'natacion': 1500, 'ciclismo': 40000, 'carrera': 10000},
    'media'   : {'natacion': 1900, 'ciclismo': 90000, 'carrera': 21100},
    'ironman' : {'natacion': 3800, 'ciclismo':180000, 'carrera': 42200},
}


# ── Funciones del plan ──

def calcular_carga(tiempo_min, fc_promedio, fc_reposo=55, fc_max=185):
    if fc_promedio <= fc_reposo: return 0.0
    hrr   = (fc_promedio - fc_reposo) / (fc_max - fc_reposo)
    trimp = tiempo_min * hrr * 0.64 * (2.718 ** (1.92 * hrr))
    return round(trimp, 1)


def es_semana_brick(numero_semana):
    return numero_semana % 2 == 0


def tipo_de_semana(numero_semana, total_semanas):
    if numero_semana == total_semanas:
        return 'tapering'
    tercio = max(1, (total_semanas - 1) // 3)
    if numero_semana <= tercio:          return 'base'
    elif numero_semana <= tercio * 2:    return 'volumen'
    else:                                return 'intensidad'


def calcular_volumen_base(perfil):
    min_totales  = perfil['horas_semana'] * 60
    factor_nivel = {'principiante': 0.7, 'intermedio': 1.0, 'avanzado': 1.3}
    factor       = factor_nivel.get(perfil['nivel'], 1.0)
    dist = {'Natacion': 0.25, 'Ciclismo': 0.45, 'Carrera': 0.30}
    debil = perfil.get('disciplina_debil')
    if debil in dist:
        dist[debil]      += 0.10
        dist['Ciclismo'] -= 0.10
    return {d: round(min_totales * p * factor) for d, p in dist.items()}


def crear_sesion(disciplina, tipo_semana, volumen_base, reducir=False):
    if disciplina == 'Fuerza':
        tiempo = 20 if tipo_semana == 'tapering' else 40
        return {'disciplina':'Fuerza','tipo':'Acondicionamiento',
                'distancia_m':0,'tiempo_min':tiempo,
                'fc_objetivo':128,'carga':calcular_carga(tiempo, 128)}
    if disciplina == 'Descanso':
        return {'disciplina':'Descanso','tipo':'Descanso activo',
                'distancia_m':0,'tiempo_min':30,'fc_objetivo':105,'carga':0}

    factor = {'base':0.80,'volumen':1.00,'intensidad':0.95,'tapering':0.40}[tipo_semana]
    if reducir: factor *= 0.65
    tiempo = max(20, min(round(volumen_base.get(disciplina, 60) * factor), 110))

    config = {
        'base'      : {'fc':135,'tipos':{'Natacion':'Tecnica',    'Ciclismo':'Fondo Z2',    'Carrera':'Z2 suave'}},
        'volumen'   : {'fc':143,'tipos':{'Natacion':'Fondo',      'Ciclismo':'Fondo largo', 'Carrera':'Fondo'}},
        'intensidad': {'fc':165,'tipos':{'Natacion':'Series',     'Ciclismo':'Umbral',      'Carrera':'Umbral'}},
        'tapering'  : {'fc':122,'tipos':{'Natacion':'Activacion', 'Ciclismo':'Suave',       'Carrera':'Suave'}},
    }
    fc          = config[tipo_semana]['fc']
    tipo_sesion = config[tipo_semana]['tipos'].get(disciplina, 'General')
    vel_kmh     = {'Natacion':2.5,'Ciclismo':33.0,'Carrera':11.0}
    dist_m      = round(vel_kmh[disciplina] * (tiempo / 60) * 1000)

    return {'disciplina':disciplina,'tipo':tipo_sesion,
            'distancia_m':dist_m,'tiempo_min':tiempo,
            'fc_objetivo':fc,'carga':calcular_carga(tiempo, fc)}


def crear_sesion_brick(volumen_base, tipo_semana):
    factor   = 0.60
    tiempo_c = max(20, round(volumen_base['Ciclismo'] * factor))
    dist_c   = round(33.0 * (tiempo_c / 60) * 1000)
    tiempo_r = max(15, round(volumen_base['Carrera'] * factor * 0.40))
    dist_r   = round(11.0 * (tiempo_r / 60) * 1000)

    return [
        {'disciplina':'Ciclismo','tipo':'Brick T2','distancia_m':dist_c,
         'tiempo_min':tiempo_c,'fc_objetivo':158,'carga':calcular_carga(tiempo_c, 158)},
        {'disciplina':'Carrera','tipo':'Brick T2','distancia_m':dist_r,
         'tiempo_min':tiempo_r,'fc_objetivo':168,'carga':calcular_carga(tiempo_r, 168)},
    ]


def generar_plan(perfil):
    volumen_base  = calcular_volumen_base(perfil)
    total_semanas = perfil['semanas_hasta_comp']
    plan          = []

    for sem in range(1, total_semanas + 1):
        tipo      = tipo_de_semana(sem, total_semanas)
        es_brick  = es_semana_brick(sem)
        es_ultima = (sem == total_semanas)
        dias      = {}

        dias['Lunes']     = [crear_sesion('Ciclismo', tipo, volumen_base, reducir=True),
                             crear_sesion('Fuerza',   tipo, volumen_base)]
        dias['Martes']    = [crear_sesion('Natacion', tipo, volumen_base)]
        dias['Miercoles'] = [crear_sesion('Carrera',  tipo, volumen_base)]
        dias['Jueves']    = [crear_sesion('Natacion', tipo, volumen_base, reducir=True),
                             crear_sesion('Fuerza',   tipo, volumen_base)]

        if es_brick:
            dias['Viernes'] = [crear_sesion('Descanso', tipo, volumen_base)]
            dias['Sabado']  = crear_sesion_brick(volumen_base, tipo)
        else:
            dias['Viernes'] = [crear_sesion('Ciclismo', tipo, volumen_base)]
            dias['Sabado']  = [crear_sesion('Carrera',  tipo, volumen_base)]

        if es_ultima:
            dias['Domingo'] = [{'disciplina':'Competencia','tipo':'Competencia',
                                'distancia_m':0,'tiempo_min':0,'fc_objetivo':0,'carga':0}]
        else:
            dias['Domingo'] = [crear_sesion('Descanso', tipo, volumen_base)]

        carga_total = sum(s['carga'] for ss in dias.values() for s in ss)
        plan.append({'numero':sem,'tipo':tipo,'es_brick':es_brick,
                     'dias':dias,'carga_total':round(carga_total, 1)})

    return plan, volumen_base


# ── Funcion principal del modulo ──

def mostrar():
    st.title('📅 Plan de Entrenamiento con IA')

    # Tabs del modulo
    tab1, tab2, tab3 = st.tabs([
        '⚙️ Generar plan',
        '📋 Ver plan detallado',
        '📊 Graficas',
    ])

    # ── TAB 1: Configurar perfil y generar plan ──
    with tab1:
        st.subheader('Configura tu perfil')

        col_a, col_b = st.columns(2)

        with col_a:
            nombre     = st.text_input('Nombre', value='Atleta')
            modalidad  = st.selectbox('Modalidad',
                         ['sprint','olimpico','media','ironman'],
                         index=1)
            nivel      = st.selectbox('Nivel',
                         ['principiante','intermedio','avanzado'],
                         index=1)
            debil      = st.selectbox('Disciplina debil',
                         ['Natacion','Ciclismo','Carrera'])

        with col_b:
            horas    = st.slider('Horas de entrenamiento por semana',
                                 min_value=4, max_value=20, value=10, step=1)
            fc_max   = st.slider('FC maxima (bpm)',
                                 min_value=150, max_value=220, value=185, step=1)
            semanas  = st.slider('Semanas hasta la competencia',
                                 min_value=2, max_value=24, value=8, step=1)
            objetivo = st.text_input('Objetivo', value='Sub 2:30')

        dist_comp = DISTANCIAS[modalidad]
        st.info(f'Distancias {modalidad.upper()}: '
                f'Natacion {dist_comp["natacion"]}m | '
                f'Ciclismo {dist_comp["ciclismo"]/1000:.0f}km | '
                f'Carrera {dist_comp["carrera"]/1000:.1f}km')

        if st.button('Generar mi plan', type='primary'):
            perfil = {
                'nombre'            : nombre,
                'fc_maxima'         : fc_max,
                'fc_reposo'         : 55,
                'horas_semana'      : horas,
                'nivel'             : nivel,
                'modalidad'         : modalidad,
                'semanas_hasta_comp': semanas,
                'objetivo'          : objetivo,
                'disciplina_debil'  : debil,
            }
            plan, volumen_base = generar_plan(perfil)
            st.session_state.plan          = plan
            st.session_state.perfil_plan   = perfil
            st.session_state.volumen_base  = volumen_base

            n_brick = sum(1 for s in plan if s['es_brick'])
            carga_max = max(s['carga_total'] for s in plan)

            st.success(f'Plan generado para {nombre} — '
                       f'{semanas} semanas | '
                       f'{n_brick} semanas brick | '
                       f'Carga maxima: {carga_max:.0f} TRIMP')

            # Resumen de semanas
            st.subheader('Resumen del plan')
            col_tipo = {'base':'🟢','volumen':'🔵','intensidad':'🟡','tapering':'⚪'}
            for sem in plan:
                brick_str = ' 🧱 BRICK' if sem['es_brick'] else ''
                st.write(f'{col_tipo[sem["tipo"]]} **Semana {sem["numero"]}** — '
                         f'{sem["tipo"].upper()}{brick_str} | '
                         f'Carga: {sem["carga_total"]:.0f} TRIMP')

    # ── TAB 2: Plan detallado ──
    with tab2:
        if 'plan' not in st.session_state:
            st.info('Primero genera el plan en la pestana "Generar plan".')
        else:
            plan = st.session_state.plan

            sem_sel = st.selectbox(
                'Selecciona la semana',
                options=[f'Semana {s["numero"]} — {s["tipo"].upper()}{"  BRICK" if s["es_brick"] else ""}'
                         for s in plan]
            )
            idx_sem = int(sem_sel.split(' ')[1]) - 1
            sem     = plan[idx_sem]

            st.markdown(f'### Semana {sem["numero"]} — {sem["tipo"].upper()}')
            st.metric('Carga total', f'{sem["carga_total"]:.0f} TRIMP')

            etiquetas_tipo = {
                'base'      : '🟢 Baja intensidad',
                'volumen'   : '🔵 Carga alta',
                'intensidad': '🟡 Alta intensidad',
                'tapering'  : '⚪ Descarga precompetitiva',
            }
            st.caption(etiquetas_tipo[sem['tipo']])
            st.divider()

            orden_dias = ['Lunes','Martes','Miercoles','Jueves',
                          'Viernes','Sabado','Domingo']

            for dia in orden_dias:
                sesiones   = sem['dias'].get(dia, [])
                carga_dia  = sum(s['carga'] for s in sesiones)
                n_entrenos = len([s for s in sesiones
                                  if s['disciplina'] not in ('Descanso','Competencia')])
                doble_str  = ' — DOBLE' if n_entrenos > 1 else ''

                with st.expander(f'**{dia}**{doble_str}  |  Carga: {carga_dia:.0f}'):
                    for s in sesiones:
                        disc = s['disciplina']
                        if disc == 'Competencia':
                            st.success(f'🏁 COMPETENCIA — '
                                       f'{st.session_state.perfil_plan["modalidad"].upper()}')
                        elif disc == 'Descanso':
                            st.info('😴 Descanso activo')
                        elif disc == 'Fuerza':
                            st.write(f'💪 **Fuerza** — {s["tipo"]} | {s["tiempo_min"]} min')
                        else:
                            dist_str = (f'{s["distancia_m"]}m'
                                        if disc == 'Natacion'
                                        else f'{s["distancia_m"]/1000:.1f}km')
                            emoji = {'Natacion':'🏊','Ciclismo':'🚴','Carrera':'🏃'}
                            st.write(f'{emoji[disc]} **{disc}** — {s["tipo"]} | '
                                     f'{dist_str} | {s["tiempo_min"]} min | '
                                     f'FC: {s["fc_objetivo"]} bpm | '
                                     f'Carga: {s["carga"]:.0f}')

    # ── TAB 3: Graficas ──
    with tab3:
        if 'plan' not in st.session_state:
            st.info('Primero genera el plan en la pestana "Generar plan".')
        else:
            plan = st.session_state.plan

            # Grafica de carga semanal
            st.subheader('Carga semanal planificada (TRIMP)')
            etiq   = [f'S{s["numero"]}{"*" if s["es_brick"] else ""}\n{s["tipo"][:3].upper()}'
                      for s in plan]
            cargas = [s['carga_total'] for s in plan]
            col_tipo = {'base':'#1D9E75','volumen':'#378ADD',
                        'intensidad':'#EF9F27','tapering':'#888780'}
            colores  = [col_tipo[s['tipo']] for s in plan]

            fig, ax = plt.subplots(figsize=(max(8, len(plan)*1.2), 4))
            barras  = ax.bar(etiq, cargas, color=colores, alpha=0.85, width=0.6)
            for b, v in zip(barras, cargas):
                ax.text(b.get_x() + b.get_width()/2,
                        b.get_height() + 3,
                        f'{v:.0f}', ha='center', fontsize=10, fontweight='bold')
            ax.plot(range(len(cargas)), cargas, 'o--', color='gray',
                    linewidth=1, alpha=0.5, markersize=4)
            ax.set_ylabel('Carga TRIMP')
            leyenda = [mpatches.Patch(color=c, label=t.capitalize())
                       for t, c in col_tipo.items()]
            ax.legend(handles=leyenda, fontsize=9)
            ax.set_title('* = semana brick', fontsize=9, color='gray')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            st.divider()

            # Grafica de volumen por disciplina
            st.subheader('Volumen por disciplina (km)')
            vol = {'Natacion':[],'Ciclismo':[],'Carrera':[]}
            for sem in plan:
                acum = {'Natacion':0,'Ciclismo':0,'Carrera':0}
                for sesiones in sem['dias'].values():
                    for s in sesiones:
                        if s['disciplina'] in acum:
                            acum[s['disciplina']] += s['distancia_m']
                for d in vol:
                    vol[d].append(round(acum[d]/1000, 1))

            x     = np.arange(len(plan))
            ancho = 0.5
            fig2, ax2 = plt.subplots(figsize=(max(8, len(plan)*1.2), 4))
            bottom    = np.zeros(len(plan))
            for disc, vals in vol.items():
                ax2.bar(x, vals, ancho, bottom=bottom,
                        label=disc, color=COLORES[disc], alpha=0.85)
                bottom += np.array(vals)
            ax2.set_xticks(x)
            ax2.set_xticklabels([f'S{s["numero"]}' for s in plan])
            ax2.set_ylabel('Distancia (km)')
            ax2.legend(fontsize=9)
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()
