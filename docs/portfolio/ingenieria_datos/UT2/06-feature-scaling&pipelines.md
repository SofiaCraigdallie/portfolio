---
title: "🏠 Feature Scaling & Pipelines — Ames Housing"
date: 2025-10-11
---

# 🏠 Feature Scaling & Pipelines — Ames Housing

---

# 🌍 Contexto

Este proyecto forma parte de la **Unidad Temática 2: Calidad y Ética de los Datos**, enfocada en garantizar la consistencia y preparación adecuada de las variables antes del modelado.  
El objetivo fue evaluar cómo distintos **métodos de escalado y transformaciones numéricas** afectan el rendimiento de modelos predictivos, destacando la importancia de evitar *data leakage* mediante el uso de **pipelines** en `scikit-learn`.

Se trabajó con el dataset **Ames Housing**, un conjunto de datos realista que describe propiedades inmobiliarias en Iowa, incluyendo superficie, número de habitaciones, área del sótano y precio de venta.

---

# 🎯 Objetivos

- Aplicar diferentes **scalers** (`StandardScaler`, `RobustScaler`, `MinMaxScaler`, `PowerTransformer`, `QuantileTransformer`) y comparar su desempeño.  
- Analizar el impacto de **outliers** y **transformaciones logarítmicas** sobre las variables.  
- Implementar **pipelines reproducibles** que eviten fugas de información (*data leakage*).  
- Evaluar el rendimiento de los modelos con **validación cruzada (cross-validation)**.  

---

# 📦 Dataset

| Aspecto | Descripción |
|----------|-------------|
| **Fuente** | [Práctica oficial — Feature Scaling & Pipelines](https://juanfkurucz.com/ucu-id/ut2/06-feature-scaling-pipeline/) |
| **Dataset** | Ames Housing Dataset |
| **Variables** | `GrLivArea`, `TotalBsmtSF`, `LotArea`, `1stFlrSF`, `SalePrice` |
| **Problemas esperados** | Outliers, asimetrías en la distribución y escalas dispares entre variables. |
| **Tamaño** | ~1 500 registros · 80 columnas. |

---

# 🧹 Limpieza y preparación de datos

1. Eliminación de columnas irrelevantes y normalización de nombres.  
2. Tratamiento de valores atípicos en `GrLivArea`, `LotArea` y `TotalBsmtSF`.  
3. Aplicación de transformaciones logarítmicas en variables sesgadas y en el target (`SalePrice`).  
4. Separación en variables predictoras `X` y variable objetivo `y`.

```python
import numpy as np
import pandas as pd

df["SalePrice_log"] = np.log1p(df["SalePrice"])
X = df[["GrLivArea", "TotalBsmtSF", "LotArea", "1stFlrSF"]]
y = df["SalePrice_log"]
```

---

# ⚙️ Escalado y construcción del pipeline

Se compararon distintos **scalers** de `scikit-learn` y su impacto en la estabilidad de los modelos:

| Scaler | Características | Observaciones |
|--------|-----------------|----------------|
| `StandardScaler` | Centra media y desvía por σ | Afectado por outliers |
| `MinMaxScaler` | Escala entre 0 y 1 | Sensible a valores extremos |
| `RobustScaler` | Usa mediana e IQR | Más resistente a outliers |
| `PowerTransformer` | Aplica transformación Box-Cox/Yeo-Johnson | Mejora distribuciones sesgadas |
| `QuantileTransformer` | Uniformiza distribuciones | Puede distorsionar relaciones lineales |

💡 Se evaluaron tres configuraciones de pipeline para demostrar el impacto del *data leakage*:

1. **Escalado antes del split →** genera *leakage* (optimismo artificial).  
2. **Split antes del escalado →** resultado más realista.  
3. **Pipeline con `cross_val_score` →** solución reproducible y ética.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold, cross_val_score

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LinearRegression())
])

cv = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(pipe, X, y, cv=cv, scoring="r2")
print(cv_scores, cv_scores.mean())
```

---

# 📈 Evidencias y resultados

### 🔹 Comparación de métodos de escalado

| Método | Descripción | Accuracy media |
|--------|--------------|----------------|
| 1️⃣ Escalar antes del split *(con leakage)* | Optimista | 0.140 |
| 2️⃣ Split antes de escalar *(correcto)* | Realista | 0.140 |
| 3️⃣ Pipeline con CV *(anti-leakage)* | Honesto y reproducible | 0.114 |

### 🔹 Validación cruzada

`Scores = [0.14, 0.075, 0.11, 0.11, 0.135]`  
`Media = 0.114 ± 0.026`

📊 **Interpretación:**  
El *pipeline* con validación cruzada entrega una evaluación más honesta, evitando fugas de información entre entrenamiento y prueba.

### 📝 [Notebook](../../../notebooks/UT2-2.ipynb)

---

# 🧠 Resultados y discusión

| Hallazgo | Interpretación |
|-----------|----------------|
| **Mejor scaler:** `RobustScaler` | Minimiza la influencia de outliers y mantiene estabilidad. |
| **Transformaciones logarítmicas** | Reducen asimetría y mejoran la correlación con el target. |
| **Pipeline anti-leakage** | Garantiza reproducibilidad y evaluación justa. |
| **Escalado correcto** | Es un paso esencial antes del entrenamiento y comparación de modelos. |

> 💬 **Discusión:**  
> El *data leakage* es uno de los errores más comunes en ciencia de datos aplicada.  
> Este ejercicio mostró que un pipeline bien diseñado no solo mejora la calidad técnica, sino también la **ética del proceso analítico**, al evitar conclusiones basadas en datos contaminados.

---

# 🔗 Conexión con otras unidades

- **UT1:** Continúa la exploración y limpieza de datos, ahora con foco en consistencia numérica.  
- **UT3:** Introduce las bases para el *feature engineering* reproducible.  
- **UT5:** Este pipeline será escalable a entornos ETL y Spark.

---

# 🧩 Reflexión final

El escalado y la preparación de datos no son tareas triviales:  
determinan la **robustez y transparencia** de todo el modelo.  
Implementar pipelines reproducibles reduce errores humanos, asegura comparabilidad y refuerza buenas prácticas éticas.

---

# 🧰 Stack técnico

**Lenguaje:** Python  
**Librerías:** Pandas · NumPy · Scikit-learn  
**Conceptos aplicados:** Escalado · Pipeline · Data Leakage · Validación Cruzada  

---

# 📚 Referencias

- Práctica: <https://juanfkurucz.com/ucu-id/ut2/06-feature-scaling-pipeline/>  
- [Documentación Scikit-learn – Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)  
- De Cock, D. (2011). *Ames, Iowa: Alternative to the Boston Housing Data Set.*