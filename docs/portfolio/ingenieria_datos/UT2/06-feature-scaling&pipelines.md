---
title: "Feature Scaling & Pipelines — Ames Housing"
date: 2025-10-11
---

# 🏠 Feature Scaling & Pipelines — Ames Housing

---

## 📘 Contexto  

Práctica de la Unidad 2 del curso de **Ingeniería de Datos (UCU-ID)** centrada en la exploración y escalado de variables numéricas del dataset **Ames Housing**.  
El objetivo fue analizar cómo distintos métodos de **escalado, transformaciones y pipelines** afectan el rendimiento de modelos predictivos sobre el precio de viviendas.  

---

## 🎯 Objetivos  

- Aplicar distintos **scalers** (`StandardScaler`, `RobustScaler`, `MinMaxScaler`, `PowerTransformer`, `QuantileTransformer`) y comparar resultados.  
- Evaluar la influencia de **outliers y transformaciones logarítmicas** sobre el rendimiento.  
- Implementar **pipelines en scikit-learn** para prevenir *data leakage* y validar modelos correctamente.  

---

## ⏱️ Actividades (con tiempos estimados)  

| Actividad | Tiempo estimado | Resultado esperado |
|------------|----------------|--------------------|
| Limpieza y preparación del dataset | 20 min | Datos consistentes y listos para el pipeline |
| Aplicación de distintos scalers | 30 min | Comparar desempeño y estabilidad |
| Transformación logarítmica de columnas sesgadas | 15 min | Reducción de asimetrías y mejora en métricas |
| Validación cruzada y comparación de pipelines | 25 min | Evaluación honesta y detección de leakage |

---

## 🛠️ Desarrollo  

1. Se cargó el dataset **Ames Housing**, con variables continuas (e.g. `GrLivArea`, `TotalBsmtSF`, `LotArea`, `1stFlrSF`) y el target `SalePrice`.  

2. Se aplicaron varios métodos de **escalado**:  
   - `StandardScaler`  
   - `MinMaxScaler`  
   - `RobustScaler`  
   - `PowerTransformer` y `QuantileTransformer` (para variables sesgadas)  

3. Se evaluó el impacto de **tratamiento de outliers y transformaciones logarítmicas** (`np.log1p(SalePrice)`) antes del escalado.  

4. Se implementaron tres enfoques para demostrar el *data leakage*:  
   - **Método 1:** Escalar antes del split (con leakage).  
   - **Método 2:** Split antes del escalado (sin leakage).  
   - **Método 3:** Uso de `Pipeline` con `cross_val_score` (anti-leakage).  

5. Finalmente, se construyó un **pipeline validado con 5-fold CV**, obteniendo un promedio de **accuracy = 0.114 ± 0.026**.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold, cross_val_score

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('modelo', LogisticRegression(max_iter=2000))
])

cv = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(pipe, X, y, cv=cv, scoring='accuracy')
print(cv_scores, cv_scores.mean())
```

---

## 📊 Evidencias 
### 🔹 Comparación de métodos
| Método | Descripción | Accuracy media |
|--------|--------------|----------------|
| 1️⃣ Escalar antes del split *(con leakage)* | Optimista | 0.140 |
| 2️⃣ Split antes de escalar *(correcto)* | Realista | 0.140 |
| 3️⃣ Pipeline con CV *(anti-leakage)* | Honesto y reproducible | 0.114 

### 🔹 Validación final
`Scores = [0.14, 0.075, 0.11, 0.11, 0.135]`  
`Media = 0.114`, `Desvío ≈ 0.026`

### 📝 [Notebook](../../../notebooks/UT2-2.ipynb)

---

## 🤔 Reflexión  

- **Mejor scaler:** `RobustScaler`, por su resistencia a *outliers* en `GrLivArea`, `LotArea`, `TotalBsmtSF`.  
- **Orden de operaciones:** tratar outliers **antes de escalar** dio métricas más estables.  
- **Log transform:** útil en `SalePrice` (target) y variables sesgadas.  
- **Transformadores avanzados:** `PowerTransformer` y `QuantileTransformer` no superaron a los métodos básicos en este caso.  
- **Data leakage:** el método con leakage dio resultados artificialmente optimistas (+22.8%).  
  El **Pipeline** con `cross_val_score` entregó una evaluación más honesta y reproducible.  

---

## 📚 Referencias  

- Práctica: <https://juanfkurucz.com/ucu-id/ut2/06-feature-scaling-pipeline/>  
- Documentación scikit-learn: <https://scikit-learn.org/stable/modules/preprocessing.html>  
- Dataset Ames Housing: *De Cock, D. (2011). Ames, Iowa: Alternative to the Boston Housing Data Set.* 