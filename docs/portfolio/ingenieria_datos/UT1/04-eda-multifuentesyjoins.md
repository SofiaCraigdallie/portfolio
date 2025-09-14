---
title: "EDA Multi-fuentes y Joins"
date: 2025-01-20
---

# EDA con múltiples fuentes y joins 🔗

## Resumen
Análisis exploratorio integrando datos de viajes y zonas mediante operaciones de **join**. Se buscó comprender cómo la combinación de múltiples fuentes enriquece el análisis, detectando patrones de revenue, propinas y diferencias por boroughs.

## Contexto
Práctica de **Análisis Exploratorio de Datos** centrada en la integración de múltiples datasets mediante **joins** (INNER, LEFT). Se trabajó principalmente con datos de viajes (trips) y zonas (zones).

## Objetivos
- Practicar la combinación de datasets con `pandas.merge`.
- Comparar diferencias entre `LEFT JOIN` e `INNER JOIN`.
- Analizar problemas comunes al unir datos de fechas/IDs.
- Detectar patrones de negocio a partir de los datos integrados.

## Actividades (con tiempos estimados)
- Carga y exploración inicial de datasets — 20 min  
- Implementación de LEFT y INNER JOINs — 25 min  
- Detección de inconsistencias en fechas y formatos — 15 min  
- Análisis de revenue, propinas y patrones por borough — 30 min  

## Desarrollo
Se realizaron merges entre el dataset de viajes y el de zonas.  
- Con **LEFT JOIN** se preservó la información completa de los viajes, evitando pérdida de datos al tener zonas faltantes.  
- Con **INNER JOIN** se observó cómo algunos viajes quedaban fuera del análisis.  
- Se identificaron posibles problemas de join por diferencias en tipos de datos y formatos (IDs y fechas).

Finalmente, el análisis integrado mostró (a modo ilustrativo):
- **Manhattan** concentra la mayor parte de los viajes.  
- En **Queens**, los viajes tienden a ser más largos y costosos.  
- El **revenue por km** puede resaltar zonas específicas (ej. EWR).  
- Diferencias en la **tasa de propinas** y en días especiales con impacto en distancia y tarifa promedio.

## Evidencias
### Comparación de JOINs
![Join Example](../../assets/img/joins_comparacion.png)


- El **LEFT JOIN** conserva más registros (viajes sin zona asignada).  
- El **INNER JOIN** elimina esos casos.

### Revenue y propinas por borough
![Revenue Propinas](../../assets/img/revenue_propinas.png)

- Comparativa de **revenue por km** y **tasa de propinas** por borough.  
- Útil para priorizar zonas o diseñar campañas.

## Reflexión
Integrar múltiples fuentes enriquece el análisis y habilita **insights** más profundos. La correcta elección del tipo de join es clave para no perder información relevante.  
Siguiente paso sugerido: automatizar el pipeline (ej. Prefect) y versionar datos (DVC).

## Referencias
- Práctica: <https://juanfkurucz.com/ucu-id/ut1/04-eda-multifuentes-joins/>  
- pandas merge: <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html>