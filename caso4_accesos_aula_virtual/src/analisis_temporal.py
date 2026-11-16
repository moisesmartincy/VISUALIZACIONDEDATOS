import pandas as pd
import numpy as np

def asignar_fechas_sinteticas(df, fecha_inicio='2026-02-02'):
    """
    Asigna una fecha sintética coherente a cada registro del dataset de 8 semanas.
    Documentación: Esta fecha es sintética y se genera únicamente para representar
    la dimensión temporal continua (Lunes de Semana 1 a Domingo de Semana 8).
    NO es una fecha histórica real.
    """
    df = df.copy()
    dias_map = {
        'Lunes': 0, 'Martes': 1, 'Miércoles': 2, 'Jueves': 3,
        'Viernes': 4, 'Sábado': 5, 'Domingo': 6
    }
    
    inicio = pd.to_datetime(fecha_inicio)
    dias_num = df['Dia'].astype(str).map(dias_map).fillna(0).astype(int)
    offset_dias = (df['Semana'].astype(int) - 1) * 7 + dias_num
    df['Fecha'] = inicio + pd.to_timedelta(offset_dias, unit='D')
    df = df.sort_values('Fecha').reset_index(drop=True)
    return df

def calcular_media_movil(df, ventana=3):
    """
    Calcula la media móvil de 3 días para suavizar la serie y evidenciar la tendencia subyacente.
    Nota metodológica: La media móvil suaviza fluctuaciones de corto plazo y NO representa
    nuevos datos observados.
    """
    df = df.copy()
    if 'Fecha' in df.columns:
        df = df.sort_values('Fecha')
    df[f'media_movil_{ventana}'] = df['Accesos'].rolling(window=ventana, min_periods=1).mean()
    return df
