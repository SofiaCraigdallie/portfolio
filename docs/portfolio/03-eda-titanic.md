---
title: "EDA de Netflix con pandas"
date: 2025-01-12
---

# EDA de Netflix con pandas 🎬

## Resumen
Análisis exploratorio de un dataset de **Netflix** usando `pandas`. 
Se examinan dimensiones del dataset, valores faltantes, distribuciones y cortes por categorías (por ejemplo, tipo de contenido y país).

## Contexto
Práctica de EDA enfocada en manipulación con `pandas` y visualizaciones base. El objetivo es comprender la estructura del dataset y encontrar patrones iniciales para futuras preguntas de negocio.

## Objetivos
- Auditar el dataset (columnas, dtypes, nulos, duplicados).
- Visualizar distribuciones relevantes (p. ej., por año de lanzamiento y tipo).
- Extraer insights preliminares (países más frecuentes, top géneros, etc.).

## Actividades (con tiempos estimados)
- Auditoría de datos (`info`, `describe`, nulos, duplicados) — 20 min  
- Limpieza mínima (casts a fechas, estandarización básica) — 20 min  
- Visualizaciones y tablas resumen — 30 min  

## Desarrollo
Se revisaron tipos de datos y se identificaron **valores nulos** en campos como `director`, `cast` o `country`.  
Se realizó una limpieza mínima (parseo de fechas y normalización simple de categorías).  
Se generaron gráficos y tablas de frecuencia para comprender:
- Evolución de lanzamientos por año.  
- Distribución por **type** (Movies vs TV Shows).  
- Países con mayor cantidad de títulos.

## Evidencias

### Dashboard final interactivo
![Dashboard](../assets/img/netflix_dashboard.png)

## Reflexión
El EDA inicial ayuda a definir preguntas más específicas (p. ej., ¿ciertas categorías crecieron más en los últimos años?, ¿existe sesgo geográfico por país?).  
Próximos pasos: enriquecer con features (p. ej., extracción de año/mes), y explorar relaciones entre **rating**, **duración** y **tipo**.

## Referencias
- Práctica: <https://juanfkurucz.com/ucu-id/ut1/03-eda-netflix-pandas/>  
- Documentación pandas: <https://pandas.pydata.org/docs/>  
- Documentación matplotlib: <https://matplotlib.org/stable/>  
