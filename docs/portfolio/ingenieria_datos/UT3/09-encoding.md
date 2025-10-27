---
title: "🧩 Encoding Avanzado — Adult Income (Census)"
date: 2025-10-27
---

# 🧩 Encoding Avanzado

---

# 🌍 Contexto

Esta práctica forma parte de la **Unidad Temática 3: Feature Engineering** y está enfocada en **comparar codificadores categóricos** y su impacto en el rendimiento, la dimensionalidad y la interpretabilidad de modelos de *Machine Learning*.  
Se trabajó con el dataset **Adult Income (US Census, 1994)** para predecir si el ingreso anual es **>50K**. El énfasis estuvo en **seleccionar el encoding adecuado según la cardinalidad** y en **evitar *data leakage*** en técnicas guiadas por el target.

---

# 🎯 Objetivos

- Diagnosticar **cardinalidad** y riesgos de **explosión dimensional**.
- Implementar y evaluar **Label, One-Hot, Target** y **pipelines ramificados** con `ColumnTransformer`.
- Medir **Accuracy, AUC-ROC, F1, tiempo y #features** como criterios de decisión.
- Analizar **feature importance** y discutir **impacto ético/interpretabilidad**.
- Explorar variantes: **Frequency, Ordinal, Leave-One-Out, Binary** y **smoothing**.

---

# 📦 Dataset

| Aspecto | Descripción |
|---|---|
| **Fuente** | UCI ML Repository — Adult (Census Income) |
| **Tarea** | Clasificación binaria (`target`: `income >50K`) |
| **Tamaño** | 32 561 registros, 16 columnas (8 categóricas, 6 numéricas + 2 auxiliares) |
| **Cardinalidad** | Baja: `workclass`, `marital-status`, `relationship`, `race`, `sex` · Media: `education` (16), `occupation` (15), `native-country` (42) · Alta (>50): **ninguna** |
| **Nota** | Se limpió espacios en categorías, se creó `target` y se estratificó el *split*. |

---

# 🧹 Limpieza y preparación

1. **Carga + limpieza:** `strip()` en categóricas, remover filas con `?`.  
2. **Target binario:** `target = (income == '>50K').astype(int)`.  
3. **Selección numéricas:** `age`, `fnlwgt`, `education-num`, `capital-gain`, `capital-loss`, `hours-per-week`.  
4. **Diagnóstico de cardinalidad:** riesgo de **one-hot = 11.8×** columnas si se aplicara a todas.

---

# 🔍 Análisis de cardinalidad

- **Baja (≤10):** 5 columnas → one-hot viable.  
- **Media (11–50):** 3 columnas → preferir *target/frequency/binary* si fuera necesario.  
- **Alta (>50):** 0 columnas → en este dataset no se activó rama *high-card*.

> **Conclusión:** *One-Hot* completo **no** es viable. Se procede con **Label**, **One-Hot solo baja** y **Target** para media/alta si aplica.

---

# 🧪 Experimentos

## 1) Label Encoding (todas las categóricas)
- **Modelo:** `RandomForestClassifier(100)`  
- **Resultados:**  
  - **Accuracy:** **0.8632** · **AUC:** **0.9101** · **F1:** **0.6931**  
  - **Tiempo:** 0.45 s · **#Features:** 14

## 2) One‑Hot (solo baja cardinalidad)
- Categóricas: `['workclass','marital-status','relationship','race','sex']`  
- **Resultados:** Accuracy 0.8483 · AUC 0.8995 · F1 0.6633 · Tiempo 0.43 s · **#Features:** 30

## 3) Target Encoding (alta/mediana cardinalidad)
- En este *split* no hubo columnas >50; se evaluó *target* para referencia.  
- **Resultados:** Accuracy 0.8021 · AUC 0.8272 · F1 0.5538 · Tiempo 0.43 s · **#Features:** 6

## 4) Pipeline ramificado (ColumnTransformer)
- **Ramas:** One‑Hot(baja) + Target(alta, 0 en este caso) + `StandardScaler`(numéricas).  
- **Resultados:** Accuracy 0.8485 · AUC 0.8996 · F1 0.6646 · Tiempo 0.44 s · **#Features:** 30

---

# 📊 Comparación de métodos

