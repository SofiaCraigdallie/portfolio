---
title: "🔎 UT3 · Práctica 10 — PCA vs Feature Selection en Ames Housing"
date: 2025-11-09
---

# 🔎 PCA vs Feature Selection en Ames Housing

---

# 🌍 Contexto

Esta práctica corresponde a la **Unidad Temática 3: Feature Engineering y Selección** del Portafolio de Ingeniería de Datos.  
Se trabaja con el dataset **Ames Housing** (competencia “House Prices” de Kaggle), un clásico para regresión de precios inmobiliarios.  
El foco es comparar dos caminos para manejar muchas variables: **reducción de dimensionalidad con PCA** vs **selección de variables** (*filter, wrapper, embedded*).

> Meta: entender **cuándo conviene proyectar** (PCA) y **cuándo conviene elegir** (FS), y cómo eso impacta en **desempeño, interpretabilidad y robustez**.

---

# 🎯 Objetivos

- Aplicar **PCA** (tras estandarizar) y evaluar el “codo” de varianza explicada.  
- Probar **Feature Selection** en tres sabores:  
  - *Filter*: `f_regression`, `mutual_info_regression`.  
  - *Wrapper*: `RFE` con estimador base.  
  - *Embedded*: `Lasso (L1)` y **Random Forest** (importancias).  
- **Comparar** con una métrica clara (RMSE, R²) y **justificar** la elección final.  
- Redactar una **reflexión** que conecte el resultado técnico con necesidades de negocio.

---

# 📦 Dataset

| Aspecto | Descripción |
|---|---|
| **Fuente** | Kaggle — *House Prices: Advanced Regression Techniques* |
| **Tarea** | Regresión (`SalePrice`) |
| **Filas/Columnas** | ~1460 × ~80 (varía según versión/limpieza) |
| **Tipos** | Numéricas y categóricas (muchas ordinales) |
| **Problemas típicos** | Valores faltantes, variables altamente correlacionadas, cardinalidad, escalas distintas |

---

# 🧹 Limpieza y preparación

Pasos mínimos esperados:
1. Eliminar `Id`.  
2. Separar `SalePrice` como `y` y el resto como `X`.  
3. **Imputar**: medianas para numéricas, más frecuente para categóricas.  
4. **Codificar** categóricas (rápido: *Label Encoding*; ideal: One-Hot/Target Encoding según pipeline).  
5. **Estandarizar** para PCA / Lasso.

```python
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler

df = pd.read_csv("train.csv").drop(columns=["Id"])
y = df["SalePrice"].copy()
X = df.drop(columns=["SalePrice"]).copy()

num_cols = X.select_dtypes(include=["number"]).columns
cat_cols = X.select_dtypes(exclude=["number"]).columns

X[num_cols] = SimpleImputer(strategy="median").fit_transform(X[num_cols])
X[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(X[cat_cols])

for c in cat_cols:
    X[c] = LabelEncoder().fit_transform(X[c].astype(str))

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # para PCA / Lasso
```

---

# 🧪 Diseño experimental

- **Partición**: `train_test_split(test_size=0.2, random_state=42)`.  
- **Modelos de evaluación**:  
  - PCA + **LinearRegression** sobre PCs.  
  - FS (*filter*, *wrapper*, *embedded*) + **LinearRegression** (para aislar el efecto de la selección).  
- **Métricas**: **RMSE** (principal), **R²** (secundaria).  
- **Comparación**: tabla final con el **mejor** resultado de cada bloque.

---

# 🧩 PCA (Dimensionalidad)

1) Ajustar PCA sobre `X_scaled`.  
2) Graficar **varianza explicada acumulada** y elegir `k` (90%–95%).  
3) Entrenar **LR** sobre las `k` PCs y evaluar.

```python
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

pca = PCA().fit(X_scaled)
cum = np.cumsum(pca.explained_variance_ratio_)

plt.plot(range(1, len(cum)+1), cum, marker="o")
plt.axhline(0.90, ls="--"); plt.axhline(0.95, ls="--")
plt.xlabel("n_components"); plt.ylabel("Explained Variance (cum)"); plt.show()

k = int(np.argmax(cum >= 0.90) + 1)

X_pca = PCA(n_components=k).fit_transform(X_scaled)
Xtr, Xte, ytr, yte = train_test_split(X_pca, y, test_size=0.2, random_state=42)

rmse = mean_squared_error(yte, LinearRegression().fit(Xtr, ytr).predict(Xte), squared=False)
```

---

# 🏷️ Feature Selection

## 1) Filter (barato y rápido)
- **F-test** (`f_regression`): relación lineal.  
- **Mutual information**: relaciones no lineales.

