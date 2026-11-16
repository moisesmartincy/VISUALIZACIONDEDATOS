import pandas as pd
import os

def cargar_datos(filepath='data/accesos_aula_virtual.csv'):
    """Carga los datos desde la ruta especificada."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo {filepath} no existe.")
    df = pd.read_csv(filepath)
    return df
