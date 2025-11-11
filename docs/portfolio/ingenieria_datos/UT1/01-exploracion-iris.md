---
title: "🌸 Explorando el dataset Iris: patrones de separación entre especies"
date: 2025-01-10
---

# 🌸 Explorando el dataset Iris

> Primer ejercicio del Portafolio de Ingeniería de Datos — Unidad Temática 1: **Exploración y Fuentes de Datos**.  
> Aquí comencé el proceso **CRISP-DM** desde su primera fase: *Comprensión de los datos*.

---

# 🌍 Contexto

El dataset **Iris** (Fisher, 1936) es un clásico en estadística y aprendizaje automático.  
Contiene mediciones de sépalos y pétalos de tres especies de flores: *setosa*, *versicolor* y *virginica*.  
El objetivo fue explorar cómo las variables numéricas ayudan a **distinguir las especies** y a entender **patrones de correlación** entre sus atributos.

---

# 🎯 Objetivos

- Explorar la estructura del dataset Iris y sus variables numéricas.  
- Visualizar relaciones entre pares de variables y las tres especies.  
- Detectar correlaciones y posibles redundancias entre atributos.  
- Identificar qué variables aportan mayor poder de discriminación entre clases.

---

# 📦 Dataset

| Aspecto | Descripción |
|----------|-------------|
| **Fuente** | [Scikit-learn Dataset: Iris](https://scikit-learn.org/stable/datasets/toy_dataset.html#iris-dataset) |
| **Autor original** | R. A. Fisher (1936) |
| **Formato** | DataFrame (4 variables numéricas + 1 categórica) |
| **Tamaño** | 150 observaciones × 5 columnas |
| **Variables** | `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, `species` |
| **Problemas detectados** | Ningún valor faltante o inconsistencia. Se observan posibles correlaciones altas entre variables de pétalo. |

---

# 📊 Análisis exploratorio (EDA)

El análisis se centró en entender la relación entre medidas y especies, usando visualizaciones básicas pero muy informativas.

---

## 🔹 Pairplot

![Pairplot Iris](../../../assets/img/iris_pairplot.png)

**Figura:** Diagrama de dispersión y distribución de las cuatro variables numéricas coloreadas por especie.

📈 **Interpretación:**  
- Las variables de **pétalo** (`petal_length`, `petal_width`) separan casi perfectamente las tres especies, sobre todo *setosa*.  
- Las de **sépalo** tienen más solapamiento, mostrando menor poder de discriminación.

---

## 🔹 Heatmap de correlación

![Heatmap Iris](../../../assets/img/iris_corr.png)

**Figura:** Mapa de correlación de Pearson entre las variables numéricas.

📈 **Interpretación:**  
- Fuerte correlación (≈ 0.96) entre `petal_length` y `petal_width`.  
- Las variables de sépalo presentan correlaciones más bajas, aportando información complementaria.

---

# ⚙️ Análisis técnico

El dataset resulta **ideal para problemas de clasificación supervisada multiclase**.  
La redundancia detectada entre `petal_length` y `petal_width` sugiere que podrían combinarse o regularizarse en etapas futuras (*Feature Engineering*, UT3).  
En general, se confirma un conjunto **limpio, balanceado y estable**: una base perfecta para probar modelos simples.

---

# 🧠 Resultados y discusión

| Hallazgo | Interpretación |
|-----------|----------------|
| Alta correlación entre variables de pétalo | Posible reducción de dimensionalidad futura |
| Buena separabilidad entre especies | Dataset ideal para clasificación |
| Sin valores faltantes | No se requiere imputación |
| Variables de sépalo poco discriminantes | Podrían tener menor peso en el modelado |

💬 **Conclusión:**  
El dataset Iris ilustra de forma simple la **separabilidad de clases** en datos reales.  
Las variables de pétalo concentran el poder predictivo, mientras que las de sépalo añaden variabilidad menor pero útil para visualizar la estructura completa.

---

# 🔗 Conexión con otras unidades

Este análisis sienta las bases para el trabajo de las siguientes unidades:  
- **UT2:** Evaluar la calidad y posibles sesgos en datasets más complejos.  
- **UT3:** Aplicar técnicas de *Feature Engineering* considerando las correlaciones detectadas.  
- **UT5:** Integrar este dataset en pipelines reproducibles de preprocesamiento.

---

# 🧩 Reflexión final

Este ejercicio me enseñó que el EDA no es solo “mirar gráficos”, sino **descubrir la historia que los datos cuentan**.  
Detectar patrones y redundancias temprano evita errores de modelado después.  
La exploración es la brújula de cualquier proyecto de datos.

> 🌱 *Próximo paso:* probar un modelo de clasificación (KNN o Random Forest) para cuantificar la separabilidad observada.

---

# 🧰 Stack técnico

**Lenguaje:** Python  
**Librerías:** Pandas · Seaborn · Matplotlib · NumPy · Scikit-learn  
**Conceptos aplicados:** EDA · Visualización · Correlación · Comprensión de datos  

---

# Evidencias

### 📝 [Notebook](../../../notebooks/UT1-1.ipynb)

---

# 📚 Referencias

- Fisher, R. A. (1936). *The use of multiple measurements in taxonomic problems.* Annals of Eugenics.  
- Práctica original: <https://juanfkurucz.com/ucu-id/ut1/01-exploracion-iris/>  
- Documentación Seaborn: <https://seaborn.pydata.org/>  
- Documentación Scikit-learn: <https://scikit-learn.org/stable/datasets/toy_dataset.html#iris-dataset>