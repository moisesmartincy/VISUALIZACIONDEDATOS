import streamlit as st
import pandas as pd
from src.carga_datos import cargar_datos
from src.limpieza import limpiar_datos
from src.analisis import generar_kpis
from src.visualizaciones import crear_mapa_calor, crear_barras_promedio
from src.analisis_temporal import asignar_fechas_sinteticas, calcular_media_movil
from src.estadistica import (
    calcular_estadisticas_detalladas,
    calcular_outliers_iqr,
    estadisticas_por_evento,
    estadisticas_semanales
)
from src.visualizaciones_avanzadas import (
    crear_serie_temporal,
    crear_boxplot_general,
    crear_boxplot_por_dia,
    crear_promedio_por_dia_ordenado,
    crear_comparativa_evento,
    crear_grafico_semanal
)

st.set_page_config(
    page_title="Accesos Aula Virtual — Caso 4",
    page_icon="📊",
    layout="wide"
)

# Encabezado institucional
st.title("Análisis de accesos al aula virtual")
st.subheader("Caso 4 — Representaciones Gráficas de Datos Procesados | Nivel Avanzado")

# Carga y limpieza de datos (reutilizando módulos existentes)
try:
    df_raw = cargar_datos()
    df, resumen_limpieza = limpiar_datos(df_raw)
    if 'Fecha' not in df.columns:
        df = asignar_fechas_sinteticas(df)
    # Cálculo previo de media móvil sobre serie cronológica completa
    df = calcular_media_movil(df, ventana=3)
except FileNotFoundError:
    st.error("No se encontró el dataset en 'data/accesos_aula_virtual.csv'. Ejecuta primero 'python src/generar_datos.py'.")
    st.stop()

# ==========================================
# FILTROS GLOBALES UNIFICADOS (Sidebar)
# ==========================================
st.sidebar.header("Filtros Globales")
st.sidebar.markdown("Filtre las observaciones para actualizar todos los indicadores y gráficos sincrónicamente:")

semanas_disp = sorted(df['Semana'].unique())
semanas_sel = st.sidebar.multiselect("Semanas académicas", options=semanas_disp, default=semanas_disp)

dias_disp = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
dias_sel = st.sidebar.multiselect("Días de la semana", options=dias_disp, default=dias_disp)

eventos_disp = sorted(df['Evento_academico'].unique())
eventos_sel = st.sidebar.multiselect("Eventos académicos", options=eventos_disp, default=eventos_disp)

min_acc = int(df['Accesos'].min())
max_acc = int(df['Accesos'].max())
rango_acc = st.sidebar.slider(
    "Rango de accesos diarios",
    min_value=min_acc,
    max_value=max_acc,
    value=(min_acc, max_acc)
)

# Único DataFrame filtrado reutilizado transversalmente
df_filtrado = df[
    (df['Semana'].isin(semanas_sel)) &
    (df['Dia'].isin(dias_sel)) &
    (df['Evento_academico'].isin(eventos_sel)) &
    (df['Accesos'].between(rango_acc[0], rango_acc[1]))
].copy()

if df_filtrado.empty:
    st.warning("No se encontraron registros que cumplan con la combinación de filtros seleccionada. Ajuste los parámetros.")
    st.stop()

# ==========================================
# ESTRUCTURA MODULAR MEDIANTE PESTAÑAS
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "1. Resumen",
    "2. Mapa de calor",
    "3. Serie temporal",
    "4. Distribución",
    "5. Eventos",
    "6. Outliers",
    "7. Conclusiones"
])

