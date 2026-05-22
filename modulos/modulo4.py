# ============================================================
# TRIAI COACH - Streamlit
# modulos/modulo4.py - Nutricion e Hidratacion
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
    'carbohidratos': '#639922',
    'proteinas'    : '#378ADD',
    'grasas'       : '#EF9F27',
    'agua'         : '#85B7EB',
}

PLANES = {
    'entrenamiento': {
        'descripcion': 'Alta demanda energetica',
        'comidas': [
            {'nombre':'Desayuno (2h antes)','momento':'Pre-entreno',
             'alimentos':[
                 {'nombre':'Avena con banano y miel','kcal':380,'carb_g':72,'prot_g':8,'gras_g':6},
                 {'nombre':'Huevos revueltos x2','kcal':180,'carb_g':2,'prot_g':14,'gras_g':12},
                 {'nombre':'Jugo de naranja natural','kcal':110,'carb_g':26,'prot_g':2,'gras_g':0},
             ]},
            {'nombre':'Snack pre-entreno (30min antes)','momento':'Pre-entreno',
             'alimentos':[
                 {'nombre':'Banana','kcal':90,'carb_g':23,'prot_g':1,'gras_g':0},
                 {'nombre':'Cafe negro sin azucar','kcal':5,'carb_g':0,'prot_g':0,'gras_g':0},
             ]},
            {'nombre':'Durante el entrenamiento','momento':'Durante',
             'alimentos':[
                 {'nombre':'Agua con electrolitos (500ml)','kcal':30,'carb_g':7,'prot_g':0,'gras_g':0},
                 {'nombre':'Gel energetico (si >60min)','kcal':100,'carb_g':25,'prot_g':0,'gras_g':0},
             ]},
            {'nombre':'Almuerzo (recuperacion)','momento':'Post-entreno',
             'alimentos':[
                 {'nombre':'Arroz integral con pollo','kcal':520,'carb_g':72,'prot_g':38,'gras_g':8},
                 {'nombre':'Ensalada con aceite de oliva','kcal':120,'carb_g':8,'prot_g':3,'gras_g':9},
             ]},
            {'nombre':'Merienda','momento':'Post-entreno',
             'alimentos':[
                 {'nombre':'Yogur griego con frutas','kcal':200,'carb_g':28,'prot_g':14,'gras_g':4},
                 {'nombre':'Nueces (20g)','kcal':130,'carb_g':3,'prot_g':3,'gras_g':12},
             ]},
            {'nombre':'Cena','momento':'Post-entreno',
             'alimentos':[
                 {'nombre':'Salmon al horno con quinoa','kcal':480,'carb_g':42,'prot_g':36,'gras_g':14},
                 {'nombre':'Verduras al vapor','kcal':80,'carb_g':16,'prot_g':4,'gras_g':0},
             ]},
        ],
    },
    'descanso': {
        'descripcion': 'Recuperacion y reparacion muscular',
        'comidas': [
            {'nombre':'Desayuno','momento':'Manana',
             'alimentos':[
                 {'nombre':'Tostadas con aguacate y huevo','kcal':380,'carb_g':38,'prot_g':16,'gras_g':18},
                 {'nombre':'Fruta de temporada','kcal':80,'carb_g':20,'prot_g':1,'gras_g':0},
             ]},
            {'nombre':'Almuerzo','momento':'Mediodia',
             'alimentos':[
                 {'nombre':'Lentejas con verduras','kcal':420,'carb_g':58,'prot_g':24,'gras_g':6},
                 {'nombre':'Pan integral x1','kcal':80,'carb_g':15,'prot_g':3,'gras_g':1},
             ]},
            {'nombre':'Cena','momento':'Noche',
             'alimentos':[
                 {'nombre':'Pechuga de pollo con batata','kcal':420,'carb_g':45,'prot_g':38,'gras_g':6},
                 {'nombre':'Ensalada verde','kcal':60,'carb_g':8,'prot_g':2,'gras_g':2},
             ]},
        ],
    },
    'competencia': {
        'descripcion': 'Maxima energia disponible',
        'comidas': [
            {'nombre':'Desayuno (3h antes)','momento':'Pre-competencia',
             'alimentos':[
                 {'nombre':'Pasta o arroz blanco con aceite','kcal':480,'carb_g':96,'prot_g':12,'gras_g':6},
                 {'nombre':'Tostadas con mermelada x2','kcal':200,'carb_g':42,'prot_g':4,'gras_g':2},
                 {'nombre':'Platano maduro','kcal':90,'carb_g':23,'prot_g':1,'gras_g':0},
             ]},
            {'nombre':'Zona de salida (30min antes)','momento':'Pre-competencia',
             'alimentos':[
                 {'nombre':'Gel energetico x1','kcal':100,'carb_g':25,'prot_g':0,'gras_g':0},
                 {'nombre':'Agua 250ml','kcal':0,'carb_g':0,'prot_g':0,'gras_g':0},
             ]},
            {'nombre':'Durante (segmento ciclismo)','momento':'Durante',
             'alimentos':[
                 {'nombre':'Gel energetico cada 30min','kcal':100,'carb_g':25,'prot_g':0,'gras_g':0},
                 {'nombre':'Bebida isotonica 500ml','kcal':120,'carb_g':30,'prot_g':0,'gras_g':0},
             ]},
            {'nombre':'Post-competencia (primeros 30min)','momento':'Post-competencia',
             'alimentos':[
                 {'nombre':'Batido de recuperacion','kcal':300,'carb_g':45,'prot_g':25,'gras_g':4},
                 {'nombre':'Agua o isotonica 500ml','kcal':60,'carb_g':15,'prot_g':0,'gras_g':0},
             ]},
        ],
    },
}


