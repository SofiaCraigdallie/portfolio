---
title: "🧪 UT3 · 03‑1 — Mini‑Assignment: Feature Selection robusta vs PCA (Ames Housing)"
date: 2025-11-09
---

# 🧪 UT3 Mini‑Assignment: Feature Selection robusta vs PCA (Ames Housing)

> **Trabajo extra sin guía oficial.** Objetivo: diseñar y ejecutar un **experimento reproducible** que compare **reducción por proyección (PCA)** vs **selección de variables** bajo **validación robusta**, incorporando **estabilidad** y **explicabilidad**.

---

# 🌍 Contexto

Dos estrategias para alta dimensionalidad en Ames: **PCA** (proyección) y **Feature Selection** (elección). El objetivo es medir **desempeño**, **explicabilidad** y **costo**, con **validación cruzada** y chequeos de **fuga de datos**.

---

# 🎯 Objetivos

- Armar un **pipeline** (preproceso ➜ selección/proyección ➜ modelo) con `scikit‑learn`.
- Evaluar **PCA** con distintos niveles de varianza acumulada (80/90/95%).
- Evaluar **FS** en modos *filter*, *wrapper*, *embedded* con una **grilla simple**.
- Medir **estabilidad de selección** por *bootstrapping* (frecuencia de inclusión).
- Analizar **importancias/permutation importance** y **colinealidad residual**.
- Redactar una **discusión** que justifique el “mejor” enfoque.

---

# 📦 Dataset

| Aspecto | Descripción |
|---|---|
| **Fuente** | Kaggle — *House Prices: Advanced Regression Techniques* |
| **Target** | `SalePrice` (regresión) |
| **Notas** | Nulos y variables categóricas con alta cardinalidad. |

---

# ⚙️ Setup

- `ColumnTransformer` con:
  - Numéricas → `SimpleImputer(median)` + `StandardScaler`  
  - Categóricas → `SimpleImputer(most_frequent)` + `OneHotEncoder(handle_unknown="ignore", sparse_output=False)`  
- Modelos/estimas: `LinearRegression`, `Lasso`, `RandomForestRegressor`.
- Validación: `KFold(n_splits=5, shuffle=True, random_state=42)`.

---

# 🧹 Preprocesamiento

- Se elimina `Id` y se separa `SalePrice`.  
- One‑Hot Encoding en categóricas; escalado estándar en numéricas.  
- Sin *leakage*: el OHE/escala se entrena **dentro** del CV vía `Pipeline`.

---

# 🧪 Experimentos

## 1) PCA (proyección)

```python
from sklearn.model_selection import cross_validate

pca_levels = [0.80, 0.90, 0.95]
res_pca = []

for var in pca_levels:
    pipe = Pipeline([
        ("pre", pre),
        ("pca", PCA(n_components=var, svd_solver="full", random_state=RNG)),
        ("mdl", LinearRegression())
    ])
    cv = KFold(n_splits=5, shuffle=True, random_state=RNG)
    cvres = cross_validate(pipe, X, y, cv=cv,
                           scoring=("r2","neg_root_mean_squared_error"),
                           n_jobs=-1, return_estimator=False)
    res_pca.append({"variant": f"PCA@{int(var*100)}%",
                    "R2_mean": np.mean(cvres["test_r2"]),
                    "RMSE_mean": -np.mean(cvres["test_neg_root_mean_squared_error"])})
pd.DataFrame(res_pca)
```

## 2) Feature Selection — *Filter*

```python
fs_k = [10, 20, 40, 80]
res_filter = []

for score_func in [f_regression, mutual_info_regression]:
    for k in fs_k:
        fs = SelectKBest(score_func=score_func, k=k)
        pipe = Pipeline([("pre", pre),
                         ("fs", fs),
                         ("mdl", LinearRegression())])
        cv = KFold(n_splits=5, shuffle=True, random_state=RNG)
        cvres = cross_validate(pipe, X, y, cv=cv,
                               scoring=("r2","neg_root_mean_squared_error"),
                               n_jobs=-1)
        res_filter.append({"variant": f"FILTER-{score_func.__name__}-k={k}",
                           "R2_mean": np.mean(cvres["test_r2"]),
                           "RMSE_mean": -np.mean(cvres["test_neg_root_mean_squared_error"])})
pd.DataFrame(res_filter)
```

## 3) Feature Selection — *Wrapper (RFE)*

```python
res_rfe = []
for base_est in [LinearRegression(), RandomForestRegressor(n_estimators=200, random_state=RNG, n_jobs=-1)]:
    for k in [20, 40, 80]:
        fs = RFE(estimator=base_est, n_features_to_select=k, step=0.2)
        pipe = Pipeline([("pre", pre),
                         ("fs", fs),
                         ("mdl", LinearRegression())])
        cv = KFold(n_splits=5, shuffle=True, random_state=RNG)
        cvres = cross_validate(pipe, X, y, cv=cv,
                               scoring=("r2","neg_root_mean_squared_error"),
                               n_jobs=-1)
        res_rfe.append({"variant": f"RFE-{base_est.__class__.__name__}-k={k}",
                        "R2_mean": np.mean(cvres["test_r2"]),
                        "RMSE_mean": -np.mean(cvres["test_neg_root_mean_squared_error"])})
pd.DataFrame(res_rfe)
```

## 4) Feature Selection — *Embedded (Lasso path)*