# ------------------------------------------
# TAB 1: RESUMEN Y CALIDAD DE DATOS
# ------------------------------------------
with tab1:
    st.header("Resumen General y Control de Calidad")
    
    # KPIs existentes
    kpis = generar_kpis(df_filtrado)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de accesos", f"{kpis['Total de accesos']:,}")
    c2.metric("Promedio diario", f"{kpis['Promedio diario']:,}")
    c3.metric("Máximo diario", f"{kpis['Máximo']:,}")
    c4.metric("Mínimo diario", f"{kpis['Mínimo']:,}")

    st.markdown("---")
    st.subheader("Auditoría de Calidad del Dato (Data Quality Assurance)")
    cal1, cal2, cal3, cal4 = st.columns(4)
    cal1.metric("Registros iniciales", resumen_limpieza['Registros iniciales'])
    cal2.metric("Valores nulos tratados", resumen_limpieza['Nulos'])
    cal3.metric("Duplicados depurados", resumen_limpieza['Duplicados'])
    cal4.metric("Inconsistencias corregidas", resumen_limpieza['Valores inválidos (antes)'])

    st.markdown("---")
    st.subheader("Resumen Estadístico Multivariado")
    stats = calcular_estadisticas_detalladas(df_filtrado)
    
    col_stat_a, col_stat_b = st.columns(2)
    with col_stat_a:
        st.markdown("**Medidas de Tendencia Central y Extremos**")
        df_tc = pd.DataFrame({
            'Métrica': ['Media', 'Mediana', 'Mínimo', 'Máximo'],
            'Valor': [stats['Media'], stats['Mediana'], stats['Mínimo'], stats['Máximo']]
        })
        st.dataframe(df_tc, use_container_width=True, hide_index=True)
        
    with col_stat_b:
        st.markdown("**Medidas de Dispersión y Variabilidad**")
        df_disp = pd.DataFrame({
            'Métrica': ['Desviación estándar', 'Q1 (P25)', 'Q3 (P75)', 'IQR (Rango Intercuartílico)', 'Coeficiente de Variación (CV%)'],
            'Valor': [f"{stats['Desviación estándar']}", f"{stats['Q1 (Percentil 25)']}", f"{stats['Q3 (Percentil 75)']}", f"{stats['IQR (Rango intercuartílico)']}", f"{stats['Coeficiente de variación (CV%)']}%"]
        })
        st.dataframe(df_disp, use_container_width=True, hide_index=True)

    st.info(
        "**Fundamento Estadístico:** La media representa el centro de gravedad aritmético, mientras que la mediana aporta "
        "robustez frente a picos o anomalías. El **Coeficiente de Variación (CV%)** expresa la dispersión relativa "
        "(Desviación Estándar / Media), permitiendo cuantificar la estabilidad del flujo de usuarios en el aula virtual."
    )

    st.markdown("---")
    st.subheader("Evolución Agregada por Semana Académica")
    modo_semanal = st.radio(
        "Seleccione métrica semanal a proyectar:",
        options=["Total semanal", "Promedio diario"],
        horizontal=True
    )
    df_sem = estadisticas_semanales(df_filtrado)
    st.plotly_chart(crear_grafico_semanal(df_sem, metrica=modo_semanal), use_container_width=True)

# ------------------------------------------
# TAB 2: MAPA DE CALOR
# ------------------------------------------
with tab2:
    st.header("Mapa de Calor: Semana × Día")
    st.markdown(
        "Visualización bidimensional que proyecta la densidad temporal agregada de accesos "
        "con una paleta secuencial perceptualmente uniforme y anotaciones simbólicas en fechas de evaluación."
    )
    
    st.plotly_chart(crear_mapa_calor(df_filtrado), use_container_width=True)

    with st.expander("Interpretación Técnica Senior del Mapa de Calor", expanded=True):
        st.markdown("""
        - **¿Qué muestra?** Cruza las 8 semanas de docencia (eje Y) con los 7 días de la semana (eje X), mapeando el volumen de accesos en una escala cromática secuencial con marcadores de eventos.
        - **¿Qué significa?** Evidencia patrones cíclicos claros: los días centrales y finales de semana laboral concentran la mayor densidad, mientras que los fines de semana reflejan una caída generalizada.
        - **¿Qué decisión permite apoyar?** Programar guardias de tutores y soporte de mesa de ayuda en días de saturación cromática alta, evitando asignar recursos en fines de semana o días de baja intensidad.
        - **¿Cuál es la limitación?** Al agregar a nivel de día completo, no describe la distribución horaria intracelular ni discrimina si los accesos provienen de usuarios únicos recurrentes o múltiples sesiones de un grupo reducido.
        """)

# ------------------------------------------
# TAB 3: SERIE TEMPORAL
# ------------------------------------------
with tab3:
    st.header("Evolución Temporal Continua de Accesos")
    st.markdown(
        "Seguimiento longitudinal ordenado de la actividad diaria con suavizamiento de tendencia "
        "mediante Media Móvil (3 días) e identificación explícita de hitos académicos."
    )

    st.plotly_chart(crear_serie_temporal(df_filtrado), use_container_width=True)

    st.caption(
        "**Aviso metodológico sobre la Media Móvil (3 días):** "
        "La línea discontinua calcula la media móvil centrada en una ventana de 3 jornadas continuas. "
        "Su finalidad es filtrar el ruido estocástico diario y exhibir la tendencia de fondo. "
        "No genera observaciones artificiales ni reemplaza el registro empírico."
    )

    with st.expander("Interpretación Técnica Senior de la Serie Temporal", expanded=True):
        st.markdown("""
        - **¿Qué muestra?** La trayectoria diaria cronológica a lo largo de las 8 semanas, contrastando los accesos puntuales con la curva suavizada y los eventos curriculares (diamantes rojos).
        - **¿Qué significa?** Se comprueba una dinámica oscilatoria con crestas periódicas que coinciden temporalmente con fechas de entregas o cuestionarios, seguidas de valles pronunciados.
        - **¿Qué decisión permite apoyar?** Coordinar el envío de alertas y recordatorios pedagógicos 48 a 72 horas antes de las crestas para amortiguar el estrés tecnológico y cognitivo de los estudiantes.
        - **¿Cuál es la limitación?** La correlación temporal entre eventos y picos no prueba causalidad determinística estricta; factores externos no registrados podrían influir en el comportamiento.
        """)