```python
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression

def run_filter(score_func, k):
    sel = SelectKBest(score_func=score_func, k=k).fit(X, y)
    cols = X.columns[sel.get_support()]
    return cols
```

## 2) Wrapper (RFE — más caro, más fino)
- `RFE` con **LinearRegression** o **RandomForestRegressor** como estimador base.  
- Costo: alto (iterativo). Beneficio: selección dirigida por el modelo.

```python
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestRegressor
RFE(LinearRegression(), n_features_to_select=20).fit(X, y)
```

## 3) Embedded
- **Lasso (L1)**: *shrinkage* a cero → selección implícita (necesita escalado).  
- **Random Forest**: ranking por importancias (robusto a escalas y no linealidades).

```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=1e-3, max_iter=20000, random_state=42).fit(X_scaled, y)
selected = [c for c, coef in zip(X.columns, lasso.coef_) if coef != 0]
```

---

# ⚙️ Análisis técnico

- **PCA**: reduce dimensionalidad **mezclando** variables → mejor **robustez** y menos colinealidad; **pierde interpretabilidad** (PCs).  
- **Filter**: simple/rápido, buena primera pasada; puede **ignorar interacciones**.  
- **Wrapper**: más preciso para un modelo específico; **costoso** y puede sobreajustar si no se cuida.  
- **Embedded**: balance entre costo y señal; Lasso da **sparsity** e interpretabilidad; RF capta **no linealidades**.

> Regla de oro rápida:  
> - ¿Querés **explicabilidad**? → **FS** (Lasso/RFE).  
> - ¿Te preocupa **colinealidad y velocidad**? → **PCA** con LR.  
> - ¿Relaciones no lineales**? → RF (importancias) como brújula.

---

# 📊 Resultados y discusión

> **Tabla final — mejores casos de cada bloque**

| Método | k / α | Modelo | RMSE | R² | Notas |
|---|---:|---|---:|---:|---|
| **PCA** | 38 | LR | 26 620 | 0.8859 | PCs ≥80 % var. (79.5 % retenida) |
| **Filter (MI)** | 38 | LR | 26 279 | 0.8891 | Captura relaciones no lineales, rápido y sólido |
| **Wrapper (RFE-LR)** | 19 | LR | — | — | Refinado iterativo; costo alto, mejora marginal |
| **Embedded (Lasso)** | α = 1375.38 | LR | 26 083 | 0.8908 | Sparse + interpretable; mejor rendimiento global |
| **Embedded (RF)** | 38 | LR | 26 238 | 0.8894 | Importancias útiles para ranking no lineal |

> 🏁 **Gana Lasso con 41→38 features:**  
> **RMSE = 26 083**, **R² = 0.8908**.  
> Lo elijo porque mantiene **interpretabilidad**, **baja dimensionalidad** y **supera a PCA** en un set con variables categóricas codificadas.

---

# 🔗 Conexión con otras unidades

- **UT2:** La selección de features mostró qué variables son realmente confiables antes de modelar.  
- **UT4:** Se consolidó un pipeline reproducible, con pasos ordenados y sin fuga de datos.  
- **UT5:** Se evaluó el costo/beneficio entre complejidad computacional e interpretabilidad del modelo.

---

# 🧩 Reflexión final

En mi caso, **Lasso** fue la técnica que mejor equilibró **rendimiento y explicabilidad**.  
Logró un RMSE ≈ 26 k con menos de la mitad de las variables originales, eliminando redundancias y estabilizando el modelo.  
El **PCA** redujo la dimensionalidad sin gran pérdida de precisión, pero sacrificó interpretabilidad: las componentes no tienen sentido directo para negocio.  
Los métodos **filter** y **wrapper** ayudaron a entender la contribución individual de cada feature, aunque los wrappers implican un costo alto para mejoras mínimas.  

En un entorno productivo recomendaría **Lasso o MI** como enfoques base: rápidos, reproducibles y fáciles de justificar frente al cliente.  
Cuidaría especialmente evitar **data leakage** (fitear PCA o selección dentro del pipeline) y monitorearía posibles **overfits** si se combinan con modelos complejos.

---

# 🧰 Stack técnico

**Lenguaje:** Python  
**Librerías:** Pandas · NumPy · Scikit-learn · Matplotlib/Seaborn  
**Conceptos:** PCA · Filter/Wrapper/Embedded FS · RMSE/R² · Estándar de evaluación

### 📝 [Notebook](../../../notebooks/UT3-3.ipynb)

---

# 📚 Referencias

- Guía UT3-10 — PCA & Feature Selection (UCU-ID): <https://juanfkurucz.com/ucu-id/ut3/10-pca-feature-selection/>  
- Scikit-learn: PCA, SelectKBest, RFE, Lasso, RandomForest.  
- Kaggle — *House Prices: Advanced Regression Techniques*.
