import pandas as pd
import numpy as np

def limpiar_datos(df):
    """
    Realiza la limpieza del dataset:
    - Trata nulos
    - Corrige tipos y valores extremos/negativos
    - Valida semanas y días
    """
    resumen = {'Registros iniciales': len(df), 'Nulos': df.isnull().sum().sum(), 'Duplicados': df.duplicated().sum()}
    
    df = df.drop_duplicates()
    df.loc[df['Accesos'] < 0, 'Accesos'] = np.nan
    df['Accesos'] = df.groupby('Dia')['Accesos'].transform(lambda x: x.fillna(x.median()))
    
    df = df[df['Semana'].between(1, 8)]
    dias_validos = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    df = df[df['Dia'].isin(dias_validos)]
    
    df['Accesos'] = df['Accesos'].astype(int)
    if 'Estudiantes_activos' in df.columns:
        df['Accesos_normalizados'] = df['Accesos'] / df['Estudiantes_activos']
    
    resumen['Valores inválidos (antes)'] = resumen['Nulos'] # Simplificación
    resumen['Registros finales'] = len(df)
    
    df['Dia'] = pd.Categorical(df['Dia'], categories=dias_validos, ordered=True)
    df = df.sort_values(['Semana', 'Dia'])
    
    from src.analisis_temporal import asignar_fechas_sinteticas
    df = asignar_fechas_sinteticas(df)
    
    return df, resumen
