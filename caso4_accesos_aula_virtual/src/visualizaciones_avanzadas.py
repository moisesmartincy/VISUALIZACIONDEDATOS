import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.analisis_temporal import asignar_fechas_sinteticas

def crear_serie_temporal(df):
    """
    Crea la serie temporal de accesos diarios junto con la media móvil de 3 días
    y la identificación explícita de eventos académicos mediante marcas y anotaciones.
    """
    if 'Fecha' not in df.columns:
        df = asignar_fechas_sinteticas(df)
    df_plot = df.sort_values('Fecha').copy()
    
    fig = go.Figure()

    # 1. Traza de accesos diarios observados
    fig.add_trace(go.Scatter(
        x=df_plot['Fecha'],
        y=df_plot['Accesos'],
        mode='lines+markers',
        name='Accesos diarios',
        line=dict(color='#0284c7', width=2),
        marker=dict(size=6, color='#0284c7'),
        customdata=df_plot[['Semana', 'Dia', 'Evento_academico']],
        hovertemplate=(
            "<b>Fecha:</b> %{x|%Y-%m-%d}<br>"
            "<b>Semana:</b> %{customdata[0]}<br>"
            "<b>Día:</b> %{customdata[1]}<br>"
            "<b>Accesos:</b> %{y}<br>"
            "<b>Evento:</b> %{customdata[2]}<extra></extra>"
        )
    ))

    # 2. Traza de media móvil (3 días) si está calculada
    if 'media_movil_3' in df_plot.columns:
        fig.add_trace(go.Scatter(
            x=df_plot['Fecha'],
            y=df_plot['media_movil_3'],
            mode='lines',
            name='Media móvil (3 días)',
            line=dict(color='#f59e0b', width=2.5, dash='dot'),
            hovertemplate=(
                "<b>Fecha:</b> %{x|%Y-%m-%d}<br>"
                "<b>Media Móvil (3d):</b> %{y:.1f}<extra></extra>"
            )
        ))

    # 3. Puntos destacados para eventos académicos
    df_eventos = df_plot[df_plot['Evento_academico'] != 'Sin evento']
    if not df_eventos.empty:
        fig.add_trace(go.Scatter(
            x=df_eventos['Fecha'],
            y=df_eventos['Accesos'],
            mode='markers+text',
            name='Evento académico',
            marker=dict(symbol='diamond', size=12, color='#ef4444', line=dict(width=1.5, color='#ffffff')),
            text=df_eventos['Evento_academico'],
            textposition='top center',
            textfont=dict(size=10, color='#991b1b'),
            customdata=df_eventos[['Semana', 'Dia', 'Evento_academico']],
            hovertemplate=(
                "<b>FECHA CON EVENTO</b><br>"
                "<b>Fecha:</b> %{x|%Y-%m-%d}<br>"
                "<b>Evento:</b> %{customdata[2]}<br>"
                "<b>Accesos:</b> %{y}<extra></extra>"
            )
        ))

    fig.update_layout(
        title='Evolución Temporal de Accesos y Ocurrencia de Eventos Académicos',
        xaxis_title='Línea Temporal (Fecha)',
        yaxis_title='Número de Accesos',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9')
    )
    return fig

def crear_boxplot_general(df):
    """
    Box plot general para evaluar la dispersión, asimetría y valores atípicos globales.
    """
    fig = px.box(
        df,
        y='Accesos',
        points='all',
        title='Distribución General de Accesos y Detección de Valores Atípicos',
        labels={'Accesos': 'Accesos Diarios'},
        color_discrete_sequence=['#0d9488']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9')
    )
    fig.update_traces(
        hovertemplate="<b>Accesos:</b> %{y}<extra></extra>"
    )
    return fig

def crear_boxplot_por_dia(df):
    """
    Box plot de accesos por día de la semana (Lunes a Domingo ordenados cronológicamente).
    Permite evaluar variabilidad intrínseca y heterogeneidad por jornada.
    """
    dias_orden = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    df_plot = df.copy()
    df_plot['Dia'] = pd.Categorical(df_plot['Dia'], categories=dias_orden, ordered=True)
    df_plot = df_plot.sort_values('Dia')

    fig = px.box(
        df_plot,
        x='Dia',
        y='Accesos',
        color='Dia',
        points='all',
        title='Distribución y Variabilidad de Accesos por Día de la Semana',
        category_orders={'Dia': dias_orden},
        labels={'Dia': 'Día de la Semana', 'Accesos': 'Accesos Diarios'}
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9')
    )
    fig.update_traces(
        hovertemplate="<b>Día:</b> %{x}<br><b>Accesos:</b> %{y}<extra></extra>"
    )
    return fig

def crear_promedio_por_dia_ordenado(df):
    """
    Gráfico de barras con el promedio de accesos por día de la semana
    respetando el orden natural cronológico (Lunes a Domingo) para contextualizar el ciclo semanal.
    """
    dias_orden = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    prom = df.groupby('Dia', observed=False)['Accesos'].mean().reindex(dias_orden).reset_index()

    fig = px.bar(
        prom,
        x='Dia',
        y='Accesos',
        title='Patrón Semanal: Promedio de Accesos por Día (Orden Cronológico)',
        labels={'Dia': 'Día de la Semana', 'Accesos': 'Promedio de Accesos'},
        color='Accesos',
        color_continuous_scale='Teal'
    )
    fig.update_traces(
        texttemplate='%{y:.1f}',
        textposition='outside',
        hovertemplate="<b>Día:</b> %{x}<br><b>Promedio diario:</b> %{y:.2f} accesos<extra></extra>"
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9')
    )
    return fig

def crear_comparativa_evento(df):
    """
    Box plot comparativo entre días con evento académico vs días sin evento académico.
    Permite contrastar medianas y dispersión sin asumir causalidad directa.
    """
    df_comp = df.copy()
    df_comp['Condicion_Evento'] = df_comp['Evento_academico'].apply(
        lambda x: 'Con evento' if str(x).strip() != 'Sin evento' else 'Sin evento'
    )

    fig = px.box(
        df_comp,
        x='Condicion_Evento',
        y='Accesos',
        color='Condicion_Evento',
        points='all',
        title='Distribución de Accesos: Días con Evento Académico vs Sin Evento',
        labels={'Condicion_Evento': 'Condición de la Jornada', 'Accesos': 'Accesos Diarios'},
        color_discrete_map={'Con evento': '#e11d48', 'Sin evento': '#64748b'}
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9')
    )
    fig.update_traces(
        hovertemplate="<b>Condición:</b> %{x}<br><b>Accesos:</b> %{y}<extra></extra>"
    )
    return fig

def crear_grafico_semanal(df_resumen_semanal, metrica='Total semanal'):
    """
    Visualiza la evolución agregada por semana (Total o Promedio diario).
    """
    y_col = 'Total_semanal' if metrica == 'Total semanal' else 'Promedio_diario'
    titulo = f'Evolución Semanal: {metrica}'
    color_bar = '#6366f1' if metrica == 'Total semanal' else '#0ea5e9'

    fig = px.bar(
        df_resumen_semanal,
        x='Semana',
        y=y_col,
        title=titulo,
        labels={'Semana': 'Semana Académica', y_col: metrica},
        text=y_col
    )
    fig.update_traces(
        marker_color=color_bar,
        texttemplate='%{y}',
        textposition='outside',
        hovertemplate="<b>Semana:</b> %{x}<br><b>" + metrica + ":</b> %{y}<extra></extra>"
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickmode='linear', dtick=1),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9')
    )
    return fig
