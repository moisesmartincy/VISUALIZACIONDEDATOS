import pandas as pd
import numpy as np
import os

def crear_dataset():
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    eventos = {
        (1, 'Lunes'): 'Inicio de unidad',
        (1, 'Viernes'): 'Entrega práctica',
        (2, 'Lunes'): 'Sin evento',
        (2, 'Viernes'): 'Cuestionario',
        (3, 'Miércoles'): 'Foro debate',
        (4, 'Viernes'): 'Examen parcial',
        (5, 'Lunes'): 'Inicio de unidad',
        (6, 'Viernes'): 'Entrega práctica',
        (7, 'Miércoles'): 'Tutoría online',
        (8, 'Viernes'): 'Examen final'
    }

    data = []
    np.random.seed(42)
    estudiantes = 500

    for semana in range(1, 9):
        for dia in dias:
            evento = eventos.get((semana, dia), 'Sin evento')
            
            if evento != 'Sin evento' or dia in ['Miércoles', 'Jueves']:
                accesos = int(np.random.normal(350, 50))
            elif dia in ['Sábado', 'Domingo']:
                accesos = int(np.random.normal(100, 30))
            else:
                accesos = int(np.random.normal(200, 40))
            
            if (semana, dia) == (1, 'Lunes'): accesos = 214
            if (semana, dia) == (1, 'Viernes'): accesos = 388
            if (semana, dia) == (2, 'Lunes'): accesos = 172
            if (semana, dia) == (2, 'Viernes'): accesos = 425
            
            accesos = max(0, accesos)
            
            if (semana, dia) == (4, 'Sábado'): accesos = -50 
            if (semana, dia) == (5, 'Domingo'): accesos = None

            data.append({
                'Semana': semana,
                'Dia': dia,
                'Accesos': accesos,
                'Evento_academico': evento,
                'Estudiantes_activos': estudiantes,
                'Accesos_normalizados': accesos / estudiantes if pd.notnull(accesos) and accesos >= 0 else None
            })

    df = pd.DataFrame(data)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/accesos_aula_virtual.csv', index=False)
    print("Dataset generado en data/accesos_aula_virtual.csv")

if __name__ == '__main__':
    crear_dataset()
