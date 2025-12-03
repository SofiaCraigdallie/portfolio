---
title: "☁️ UT5 – Actividad 16: A Tour of Google Cloud Hands-on Labs"
date: 2025-12-02
---

# ☁️ UT5 – Google Cloud Skills: *A Tour of Google Cloud Hands-on Labs*

> 🚀 Lab GSP282 — Mi primera vuelta por Google Cloud

---

# 🌍 Contexto

En esta actividad hice el lab introductorio **“A Tour of Google Cloud Hands-on Labs (GSP282)”** de Google Cloud Skills Boost.
Es un lab pensado para el primer contacto con Google Cloud: te dan un proyecto temporal, credenciales temporales, y te hacen recorrer las partes esenciales de la consola.

El objetivo es simple: **entender cómo se mueve uno dentro de Google Cloud**, qué es un proyecto, cómo funcionan permisos, y cómo habilitar APIs.

---

# 🎯 Objetivos del lab

- Entrar al ambiente temporal del lab sin mezclar cuentas.
- Navegar la Cloud Console y entender dónde está todo.
- Comprender la idea de “Project” en Google Cloud.
- Revisar roles y permisos básicos (IAM).
- Habilitar una API desde la consola.
- Familiarizarme con el formato típico de los labs de Google.

---

# 🕒 Actividades realizadas

| Actividad                 | Tiempo | Resultado                                       |
| ------------------------- | :----: | ----------------------------------------------- |
| Acceso a la Cloud Console |   10m  | Sesión limpia con credenciales temporales       |
| Exploración del proyecto  |   10m  | Entendí Project ID, organización y recursos     |
| IAM y permisos            |   15m  | Roles Viewer / Editor / Owner y cómo asignarlos |
| Habilitar APIs            |   10m  | Activé Dialogflow API y exploré la API Library  |

---

# 🧭 Desarrollo del Lab

## 1) Cómo funcionan los labs de Google Cloud

Antes de comenzar con las tareas prácticas, se aprendió sobre los componentes estándar de todos los labs en la plataforma:

- **Start Lab (botón)**: Crea un ambiente temporal de Google Cloud con todos los servicios y credenciales necesarios habilitados. Inicia un temporizador de cuenta regresiva.

- **Créditos**: El costo de un lab. Generalmente 1 crédito equivale a 1 dólar estadounidense. Algunos labs introductorios (como este) son gratuitos. Los labs más especializados cuestan más porque involucran tareas de computación más pesadas.

- **Tiempo**: Especifica la cantidad de tiempo disponible para completar el lab. Cuando el temporizador llega a 00:00:00, el ambiente temporal y los recursos son eliminados.

- **Score (Puntuación)**: Muchos labs incluyen un sistema de puntuación llamado "activity tracking" que verifica la finalización de pasos específicos en orden. Solo completando todos los pasos se puede recibir crédito de finalización.

Qwiklabs (ahora Skills Boost) es la plataforma que administra esto: te crea un entorno seguro donde no podés romper tu cuenta real.

---

## 2) Acceso a la Cloud Console

El panel del lab te da:

- Botón **Open Google Cloud Console**
- Usuario y contraseña temporales
- **Project ID** único

**Regla de oro**: SIEMPRE abrir en ventana incógnita. Si mezclás cuentas, el lab te rompe la sesión.

Pasos:

1. Click → “Open Google Cloud Console”
2. Loguearse con las credenciales del lab
3. Aceptar términos
4. Llegás al dashboard de Google Cloud

---

## 3) Exploración del Proyecto

### ¿Qué es un Project en Google Cloud?

Un **Project** es la unidad base de organización. Aísla:

- Recursos
- Configuraciones
- API habilitadas
- Permisos
- Facturación

**Project ID** → único, permanente, y no se puede cambiar.
**Project Name** → lo podés renombrar cuando quieras.

Exploré los menús principales:

- Compute Engine
- Cloud Storage
- IAM
- APIs & Services
- BigQuery
- Networking

Google Cloud está ordenado por categorías, lo cual ayuda bastante.

---

## 4) IAM — Roles y Permisos

