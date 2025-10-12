---
title: "Unidad Temática 2 — Calidad y Ética de los Datos"
date: 2025-10-15
---

# 🧭 Unidad Temática 2 — Calidad y Ética de los Datos

---

## 🌍 Contexto general

La **Unidad Temática 2 (UT2)** aborda los pilares de la **calidad, completitud y ética** en la gestión de datos.  
A lo largo de esta unidad se trabajó en la **detección de errores, tratamiento de valores faltantes, normalización numérica, y análisis de sesgos**, integrando tanto técnicas estadísticas como reflexiones éticas sobre el impacto del modelado automatizado.

Los ejercicios se centraron en **asegurar la integridad de los datos y promover buenas prácticas profesionales**, con énfasis en la trazabilidad, transparencia y reproducibilidad.

---

## 🎯 Objetivos generales

- Analizar la **calidad de datos** y los distintos tipos de valores faltantes (MCAR, MAR, MNAR).  
- Implementar **pipelines reproducibles** para limpieza y preprocesamiento.  
- Aplicar métodos de **escalado y transformación** para mejorar la consistencia numérica.  
- Evaluar y mitigar **sesgos algorítmicos**, aplicando métricas de equidad con *Fairlearn*.  
- Reflexionar sobre la **ética y la justicia** en la ciencia de datos aplicada.

---

## 🧩 Proyectos incluidos

| Proyecto | Descripción | Enlace |
|-----------|--------------|--------|
| 🕵️ **Detección de valores faltantes** | Análisis y tratamiento de datos faltantes mediante imputación y detección de outliers. | [Ver artículo](./05-missing-data-detective.md) |
| 🏠 **Escalando variables con estilo** | Comparación de técnicas de escalado y construcción de pipelines reproducibles en *scikit-learn*. | [Ver artículo](./06-feature-scaling&pipelines.md) |
| ⚖️ **Modelos más justos** | Detección, medición y mitigación de sesgos en modelos predictivos, integrando consideraciones éticas. | [Ver artículo](./07-deteccion-sesgo.md) |

---

## 🧠 Reflexión de la unidad

La calidad y la ética son dimensiones inseparables del trabajo con datos.  
Un modelo correcto en lo técnico puede ser **injusto en lo social** si no se audita su comportamiento sobre distintos grupos.  
Esta unidad me permitió comprender que el rol de un ingeniero/a de datos va más allá del código:  
también implica **responsabilidad, transparencia y sentido crítico** frente a los resultados que produce.

---

## 🧰 Stack técnico general

**Lenguaje:** Python  
**Principales librerías:** Pandas · NumPy · Scikit-learn · Fairlearn · Matplotlib · Seaborn  
**Conceptos clave:** Calidad de datos · Imputación · Escalado · Pipelines · Sesgo · Fairness  

---

## 📚 Referencias generales

- Curso: [Ingeniería de Datos — UCU-ID](https://juanfkurucz.com/ucu-id/)  
- Little & Rubin (2019). *Statistical Analysis with Missing Data.*  
- Barocas, S., Hardt, M., & Narayanan, A. (2023). *Fairness and Machine Learning.*  
- Documentación oficial: [Scikit-learn](https://scikit-learn.org/) · [Fairlearn](https://fairlearn.org/)