# ── Funciones de calculo ──

def calcular_tmb(perfil):
    p, h, e = perfil['peso_kg'], perfil['altura_cm'], perfil['edad']
    if perfil['sexo'] == 'masculino':
        return round(10*p + 6.25*h - 5*e + 5)
    return round(10*p + 6.25*h - 5*e - 161)

def calcular_calorias(perfil, tipo_dia):
    tmb    = calcular_tmb(perfil)
    factor = {'descanso':1.40,'entrenamiento':1.70,'competencia':2.00}[tipo_dia]
    ajuste = {'principiante':0.95,'intermedio':1.0,'avanzado':1.08}.get(perfil['nivel'], 1.0)
    return round(tmb * factor * ajuste)

def calcular_macros(calorias, tipo_dia):
    dist = {'entrenamiento':{'carb':0.55,'prot':0.25,'gras':0.20},
            'descanso'     :{'carb':0.45,'prot':0.30,'gras':0.25},
            'competencia'  :{'carb':0.65,'prot':0.15,'gras':0.20}}[tipo_dia]
    return {
        'carbohidratos_g': round(calorias * dist['carb'] / 4),
        'proteinas_g'    : round(calorias * dist['prot'] / 4),
        'grasas_g'       : round(calorias * dist['gras'] / 9),
    }

def calcular_agua(perfil, tipo_dia, temperatura='templado', duracion_min=0):
    base      = (perfil['peso_kg'] * 35) / 1000
    extra_tipo= {'descanso':0.0,'entrenamiento':0.5,'competencia':1.0}[tipo_dia]
    extra_temp= {'frio':0.0,'templado':0.3,'calor':0.8}[temperatura]
    extra_dur = (duracion_min / 60) * 0.6
    return round(base + extra_tipo + extra_temp + extra_dur, 1)


