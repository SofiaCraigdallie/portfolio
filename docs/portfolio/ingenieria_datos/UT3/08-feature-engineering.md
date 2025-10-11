---
title: "Feature Engineering — Ames Housing"
date: 2025-10-11
---

# 🧩 Feature Engineering — Ames Housing

---

## 📘 Contexto  

Práctica de la **Unidad 3 (UT3)** del curso de Ingeniería de Datos, enfocada en el **proceso de creación y evaluación de nuevas features**.  
Se utilizó el dataset **Ames Housing**, aplicando criterios de dominio inmobiliario y técnicas avanzadas de *feature engineering* para mejorar el rendimiento predictivo y la interpretabilidad de los modelos.

---

## 🎯 Objetivos  

- Crear **nuevas variables** basadas en el dominio inmobiliario (espacio, eficiencia, edad, ubicación).  
- Desarrollar **features de interacción** que combinen múltiples variables relevantes.  
- Evaluar la **importancia y correlación** de las nuevas features con el precio (`SalePrice`).  
- Comparar **datos sintéticos vs. datos reales** y reflexionar sobre sus diferencias.  

---

## ⏱️ Actividades (con tiempos estimados)  

| Actividad | Tiempo estimado | Resultado esperado |
|------------|----------------|--------------------|
| Creación de features de dominio | 30 min | Variables con sentido económico y espacial |
| Generación de features de interacción | 25 min | Capturar relaciones no lineales entre atributos |
| Análisis de correlaciones y visualizaciones | 20 min | Identificar impacto de las nuevas features |
| Prueba con datos reales de Ames | 25 min | Validar la aplicabilidad en escenarios reales |

---

## 🛠️ Desarrollo  

1. Se partió de un dataset limpio con columnas como `SalePrice`, `GrLivArea`, `LotArea`, `BedroomAbvGr`, `YearBuilt` y `Neighborhood`.  

2. Se crearon features de **dominio inmobiliario**:
   - `space_efficiency = GrLivArea / LotArea` → mide eficiencia del uso del terreno.  
   - `crowded_property = TotRmsAbvGrd / GrLivArea` → indica densidad de habitaciones.  
   - `location_score` → basado en la mediana de precio por vecindario.  

3. Se construyeron **features de interacción**:
   - `price_age_interaction = (SalePrice/GrLivArea) * age`  
   - `new_large_property` (1 si está en el cuartil superior de tamaño y año).  
   - `distance_school_interaction = location_score * space_efficiency`.

4. Se evaluaron correlaciones con `SalePrice` y se graficaron distribuciones de las nuevas features.

5. Finalmente, se aplicaron las mismas transformaciones a una **muestra real** de Ames Housing para validar los resultados.

```python
import pandas as pd
import numpy as np

ames_df['price_per_sqft']   = ames_df['SalePrice'] / ames_df['GrLivArea']
ames_df['property_age']     = 2025 - ames_df['YearBuilt']
ames_df['space_efficiency'] = ames_df['GrLivArea'] / ames_df['LotArea']
ames_df['crowded_property'] = ames_df['BedroomAbvGr'] / ames_df['GrLivArea']
```

---

## 📊 Evidencias  
### 🔹 Nuevas features principales
| Feature | Significado | Esperado efecto sobre precio |
|----------|--------------|------------------------------|
| `price_per_sqft` | Valor del m² habitable | Positivo |
| `property_age` | Antigüedad de la vivienda | Negativo |
| `space_efficiency` | Relación superficie/lote | Positivo |
| `crowded_property` | Densidad de habitaciones | Negativo |
| `location_score` | Calidad promedio del vecindario | Positivo |

### 🔹 Correlaciones (ejemplo con muestra)
| Feature | Correlación con `SalePrice` |
|----------|------------------------------|
| price_per_sqft | 0.82 |
| space_efficiency | 0.61 |
| property_age | -0.55 |
| crowded_property | -0.47 |
| location_score | 0.44 |

### 📝 [Notebook](../../../notebooks/UT3-1.ipynb)

---

## 🤔 Reflexión  

- **Features más importantes:** `price_per_sqft`, `location_score`, `property_age`.  
- **Sorpresas:** propiedades pequeñas o antiguas con alto precio por ubicación.  
- **Mejoras posibles:** usar selección automática de features y normalización logarítmica.  
- **Técnicas adicionales:** `PolynomialFeatures`, *Target Encoding*, *Binning*, *PCA*, *One-Hot Encoding*.  
- **Diferencias entre sintéticos y reales:** los datos reales presentan outliers, ruido y correlaciones más complejas, requiriendo escalado robusto y pipelines más cuidados.

---

## 📚 Referencias  

- Práctica: <https://juanfkurucz.com/ucu-id/ut3/08-feature-engineering-assignment/>  
- Documentación scikit-learn: <https://scikit-learn.org/stable/modules/compose.html>  
- Dataset: *Ames Housing — De Cock, D. (2011). Alternative to the Boston Housing Data Set.*  