---
title: "🧩 Ingeniería de Features — Mejorando el modelo de Ames Housing"
date: 2025-10-11
---

# 🧩 Ingeniería de Features

---

# 🌍 Contexto

Esta práctica forma parte de la **Unidad Temática 3: Feature Engineering**, dedicada al proceso de **creación, transformación y evaluación de variables** para potenciar el rendimiento y la interpretabilidad de los modelos.  

Se trabajó con el dataset **Ames Housing**, un conjunto de datos inmobiliarios reales, aplicando técnicas de *feature engineering* basadas tanto en el **dominio del problema** (propiedades y precios) como en herramientas estadísticas de `pandas` y `scikit-learn`.  
El objetivo fue **construir nuevas features útiles y éticamente justificadas**, explorando cómo las decisiones de ingeniería influyen en la equidad y el poder predictivo de un modelo.

---

# 🎯 Objetivos

- Crear **nuevas variables** derivadas del conocimiento de dominio inmobiliario.  
- Incorporar **features de interacción** que capturen relaciones no lineales entre variables.  
- Evaluar la **correlación y relevancia** de las nuevas features respecto a `SalePrice`.  
- Comparar el comportamiento entre **datos sintéticos y reales**.  
- Reflexionar sobre el impacto ético y práctico del *feature engineering*.

---

# 📦 Dataset

| Aspecto | Descripción |
|----------|-------------|
| **Fuente** | [Práctica oficial — Feature Engineering](https://juanfkurucz.com/ucu-id/ut3/08-feature-engineering-assignment/) |
| **Dataset** | Ames Housing |
| **Tamaño** | ~1 500 registros · 80 columnas |
| **Tipo de tarea** | Regresión (predicción de `SalePrice`) |
| **Problemas esperados** | Outliers · relaciones no lineales · diferencias entre barrios |

---

# 🧹 Limpieza y preparación

1. **Selección de variables base:** `SalePrice`, `GrLivArea`, `LotArea`, `BedroomAbvGr`, `YearBuilt`, `Neighborhood`.  
2. **Normalización de tipos** y tratamiento de nulos.  
3. **Creación de variables auxiliares** (`price_per_sqft`, `property_age`).  
4. Aplicación de transformaciones básicas (`np.log1p`) y escalado preliminar.

```python
import pandas as pd
import numpy as np

ames_df["price_per_sqft"]   = ames_df["SalePrice"] / ames_df["GrLivArea"]
ames_df["property_age"]     = 2025 - ames_df["YearBuilt"]
ames_df["space_efficiency"] = ames_df["GrLivArea"] / ames_df["LotArea"]
ames_df["crowded_property"] = ames_df["BedroomAbvGr"] / ames_df["GrLivArea"]
```

---

# ⚙️ Creación de nuevas features

## 🔹 Features de dominio

| Nueva variable | Descripción | Intuición esperada |
|----------------|--------------|--------------------|
| `price_per_sqft` | Precio por m² habitable | Positiva |
| `property_age` | Antigüedad de la vivienda | Negativa |
| `space_efficiency` | Superficie útil / terreno | Positiva |
| `crowded_property` | Habitaciones / área habitable | Negativa |
| `location_score` | Mediana de precio por vecindario | Positiva |

Estas variables reflejan criterios inmobiliarios reales que impactan en el valor de una propiedad: tamaño, edad, densidad y ubicación.

---

## 🔹 Features de interacción

Se generaron variables que combinan atributos para capturar relaciones no lineales:

```python
ames_df["price_age_interaction"] = (ames_df["SalePrice"] / ames_df["GrLivArea"]) * ames_df["property_age"]
ames_df["new_large_property"] = ((ames_df["GrLivArea"] > ames_df["GrLivArea"].quantile(0.75)) &
                                 (ames_df["YearBuilt"] > ames_df["YearBuilt"].quantile(0.75))).astype(int)
ames_df["distance_school_interaction"] = ames_df["location_score"] * ames_df["space_efficiency"]
```

> 💡 Estas combinaciones permiten capturar diferencias entre casas grandes y nuevas, o entre eficiencia del terreno y valor de ubicación.

---

# 📈 Evidencias

### 🔹 Correlaciones con el precio (`SalePrice`)

| Feature | Correlación |
|----------|-------------|
| `price_per_sqft` | 0.82 |
| `space_efficiency` | 0.61 |
| `property_age` | −0.55 |
| `crowded_property` | −0.47 |
| `location_score` | 0.44 |

**Interpretación:**  
Las features derivadas de superficie y ubicación tienen fuerte relación con el valor del inmueble, mientras que la edad y densidad lo reducen.

### 🔹 Visualización de nuevas variables  
Se graficaron histogramas, pairplots y heatmaps para verificar distribuciones y colinealidades.  
Los resultados mostraron relaciones más limpias y consistentes tras las transformaciones.

### 📝 [Notebook](../../../notebooks/UT3-1.ipynb)

---

# 🧠 Resultados y discusión

| Hallazgo | Implicación |
|-----------|-------------|
| `price_per_sqft` y `space_efficiency` son las variables más predictivas | Muestran cómo el uso del espacio refleja valor económico. |
| Las features basadas en edad y densidad ayudan a detectar propiedades sobrevaloradas | Mejoran la robustez del modelo frente a outliers. |
| `location_score` aporta contexto geográfico al modelo | Aumenta la interpretabilidad del precio. |

> 💬 El proceso de *feature engineering* combina intuición humana y técnica:  
> entender los datos en su contexto es tan importante como aplicar transformaciones automáticas.

---

# 🔗 Conexión con otras unidades

- **UT1:** los patrones detectados en EDA inspiran qué variables derivar.  
- **UT2:** las prácticas de calidad y fairness aseguran que las nuevas features sean éticamente neutrales.  
- **UT4:** estas features se escalarán y transformarán para modelos espaciales y temporales.  

---

# 🧩 Reflexión final

El *feature engineering* es la etapa donde los datos “cobran significado”.  
Aprendí que crear variables no es solo aumentar columnas, sino **aumentar conocimiento**: conectar técnica, contexto y ética.  
Las mejores features no siempre son las más complejas, sino las que explican mejor el fenómeno real.

---

# 🧰 Stack técnico

**Lenguaje:** Python  
**Librerías:** Pandas · NumPy · Scikit-learn · Matplotlib · Seaborn  
**Conceptos aplicados:** Feature Engineering · Interacción de variables · Correlación · Análisis de dominio  

---

# 📚 Referencias

- Práctica: <https://juanfkurucz.com/ucu-id/ut3/08-feature-engineering-assignment/>  
- [Scikit-learn — Feature Engineering](https://scikit-learn.org/stable/modules/compose.html)  
- Dataset: De Cock, D. (2011). *Ames, Iowa: Alternative to the Boston Housing Data Set.*