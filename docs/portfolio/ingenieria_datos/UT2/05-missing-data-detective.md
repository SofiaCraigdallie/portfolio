---
title: "🕵️ Missing Data Detective: detección y tratamiento de datos faltantes"
date: 2025-01-28
---

# 🕵️ Missing Data Detective: detección y tratamiento de datos faltantes

# 🌍 Contexto

Esta práctica forma parte de la **Unidad Temática 2: Calidad y Ética de los Datos**, donde se abordan los problemas de **completitud y confiabilidad** de la información.  
El objetivo es aprender a detectar, analizar y tratar **valores faltantes y outliers**, comprendiendo su impacto en el análisis posterior y garantizando la reproducibilidad mediante pipelines de limpieza.

El ejercicio utiliza escenarios con distintos mecanismos de ausencia (MCAR, MAR y MNAR) y muestra cómo aplicar estrategias de imputación controlada, documentando el proceso de forma transparente y ética.

---

# 🎯 Objetivos

- Detectar y clasificar valores faltantes según su mecanismo (MCAR, MAR, MNAR).  
- Identificar outliers mediante métodos estadísticos (IQR, z-score).  
- Aplicar estrategias de imputación apropiadas (media, mediana, forward/backward fill).  
- Diseñar un **pipeline reproducible de limpieza** en Python.  
- Reflexionar sobre las **implicaciones éticas** del tratamiento de datos incompletos.

---

# 📦 Dataset

| Aspecto | Descripción |
|----------|-------------|
| **Fuente** | [Práctica oficial – Missing Data Detective](https://juanfkurucz.com/ucu-id/ut2/05-missing-data-detective/) |
| **Formato** | CSV |
| **Tamaño** | ~1 000 observaciones × 20 variables |
| **Problemas esperados** | Faltantes, outliers y correlaciones alteradas tras la imputación. |
| **Escenario** | Datos simulados con distintos mecanismos de ausencia (MCAR, MAR, MNAR). |

---

# 🧹 Limpieza y preparación de datos

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("dataset_missing.csv")

# Conteo y visualización de nulos
print(df.isna().sum())
sns.heatmap(df.isna(), cbar=False)
plt.title("Mapa de valores faltantes")
plt.show()
```

📈 **Interpretación:**  
Se detectaron columnas con alta proporción de valores faltantes, principalmente en variables numéricas relacionadas con superficie y precio.

---

# 📊 Análisis exploratorio de ausencias

Los valores faltantes pueden clasificarse según su mecanismo:

- **MCAR (Missing Completely at Random):** ausencia totalmente aleatoria.  
- **MAR (Missing At Random):** depende de otras variables observadas.  
- **MNAR (Missing Not At Random):** depende del propio valor faltante.

📘 **Ejemplo práctico:**  
Se comprobó que las ausencias en `GarageArea` correlacionaban con el tipo de vivienda → mecanismo **MAR**.

---

# ⚙️ Identificación de outliers

```python
import numpy as np

Q1 = df["columna"].quantile(0.25)
Q3 = df["columna"].quantile(0.75)
IQR = Q3 - Q1

outliers = df[(df["columna"] < Q1 - 1.5*IQR) | (df["columna"] > Q3 + 1.5*IQR)]
outliers.shape
```

📊 **Interpretación:**  
Los valores atípicos se concentraron en variables como `SalePrice` y `LotArea`.  
El IQR resultó más estable que el z-score frente a distribuciones sesgadas.

---

# 🧠 Imputación de valores

```python
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy="median")
df["columna"] = imputer.fit_transform(df[["columna"]])
```

💡 **Estrategias evaluadas:**  
- **Media / Mediana:** adecuadas para distribuciones simétricas.  
- **Forward / Backward Fill:** útiles en series temporales.  
- **Modelo predictivo (no aplicado aquí):** opción avanzada en futuras unidades.

La imputación con **mediana** mantuvo la forma original de la distribución y minimizó el sesgo.

---

# 🧩 Pipeline reproducible

Se desarrolló un conjunto de funciones modulares para:  
1. Detectar nulos y calcular porcentajes.  
2. Imputar columnas según estrategia configurable.  
3. Validar la completitud final y guardar el reporte.  

Este pipeline permite replicar la limpieza en nuevos datasets con los mismos pasos.

---

# 📈 Evidencias visuales

### 🔹 Patrones de datos faltantes  
![Patrones de missing](../../../assets/img/missing_patterns.png)  
> Columnas con mayor proporción de nulos y distribución de registros incompletos.

### 🔹 Outliers detectados  
![Outliers](../../../assets/img/outliers_analysis.png)  
> Detección mediante boxplots e IQR en variables como `SalePrice`, `LotArea`, `GarageArea`.

### 🔹 Distribución antes y después de imputación  
![Distribución imputación](../../../assets/img/distribution_comparison.png)  
> La imputación con mediana preservó la forma general de la distribución.

### 🔹 Correlaciones originales vs imputadas  
![Correlaciones](../../../assets/img/correlation_comparison.png)  
> Poca variación en las correlaciones → imputación estable.

### 📝 [Notebook](../../../notebooks/UT2-1.ipynb)

---

# 🧠 Resultados y discusión

| Aspecto | Hallazgo | Interpretación |
|----------|-----------|----------------|
| Mecanismo MAR predominante | Ausencias ligadas al tipo de vivienda | No aleatorias → deben imputarse con contexto |
| Imputación con mediana | Estable y no distorsiona correlaciones | Adecuada para datos asimétricos |
| Outliers controlados | Reducción de sesgo en métricas | Evita sesgos en modelos posteriores |
| Pipeline reproducible | Limpieza transparente y trazable | Mejora la calidad y ética del proceso |

> 💬 **Discusión:**  
> La imputación es tanto un desafío técnico como ético: reemplazar valores implica asumir supuestos que deben documentarse.  
> Una buena práctica es conservar los indicadores de imputación para futuras auditorías.

---

# 🔗 Conexión con otras unidades

- **UT1:** Amplía el análisis exploratorio incorporando la dimensión de calidad y completitud.  
- **UT3:** La limpieza reproducible mejora el proceso de *Feature Engineering*.  
- **UT5:** El pipeline podrá integrarse en un flujo ETL automatizado.

---

# 🧩 Reflexión final

Comprendí que los valores faltantes no son solo “errores”, sino **información en sí mismos**.  
El reto está en tratarlos sin distorsionar la realidad ni introducir sesgos ocultos.  
El equilibrio entre completitud, precisión y ética es clave en la ingeniería de datos.

---

# 🧰 Stack técnico

**Lenguaje:** Python  
**Librerías:** Pandas · Seaborn · Matplotlib · NumPy · Scikit-learn  
**Conceptos aplicados:** MCAR-MAR-MNAR · Imputación · Outliers · Pipeline reproducible  

---

# 📚 Referencias

- Práctica: <https://juanfkurucz.com/ucu-id/ut2/05-missing-data-detective/>  
- Little, R. J. A. & Rubin, D. B. (2019). *Statistical Analysis with Missing Data.*  
- [scikit-learn Imputers](https://scikit-learn.org/stable/modules/impute.html)