En IAM se controla quién puede hacer qué.

Elementos clave:

- **Principals** → usuarios, grupos, service accounts
- **Permisos** → acciones específicas
- **Roles** → conjunto de permisos

Roles básicos del proyecto:

| Rol        | Qué puede hacer                         |
| ---------- | --------------------------------------- |
| **Viewer** | Ver todo, modificar nada                |
| **Editor** | Ver + modificar recursos                |
| **Owner**  | Editor + manejar permisos y facturación |

Tarea hecha:

- Entré a **IAM & Admin > IAM**
- Agregué un usuario con rol Viewer
- Verifiqué que apareciera en la lista

**Dato importante**: el rol *Editor* NO puede cambiar permisos, solo Owner.

---

## 5) APIs y Servicios

Google Cloud tiene **+200 APIs**.

Para usarlas hay que **habilitarlas** explícitamente en cada proyecto.

Tarea hecha: Habilitar **Dialogflow API**.

Pasos:

1. APIs & Services → Library
2. Buscar “Dialogflow”
3. Click → Enable
4. Verificar que quedó habilitada
5. Revisar documentación y “Try this API”

La API Library está organizada por categorías: ML, Storage, Compute, Networking, Security, Big Data, etc.

---

# 🧠 Conceptos clave que me llevé

### 🔹 Google Cloud Platform

Plataforma enorme con servicios para cómputo, almacenamiento, ML, redes, seguridad y más.

### 🔹 Proyectos

Donde viven los recursos. Cada proyecto tiene su propio Project ID y su propia facturación.

### 🔹 IAM

Sistema de permisos con granularidad fina. Fundamental para seguridad y DataOps.

### 🔹 APIs

Servicios específicos que tenés que *habilitar* antes de usar.
Vienen con métricas, documentación y client libraries.

### 🔹 Cloud Console

El “hub” visual de Google Cloud. Todo está ahí.

---

# 🧩 Aplicaciones prácticas para Ingeniería de Datos

### 🔸 Organización

Proyectos diferentes para dev / staging / prod.

### 🔸 Seguridad

IAM es *clave* para controlar quién toca datos, notebooks, buckets, VMs, etc.

### 🔸 APIs

Para data engineering vas a usar varias:
BigQuery, Dataflow, Storage, Pub/Sub, Vertex AI.

### 🔸 Automatización

Habilitar APIs y permisos es parte esencial del setup de cualquier pipeline.

---

# ⚠️ Desafíos encontrados

### 1) La consola abruma al principio

Muchísimas opciones.
**Solución**: recorrer categoría por categoría.

### 2) IAM al principio parece abstracto

Hasta que asignás un rol y ves qué cambia.
**Conclusión**: IAM se aprende haciéndolo.

### 3) “Habilitar una API” no es intuitivo

Después entendés: es literalmente “activar un servicio”.

---

# 📝 Reflexión final

Este lab es perfecto como puerta de entrada al ecosistema de Google Cloud.
Te obliga a moverte, tocar, habilitar, explorar y entender la estructura real que Google usa para administrar proyectos.

**Takeaways:**

- Google Cloud organiza todo alrededor del Project ID
- IAM es crítico para cualquier flujo de datos
- Las APIs hay que habilitarlas manualmente
- La consola es muy potente, pero lleva práctica
- Los labs son la mejor forma de aprender: cero riesgo, todo práctico

**Valor para Ingeniería de Datos**:

- Te da el vocabulario base para hablar de GCP
- Te prepara para labs más técnicos (BigQuery, Dataflow, GCS)
- Sienta las bases para MLOps / DataOps en la nube
- Te permite avanzar hacia certificaciones Google Cloud

---

# 📚 Referencias

- [Google Cloud Skills Boost](https://www.skills.google/)
- [Lab GSP282: A Tour of Google Cloud Hands-on Labs](https://www.skills.google/focuses/2794?parent=catalog)
- [Google Cloud Console Documentation](https://cloud.google.com/docs/overview)
- [Cloud IAM Documentation](https://cloud.google.com/iam/docs)
- [APIs Explorer Directory](https://developers.google.com/apis-explorer)