---
title: "🎬 Explorando el catálogo de Netflix: análisis exploratorio con pandas"
date: 2025-01-12
---

# 🎬 Explorando el catálogo de Netflix: análisis exploratorio con pandas

# 🌍 Contexto

Este proyecto forma parte de la **Unidad Temática 1: Exploración y fuentes de datos** del Portafolio de Ingeniería de Datos.  
En esta práctica se aplica el proceso de **Análisis Exploratorio de Datos (EDA)** al dataset de títulos de **Netflix**, con el objetivo de obtener una visión inicial del catálogo de la plataforma y sus tendencias.

El conjunto de datos incluye información sobre miles de títulos —películas y series— con atributos como país, director, reparto, fecha de lanzamiento, tipo de contenido y clasificación.  
El análisis permite detectar problemas de calidad, generar visualizaciones descriptivas y formular preguntas de negocio para etapas posteriores de análisis o modelado.

---

# 🎯 Objetivos

- Auditar la estructura y calidad del dataset (tipos de datos, valores nulos, duplicados).  
- Aplicar una **limpieza básica** (normalización de fechas y categorías).  
- Visualizar distribuciones de variables clave: tipo de contenido, año de lanzamiento y país.  
- Extraer patrones y tendencias generales para futuros análisis de comportamiento y producción audiovisual.

---

# 📦 Dataset

| Aspecto | Descripción |
|----------|-------------|
| **Fuente** | Kaggle – [Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) |
| **Formato** | CSV |
| **Tamaño** | ~8.800 registros × 12 columnas |
| **Variables principales** | `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in` |
| **Problemas detectados** | Valores nulos frecuentes en `director`, `cast` y `country`; duplicados; inconsistencias en formato de fecha. |

---

# 🧹 Limpieza y preparación de datos

Se realizó una limpieza mínima para asegurar la consistencia de las variables:

- Conversión de `date_added` a tipo **datetime**.  
- Extracción del año desde `release_year`.  
- Eliminación de duplicados.  
- Revisión de valores nulos y normalización básica de texto.

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv")

# Auditoría inicial
print(df.info())
print(df.isna().sum())

# Limpieza mínima
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year'] = df['release_year']
df.drop_duplicates(inplace=True)
```

---

# 📊 Análisis exploratorio (EDA)

## 🔹 Distribución de contenido por tipo

Se analizó la proporción de **películas** y **series de TV** en el catálogo.

```python
df['type'].value_counts().plot(kind="bar", color=["#1f77b4", "#ff7f0e"])
plt.title("Distribución de contenido por tipo")
plt.show()
```

📈 **Interpretación:**  
El catálogo de Netflix está dominado por **películas**, que representan aproximadamente el **70%** del total, frente al 30% de series.

---

## 🔹 Evolución de lanzamientos por año

Se estudió la cantidad de títulos agregados a la plataforma por año.

```python
df['year'].value_counts().sort_index().plot(kind="line")
plt.title("Lanzamientos por año")
plt.xlabel("Año")
plt.ylabel("Cantidad de títulos")
plt.show()
```

📈 **Interpretación:**  
Se observa un **crecimiento exponencial desde 2015**, coincidente con la expansión global de la plataforma.  
Este aumento refleja la estrategia de Netflix de incrementar su producción y diversificar géneros.

---

## 🔹 Países con mayor cantidad de títulos

```python
top_countries = df['country'].value_counts().head(10)
top_countries.plot(kind="barh", color="#d62728")
plt.title("Países con mayor cantidad de títulos")
plt.show()
```

📈 **Interpretación:**  
Los países más representados son **Estados Unidos** e **India**, seguidos por **Reino Unido** y **Japón**.  
Esto revela un fuerte sesgo hacia mercados angloparlantes, aunque se aprecia crecimiento en producciones asiáticas.

---

![Dashboard Netflix](../../../assets/img/netflix_dashboard.png)

### 📝 [Notebook](../../../notebooks/UT1-2.ipynb)

---

# ⚙️ Análisis técnico

- Se identificaron columnas con valores faltantes y se aplicaron estrategias simples de limpieza.  
- Se evaluó la estructura temporal del catálogo mediante series anuales.  
- Se detectó un **aumento sostenido de títulos** en la última década.  
- El análisis confirmó la necesidad de una futura **normalización por país y género**, ideal para aplicar técnicas de *feature engineering* (UT3).

---

# 🧠 Resultados y discusión

| Hallazgo | Interpretación |
|-----------|----------------|
| Crecimiento post-2015 | Expansión global de la plataforma |
| Dominio de películas sobre series | Foco principal en contenido cinematográfico |
| Concentración en pocos países | Sesgo geográfico (EE.UU. e India) |
| Presencia de datos faltantes | Oportunidad para limpieza avanzada o imputación |

> 💬 **Discusión:**  
> El análisis revela un dataset heterogéneo con problemas típicos de calidad en fuentes reales.  
> La tendencia temporal y la concentración geográfica ofrecen una base sólida para estudios de segmentación, diversidad de contenido o predicción de lanzamientos.

---

# 🔗 Conexión con otras unidades

Este proyecto conecta directamente con:
- **UT2:** Evaluar la calidad y sesgos del dataset de Netflix (por país, género o tipo de contenido).  
- **UT3:** Crear nuevas variables (ej. `continent`, `content_length`) para modelos de predicción de popularidad.  
- **UT5:** Integrar el dataset en un pipeline ETL con Spark.

---

# 🧩 Reflexión final

Este análisis fue una primera experiencia con **datos reales y desordenados**, mostrando que la limpieza y el EDA son etapas críticas en cualquier proyecto de datos.  
Entendí que las visualizaciones simples pueden responder preguntas estratégicas y abrir nuevas líneas de investigación.  

> 🌱 *Próximos pasos:*  
> Analizar la relación entre **rating, duración y país**, y extender el estudio hacia **recomendación de contenidos** basados en similitud temática.

---

# 🧰 Stack técnico

**Lenguaje:** Python  
**Librerías:** Pandas · Matplotlib · Seaborn · NumPy  
**Conceptos aplicados:** Auditoría de datos · Limpieza básica · Visualización descriptiva · Tendencias temporales

---

# 📚 Referencias

- Práctica original: <https://juanfkurucz.com/ucu-id/ut1/03-eda-netflix-pandas/>  
- Kaggle Dataset: [Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)  
- [Documentación pandas](https://pandas.pydata.org/docs/)  
- [Documentación matplotlib](https://matplotlib.org/stable/)