import plotly.express as px
import plotly.graph_objects as go

def crear_mapa_calor(df):
    pivot = df.pivot(index='Semana', columns='Dia', values='Accesos')
    
    hover_text = []
    for sem in pivot.index:
        row_hover = []
        for dia in pivot.columns:
            val = pivot.loc[sem, dia]
            evento = df[(df['Semana']==sem) & (df['Dia']==dia)]['Evento_academico'].values[0]
            row_hover.append(f"Semana: {sem}<br>Día: {dia}<br>Accesos: {val}<br>Evento: {evento}")
        hover_text.append(row_hover)
        
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=[f'Semana {i}' for i in pivot.index],
        colorscale='Teal',
        text=pivot.values,
        texttemplate="%{text}",
        hoverinfo='text',
        textfont={"size":12},
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover_text
    ))
    
    for sem in pivot.index:
        for j, dia in enumerate(pivot.columns):
            evento = df[(df['Semana']==sem) & (df['Dia']==dia)]['Evento_academico'].values[0]
            if evento != 'Sin evento':
                fig.add_annotation(
                    x=j,
                    y=f'Semana {sem}',
                    text='⚠️',
                    showarrow=False,
                    yshift=15,
                    xshift=20,
                    hovertext=f"Evento: {evento}"
                )
                
    fig.update_layout(
        title='Mapa de Calor: Accesos al Aula Virtual por Semana y Día',
        xaxis_title='Día de la semana',
        yaxis_title='Semana',
        yaxis_autorange='reversed',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def crear_barras_promedio(df):
    promedio_dia = df.groupby('Dia', observed=False)['Accesos'].mean().reset_index()
    promedio_dia = promedio_dia.sort_values('Accesos', ascending=False)
    
    fig = px.bar(
        promedio_dia, 
        x='Dia', 
        y='Accesos', 
        title='Promedio de Accesos por Día de la Semana',
        labels={'Accesos': 'Promedio de accesos', 'Dia': 'Día'},
        color='Accesos',
        color_continuous_scale='Blues'
    )
    
    fig.update_traces(
        hovertemplate='Día: %{x}<br>Promedio de accesos: %{y:.0f}<extra></extra>',
        texttemplate='%{y:.0f}', textposition='outside'
    )
    
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    
    return fig
