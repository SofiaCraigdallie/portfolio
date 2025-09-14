---
title: "EDA Multi-fuentes y Joins"
date: 2025-01-20
---

# 🔗 EDA con múltiples fuentes y joins  

---

## 📘 Contexto  

Práctica de **Análisis Exploratorio de Datos** enfocada en integrar múltiples datasets mediante **joins** (`pandas.merge`).  
Se trabajó principalmente con:  
- Dataset de viajes (*trips*).  
- Dataset de zonas (*zones*).  

El objetivo fue analizar cómo la combinación de fuentes enriquece el análisis y qué problemas pueden surgir en la unión de datos.  

---

## 🎯 Objetivos  

- Practicar la combinación de datasets con `pandas.merge`.  
- Comparar diferencias entre `LEFT JOIN` e `INNER JOIN`.  
- Identificar problemas comunes (tipos de datos, IDs, fechas).  
- Detectar patrones de negocio a partir de datos integrados.  

---

## ⏱️ Actividades (con tiempos estimados)  

| Actividad | Tiempo estimado | Resultado esperado |
|-----------|-----------------|--------------------|
| Carga y exploración inicial de datasets | 20 min | Comprender estructura de *trips* y *zones* |
| Implementación de LEFT e INNER JOINs | 25 min | Integración de datasets |
| Detección de inconsistencias | 15 min | Identificación de problemas de join |
| Análisis de revenue, propinas y patrones | 30 min | Insights de negocio por borough |

---

## 🛠️ Desarrollo  

1. **Carga de datasets**  
```python
import pandas as pd

trips = pd.read_csv("trips.csv")
zones = pd.read_csv("zones.csv")

print(trips.head())
print(zones.head())
```

2. **Left Join** se preservó la información completa de los viajes, evitando pérdida de datos al tener zonas faltantes. 
```python
left_join = trips.merge(zones, how="left", left_on="pulocationid", right_on="locationid")
left_join.head()
```

3. **Inner Join** se observó cómo algunos viajes quedaban fuera del análisis.
```python
inner_join = trips.merge(zones, how="inner", left_on="pulocationid", right_on="locationid")
inner_join.head()
```
  
4. **Problemas comunes detectados**  
- Diferencias en tipos de datos (`int` vs `string`).  
- Fechas en distintos formatos (`YYYY-MM-DD` vs `MM/DD/YYYY`).  
- IDs faltantes en el dataset de zonas.  

5. **Análisis de negocio: revenue y propinas por borough**
```python
group = left_join.groupby("borough_pick", dropna=False).agg(
    viajes=("pulocationid","size"),
    revenue_total=(lambda x: (left_join.loc[x.index,'fare_amount'] 
                            + left_join.loc[x.index,'tip_amount']).sum()),
    distancia_total=("trip_distance","sum"),
    tip_total=("tip_amount","sum")
)

group["revenue_por_km"] = group["revenue_total"] / group["distancia_total"].replace(0, pd.NA)
group["tip_rate"] = group["tip_total"] / group["revenue_total"].replace(0, pd.NA)

display(group)
```

Finalmente, el análisis integrado mostró (a modo ilustrativo):
- **Manhattan** concentra la mayor parte de los viajes.  
- En **Queens**, los viajes tienden a ser más largos y costosos.  
- El **revenue por km** puede resaltar zonas específicas (ej. EWR).  
- Diferencias en la **tasa de propinas** y en días especiales con impacto en distancia y tarifa promedio.

---

## 📊 Evidencias 
### 🔹 Comparación de JOINs 
![Join Example](../assets/img/joins_comparacion.png)

- El **LEFT JOIN** conserva más registros (viajes sin zona asignada).  
- El **INNER JOIN** elimina esos casos.

### 🔹 Revenue y propinas por borough  
![Revenue Propinas](../assets/img/revenue_propinas.png)

- Comparativa de **revenue por km** y **tasa de propinas** por borough.  
- Útil para priorizar zonas o diseñar campañas.

---

## 🤔 Reflexión  

- Integrar múltiples fuentes enriquece el análisis y permite encontrar **insights de negocio más profundos**.  
- La elección correcta del tipo de join es fundamental:  
  - **LEFT JOIN** evita pérdida de información.  
  - **INNER JOIN** asegura consistencia en los registros.  
- Futuro trabajo:  
  - Automatizar el pipeline con **Prefect**.  
  - Versionar datos con **DVC** para mejorar reproducibilidad.  

---

## 📚 Referencias  

- Práctica: <https://juanfkurucz.com/ucu-id/ut1/04-eda-multifuentes-joins/>  
- [pandas merge](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html) 