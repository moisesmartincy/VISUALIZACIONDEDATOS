import pandas as pd
import numpy as np

def calcular_estadisticas_detalladas(df):
    """
    Calcula indicadores robustos y paramétricos de tendencia central y dispersión:
    - Tendencia central: Media, Mediana.
    - Dispersión: Desviación estándar, IQR, Coeficiente de variación (CV%).
    - Extremos: Mínimo, Máximo, Q1, Q3.
    """
    accesos = df['Accesos'].dropna()
    total = int(accesos.sum())
    media = float(accesos.mean())
    mediana = float(accesos.median())
    std = float(accesos.std())
    minimo = int(accesos.min())
    maximo = int(accesos.max())
    q1 = float(np.percentile(accesos, 25))
    q3 = float(np.percentile(accesos, 75))
    iqr = float(q3 - q1)
    cv = float((std / media) * 100) if media != 0 else 0.0

    return {
        'Total de accesos': total,
        'Media': round(media, 2),
        'Mediana': round(mediana, 2),
        'Desviación estándar': round(std, 2),
        'Mínimo': minimo,
        'Máximo': maximo,
        'Q1 (Percentil 25)': round(q1, 2),
        'Q3 (Percentil 75)': round(q3, 2),
        'IQR (Rango intercuartílico)': round(iqr, 2),
        'Coeficiente de variación (CV%)': round(cv, 2)
    }

def calcular_outliers_iqr(df):
    """
    Identifica valores atípicos mediante el método de Tukey (criterio IQR):
    - Límite inferior: Q1 - 1.5 * IQR
    - Límite superior: Q3 + 1.5 * IQR
    Clasifica cada observación en: Normal, Potencialmente alto, Potencialmente bajo.
    """
    df_calc = df.copy()
    q1 = np.percentile(df_calc['Accesos'], 25)
    q3 = np.percentile(df_calc['Accesos'], 75)
    iqr = q3 - q1
    limite_inf = q1 - 1.5 * iqr
    limite_sup = q3 + 1.5 * iqr

    def clasificar(val):
        if val > limite_sup:
            return 'Potencialmente alto'
        elif val < limite_inf:
            return 'Potencialmente bajo'
        return 'Normal'

    df_calc['Outlier'] = df_calc['Accesos'].apply(clasificar)
    
    # Columnas ordenadas para presentación
    cols = ['Fecha', 'Dia', 'Semana', 'Accesos', 'Evento_academico', 'Outlier']
    cols_existentes = [c for c in cols if c in df_calc.columns]
    
    df_outliers = df_calc[cols_existentes].sort_values(['Semana', 'Dia']).reset_index(drop=True)
    return df_outliers, {
        'Q1': round(q1, 2),
        'Q3': round(q3, 2),
        'IQR': round(iqr, 2),
        'Limite_Inferior': round(limite_inf, 2),
        'Limite_Superior': round(limite_sup, 2)
    }

def estadisticas_por_evento(df):
    """
    Calcula métricas agregadas por tipo de evento académico:
    Número de ocurrencias, Promedio de accesos, Mediana y Máximo.
    """
    resumen = df.groupby('Evento_academico')['Accesos'].agg(
        Número_de_ocurrencias='count',
        Promedio_de_accesos='mean',
        Mediana='median',
        Máximo='max'
    ).reset_index()

    resumen['Promedio_de_accesos'] = resumen['Promedio_de_accesos'].round(2)
    resumen = resumen.sort_values('Promedio_de_accesos', ascending=False).reset_index(drop=True)
    return resumen

def estadisticas_semanales(df):
    """
    Calcula el total de accesos y el promedio diario por semana.
    """
    resumen = df.groupby('Semana')['Accesos'].agg(
        Total_semanal='sum',
        Promedio_diario='mean'
    ).reset_index()
    resumen['Promedio_diario'] = resumen['Promedio_diario'].round(2)
    return resumen