def cargar_historial_ejemplo(perfil):
    datos = [
        {'fecha':'2025-05-05','tipo_dia':'entrenamiento','kcal_real':3050,
         'carb_g':340,'prot_g':130,'gras_g':72,'agua_L':2.8,'notas':'Buen dia'},
        {'fecha':'2025-05-06','tipo_dia':'entrenamiento','kcal_real':2980,
         'carb_g':325,'prot_g':128,'gras_g':70,'agua_L':3.0,'notas':''},
        {'fecha':'2025-05-07','tipo_dia':'entrenamiento','kcal_real':3100,
         'carb_g':355,'prot_g':132,'gras_g':75,'agua_L':3.2,'notas':''},
        {'fecha':'2025-05-08','tipo_dia':'entrenamiento','kcal_real':2850,
         'carb_g':310,'prot_g':135,'gras_g':68,'agua_L':2.6,'notas':''},
        {'fecha':'2025-05-09','tipo_dia':'descanso','kcal_real':2400,
         'carb_g':260,'prot_g':138,'gras_g':72,'agua_L':2.4,'notas':''},
        {'fecha':'2025-05-10','tipo_dia':'entrenamiento','kcal_real':3200,
         'carb_g':365,'prot_g':128,'gras_g':78,'agua_L':3.5,'notas':'Dia brick'},
    ]
    df = pd.DataFrame(datos)
    df['fecha']           = pd.to_datetime(df['fecha'])
    df['kcal_obj']        = df['tipo_dia'].apply(lambda t: calcular_calorias(perfil, t))
    df['diferencia_kcal'] = df['kcal_real'] - df['kcal_obj']
    return df


