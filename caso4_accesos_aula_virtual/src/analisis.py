import pandas as pd

def generar_kpis(df):
    kpis = {
        'Total de accesos': int(df['Accesos'].sum()),
        'Promedio diario': int(df['Accesos'].mean()),
        'Máximo': int(df['Accesos'].max()),
        'Mínimo': int(df['Accesos'].min())
    }
    return kpis

def generar_estadisticas_eda(df):
    desc = df['Accesos'].describe().to_dict()
    promedio_semana = df.groupby('Semana')['Accesos'].mean().to_dict()
    promedio_dia = df.groupby('Dia', observed=False)['Accesos'].mean().to_dict()
    
    con_evento = df[df['Evento_academico'] != 'Sin evento']['Accesos'].mean()
    sin_evento = df[df['Evento_academico'] == 'Sin evento']['Accesos'].mean()
    
    return {
        'Descriptivas': desc,
        'Promedio Semana': promedio_semana,
        'Promedio Día': promedio_dia,
        'Accesos con evento': con_evento,
        'Accesos sin evento': sin_evento
    }
