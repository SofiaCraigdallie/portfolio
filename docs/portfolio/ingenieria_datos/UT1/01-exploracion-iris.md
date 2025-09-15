---
title: "Exploración del dataset Iris"
date: 2025-01-10
---

# 🌸 Exploración del dataset Iris  

---

## 📘 Contexto  

Práctica introductoria de **Análisis Exploratorio de Datos (EDA)** utilizando el dataset clásico de *Iris* (Fisher, 1936).  
El objetivo fue identificar patrones de separabilidad entre especies a través de visualizaciones estadísticas básicas.  

---

## 🎯 Objetivos  

- Visualizar relaciones entre variables numéricas y especies.  
- Detectar correlaciones relevantes y posibles redundancias.  
- Justificar qué variables aportan mayor poder de discriminación.  

---

## ⏱️ Actividades (con tiempos estimados)  

| Actividad | Tiempo estimado | Resultado esperado |
|-----------|-----------------|--------------------|
| Carga, limpieza y descripción inicial | 15 min | Dataset listo y comprendido |
| Visualización con pairplot | 20 min | Identificar separabilidad entre especies |
| Heatmap de correlación | 15 min | Detectar correlaciones entre variables |
 
---

## 🛠️ Desarrollo  

1. Se cargaron los datos y se calcularon estadísticas descriptivas (media, desvío, rangos).  
2. Con `seaborn.pairplot` se analizaron las relaciones bivariadas entre variables, diferenciadas por especie.  
    - Las variables de **pétalo** muestran una clara separación de clases, en especial *setosa*.  
3. Se construyó un **mapa de calor de correlaciones**:  
    - Se observó una correlación alta entre `petal_length` y `petal_width`, sugiriendo posible redundancia.  
    - Las variables de **sépalo** muestran mayor solapamiento entre especies.  

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_iris

# Cargar dataset
iris = load_iris(as_frame=True)
df = iris.frame

# Pairplot
sns.pairplot(df, hue="target", diag_kind="hist")
plt.show()

# Heatmap
corr = df.drop(columns="target").corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.show()
```

---

## 📊 Evidencias  
### 🔹 Pairplot 
![Pairplot Iris](../../../assets/img/iris_pairplot.png)

- Las variables de pétalo separan bien las especies.  
- `sepal_length` y `sepal_width` presentan mayor solapamiento.

### 🔹 Heatmap de correlación 
![Heatmap Iris](../../../assets/img/iris_corr.png)

- Correlación alta entre `petal_length` y `petal_width`.  
- Variables de sépalo aportan menos discriminación.

---

## 🤔 Reflexión  

- La **selección de variables** es fundamental antes de modelar.  
- En este caso, las variables de pétalo son más discriminativas que las de sépalo.  
- Un siguiente paso natural sería entrenar un **clasificador KNN o Random Forest** para cuantificar la separabilidad observada en las visualizaciones.  

---

## 📚 Referencias  

- Práctica: <https://juanfkurucz.com/ucu-id/ut1/01-exploracion-iris/>  
- Documentación seaborn: <https://seaborn.pydata.org/>  
- Fisher, R. A. (1936). *The use of multiple measurements in taxonomic problems*.