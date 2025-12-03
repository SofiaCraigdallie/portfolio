---
title: "☁️ UT5 – Actividad 17: Creating a Data Transformation Pipeline with Cloud Dataprep"
date: 2025-12-02
---

# UT5 – Google Cloud Skills: *Creating a Data Transformation Pipeline with Cloud Dataprep*

> 🚀 Lab GSP430 — Creando un pipeline de transformación con Dataprep

---

# 🌍 Contexto

En esta actividad completé el lab **“Creating a Data Transformation Pipeline with Cloud Dataprep (GSP430)”**, un lab intermedio donde usás **Cloud Dataprep / Alteryx Designer Cloud** para preparar, limpiar y transformar datos de forma visual.

El lab es un clásico caso de e-commerce: datos de sesiones en BigQuery → los preparo en Dataprep → los vuelvo a dejar listos en BigQuery como tabla final para reporting. Ideal para entender cómo es un pipeline ETL visual en Google Cloud.

---

# 🎯 Objetivos

- Usar la interfaz visual de Dataprep sin morir en el intento
- Conectar BigQuery como fuente y como destino
- Explorar calidad y estructura del dataset
- Limpiar datos y quitar ruido
- Crear columnas nuevas y enriquecer el dataset
- Ejecutar el pipeline en Dataflow (bajo el capó)
- Dejar los datos listos en BigQuery para análisis

---

# 🕒 Actividades realizadas

| Actividad                    | Tiempo | Resultado                              |
| ---------------------------- | :----: | -------------------------------------- |
| Habilitar Dataprep           |   10m  | Servicio listo y permisos configurados |
| Crear dataset en BigQuery    |   10m  | Dataset `ecommerce` + tabla raw creada |
| Conectar BigQuery a Dataprep |   10m  | Flow creado y dataset importado        |
| Explorar columnas            |   15m  | Tipos, calidad, nulos, distribuciones  |
| Limpieza                     |   15m  | Filtros + columnas removidas           |
| Enriquecimiento              |   15m  | Nuevas columnas calculadas             |
| Ejecutar job                 |   10m  | Tabla `revenue_reporting` generada     |

---

# 🏗️ Desarrollo del Lab

## 1) Habilitación y acceso a Dataprep

Antes de usar Dataprep hay que habilitar el servicio y crear la identidad:

```bash
gcloud beta services identity create --service=dataprep.googleapis.com
```

Luego entré por:

**Console → Analytics → Alteryx Designer Cloud**

- Aceptás términos
- Permitís acceso al proyecto
- Te logueás con la cuenta temporal
- Dataprep crea su bucket y listo

**Dato importante**: solo funciona bien en Chrome.

---

## 2) Dataset inicial en BigQuery

Creé un dataset:

- **ID**: `ecommerce`
- Ubicación default (US)

Después ejecuté una query para traer un subset de datos reales de Google Analytics (solo un día):

```sql
CREATE OR REPLACE TABLE ecommerce.all_sessions_raw_dataprep AS
SELECT *
FROM `data-to-insights.ecommerce.all_sessions_raw`
WHERE date = '20170801';
```

Quedan ~56.000 filas con datos reales de sessions:
visitorId, hits, revenue, pageviews, ciudades, etc.

---

## 3) Conectar BigQuery a Dataprep

En Dataprep:

1. **Create a new flow**

   * Name: *Ecommerce Analytics Pipeline*
   * Description: *Revenue reporting table*

2. Add dataset → elegir BigQuery → dataset `ecommerce` → tabla `all_sessions_raw_dataprep`.

Dataprep analiza automáticamente la estructura y calidad apenas cargas los datos.

---

## 4) Exploración visual

La interfaz de Dataprep es muy cómoda para revisar el dataset:

- **Esquema** (izquierda): tipos detectados, longitudes, nulos
- **Datos sampleados** (centro): preview con colores según calidad
- **Sugerencias** (derecha): transformaciones recomendadas

Lo mejor:

- Histogramas por columna
- Detecta tipos erróneos
- Marca problemas de calidad
- Identifica valores raros

Encontré:

- Campos numéricos típicos: revenue, pageviews
- Datos categóricos: city, country, SKU
- Varios nulos en columnas de transacción
- Columna `eCommerceAction_type` codificada (0–8)

---

## 5) Limpieza de datos

### 🔹 Filtro de hits relevantes (PAGE)

El dataset tenía varios tipos de hit. Para análisis de páginas, solo me sirven los **PAGE**.

Pasos:

- Click en la barra “PAGE” del histograma
- “Keep rows”
- Listo, filtrado sin escribir código

### 🔹 Eliminación de columnas inútiles

Removí varias columnas:

- Totalmente nulas
- Duplicadas
- Metadatos internos que no aportaban

---

## 6) Enriquecimiento del dataset

### 🔹 Crear `unique_session_id`

Los campos `fullVisitorId` y `visitId` por separado no identifican una sesión globalmente.

Solución: concatenarlos.

Dataprep → Merge columns

- Separador: `-`
- Nuevo campo: `unique_session_id`

### 🔹 Etiquetar acciones e-commerce

La columna `eCommerceAction_type` venía con números 0–8.

Creé un **case statement** con etiquetas inteligibles:

- 0 → Unknown
- 3 → Add to cart
- 6 → Completed purchase
  ... etc.

Nueva columna: `eCommerceAction_label`.

### 🔹 Normalización de revenue

`totalTransactionRevenue` viene *multiplicado por un millón*.

Transformación:

```
DIVIDE(totalTransactionRevenue,1000000)
```

Nueva columna decimal: `totalTransactionRevenue1`.

---

## 7) Ejecución del pipeline → BigQuery

La ejecución se hace vía:

**Dataflow + BigQuery**

Pasos:

- Run Job → Edit
- Output: BigQuery
- Dataset: `ecommerce`
- Nueva tabla: `revenue_reporting`
- Opción: Overwrite (“Drop table every run”)
- RUN

Dataflow compila todo a Apache Beam y lo ejecuta en paralelo.

Luego verifiqué la tabla final en BigQuery.

---

# 🧠 Conceptos clave aprendidos

### 🔸 Cloud Dataprep

- Herramienta visual, cero código
- Detección automática de calidad
- Sugerencias inteligentes
- Integración total con Google Cloud

### 🔸 Flows & Recipes

- Flow = el pipeline entero
- Recipe = la lista de transformaciones
- Cada paso se puede ver/editar con preview en tiempo real

### 🔸 Transformaciones útiles

- Filtros
- Eliminación de columnas
- Create column
- Case statements
- Merge columns
- Custom formulas

### 🔸 BigQuery ↔ Dataprep

- BigQuery como entrada y salida
- Lectura rápida de datos grandes
- Escritura escalable con Dataflow

### 🔸 Dataflow

Dataprep → genera código Beam → Dataflow lo ejecuta escalado.
Escala solo, maneja errores y paraleliza sin esfuerzo.

---

# 🚀 Aplicaciones prácticas

### ✔️ ML

Ideal para preparar features antes de entrenar modelos (normalización, limpieza, derivación).

### ✔️ ETL visual

Perfecto para analistas o equipos mixtos que no quieren escribir Python/Spark.

### ✔️ Reporting

Facilita la construcción de tablas limpias para dashboards.

### ✔️ Data Quality

Te permite entender un dataset desconocido en minutos.

### ✔️ Colaboración

Documenta las transformaciones de forma visual —todo el equipo lo entiende.

---

# ⚠️ Desafíos

1. **Interfaz cargada**
   → Se resuelve con práctica y entendiendo Flow → Recipe.

2. **Solo Chrome**
   → Limitación técnica.

3. **Case statements largos**
   → Requieren paciencia, pero Dataprep te deja ver todo antes de aplicar.

4. **Jobs lentos**
   → Dataflow tarda. Normal en pipelines distribuidos.

5. **Debugging**
   → Hacer transformaciones de a una ayuda muchísimo.

---

# 📝 Reflexión final

Este lab es una excelente introducción al enfoque “visual-first” para ETL. Te muestra:

- Que Dataprep puede reemplazar mucho código para tareas repetitivas
- Que BigQuery y Dataprep se integran sin fricción
- Que Dataflow te da escalabilidad real sin escribir Beam
- Que explorar datos visualmente acelera muchísimo la comprensión

**Takeaways clave**:

- Explorá antes de transformar
- Dataprep es fuerte en calidad de datos
- La integración BigQuery ↔ Dataprep ↔ Dataflow es muy poderosa
- Los recipes funcionan como documentación ejecutable
- Es una herramienta ideal para prototipar rápido ETLs complejos

---

# 📚 Referencias

- [Google Cloud Skills Boost](https://www.skills.google/)
- [Lab GSP430: Creating a Data Transformation Pipeline with Cloud Dataprep](https://www.skills.google/focuses/4415?catalog_rank=%7B%22rank%22%3A6%2C%22num_filters%22%3A1%2C%22has_search%22%3Atrue%7D&parent=catalog&search_id=60910456)
- [Cloud Dataprep Documentation](https://cloud.google.com/dataprep/docs)
- [Alteryx Designer Cloud](https://www.alteryx.com/products/alteryx-designer-cloud)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Cloud Dataflow Documentation](https://cloud.google.com/dataflow/docs)