# ------------------------------------------
# TAB 4: DISTRIBUCIÓN Y VARIABILIDAD
# ------------------------------------------
with tab4:
    st.header("Distribución Estadística y Variabilidad de Accesos")
    
    col_box1, col_box2 = st.columns(2)
    with col_box1:
        st.plotly_chart(crear_boxplot_general(df_filtrado), use_container_width=True)
    with col_box2:
        st.plotly_chart(crear_boxplot_por_dia(df_filtrado), use_container_width=True)

    st.markdown("---")
    st.subheader("Comparativa de Patrón Semanal")
    col_bar1, col_bar2 = st.columns(2)
    with col_bar1:
        st.plotly_chart(crear_promedio_por_dia_ordenado(df_filtrado), use_container_width=True)
    with col_bar2:
        st.plotly_chart(crear_barras_promedio(df_filtrado), use_container_width=True)

    with st.expander("Interpretación Técnica Senior de la Distribución", expanded=True):
        st.markdown("""
        - **¿Qué muestra?** El Box Plot global exhibe la mediana, cuartiles (Q1 y Q3) y la longitud del rango intercuartílico (IQR). El Box Plot por día segmenta la heterogeneidad intrínseca según el día de la semana.
        - **¿Qué significa?** Los días viernes y jueves presentan medianas elevadas y mayor amplitud intercuartílica, lo que indica alta dispersión (comportamiento muy sensible a fechas de entrega). Los fines de semana son compactos y con baja dispersión.
        - **¿Qué decisión permite apoyar?** Dimensionar la capacidad de los servidores de la plataforma educativa tomando como referencia los cuantiles superiores (Q3 y bigote superior) de los días laborales de alta carga.
        - **¿Cuál es la limitación?** El box plot asume distribuciones unimodales para sintetizar la dispersión; si existieran subpoblaciones estudiantiles divergentes, se requiere desagregar por turnos o cohortes.
        """)

