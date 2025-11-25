---
title: "UT4 – Geodatos, Imágenes y Audio"
date: 2025-11-25
---

# 🌎 Unidad Temática 4: Geodatos, Imágenes y Audio

La cuarta unidad del portafolio marca la transición hacia el trabajo con **datos no tabulares**, incorporando tres universos fundamentales del aprendizaje automático moderno:  
**datos geoespaciales**, **procesamiento de imágenes** y **señales de audio**.

Esta unidad amplía el enfoque de Ingeniería de Datos hacia modalidades donde la estructura, la orientación, la escala y el tiempo adquieren un rol central. Aprendí a transformar, representar y analizar información que vive fuera del Excel: mapas, matrices de pixeles y ondas digitales.

---

## 🎯 Objetivos generales

- Comprender los fundamentos de los **modelos vectoriales** y los **Sistemas de Referencia de Coordenadas (CRS)**.  
- Manipular **geodatabases** con GeoPandas, realizar *joins espaciales*, buffers y cálculos métricos.  
- Preprocesar **imágenes digitales** mediante histogramas, filtrado, ecualización y detección de bordes.  
- Aplicar técnicas de **representación tiempo–frecuencia** para señales de audio (STFT, Mel-Spectrogram).  
- Implementar estrategias de **preprocesamiento**, **augmentations** y **normalización** para imágenes y audio.  
- Entender cómo estas modalidades generan **features ricas** para modelos de Machine Learning.

---

## 🧩 Proyectos incluidos

| Proyecto | Descripción | Enlace |
|-----------|--------------|----------|
| 🗺️ **Análisis Geoespacial en CABA** | Cálculo de áreas, distancias y cobertura urbana con GeoPandas. | [Ver artículo](./12-geoespacial_geopandas.md) |
| 🖼️ **Preprocesamiento de Imágenes** | Histogramas, CLAHE, filtros, Canny y keypoints. | [Ver artículo](./13-preprocesamiento_img.md) |
| 🎵 **Preprocesamiento de Audio** | Waveform, STFT, Mel, normalización, ruido y augmentations. | [Ver artículo](./14-procesamiento_audio.md) |

---

## 📊 Competencias desarrolladas

- Manejo profesional de **geodatos**: reproyección, distancias en metros, uniones espaciales.  
- Creación de **mapas temáticos** y análisis territorial con contexto urbano.  
- Lectura y transformación de **imágenes RGB** y escalas de grises.  
- Aplicación de **CLAHE**, filtros Gaussianos/Bilaterales y detección de bordes.  
- Representación de audio en **tiempo, frecuencia y tiempo–frecuencia**.  
- Implementación de **augmentations** (pitch shift, time stretch, ruido blanco).  
- Interpretación de **métricas espectrales** (centroid, rolloff, bandwidth).  

---

## 🧠 Reflexión final

UT4 me cambió la forma de ver los datos.  
Entendí que no todo cabe en una tabla: el *espacio*, la *luz* y el *sonido* también son datos que pueden modelarse, limpiarse y transformarse.

Aprendí a trabajar con imágenes, mapas y audio de manera sistemática, construyendo representaciones que respeten la geometría del mundo real.  
Esta unidad me dio herramientas concretas para enfrentar proyectos modernos donde el contexto espacial, visual o acústico es clave para extraer conocimiento.

---

# 🧰 Stack técnico

**Lenguaje:** Python  
**Librerías:** GeoPandas · Shapely · Contextily · Matplotlib · NumPy · Pandas · Librosa · OpenCV  
**Conceptos:** CRS · Spatial Join · Histogramas · CLAHE · STFT · Mel-Spectrogram · Augmentation

---

# 📚 Referencias

- Material de cátedra: <https://juanfkurucz.com/ucu-id/ut4/>  
- GeoPandas Documentation — https://geopandas.org/  
- Librosa — https://librosa.org/  
- OpenCV — https://docs.opencv.org/  