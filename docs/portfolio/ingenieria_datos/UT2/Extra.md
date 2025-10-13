---
title: "🎬 Proyecto extra — Auditoría de calidad y joins con TMDb 5000 (movies & credits)"
date: 2025-10-12
---

# 🎬 Proyecto extra — Auditoría de calidad y joins con TMDb 5000 (movies & credits)

---

# 🌍 Contexto

Proyecto extra de **UT2 – Calidad y Ética de los Datos** usando el dataset de Kaggle **TMDb 5000**  
(archivos: `tmdb_5000_movies.csv` y `tmdb_5000_credits.csv`).  
Integramos ambos recursos para evaluar **completitud, consistencia, unicidad e integridad referencial**, y para practicar **joins** reales.

---

# 🎯 Objetivos

- Cargar **dos fuentes CSV** (movies y credits) y unificarlas con claves (`movies.id` ↔︎ `credits.movie_id`).  
- Medir **calidad**: nulos, duplicados por `(title, release_date)`, rangos válidos (`budget`, `revenue`, `runtime`).  
- Detectar **huérfanos** en `credits.movie_id` que no estén en `movies.id`.  
- Visualizar distribuciones y relaciones (e.g., `budget` vs `revenue`).

---

# 📦 Datos y esquema
- **Archivos**: `tmdb_5000_movies.csv`, `tmdb_5000_credits.csv`  
- **Claves**: `movies.id` (entero) y `credits.movie_id` (entero)  
- **Campos JSON como texto** (a limpiar en futuras unidades): `genres`, `cast`, `crew`, `keywords`, etc.

---

# 🛠️ Desarrollo (resumen)

1. **Carga** de ambos CSV con `pandas`.  
2. **Normalización mínima** de tipos (fechas y numéricos) y limpieza básica.  
3. **Checks de calidad**: nulos críticos, duplicados, rangos plausibles.  
4. **Integridad referencial**: `credits.movie_id` ∈ `movies.id`.  
5. **Joins** y **visualizaciones** exploratorias.

---

# 📈 Evidencias (muestra)

- **Duplicados** por `(title, release_date)` → se detectan títulos repetidos con mismas fechas.  
- **Rangos inválidos**: `budget < 0`, `revenue < 0`, `runtime <= 0` o `> 500`.  
- **Huérfanos** en `credits`: filas cuyo `movie_id` no está en `movies.id`.  
- **Distribuciones**: histograma de `runtime`; dispersión `budget` vs `revenue`.

### 📝 [Notebook](../../../notebooks/UT2-Extra.ipynb)

---

# 🧠 Resultados y discusión

| Hallazgo | Implicación |
|---|---|
| Tipos inconsistentes y nulos en campos clave | Requiere reglas de limpieza y *coercion* a numérico/fecha |
| Duplicados de títulos en misma fecha | Necesario definir una clave compuesta o usar `id` como referencia única |
| Huérfanos en `credits` | Riesgo de errores al hacer joins/aggregations |
| Presupuestos/ingresos extremos | Posibles outliers o registros mal tipeados |

> 💬 **Discusión:**  
> Este dataset refleja problemas “del mundo real”: campos JSON en texto, ids que no matchean perfecto, valores fuera de rango.  
> Para producción, conviene automatizar estos checks en **pipelines de validación** (Great Expectations/Pandera) y documentar supuestos.

---

# 🔗 Conexión con otras unidades

- **UT1:** EDA y multifuente → ahora con dos CSV y claves.  
- **UT3:** *Feature engineering* a partir de `genres`, `cast`, `crew` (parseo JSON).  
- **UT5:** Integración en pipelines ETL y almacenamiento en formatos columnares.

---

# 🧰 Stack técnico

**Python** · `pandas` · `matplotlib` · (`sqlite3` opcional para persistir tablas)

---

# 📚 Referencias

- Kaggle — *TMDB 5000 Movie Dataset*  
- Pandas — lectura de CSV, manejo de fechas y tipos  
- Validación de datos — Great Expectations / Pandera