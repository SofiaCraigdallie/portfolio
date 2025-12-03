---
title: "⚙️ UT5 – Pipelines ETL, DataOps y Orquestación con Prefect"
date: 2025-12-02
---

# ⚙️ Unidad Temática 5: Pipelines ETL, DataOps y Orquestación con Prefect

La quinta unidad del portafolio se mete de lleno en el corazón de la **Ingeniería de Datos moderna**: construir pipelines limpios, reproducibles y monitoreables.
Acá pasé de “escribir scripts sueltos” a **pensar en sistemas**, flujos completos y ciclos de vida de datos.

UT5 introduce tres pilares que hoy son estándar en cualquier equipo de datos serio:
**ETL estructurado**, **DataOps** y **orquestación declarativa** con Prefect.

Aprendí a diseñar pipelines robustos, separando tareas, controlando estados, registrando logs y automatizando ejecuciones. Es el puente entre el código y la operación continua.

---

## 🎯 Objetivos generales

- Construir **pipelines ETL reales** con Prefect (extract–transform–load).
- Comprender la arquitectura de **Tasks**, **Flows**, dependencias y estados.
- Implementar **retries**, caching, logging estructurado y validación.
- Crear **Deployments** y programar ejecuciones con *scheduling*.
- Conectar conceptos de **DataOps**: observabilidad, reproducibilidad, CI/CD para datos.
- Comparar Prefect con herramientas de orquestación como **Airflow** y **Dagster**.
- Integrar flows con prácticas profesionales de ingeniería de datos.

---

## 🧩 Proyectos incluidos

| Proyecto                                 | Descripción                                                   | Enlace                                      |
| ---------------------------------------- | ------------------------------------------------------------- | ------------------------------------------- |
| 🔄 **ETL con Prefect**                   | Extract–Transform–Load con tasks, retries, logs y estado.     | [Ver artículo](./15-prefect.md) |
| 🧪 **Validación + Logging estructurado** | Validación de datos, tests simples y manejo de errores.       | [Ver artículo](./16-googlecloud.md) |
| 📦 **Deployments + Scheduling**          | Servir flows, crear cron jobs y preparar pipeline productivo. | [Ver artículo](./17-googlecloud2.md) |

---

## 📊 Competencias desarrolladas

- Diseño de **pipelines ETL robustos** en Python.
- Manejo profesional de **Prefect**: flows, tasks, mappings, runners y deployments.
- Uso de **logging estructurado** para trazabilidad clara.
- Implementación de **retries**, **time-outs** y **cache** en tareas críticas.
- Creación de **schedules** (cron) y ejecución automática.
- Integración del concepto de **DataOps**: mantener pipelines limpios, observables y reproducibles.
- Comparación crítica entre herramientas de orquestación (Prefect vs Airflow vs Dagster).
- Comprensión de cómo se lleva un pipeline de “notebook” a “producción”.

---

## 🧠 Reflexión final

UT5 me hizo pensar como un ingeniero de datos que trabaja para producción y no solo para un notebook.
Aprendí que un pipeline no es código corriendo: es **un sistema que debe sobrevivir al tiempo, a los errores y a las sorpresas de los datos**.

Prefect me mostró un camino moderno y elegante para orquestar procesos:
flujos declarativos, logs claros, retries automáticos, y la posibilidad de versionar y desplegar como si fuese software real.

Esta unidad consolidó la mentalidad DataOps:
**visibilidad, orden, reproducibilidad y automatización**.
Hoy puedo diseñar un pipeline que no solo funciona, sino que se puede operar todos los días sin drama.

---

# 🧰 Stack técnico

**Lenguaje:** Python
**Librerías:** Prefect · Pandas · NumPy
**Conceptos:** Tasks · Flows · Retries · Logging estructurado · Caching · Deployments · Scheduling · DataOps

---

# 📚 Referencias

- Material oficial UT5: [https://juanfkurucz.com/ucu-id/ut5/](https://juanfkurucz.com/ucu-id/ut5/)
- [Docs Prefect](https://docs.prefect.io/)
- [Conceptos de orquestación](https://docs.prefect.io/latest/concepts/)
- [Prefect Deployments](https://docs.prefect.io/latest/concepts/deployments/)