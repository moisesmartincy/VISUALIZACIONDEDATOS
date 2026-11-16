# Caso 4: Accesos al aula virtual y calendario de evaluación

## 1. Descripción
Análisis de accesos al aula virtual durante 8 semanas para el equipo de educación virtual. Permite detectar días de alta/baja actividad, relacionarlos con eventos y proponer intervenciones de acompañamiento.

## 2. Requisitos
- Python 3.9+
- pandas, numpy, plotly, streamlit

## 3. Creación del entorno virtual
Ejecutar en la raíz del proyecto:
```bash
python -m venv .venv
```

## 4. Activación de .venv
En Windows (CMD):
```cmd
.venv\Scripts\activate
```
En Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

## 5. Instalación
Con el entorno virtual activado:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Estructura
- `data/`: Datasets.
- `src/`: Scripts de procesamiento.
- `app.py`: Dashboard Streamlit.
- `docs/`: Informes.

## 7. Ejecución
1. Generar los datos sintéticos (solo la primera vez):
```bash
python src/generar_datos.py
```
2. Iniciar el Dashboard:
```bash
streamlit run app.py
```

## 8. Resultados
El dashboard mostrará el mapa de calor, análisis de KPIs e interpretaciones de la actividad estudiantil.

## 9. Desactivación del entorno
```bash
deactivate
```
Esto devuelve la terminal al entorno global, pero NO desinstala las librerías del proyecto.
