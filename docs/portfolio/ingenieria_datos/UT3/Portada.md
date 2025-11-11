---
title: "UT3 – Feature Engineering y Representación de Datos"
date: 2025-11-09
---

# 🧱 Unidad Temática 3: Feature Engineering y Representación de Datos

Esta unidad marca un salto clave en el portafolio: pasar de **entender los datos** a **transformarlos estratégicamente** para maximizar el poder predictivo de los modelos.  
El foco estuvo en el **Feature Engineering**, es decir, en cómo representar la información de forma que los algoritmos puedan **aprender patrones con mayor eficacia y menor sesgo**.

A lo largo de las prácticas se aplicaron técnicas desde el escalado y codificación básica hasta transformaciones avanzadas y reducción de dimensionalidad, incorporando también el componente temporal de las variables.

---

## 🎯 Objetivos generales

- Comprender el rol del **Feature Engineering** dentro del pipeline de Machine Learning.  
- Aplicar transformaciones numéricas y categóricas con `pandas` y `scikit-learn`.  
- Implementar **encoding avanzado**: *Target Encoding*, *One-Hot*, *Ordinal* y *Frequency*.  
- Utilizar técnicas de **reducción de dimensionalidad** como **PCA** y **Feature Selection**.  
- Generar **features temporales** (lags, rolling windows, diferencias) sin *data leakage*.  
- Evaluar cómo cada transformación impacta en el rendimiento del modelo.

---

## 🧩 Proyectos incluidos

| Proyecto | Descripción | Enfoque |
|-----------|--------------|----------|
| 🧰 **Feature Engineering con Pandas** | Transformaciones numéricas y categóricas iniciales. | Limpieza, normalización y construcción manual de variables. | [Ver artículo](./08-feature-engineering.md) |
| 🔢 **Encoding Avanzado y Target Encoding** | Comparación de estrategias de codificación para variables categóricas. | Codificación supervisada y análisis de impacto en el modelo. | [Ver artículo](./09-encoding.md) |
| 🧮 **PCA y Feature Selection** | Reducción de dimensionalidad y selección de atributos relevantes. | Análisis de varianza explicada y ranking de importancia. | [Ver artículo](./10-PCAFeature-selection.md) |
| ⏱️ **Temporal Feature Engineering** | Construcción de variables basadas en el tiempo. | Lags, rolling windows y validación temporal sin fugas. | [Ver artículo](./11-Temporal-feature-engineering.md) |

---

## 📊 Competencias desarrolladas

- Diseño y evaluación de *features* efectivas.  
- Codificación categórica y normalización de variables numéricas.  
- Análisis de correlaciones y redundancias entre atributos.  
- Uso de `scikit-learn` para *pipelines* y preprocesamiento modular.  
- Aplicación de PCA y selección de variables basada en importancia.  
- Creación de *features* temporales seguras frente al *leakage*.

---

## 🧠 Reflexión final

Esta unidad me enseñó que el **modelo no es nada sin buenas features**.  
Aprendí a **pensar los datos como representaciones del fenómeno**, no solo como números: cada transformación, codificación o selección redefine la capacidad del modelo para generalizar.  
El *Feature Engineering* se convirtió así en una de las etapas más creativas y estratégicas de todo el pipeline.

---

# 🧰 Stack técnico

**Lenguaje:** Python  
**Librerías:** Pandas · NumPy · Scikit-learn · Matplotlib · Seaborn  
**Conceptos:** Feature Engineering · Encoding · PCA · Feature Selection · Variables temporales

---

# 📚 Referencias

- [Scikit-learn preprocessing guide](https://scikit-learn.org/stable/modules/preprocessing.html)  
- [Pandas transformations](https://pandas.pydata.org/docs/)  
- [Feature Engineering Handbook (Google Developers)](https://developers.google.com/machine-learning/data-prep/transform/feature-engineering)  
- Material de cátedra: <https://juanfkurucz.com/ucu-id/ut3/>