---
title: "⚙️ UT5 – Actividad 15: Pipelines ETL, DataOps y Orquestación con Prefect"
date: 2025-12-02
---

# ⚙️ Pipelines ETL, DataOps y Orquestación con Prefect

---

# 🌍 Contexto

En esta actividad trabajé por primera vez con **Prefect**, una herramienta moderna para la orquestación de pipelines de datos.
Construí un **pipeline ETL completo** y exploré conceptos clave como **Tasks, Flows, DAGs implícitos, retries, caching, logging y concurrencia.**
Todo esto lo conecté con principios de **DataOps** como observabilidad, reproducibilidad y CI/CD para datos.
El escenario elegido fue un e-commerce con ventas diarias, ideal para modelar un flujo ETL clásico.

---

# 🎯 Objetivos

- Comprender los conceptos principales de Prefect.
- Implementar un pipeline **extract → transform → load** real.
- Investigar funcionalidades avanzadas: retries, caching, logging y concurrencia.
- Entender cómo funcionan los **Deployments** y los **Schedules**.
- Conectar Prefect con prácticas de **DataOps**.
- Comparar Prefect con herramientas alternativas (Airflow, Dagster).

---

# 🔧 Diseño del escenario

| Rol | Responsabilidad |
|------|----------------|
| **Business Data Owner** | Generar las ventas diarias |
| **Data Engineer** | Construir y operar el pipeline ETL |
| **Consumidores** | Dashboards, analistas y modelos |

El pipeline elegido es **batch**, porque las ventas ocurren diariamente y no requieren tiempo real.
Esto favorece la reproducibilidad, la validación y el control de calidad.

---

# 🏗️ Implementación del ETL en Prefect

## 1. Tasks implementadas

### 🔹 `extract_data()`
- Genera datos simulados de ventas.  
- Incluye logs para validar volumen y estructura.

### 🔹 `transform_data()`
Transforma los datos agregando:
- `total = cantidad * precio_unitario`  
- ticket size por categorías  
- mes y día de la semana  

### 🔹 `load_data()`
- Guarda los datos transformados en CSV.  
- Tiene **retries** configurados:
  - `retries=2`
  - `retry_delay_seconds=3`

Todas las tasks utilizan `log_prints=True` para capturar logs automáticamente.

---

## 2. Flow principal

### 🔹 `etl_flow()`

Orquesta todo:

1. Extraer  
2. Transformar  
3. Cargar  

Prefect detecta **dependencias automáticas** (DAG implícito) al pasar el resultado de una task como input de otra.

---

# ⚙️ Funcionalidades avanzadas investigadas

## 🔸 Retries  
Indispensables cuando hay fallos intermitentes en I/O o escritura.
Se validó usando una task que falla aleatoriamente.

## 🔸 Caching  
Permite evitar re-ejecuciones innecesarias cuando los inputs no cambiaron.
Ayuda directamente a la reproducibilidad y optimización del pipeline.

## 🔸 Logging estructurado  
Usé tanto:
- `log_prints=True`
- `get_run_logger()`

Permite logs centralizados y limpios en la UI de Prefect.

## 🔸 Concurrencia  
Prefect soporta ejecución paralela con `ConcurrentTaskRunner()`.  
Probado conceptualmente con procesamiento por región.

---

# 🛡️ Extensión DataOps — Validación de datos

Implementé la Opción A: **Validación con logging estructurado**.

### 🔹 `validate_data()`  

Validaciones implementadas:
- DataFrame no vacío  
- Nulos (warning)  
- Columnas requeridas (`fecha`, `producto`, `cantidad`, `precio_unitario`, `total`)  
- Tipos correctos  
- Valores negativos (warning)

Niveles de log usados:
- `logger.info()` → Todo ok  
- `logger.warning()` → Algo raro pero no crítico  
- `logger.error()` → Error crítico que frena el pipeline  

El flow actualizado `etl_flow_with_validation()` ejecuta:

`extract → validate → transform → load`

---

# 🔭 Conexión con DataOps

## 🟦 Observabilidad
Prefect ofrece:
- Estados claros para cada task  
- Logs centralizados  
- Métricas de ejecución  
- UI para monitoreo en tiempo real  
- Retries y errores visibles  

## 🟩 Reproducibilidad
El caching y la persistencia de resultados permiten:
- Repetir ejecuciones con resultados consistentes  
- Evitar reprocesamientos costosos  
- Recuperar pipelines fallados  

## 🟥 CI/CD para datos
Los **Deployments** permiten:
- Versionado de flows  
- Schedules programados  
- Separación de ambientes (dev/staging/prod)  
- Integración con GitHub Actions  

---

# ⚖️ Comparación rápida

## Prefect vs Airflow
| Aspecto     | Prefect          | Airflow                  |
| ----------- | ---------------- | ------------------------ |
| DAGs        | Implícitos       | Explícitos               |
| Complejidad | Baja             | Alta                     |
| Estilo      | Python puro      | DAG objects + operadores |
| UI          | Moderna          | Tradicional              |
| Ideal para  | Proyectos ágiles | Pipelines enterprise     |

## Prefect vs Dagster
| Aspecto    | Prefect          | Dagster                             |
| ---------- | ---------------- | ----------------------------------- |
| Enfoque    | Tasks/flows      | Data assets                         |
| Estructura | Flexible         | Muy opinada                         |
| Ideal      | Rápida iteración | Equipos grandes con linaje estricto |

---

# 📊 Resultados

- Pipeline ETL funcionando end-to-end
- Validación incorporada
- Logs detallados
- Retries funcionando
- Research completo de caching, logging, concurrencia y deployments
- Conexión clara con DataOps

---

# 🧠 Aprendizajes clave

- Prefect simplifica muchísimo la orquestación.
- Los DAGs implícitos permiten código mucho más limpio que Airflow.
- El logging estructurado es esencial en pipelines reales.
- La validación previa ahorra errores en producción.
- Entendí completamente la diferencia entre **Flow** (lógica) y **Deployment** (configuración ejecutable).

---

# 🔮 Próximos pasos

- Probar Prefect Cloud/Server para monitoreo visual.  
- Integrar validaciones con Great Expectations.  
- Explorar ejecución concurrente por región.  
- Crear un Deployment real con scheduling diario.  
- Integrar con GitHub Actions para CI/CD de datos.  

---

# 🧰 Stack técnico

**Python** · Prefect · Pandas · NumPy  
Conceptos: ETL · Orquestación · Retries · Logging · DAGs · DataOps

---

# 📝 Evidencias

### 📝 [Notebook](../../../notebooks/UT5-1.ipynb)

---

# 📚 Referencias

- Práctica oficial: <https://juanfkurucz.com/ucu-id/ut5/15-etl-dataops-prefect/>  
- [Documentación oficial de Prefect](https://docs.prefect.io/)
- [Prefect Concepts Overview](https://docs.prefect.io/latest/concepts/)
- [Prefect Tasks Documentation](https://docs.prefect.io/latest/concepts/tasks/)
- [Prefect Flows Documentation](https://docs.prefect.io/latest/concepts/flows/)
- [Prefect Caching Documentation](https://docs.prefect.io/latest/concepts/tasks/#caching)
- [Prefect Deployments Documentation](https://docs.prefect.io/latest/concepts/deployments/)