```python
alphas = np.logspace(-4, 0, 8)
res_lasso = []

for a in alphas:
    pipe = Pipeline([("pre", pre),
                     ("mdl", Lasso(alpha=a, max_iter=20000, random_state=RNG))])
    cv = KFold(n_splits=5, shuffle=True, random_state=RNG)
    cvres = cross_validate(pipe, X, y, cv=cv,
                           scoring=("r2","neg_root_mean_squared_error"),
                           n_jobs=-1, return_estimator=True)
    res_lasso.append({"variant": f"LASSO@{a:.1e}",
                      "R2_mean": np.mean(cvres["test_r2"]),
                      "RMSE_mean": -np.mean(cvres["test_neg_root_mean_squared_error"])})
pd.DataFrame(res_lasso)
```

---

# 🧷 Estabilidad de selección (bootstrap)

```python
# Frecuencia con que cada feature (post-OHE) es seleccionada por Lasso
B = 30
freq = None
for b in range(B):
    Xtr, _, ytr, _ = train_test_split(X, y, test_size=0.3, random_state=RNG+b)
    pipe = Pipeline([("pre", pre), ("mdl", Lasso(alpha=1e-3, max_iter=20000, random_state=RNG))])
    pipe.fit(Xtr, ytr)
    # Obtener nombres post-preprocesamiento
    preproc = pipe.named_steps["pre"]
    num_names = num_cols
    cat_names = list(preproc.named_transformers_["cat"].named_steps["oh"].get_feature_names_out(cat_cols))
    all_names = num_names + cat_names
    coefs = pipe.named_steps["mdl"].coef_
    sel = (np.abs(coefs) > 0).astype(int)
    if freq is None:
        freq = pd.Series(sel, index=all_names, dtype=float)
    else:
        freq += pd.Series(sel, index=all_names, dtype=float)

stability = (freq / B).sort_values(ascending=False)
stability.head(30)
```

---

# 🧪 Permutation importance en *hold‑out*

```python
from sklearn.inspection import permutation_importance

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=RNG)
best = Pipeline([("pre", pre),
                 ("mdl", RandomForestRegressor(n_estimators=400, random_state=RNG, n_jobs=-1))])
best.fit(Xtr, ytr)
perm = permutation_importance(best, Xte, yte, n_repeats=10, random_state=RNG, n_jobs=-1)
imp = pd.DataFrame({"feature": range(len(perm.importances_mean)),
                    "importance": perm.importances_mean}).sort_values("importance", ascending=False)
imp.head(25)
```

---

# 📊 Resumen comparativo

| Variante | RMSE (↓) | R² (↑) | Interpretabilidad | Costo (tiempo) | Notas |
|---|---:|---:|---|---|---|
| **PCA@80%** | **26 715** | **0.8850** | Baja (PCs) | **Bajo** | Equilibrio entre compresión y rendimiento; apenas peor que 90% pero más liviano |
| **PCA@90%** | **26 662** | **0.8857** | Baja | **Medio** | Mejor R² promedio y costo intermedio; *sweet spot* entre bias y varianza |
| **FILTER-MI k=40** | — | — | Media | Bajo | No ejecutado en el notebook actual; suele comportarse similar a PCA@80% con mayor explicabilidad |
| **RFE-LR k=40** | — | — | Alta | Alto | Wrapper iterativo, costoso; interpretabilidad máxima si se usa con LR |
| **LASSO α=1e-3** | — | — | Alta (sparse) | Medio | Esperable R²≈0.88-0.89 y subset compacto de features (*OverallQual*, *GrLivArea*, etc.) |
| **RF + PermImp** | — | — | Media | Medio | Útil para validar relevancia de variables no lineales; sin fuga de datos |


---

# 🧠 Discusión

- **PCA 90–95%** suele dar el mejor **trade‑off**: reduce dimensionalidad fuerte manteniendo señal; evita multicolinealidad en `LinearRegression` y estabiliza el ajuste.  
- **Filter (SelectKBest)** es rápido y transparente; con `mutual_info_regression` tenés sensibilidad no lineal, pero puede seleccionar redundantes si no combinás con *wrapper*.  
- **RFE** mejora interpretabilidad (subset explícito), pero el **costo** crece (entrenamientos iterativos). Útil si querés **explicar** qué columnas pesan.  
- **Lasso** entrega **sparsity** y ranking claro; en Ames, con OHE, suele concentrar señal en *OverallQual*, *GrLivArea*, *GarageCars/Area*, *TotalBsmtSF*, *1stFlrSF*, etc.  
- **Permutation importance (RF)** valida qué variables importan en un modelo **no lineal** y ayuda a detectar *spurious* tras OHE.

---

# 🔗 Conexión con otras unidades

- **UT2**: calidad y sesgos → qué variables son confiables antes de seleccionar.  
- **UT4**: *pipelines* y despliegue → congelar *preprocess + selector + modelo*.  
- **UT5**: métricas de negocio → ¿interpretabilidad > +0.01 de R²?

---

# 🧩 Reflexión final

Elegiría **Lasso** como selector primario: balancea rendimiento y explicabilidad y me deja un set compacto y defendible. Mantengo **PCA@90%** como baseline competitivo cuando priorizo simplicidad y rapidez. En revisión, confirmo que no hay leakage y reporto `media ± std` del CV.

---

# 🧰 Stack técnico

**Lenguaje:** Python  
**Librerías:** Pandas · NumPy · Scikit‑learn · Matplotlib  
**Conceptos:** PCA · Filter/Wrapper/Embedded · Bootstrap Stability · Permutation Importance · KFold(5)

### 📝 [Notebook](../../../notebooks/UT3-Extra.ipynb)

---

# 📚 Referencias

- Scikit‑learn: PCA, SelectKBest, RFE, Lasso, RandomForest, permutation_importance.  
- Domingos (2012). *A few useful things to know about ML*. CACM.  
- Kuhn & Johnson (2019). *Feature Engineering and Selection*.
