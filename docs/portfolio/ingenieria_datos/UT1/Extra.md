---
title: "🌐 Proyecto extra — Explorando datos meteorológicos desde una API (Open-Meteo)"
date: 2025-10-12
---

# 🌐 Proyecto extra — Explorando datos meteorológicos desde una API (Open-Meteo)

---

# 🌍 Contexto

Proyecto extra de **UT1 – Exploración y Fuentes** para demostrar manejo de **fuentes JSON vía API**, normalización y EDA básico.  
Usamos la API pública de **Open-Meteo** para descargar series horarias de temperatura, humedad y viento de una ciudad (ej.: Montevideo), y transformarlas en un dataframe analizable.

---

# 🎯 Objetivos

- Consumir una **API pública** (JSON) y documentar el request.
- **Normalizar** la respuesta con `pandas` y manejar **timezones**.
- Realizar **EDA**: distribuciones, resampling diario, outliers.
- Guardar datasets en **parquet/csv** para reproducibilidad.

---

# 📦 Fuente de datos

| Aspecto | Detalle |
|---|---|
| API | Open-Meteo (gratuita, sin API key) |
| Endpoint | `/v1/forecast?latitude=...&longitude=...` |
| Variables | `temperature_2m`, `relative_humidity_2m`, `wind_speed_10m` (hourly) |
| Zona horaria | configurable (`timezone=auto`) |
| Formato | JSON anidado (`hourly.time`, `hourly.temperature_2m`, …) |

---

# 🧰 Requisitos

```bash
pip install pandas pyarrow requests matplotlib
```

---

# 🛠️ Ingesta + Normalización (código)

```python
import os, json, requests
import pandas as pd
from pathlib import Path

# --- Parámetros (Montevideo aprox.)
LAT, LON = -34.9011, -56.1645
PARAMS = {
    "latitude": LAT,
    "longitude": LON,
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "timezone": "auto"  # usa la TZ local del lugar
}

URL = "https://api.open-meteo.com/v1/forecast"

# --- Descarga
r = requests.get(URL, params=PARAMS, timeout=30)
r.raise_for_status()
raw = r.json()

# --- Normalización a DataFrame
hourly = raw.get("hourly", {})
df = pd.DataFrame(hourly)

# Esperamos columnas: time, temperature_2m, relative_humidity_2m, wind_speed_10m
assert {"time", "temperature_2m", "relative_humidity_2m", "wind_speed_10m"}.issubset(df.columns), \
    f"Columnas inesperadas: {df.columns.tolist()}"

# --- Tipos y fecha
df["time"] = pd.to_datetime(df["time"], utc=False)  # ya viene en TZ 'auto'
df = df.set_index("time").sort_index()

# --- Guardar crudos y limpios
out = Path("data/openmeteo")
out.mkdir(parents=True, exist_ok=True)
Path(out / "raw_response.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
df.to_csv(out / "hourly_montevideo.csv", index=True)
df.to_parquet(out / "hourly_montevideo.parquet")  # eficiente para pipelines

df.head()
```

---

# 🧹 Limpieza mínima

```python
# Renombrado amistoso
df = df.rename(columns={
    "temperature_2m": "temp_c",
    "relative_humidity_2m": "rh_pct",
    "wind_speed_10m": "wind_ms"
})

# Filtros y validaciones simples
df = df[(df["temp_c"].between(-40, 60)) & (df["rh_pct"].between(0, 100)) & (df["wind_ms"].between(0, 60))]
summary = df.describe()
summary
```

---

# 📊 EDA rápido

```python
import matplotlib.pyplot as plt

# Resampling diario
daily = df.resample("D").agg({"temp_c":"mean", "rh_pct":"mean", "wind_ms":"mean"})

# 1) Tendencia diaria de temperatura
daily["temp_c"].plot(figsize=(9,4), title="Temperatura media diaria (°C)")
plt.xlabel("Fecha"); plt.ylabel("°C"); plt.tight_layout(); plt.show()

# 2) Distribución de humedad
df["rh_pct"].plot(kind="hist", bins=30, title="Distribución de humedad relativa (%)")
plt.xlabel("%"); plt.tight_layout(); plt.show()

# 3) Relación viento vs temperatura
df.plot(x="wind_ms", y="temp_c", kind="scatter", title="Viento (m/s) vs Temperatura (°C)", s=10, alpha=0.6)
plt.tight_layout(); plt.show()
```

---

# 🧠 Resultados y discusión

| Hallazgo | Interpretación |
|---|---|
| Variabilidad diaria de temperatura | Picos y valles coherentes con ciclos día/noche y condiciones locales. |
| Humedad centrada en rangos medios-altos | Consistente con clima costero; colas altas en días lluviosos. |
| Viento y temperatura con correlación baja | Fenómeno más influido por presión/sistemas frontales que por temperatura local. |

---

# 🔗 Conexión con otras unidades

- **UT2:** calidad de datos (faltantes en API, picos espurios) y **pipelines** de limpieza.
- **UT3:** *feature engineering* temporal (lags, rolling mean) y codificación estacional (mes/día).

---

# ⚖️ Consideraciones éticas / licencia

- La API es **pública** y gratuita; citar **Open-Meteo** en el repositorio.  
- Documentar **limitaciones** (horizonte corto, posibles cortes del servicio).  
- Evitar sobrecargar el endpoint (incluir **caché** local como arriba).

---

# 🧰 Stack técnico

**Python** · `requests` · `pandas` · `matplotlib` · `pyarrow` (parquet)

---

# 📂 Artefactos

- `data/openmeteo/raw_response.json` (crudo)
- `data/openmeteo/hourly_montevideo.parquet` y `.csv` (normalizados)

---

# 📚 Referencias

- Open-Meteo API (Forecast): https://open-meteo.com/en/docs
- Pandas IO JSON: https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-json
- Time series resampling: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

---

### 📝 [Notebook](../../../notebooks/UT1-Extra.ipynb)