| Encoding | Accuracy | AUC-ROC | F1-Score | Tiempo (s) | #Features |
|---|---:|---:|---:|---:|---:|
| **Label Encoding** | **0.8632** | **0.9101** | **0.6931** | 0.45 | **14** |
| One‑Hot (low card) | 0.8483 | 0.8995 | 0.6633 | 0.43 | 30 |
| Target (high card) | 0.8021 | 0.8272 | 0.5538 | **0.43** | **6** |
| Branched Pipeline | 0.8485 | 0.8996 | 0.6646 | 0.44 | 30 |

**Hallazgos clave**  
- **Mejor rendimiento global:** **Label Encoding** (todas las métricas).  
- **Más compacto:** Target (6 cols) pero con caída de métricas.  
- **Trade‑off:** One‑Hot/Branched elevan dimensionalidad sin mejora sustancial en este dataset.

---

# 🔍 Explicabilidad — Feature Importance (Pipeline)

**Top features:** `fnlwgt`, `age`, `education-num`, `capital-gain`, `hours-per-week`, `capital-loss`.  
Las categóricas *one‑hot* con mayor peso: `marital-status_Married-civ-spouse`, `Never-married`, `sex_Male`, relaciones familiares y `workclass_Private`.

**Importancia por tipo**  
- **Numéricas:** **76.7 %** del total (6 variables).  
- **One‑Hot:** 23.3 % (24 variables).  
> Indica que la **estructura cuantitativa** del censo domina la predicción del ingreso.

---

# 🧪 Desafíos (extras)

- **Frequency(native-country):** Acc 0.8081 · AUC 0.8311 · F1 0.5645 · 7 feats.  
  - Útil, bajo riesgo si se calcula **solo en train**.  
- **Ordinal(education):** Acc 0.8019 · AUC 0.8272 · F1 0.5546 · 7 feats.  
  - Preserva orden; beneficia a árboles/lineales cuando hay escala.  
- **LOO(native-country):** Acc 0.7640 · AUC 0.6732 · F1 0.0576 · 7 feats.  
  - Reduce fuga usando media que **excluye** el propio registro; aquí no rindió.  
- **Binary(native-country):** Acc 0.8062 · AUC 0.8315 · F1 0.5572 · 12 feats (≈log₂ 42 ≈ 6 bits).  
  - Compacta alta cardinalidad sin usar el target.  
- **Target smoothing:** `s∈(1, 10, 100, 1000)` → AUC ≈ 0.828–0.832; **s=100** levemente mejor.  
  - `s` interpola media global ↔ media por categoría; alto `s` estabiliza clases raras.

---

# 🧠 Resultados y discusión

| Hallazgo | Implicación |
|---|---|
| **Label Encoding** domina en métricas con baja dimensionalidad | Preferible con **modelos de árboles** cuando no hay cardinalidades extremas |
| One‑Hot (baja) y Pipeline (mixto) son similares | La expansión de columnas **no** aportó ganancia en este dataset |
| Target/LOO no superaron alternativas | Útiles en **alta cardinalidad** o con regularización/CV; aquí no había |
| Predictores numéricos explican la mayor parte | La carga horaria, capital y edad **condicionan** el ingreso; vigilar sesgos |

---

# 🔗 Conexión con otras unidades

- **UT1 (EDA):** el diagnóstico de cardinalidad y leakage nace del análisis exploratorio.  
- **UT2 (Calidad & Ética):** fairness: evitar que el modelo refuerce sesgos (sexo/estado civil).  
- **UT4 (Especiales):** pipelines reproducibles y escalables; *deploy* sin fugas.  

---

# 🧩 Reflexión final

**Qué aprendí:** el *encoding* define el **espacio de hipótesis** del modelo. En Adult Income, **árboles + Label** bastan; *One‑Hot* no mejora y *Target* requiere cuidado contra **data leakage**.  
**Para producción:** usaría **pipeline con `ColumnTransformer`** (activando la rama *target* solo si aparece alta cardinalidad) y monitoreo de **métricas de equidad**.

---

# 🧰 Stack técnico

**Python** · pandas · NumPy · scikit‑learn · category_encoders · matplotlib  
**Conceptos:** cardinalidad, *data leakage*, *target smoothing*, pipelines, *feature importance*

---

# 📚 Referencias

- Práctica: <https://juanfkurucz.com/ucu-id/ut3/09-encoding-avanzado-assignment/>  
- UCI Adult: Dua, D. & Graff, C. (2019). *UCI ML Repository* — Adult.  
- Scikit‑learn: *ColumnTransformer*, *Pipelines*, *OneHotEncoder*.  
- `category_encoders`: *Target*, *Binary* encoders.

### 📝 [Notebook](../../../notebooks/UT3-2.ipynb)