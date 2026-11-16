# Informe - Caso 4: Accesos al aula virtual

## 1. Introducción
Este informe presenta el análisis de accesos de estudiantes a un aula virtual durante un periodo de 8 semanas.

## 2. Situación problemática
El equipo de educación virtual requiere planificar recordatorios y la disponibilidad de tutores con base en patrones de actividad en la plataforma.

## 3. Pregunta analítica
¿Qué patrones de actividad del aula virtual se observan durante las ocho semanas y cómo se relacionan temporalmente con los eventos académicos?

## 4. Objetivo
Detectar días de alta y baja actividad, relacionarlos con las evaluaciones y proponer una intervención de acompañamiento adecuada.

## 5. Ficha de datos
- **Fuente**: Datos sintéticos construidos con fines académicos, que integran los registros solicitados para la semana 1 y 2.
- **Unidad de análisis**: Accesos diarios agregados al aula virtual.
- **Variables principales**: Semana, Día, Accesos, Evento Académico.

## 6. CRISP-DM
- **Comprensión**: Identificación de patrones para asignar tutores.
- **Datos**: Generación y revisión inicial de calidad.
- **Preparación**: Limpieza de nulos y atípicos negativos.
- **Modelado visual**: Construcción de un mapa de calor y gráfico de barras.
- **Evaluación**: Revisión de legibilidad y accesibilidad (WCAG 2.2).
- **Comunicación**: Dashboard en Streamlit interactivo.

## 7. Riesgos y Accesibilidad
### Riesgos de interpretación
1. **Asumir causalidad directa**: El incremento de accesos el viernes no implica que el evento causó el 100% de los accesos. Control: Comunicar correlación temporal.
2. **Confusión en la intensidad de color**: Problemas de percepción visual. Control: Uso de escala perceptualmente uniforme (Viridis/Teal) y tooltips.
3. **Pérdida de legibilidad por sobrecarga**: Muchas anotaciones entorpecen la vista. Control: Uso de un indicador sutil (⭐/⚠️) y hover.

### Accesibilidad (WCAG 2.2)
- El color no es el único medio para transmitir información (hay texto y símbolos).
- Contraste adecuado.

## 8. Hallazgos
- Los días con evaluaciones y entregas presentan picos marcados.
- Los fines de semana muestran actividad significativamente reducida.

## 9. Recomendación
- Programar tutorías online intensivas los días previos a grandes picos de acceso.
- Enviar notificaciones de recordatorio en días de baja actividad (ej. martes).

## 10. Limitaciones
- Datos sintéticos agregados, por lo que no se observa la actividad a nivel de usuario individual. No se puede medir causalidad.
