---
title: "Exploración del dataset Iris"
date: 2025-01-10
---

# Exploración del dataset Iris 🌸

## Resumen
Exploración de relaciones entre variables del dataset **Iris** para identificar patrones de separabilidad entre especies mediante visualizaciones básicas (pairplot y correlaciones).

## Contexto
Práctica introductoria de Análisis Exploratorio de Datos (EDA) con un dataset clásico de ML (Fisher, 1936).

## Objetivos
- Visualizar relaciones entre variables numéricas y especies.
- Detectar correlaciones relevantes y posibles redundancias.
- Justificar qué variables aportan mayor poder de discriminación.

## Actividades (con tiempos estimados)
- Carga/limpieza y descripción inicial — 15 min  
- Pairplot por especie — 20 min  
- Heatmap de correlación — 15 min  

## Desarrollo
Se cargaron los datos y se revisaron estadísticas básicas (media, desvío, rangos).  
Con `seaborn.pairplot` se observaron relaciones bivariadas por especie. Las variables de **pétalo** muestran mejor separación de clases (especialmente *setosa*).  
Con un **mapa de calor** de correlaciones se detectó alta correlación entre `petal_length` y `petal_width`, sugiriendo posible redundancia.

## Evidencias
### Pairplot
![Pairplot Iris](../../assets/img/iris_pairplot.png)

- Las variables de pétalo separan bien las especies.  
- `sepal_length` y `sepal_width` presentan mayor solapamiento.

### Heatmap de correlación
![Heatmap Iris](../../assets/img/iris_corr.png)

- Correlación alta entre `petal_length` y `petal_width`.  
- Variables de sépalo aportan menos discriminación.

## Reflexión
La elección de variables es clave incluso antes de modelar. Un siguiente paso sería entrenar un clasificador simple (KNN o Random Forest) para cuantificar la separabilidad observada.

## Referencias
- Práctica: <https://juanfkurucz.com/ucu-id/ut1/01-exploracion-iris/>  
- Documentación seaborn: <https://seaborn.pydata.org/>  