# ------------------------------------------
# TAB 5: EVENTOS ACADÉMICOS
# ------------------------------------------
with tab5:
    st.header("Impacto Asociado a Eventos Académicos")
    st.markdown(
        "Evaluación comparativa de la intensidad de uso según la concurrencia de hitos académicos "
        "(inicios de unidad, foros, tutorías, entregas prácticas y cuestionarios)."
    )

    st.plotly_chart(crear_comparativa_evento(df_filtrado), use_container_width=True)

    st.markdown("---")
    st.subheader("Estadísticas Agregadas por Modalidad de Evento")
    df_stats_eventos = estadisticas_por_evento(df_filtrado)
    st.dataframe(df_stats_eventos, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Registro Detallado de Jornadas con Evento")
    df_eventos_reg = df_filtrado[df_filtrado['Evento_academico'] != 'Sin evento'][
        ['Semana', 'Dia', 'Fecha', 'Evento_academico', 'Accesos']
    ].sort_values(['Semana', 'Dia']).reset_index(drop=True)
    st.dataframe(df_eventos_reg, use_container_width=True, hide_index=True)

    with st.expander("Interpretación Técnica Senior de Eventos", expanded=True):
        st.markdown("""
        - **¿Qué muestra?** La disparidad en la distribución de accesos entre días con evento curricular registrado versus jornadas sin evento formal programado.
        - **¿Qué significa?** Las jornadas con evento exhiben una mediana notablemente superior y un desplazamiento hacia la derecha en la masa probabilística de accesos.
        - **¿Qué decisión permite apoyar?** Programar sesiones de consulta sincrónica y presencia activa docente en los días que concentran eventos con mayor promedio y máximo de accesos.
        - **¿Cuál es la limitación?** No se puede declarar que el evento *cause* unívocamente todos los accesos registrados, sino que se constata una coincidencia temporal sistemática de mayor intensidad de uso.
        """)

# ------------------------------------------
# TAB 6: DETECCIÓN DE OUTLIERS
# ------------------------------------------
with tab6:
    st.header("Detección y Clasificación Contextual de Outliers (Criterio IQR)")
    st.markdown(
        "Identificación de observaciones atípicas basada en el método no paramétrico de Tukey: "
        "`[Q1 - 1.5 × IQR, Q3 + 1.5 × IQR]`."
    )

    df_outliers, umbrales_iqr = calcular_outliers_iqr(df_filtrado)

    c_iqr1, c_iqr2, c_iqr3, c_iqr4 = st.columns(4)
    c_iqr1.metric("Q1 (25%)", umbrales_iqr['Q1'])
    c_iqr2.metric("Q3 (75%)", umbrales_iqr['Q3'])
    c_iqr3.metric("Límite Inferior", umbrales_iqr['Limite_Inferior'])
    c_iqr4.metric("Límite Superior", umbrales_iqr['Limite_Superior'])

    st.markdown("---")
    st.subheader("Auditoría de Observaciones y Estado de Clasificación")
    
    # Filtro visual para inspeccionar sólo outliers o todo el conjunto
    ver_solo_outliers = st.checkbox("Mostrar únicamente valores potencialmente atípicos (Altos o Bajos)", value=False)
    if ver_solo_outliers:
        df_mostrar_outliers = df_outliers[df_outliers['Outlier'] != 'Normal']
    else:
        df_mostrar_outliers = df_outliers

    st.dataframe(df_mostrar_outliers, use_container_width=True, hide_index=True)

    with st.expander("Interpretación Técnica Senior sobre Outliers", expanded=True):
        st.markdown("""
        - **¿Qué muestra?** Cuantifica qué observaciones rebasan las fronteras estadísticas teóricas de la muestra.
        - **¿Qué significa?** Un valor catalogado como *potencialmente alto* no es un error de medición; en analítica de aprendizaje (*learning analytics*), coincide usualmente con entregas de proyectos o exámenes donde el alumnado accede masivamente.
        - **¿Qué decisión permite apoyar?** Aislar anomalías técnicas reales (p. ej. caídas de servidor o accesos negativos ya resueltos en limpieza) de eventos pedagógicos excepcionales que ameritan refuerzo de servidores y personal.
        - **¿Cuál es la limitación?** El umbral 1.5 × IQR es una regla heurística paramétricamente neutra; en distribuciones marcadamente asimétricas, puede clasificar picos genuinos como atípicos si no se analizan en su contexto.
        """)

# ------------------------------------------
# TAB 7: CONCLUSIONES Y PLAN DE INTERVENCIÓN
# ------------------------------------------
with tab7:
    st.header("Historia Analítica y Propuesta de Intervención Institucional")
    
    st.markdown("""
    ### 🧭 Síntesis de la Historia Analítica
    1. **Densidad Temporal (Heatmap):** La concurrencia masiva está circunscrita a la franja Miércoles–Viernes, con desmovilización en fines de semana.
    2. **Evolución Dinámica (Serie Temporal):** Los ciclos responden a un ritmo semanal sostenido con picos sincrónicos a los hitos de evaluación.
    3. **Variabilidad y Dispersión (Box Plots):** Los días Viernes concentran la mayor incertidumbre operativa (alta variabilidad), requiriendo elasticidad de recursos.
    4. **Comportamiento ante Eventos:** Las fechas con evaluaciones multiplican significativamente el volumen de accesos respecto a jornadas ordinarias.
    5. **Auditoría de Outliers:** Los picos atípicos son de naturaleza académica y coinciden con cierres de módulo y entregas ponderadas.

    ---
    ### 🚀 Plan de Intervención Recomendado para Educación Virtual
    - **1. Estrategia de Comunicación Proactiva (Martes/Miércoles):**
      - Despachar recordatorios estructurados y pautas de rúbrica a mitad de semana para desahogar la carga de consultas de último momento.
    - **2. Asignación Flexible de Guardias de Tutoría:**
      - Reorientar la carga horaria de tutores hacia las tardes de jueves y jornadas de viernes (días de mayor densidad), reduciendo presencia en sábado y domingo.
    - **3. Campañas de Nivelación en Fines de Semana:**
      - Diseñar micro-actividades asincrónicas o foros de incentivo para reactivar a estudiantes que trabajan y fomentar un ritmo de estudio continuo.
    - **4. Respaldo y Mantenimiento de Infraestructura:**
      - Programar mantenimientos de la plataforma exclusivamente en domingos de madrugada para evitar cortes en momentos de saturación operativa.
    """)
