---
title: "⚖️ Sesgo y Fairness — Boston, Titanic y Ames"
date: 2025-10-12
---

# ⚖️ Sesgo y Fairness — Boston, Titanic y Ames

# 🌍 Contexto

Esta práctica pertenece a la **Unidad Temática 2: Calidad y Ética de los Datos**, centrada en el análisis de **sesgo y equidad algorítmica** en distintos contextos.  
El objetivo fue comprender cómo los datos reflejan desigualdades estructurales y cómo medir, mitigar y documentar el impacto de decisiones algorítmicas sobre grupos sensibles.

Se trabajó con tres datasets clásicos:
1. **Boston Housing** → regresión y sesgo racial histórico.  
2. **Titanic** → clasificación y sesgo sistemático por género y clase social.  
3. **Ames Housing** → regresión con brechas geográficas y temporales.  

El análisis combinó métricas de *fairness*, evaluaciones interseccionales y mitigación con **Fairlearn**, destacando los *trade-offs* entre equidad y performance.

---

# 🎯 Objetivos

- Detectar **brechas y sesgos sistemáticos** en distintos contextos de predicción.  
- Medir la equidad mediante métricas como **Demographic Parity** y **Equalized Odds**.  
- Implementar **Fairlearn (ExponentiatedGradient)** para mitigar desigualdades.  
- Cuantificar el **performance loss** tras la mitigación.  
- Reflexionar sobre las **implicancias éticas y sociales** del sesgo en modelos predictivos.

---

# 📦 Datasets

| Dataset | Tipo | Grupo sensible | Ejemplo de sesgo analizado |
|----------|------|----------------|-----------------------------|
| **Boston Housing** | Regresión | Variable racial (Bk_racial / B) | Diferencias estructurales históricas |
| **Titanic** | Clasificación | Sexo × Clase | Probabilidad de supervivencia desigual |
| **Ames Housing** | Regresión | Barrio / Año de construcción | Brechas geográficas y temporales |

---

# 🧹 Limpieza y preparación de datos

Cada dataset fue preparado para su análisis:

1. **Boston:** se eliminó la variable sensible del modelo, pero se evaluaron brechas en los residuales.  
2. **Titanic:** se estandarizaron categorías (`sex`, `pclass`) y se generó la intersección `sexo × clase`.  
3. **Ames:** se agruparon propiedades por `Neighborhood` y `YearBuilt` para medir disparidades.

El pipeline de fairness incluyó pasos de preprocesamiento, modelado base, cálculo de métricas y mitigación.

---

# ⚙️ Análisis técnico

## 🔹 1) Boston Housing — Regresión y sesgo racial

El dataset contiene correlaciones históricas entre raza y precio de vivienda.  
Se cuantificó la brecha promedio en las predicciones por grupo racial.

📊 **Resultado:**  
> Diferencia de predicción media ≈ **−2.4%** (precio menor para zonas de población no blanca).

📎 **Decisión ética:**  
Caso **solo educativo**, no apto para uso productivo debido a su sesgo estructural.

---

## 🔹 2) Titanic — Clasificación, género y clase

Se entrenó un modelo base y se evaluaron métricas de fairness por grupo (`sexo`, `clase`) usando `Fairlearn.MetricFrame`.

```python
from fairlearn.metrics import MetricFrame, selection_rate
from fairlearn.reductions import ExponentiatedGradient, DemographicParity
from sklearn.metrics import accuracy_score, recall_score

mf_sex = MetricFrame(
    metrics={"accuracy": accuracy_score, "selection_rate": selection_rate,
             "tpr": lambda yt, yp: recall_score(yt, yp, zero_division=0)},
    y_true=y_test_t, y_pred=titanic_baseline_pred, sensitive_features=A_test_t
)
mf_sex.by_group  # resumen por sexo
```

📈 **Métricas principales:**

| Métrica | Valor | Interpretación |
|----------|--------|----------------|
| Demographic Parity Diff | 0.113 | Brecha de probabilidad de resultado positivo |
| Equalized Odds Diff | 0.240 | Diferencias en verdaderos positivos por grupo |
| Performance loss tras mitigación | 8.3% | Disminución de accuracy para ganar equidad |

🧠 **Interseccionalidad (`sexo × clase`):**
- Peor subgrupo: **male_3** → selection_rate = 0.095, TPR = 0.154  
- Refleja desigualdad combinada de género y estatus socioeconómico.

---

## 🔹 3) Ames Housing — Regresión con brechas espaciales y temporales

Se analizó la variación del **MAE** por `Neighborhood` y año de construcción.  

| Grupo | Métrica | Brecha relativa |
|--------|----------|----------------|
| Barrios caros vs. baratos | MAE | +132% |
| Viviendas nuevas vs. antiguas | MAE | +47% |

📊 **Conclusión:**  
Las disparidades reflejan diferencias estructurales de acceso y valor territorial, lo que puede amplificar desigualdades si no se ajusta el modelo.

---

# 📈 Evidencias

### 🔹 Titanic — Fairness e interseccionalidad  
- **Demographic Parity Diff (sexo): 0.113**  
- **Equalized Odds Diff (sexo): 0.240**  
- **Peor subgrupo (`sexo×clase`):** male_3 — selection_rate=0.095, TPR=0.154.  
- **Trade-off (mitigación):** Performance loss ≈ 8.3%.

### 🔹 Boston — Brecha histórica  
- **Brecha detectada:** −2.4% en predicciones medias.

### 🔹 Ames — Disparidades por grupo  
- **Brecha geográfica (MAE):** +132% (barrio más caro vs. más barato).  
- **Brecha temporal (MAE):** +47% (casas nuevas vs. antiguas).

### 📝 [Notebook](../../../notebooks/UT2-3.ipynb)

---

# 🧠 Resultados y discusión

| Caso | Hallazgo clave | Implicación ética |
|------|----------------|------------------|
| **Boston** | Sesgo racial estructural | No desplegar, mantener como caso educativo |
| **Titanic** | Disparidad de oportunidades por género y clase | Mitigar con Fairlearn y documentar pérdida de rendimiento |
| **Ames** | Diferencias geográficas y temporales | Auditar antes de aplicar decisiones financieras o de crédito |

> 💬 **Discusión:**  
> La equidad algorítmica no es un estado binario, sino un proceso continuo.  
> Cada modelo requiere auditoría, transparencia y responsabilidad sobre cómo sus predicciones afectan a distintos grupos sociales.

---

# 🔗 Conexión con otras unidades

- **UT1:** Expande el análisis de fuentes, ahora con foco en los impactos éticos.  
- **UT3:** Fairness influye directamente en el diseño de *features* y variables sensibles.  
- **UT5:** Se integrará dentro de pipelines automatizados de evaluación ética.

---

# 🧩 Reflexión final

El sesgo en los datos no se elimina, se **reconoce y gestiona**.  
Aprendí que la equidad requiere decisiones conscientes: a veces, un modelo menos preciso puede ser más justo.  
La ética de datos es una dimensión técnica, pero también profundamente humana.

---

# 🧰 Stack técnico

**Lenguaje:** Python  
**Librerías:** Pandas · Scikit-learn · Fairlearn  
**Conceptos aplicados:** Fairness · Mitigación · Métricas por grupo · Performance loss  

---

# 📚 Referencias

- Práctica: <https://juanfkurucz.com/ucu-id/ut2/07-sesgo-y-fairness/>  
- [Fairlearn Documentation](https://fairlearn.org/)  
- Barocas, S., Hardt, M., & Narayanan, A. (2023). *Fairness and Machine Learning.*  
- [scikit-learn Documentation](https://scikit-learn.org/)