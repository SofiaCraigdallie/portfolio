---
title: "Sesgo y Fairness — Boston, Titanic y Ames"
date: 2025-10-12
---

# ⚖️ Sesgo y Fairness — Boston, Titanic y Ames

---

## 📘 Contexto

Práctica de **UT2 / 07 – Sesgo y Fairness**. Se analiza sesgo en tres casos:  
1) **Boston Housing** (regresión, sesgo racial histórico),  
2) **Titanic** (clasificación, sesgo sistemático por género y clase),  
3) **Ames Housing** (regresión, brechas geográficas/temporales).  
Se usan métricas de fairness y **Fairlearn** (mitigación) con reporte de *trade-off*.

---

## 🎯 Objetivos

- Detectar **brechas por grupo** e **interseccionalidad** (p. ej., `sexo × clase` en Titanic).  
- Medir fairness con **Demographic Parity** y **Equalized Odds**.  
- Aplicar **Fairlearn (ExponentiatedGradient)** y documentar **performance loss**.  
- En regresión (Boston/Ames), evaluar **errores/brechas por grupo** y reflexionar.

---

## ⏱️ Actividades (con tiempos estimados)

| Actividad | Tiempo estimado | Resultado esperado |
|-----------|-----------------|--------------------|
| Boston: carga + análisis de sesgo | 25 min | Brecha histórica cuantificada |
| Titanic: baseline + fairness + mitigación | 40 min | Métricas por grupo e intersección; trade-off |
| Ames: error por barrio/tiempo | 25 min | Disparidades por grupo (MAE, diferencias relativas) |
| Reflexión y decisiones éticas | 15 min | Conclusiones accionables |

---

## 🛠️ Desarrollo

### 1) Boston Housing — Regresión + Sesgo racial
- Se cargó Boston y se derivó una variable racial (e.g., `Bk_racial`/`B`).  
- Se cuantificó **brecha de precios** entre grupos.  
- **Decisión:** caso **educativo**, **no** para producción.

### 2) Titanic — Clasificación + Fairness
- Baseline: se entrenó y se midieron métricas por **sexo**.  
- **Interseccionalidad (`sexo × clase`)** con `MetricFrame`.  
- Mitigación con **Fairlearn ExponentiatedGradient + DemographicParity** y reporte de **performance loss**.

```python
from fairlearn.metrics import MetricFrame, selection_rate
from fairlearn.reductions import ExponentiatedGradient, DemographicParity
from sklearn.metrics import accuracy_score, recall_score

# Ejemplo de métricas por grupo:
mf_sex = MetricFrame(
    metrics={"accuracy": accuracy_score, "selection_rate": selection_rate,
             "tpr": lambda yt, yp: recall_score(yt, yp, zero_division=0)},
    y_true=y_test_t, y_pred=titanic_baseline_pred, sensitive_features=A_test_t
)
mf_sex.by_group  # resumen por sexo
```

### 3) Ames Housing — Regresión + Brechas geográficas/temporales
- Modelo lineal simple y **MAE por barrio** (grupo sensible).
- Brechas relativas entre barrios y **diferencia temporal** (casas nuevas vs. antiguas).

---

## 📊 Evidencias
### 🔹 Titanic — Fairness e interseccionalidad

- **Demographic Parity Diff (sexo): 0.113**
- **Equalized Odds Diff (sexo): 0.240**
- **Peor subgrupo (sexo×clase):** male_3 — selection_rate=0.095, TPR=0.154.
- **Trade-off (mitigación):** Performance loss = 8.3%.

### 🔹 Boston — Brecha histórica

- **Brecha detectada: -2.4%**

### 🔹 Ames — Disparidades (muestra del notebook)

- **Brecha geográfica (MAE/valores por barrio): ≈ +132%** (barrio más caro vs. más barato, muestra usada).
- **Brecha temporal (nuevas vs. antiguas): ≈ +47%** (promedios en la muestra).

### 📝 [Notebook](../../../notebooks/UT2-3.ipynb)

---

## 🤔 Reflexión

- **Boston:** sesgo estructural histórico → **no desplegar** el modelo; usar solo para aprendizaje.
- **Titanic:** sesgo sistemático por género/clase → **mitigar** con Fairlearn; documentar **performance loss.**
- **Ames:** alto riesgo de **perpetuar desigualdades** por barrio/época; auditar por grupo y no usar como único criterio (p. ej., crédito/hipotecas).

---

## 📚 Referencias

- Práctica: https://juanfkurucz.com/ucu-id/ut2/07-sesgo-y-fairness/
- Fairlearn: https://fairlearn.org/
- scikit-learn (métricas/modelos): https://scikit-learn.org/