def mostrar():
    st.title('🍎 Nutricion e Hidratacion')

    # Perfil nutricional en sidebar del modulo
    with st.expander('⚙️ Configura tu perfil nutricional', expanded=False):
        col_a, col_b = st.columns(2)
        with col_a:
            peso   = st.number_input('Peso (kg)', min_value=40, max_value=120, value=72)
            altura = st.number_input('Altura (cm)', min_value=140, max_value=220, value=175)
            edad   = st.number_input('Edad', min_value=16, max_value=65, value=32)
        with col_b:
            sexo   = st.selectbox('Sexo', ['masculino','femenino'])
            nivel  = st.selectbox('Nivel', ['principiante','intermedio','avanzado'], index=1)

    perfil_nut = {
        'peso_kg': peso, 'altura_cm': altura,
        'edad': edad, 'sexo': sexo, 'nivel': nivel,
    }

    if 'historial_nut' not in st.session_state:
        st.session_state.historial_nut = cargar_historial_ejemplo(perfil_nut)

    tab1, tab2, tab3, tab4 = st.tabs([
        '🥗 Plan nutricional',
        '💧 Hidratacion',
        '📋 Registro diario',
        '🤖 Recomendaciones IA',
    ])

    # ── TAB 1: Plan nutricional ──
    with tab1:
        st.subheader('Plan nutricional del dia')

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            tipo_dia = st.selectbox('Tipo de dia',
                       ['entrenamiento','descanso','competencia'])
        with col_b:
            temperatura = st.selectbox('Temperatura', ['frio','templado','calor'], index=1)
        with col_c:
            duracion = st.slider('Duracion entreno (min)', 0, 240, 90, step=10)

        kcal   = calcular_calorias(perfil_nut, tipo_dia)
        macros = calcular_macros(kcal, tipo_dia)
        agua   = calcular_agua(perfil_nut, tipo_dia, temperatura, duracion)

        st.divider()

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric('Calorias objetivo', f'{kcal} kcal')
        with col2: st.metric('Carbohidratos', f'{macros["carbohidratos_g"]}g')
        with col3: st.metric('Proteinas', f'{macros["proteinas_g"]}g')
        with col4: st.metric('Grasas', f'{macros["grasas_g"]}g')

        st.metric('Agua minima del dia', f'{agua} L')

        st.divider()

        plan  = PLANES[tipo_dia]
        total_kcal = total_carb = total_prot = total_gras = 0

        momento_color = {
            'Pre-entreno'     : '🟡',
            'Durante'         : '🔵',
            'Post-entreno'    : '🟢',
            'Pre-competencia' : '🟡',
            'Post-competencia': '🟢',
            'Manana'          : '🟡',
            'Mediodia'        : '🔵',
            'Noche'           : '🟢',
        }

        for comida in plan['comidas']:
            sub_kcal = sum(a['kcal']   for a in comida['alimentos'])
            sub_carb = sum(a['carb_g'] for a in comida['alimentos'])
            sub_prot = sum(a['prot_g'] for a in comida['alimentos'])
            sub_gras = sum(a['gras_g'] for a in comida['alimentos'])
            total_kcal += sub_kcal
            total_carb += sub_carb
            total_prot += sub_prot
            total_gras += sub_gras

            emoji = momento_color.get(comida['momento'], '⚪')
            with st.expander(f'{emoji} **{comida["nombre"]}** — {sub_kcal} kcal'):
                for a in comida['alimentos']:
                    col_n, col_k = st.columns([4, 1])
                    with col_n: st.write(f'• {a["nombre"]}')
                    with col_k: st.write(f'{a["kcal"]} kcal')
                st.caption(f'C: {sub_carb}g | P: {sub_prot}g | G: {sub_gras}g')

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric('Total del dia', f'{total_kcal} kcal',
                      f'{total_kcal - kcal:+.0f} vs objetivo')
        with col2:
            st.caption(f'C: {total_carb}g | P: {total_prot}g | G: {total_gras}g')

    # ── TAB 2: Hidratacion ──
    with tab2:
        st.subheader('Control de hidratacion')

        tipo_h = st.selectbox('Tipo de dia ', ['entrenamiento','descanso','competencia'],
                              key='tipo_hidra')
        temp_h = st.selectbox('Temperatura ', ['frio','templado','calor'],
                              index=1, key='temp_hidra')
        dur_h  = st.slider('Duracion entreno (min) ', 0, 240, 90,
                           step=10, key='dur_hidra')

        agua_total = calcular_agua(perfil_nut, tipo_h, temp_h, dur_h)
        vasos      = round(agua_total / 0.25)

        col1, col2 = st.columns(2)
        with col1: st.metric('Agua total recomendada', f'{agua_total} L')
        with col2: st.metric('Vasos de 250ml', f'{vasos} vasos')

        st.progress(min(1.0, agua_total / 4.0),
                    text=f'{agua_total}L de 4L maximo')

        st.divider()
        st.subheader('Distribucion durante el dia')

        momentos = [
            ('Al despertar',             0.5),
            ('Desayuno',                 0.5),
            ('Media manana',             0.5),
            ('Almuerzo',                 0.5),
            ('Durante entrenamiento',    round(dur_h / 60 * 0.6, 1)),
            ('Media tarde',              0.5),
            ('Cena',                     0.5),
            ('Antes de dormir',          0.3),
        ]
        for momento, litros in momentos:
            col1, col2 = st.columns([3, 1])
            with col1: st.write(f'💧 {momento}')
            with col2: st.write(f'{litros} L')

        st.divider()
        st.info('Si orinas oscuro, necesitas mas agua. '
                'La orina debe ser amarillo palido.')

    # ── TAB 3: Registro diario ──
    with tab3:
        st.subheader('Registrar nutricion del dia')

        col_a, col_b = st.columns(2)
        with col_a:
            fecha_n  = st.date_input('Fecha ', value=datetime.today())
            tipo_n   = st.selectbox('Tipo de dia  ',
                       ['entrenamiento','descanso','competencia'])
            kcal_r   = st.number_input('Calorias consumidas (kcal)',
                       min_value=0, max_value=6000, value=3000)
            carb_r   = st.number_input('Carbohidratos (g)',
                       min_value=0, max_value=800, value=340)
        with col_b:
            prot_r   = st.number_input('Proteinas (g)',
                       min_value=0, max_value=400, value=130)
            gras_r   = st.number_input('Grasas (g)',
                       min_value=0, max_value=300, value=70)
            agua_r   = st.slider('Agua consumida (litros)',
                       min_value=0.5, max_value=6.0, value=2.5, step=0.1)
            notas_n  = st.text_area('Notas ',
                       placeholder='Como te sentiste...')

        kcal_obj = calcular_calorias(perfil_nut, tipo_n)
        dif_kcal = kcal_r - kcal_obj
        st.info(f'Objetivo del dia: {kcal_obj} kcal | '
                f'Diferencia: {dif_kcal:+.0f} kcal')

        if st.button('Guardar registro nutricional', type='primary'):
            nueva = {
                'fecha'          : pd.Timestamp(fecha_n),
                'tipo_dia'       : tipo_n,
                'kcal_real'      : kcal_r,
                'carb_g'         : carb_r,
                'prot_g'         : prot_r,
                'gras_g'         : gras_r,
                'agua_L'         : round(agua_r, 1),
                'notas'          : notas_n,
                'kcal_obj'       : kcal_obj,
                'diferencia_kcal': dif_kcal,
            }
            st.session_state.historial_nut = pd.concat(
                [st.session_state.historial_nut, pd.DataFrame([nueva])],
                ignore_index=True
            )
            if abs(dif_kcal) <= 200:
                st.success(f'Registro guardado — {kcal_r} kcal | Diferencia: {dif_kcal:+.0f}')
            else:
                st.warning(f'Registro guardado — diferencia alta: {dif_kcal:+.0f} kcal')

        st.divider()
        st.subheader('Historial nutricional')
        historial = st.session_state.historial_nut
        st.dataframe(
            historial[['fecha','tipo_dia','kcal_real','kcal_obj',
                       'diferencia_kcal','agua_L','notas']
                     ].sort_values('fecha', ascending=False).reset_index(drop=True),
            use_container_width=True,
        )

        if len(historial) >= 2:
            st.subheader('Calorias: consumido vs objetivo')
            fechas  = historial['fecha'].dt.strftime('%d/%m')
            reales  = historial['kcal_real'].values
            objs    = historial['kcal_obj'].values
            colores = ['#1D9E75' if abs(r-o) <= 200 else '#D85A30'
                       for r, o in zip(reales, objs)]

            x     = np.arange(len(fechas))
            ancho = 0.35
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(x - ancho/2, reales, ancho, color=colores, alpha=0.85, label='Consumido')
            ax.bar(x + ancho/2, objs,   ancho, color='#B4B2A9', alpha=0.6, label='Objetivo')
            ax.set_xticks(x)
            ax.set_xticklabels(fechas)
            ax.set_ylabel('Calorias (kcal)')
            ax.legend(fontsize=9)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

    # ── TAB 4: Recomendaciones IA ──
    with tab4:
        st.subheader('Recomendaciones IA — Nutricion')

        historial = st.session_state.historial_nut
        if historial.empty:
            st.info('Sin datos. Registra tu primer dia para ver recomendaciones.')
            return

        dif_prom  = historial['diferencia_kcal'].mean()
        agua_prom = historial['agua_L'].mean()

        col1, col2 = st.columns(2)
        with col1:
            st.metric('Balance calorico promedio', f'{dif_prom:+.0f} kcal/dia')
        with col2:
            st.metric('Hidratacion promedio', f'{agua_prom:.1f} L/dia')

        st.divider()

        if dif_prom > 300:
            st.error('Estas comiendo bastante mas de lo necesario. '
                     'Revisa las porciones, especialmente en cenas.')
        elif dif_prom < -300:
            st.warning('Deficit calorico alto — puede afectar la recuperacion. '
                       'Aumenta carbohidratos en desayuno y merienda post-entreno.')
        else:
            st.success('Balance calorico dentro del rango aceptable.')

        if agua_prom < 2.5:
            st.warning('Hidratacion insuficiente. '
                       'Objetivo minimo: 2.5L en dias de descanso, mas en entrenos.')
        else:
            st.success('Buena hidratacion promedio.')

        st.divider()
        st.subheader('Consejos generales')
        consejos = [
            'Come dentro de los 30min post-entrenamiento (ventana anabolica)',
            'Prioriza carbohidratos la noche antes de un brick o competencia',
            'No pruebes alimentos nuevos el dia de competencia',
            'La cafeina mejora el rendimiento — usala 45-60min antes',
            'Si orinas oscuro, necesitas mas agua',
        ]
        for c in consejos:
            st.write(f'• {c}')
