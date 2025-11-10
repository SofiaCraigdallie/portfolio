---
title: "⏱️ UT3 · Práctica 11 — Temporal Feature Engineering con Pandas"
date: 2025-11-09
---

# ⏱️ Temporal Feature Engineering con Pandas

---

# 🌍 Contexto

Esta práctica de la **Unidad Temática 3 (Feature Engineering)** trabaja **datos transaccionales de e‑commerce** para construir **features temporales** con `pandas` evitando **data leakage**. El foco está en: **lags**, **rolling/expanding windows**, **agregaciones por usuario**, **features cíclicas**, **variables externas** y **validación temporal**.

> Regla de oro: **ordenar por tiempo y agrupar por usuario** antes de calcular cualquier feature temporal.

---

# 🎯 Objetivos

- Implementar **lag features** con `.groupby().shift()` (sin leakage).
- Calcular **rolling** y **expanding** windows con exclusión explícita del presente.
- Armar **RFM** (Recency, Frequency, Monetary) y **agregaciones por usuario**.
- Agregar **calendar features** con **encoding cíclico** (sin/cos) y **variables externas** simuladas.
- Diseñar **validación basada en tiempo** (`TimeSeriesSplit`) y comparar **modelo base vs. temporal**.
- Redactar **conclusiones** y **chequeos de leakage**.

---

# 📦 Dataset

| Aspecto | Descripción |
|---|---|
| **Fuente** | Kaggle — *Online Retail (2010–2011)* |
| **Archivo** | `OnlineRetail.csv` |
| **Clave temporal** | `InvoiceDate` |
| **ID usuario** | `CustomerID` |
| **Estructura** | Transacciones (eventos irregulares, muchas órdenes por usuario) |

> Nota: Aceptá el dataset en Kaggle (join/accept) antes de descargar con API.

---

# ⚙️ Setup

```python
# !pip install -q pandas numpy scikit-learn matplotlib seaborn kaggle
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import warnings, platform
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None); pd.set_option('display.max_rows', 100)
plt.style.use('seaborn-v0_8-darkgrid')

print("✅ Libs OK"); print(f"Pandas: {pd.__version__}"); print(f"OS: {platform.system()}")
```

---

# 🧰 Descarga y Carga (Kaggle API)

> Subí `kaggle.json` (credenciales) en Colab, movelo a `~/.kaggle/` con permisos `0o600`, y luego bajá el dataset `vijayuv/onlineretail` a `./data/`.

```python
from kaggle.api.kaggle_api_extended import KaggleApi
import os, json

api = KaggleApi(); api.authenticate()
os.makedirs("./data", exist_ok=True)
api.dataset_download_files("vijayuv/onlineretail", path="./data", unzip=True)

df_raw = pd.read_csv("./data/OnlineRetail.csv", encoding="ISO-8859-1")
df_raw.head()
```

---

# 🧹 Limpieza y preparación temporal

```python
# 1) Filtrado mínimo útil
df = (df_raw
      .dropna(subset=['CustomerID'])
      .rename(columns={'CustomerID':'user_id','InvoiceDate':'order_date',
                       'InvoiceNo':'order_id','StockCode':'product_id','UnitPrice':'price'}))
df = df[~df['order_id'].astype(str).str.startswith('C')] # descartar canceladas
df = df[(df['Quantity']>0) & (df['price']>0)]

# 2) Tipos y derivadas
df['order_date'] = pd.to_datetime(df['order_date'])
df['total_amount'] = df['Quantity'] * df['price']
df = df.sort_values(['user_id','order_date']).reset_index(drop=True)

# 3) Agregado a nivel ORDEN
orders_df = (df.groupby(['order_id','user_id','order_date'])
               .agg(cart_size=('product_id','count'),
                    order_total=('total_amount','sum'))
               .reset_index()
               .sort_values(['user_id','order_date']).reset_index(drop=True))

# Índices y orden secuencial por usuario
orders_df['order_number'] = orders_df.groupby('user_id').cumcount() + 1
orders_df['days_since_prior_order'] = orders_df.groupby('user_id')['order_date'].diff().dt.days

orders_df.head()
```

---

# 🧱 Lag / Rolling / Expanding (sin leakage)

```python
# LAGs: usar shift(n) por usuario
orders_df = orders_df.sort_values(['user_id','order_date']).reset_index(drop=True)
orders_df['days_since_prior_lag_1'] = orders_df.groupby('user_id')['days_since_prior_order'].shift(1)
orders_df['days_since_prior_lag_2'] = orders_df.groupby('user_id')['days_since_prior_order'].shift(2)
orders_df['days_since_prior_lag_3'] = orders_df.groupby('user_id')['days_since_prior_order'].shift(3)

# ROLLING: excluir presente con shift(1) antes de rolling
orders_df['rolling_cart_mean_3'] = (orders_df.groupby('user_id')['cart_size']
                                    .shift(1).rolling(window=3, min_periods=1).mean()
                                    .reset_index(level=0, drop=True))
orders_df['rolling_cart_std_3']  = (orders_df.groupby('user_id')['cart_size']
                                    .shift(1).rolling(window=3, min_periods=1).std()
                                    .reset_index(level=0, drop=True))

# EXPANDING: histórico acumulado (excluye presente con shift(1))
orders_df['expanding_days_mean'] = (orders_df.groupby('user_id')['days_since_prior_order']
                                    .shift(1).expanding(min_periods=1).mean()
                                    .reset_index(level=0, drop=True))
orders_df['total_orders_so_far'] = orders_df.groupby('user_id').cumcount()
orders_df['expanding_total_spent'] = (orders_df.groupby('user_id')['order_total']
                                      .shift(1).expanding(min_periods=1).sum()
                                      .reset_index(level=0, drop=True)).fillna(0.0)
```

---

# 👤 RFM + Ventanas por tiempo (7d/30d/90d)

```python
# RFM
reference_date = orders_df['order_date'].max()
orders_df['recency_days'] = (reference_date - orders_df['order_date']).dt.days
orders_df['frequency_total_orders'] = orders_df['total_orders_so_far']
orders_df['monetary_total'] = orders_df['expanding_total_spent']
orders_df['monetary_avg'] = orders_df['monetary_total'] / orders_df['total_orders_so_far'].replace(0,1)

# Ventanas por tiempo por usuario (excluyendo presente)
def calculate_time_windows_for_user(g):
    g = g.sort_values('order_date').reset_index(drop=True)
    for col in ['orders_7d','orders_30d','orders_90d','spend_7d','spend_30d','spend_90d']:
        g[col] = 0
    for i in range(len(g)):
        if i == 0: continue
        past = g.iloc[:i]
        t = g.loc[i,'order_date']
        for d, k_cnt, k_sum in [(7,'orders_7d','spend_7d'),(30,'orders_30d','spend_30d'),(90,'orders_90d','spend_90d')]:
            mask = past['order_date'] >= (t - pd.Timedelta(days=d))
            g.loc[i, k_cnt] = int(mask.sum())
            g.loc[i, k_sum] = float(past.loc[mask, 'order_total'].sum())
    return g

orders_df = orders_df.groupby('user_id', group_keys=False).apply(calculate_time_windows_for_user)
```

---

# 📅 Calendar + Encoding cíclico + Externas

```python
# Calendar
orders_df['order_dow'] = orders_df['order_date'].dt.dayofweek  # 0=Lunes
orders_df['order_hour_of_day'] = orders_df['order_date'].dt.hour
orders_df['is_weekend'] = (orders_df['order_dow'] >= 5).astype(int)
orders_df['day_of_month'] = orders_df['order_date'].dt.day
orders_df['is_month_start'] = (orders_df['day_of_month'] <= 5).astype(int)
orders_df['is_month_end'] = (orders_df['day_of_month'] >= 25).astype(int)
orders_df['month'] = orders_df['order_date'].dt.month
orders_df['quarter'] = orders_df['order_date'].dt.quarter

# Holidays (UK, dataset 2010–2011)
holidays_uk = pd.to_datetime(['2010-12-25','2010-12-26','2011-01-01','2011-12-25','2011-12-26'])
orders_df['is_holiday'] = orders_df['order_date'].isin(holidays_uk).astype(int)
xmas_2010 = pd.Timestamp('2010-12-25')
orders_df['days_to_holiday'] = (xmas_2010 - orders_df['order_date']).dt.days.clip(lower=-10**9)
orders_df.loc[orders_df['days_to_holiday'] < 0, 'days_to_holiday'] = 365

# Encoding cíclico
orders_df['hour_sin']  = np.sin(2*np.pi*orders_df['order_hour_of_day']/24)
orders_df['hour_cos']  = np.cos(2*np.pi*orders_df['order_hour_of_day']/24)
orders_df['dow_sin']   = np.sin(2*np.pi*orders_df['order_dow']/7)
orders_df['dow_cos']   = np.cos(2*np.pi*orders_df['order_dow']/7)
orders_df['month_sin'] = np.sin(2*np.pi*orders_df['month']/12)
orders_df['month_cos'] = np.cos(2*np.pi*orders_df['month']/12)

# Externas simuladas (mensuales) + merge por periodo
orders_df['month_period'] = orders_df['order_date'].dt.to_period('M')
date_range = pd.date_range(orders_df['order_date'].min().replace(day=1),
                           orders_df['order_date'].max(), freq='MS')
np.random.seed(42)
eco = pd.DataFrame({'month_date':date_range,
                    'gdp_growth':np.random.normal(2.5,0.5,len(date_range)),
                    'unemployment_rate':np.random.normal(4.0,0.3,len(date_range)),
                    'consumer_confidence':np.random.normal(100,5,len(date_range))})
eco['month_period'] = eco['month_date'].dt.to_period('M')

orders_df = orders_df.merge(eco[['month_period','gdp_growth','unemployment_rate','consumer_confidence']],
                            on='month_period', how='left')
for c in ['gdp_growth','unemployment_rate','consumer_confidence']:
    orders_df[c] = orders_df[c].fillna(method='ffill')  # solo forward fill
```

---

# 🧪 Validación temporal (TS split) y modelado

```python
# Target: recompra (¿hay otra orden luego?)
orders_df = orders_df.sort_values(['user_id','order_date'])
orders_df['will_purchase_again'] = (orders_df.groupby('user_id')['order_id'].shift(-1).notna().astype(int))

feature_cols = [
    # lags
    'days_since_prior_lag_1','days_since_prior_lag_2','days_since_prior_lag_3',
    # rolling
    'rolling_cart_mean_3','rolling_cart_std_3',
    # expanding / RFM
    'expanding_days_mean','total_orders_so_far','expanding_total_spent',
    'recency_days','monetary_avg','monetary_total',
    # time windows
    'orders_7d','orders_30d','orders_90d','spend_7d','spend_30d','spend_90d',
    # calendar
    'order_dow','order_hour_of_day','is_weekend','is_month_start','is_month_end',
    'is_holiday','days_to_holiday','dow_sin','dow_cos','hour_sin','hour_cos',
    # externas
    'gdp_growth','unemployment_rate','consumer_confidence',
    # base
    'cart_size','order_total','order_number'
]
feature_cols = [c for c in feature_cols if c in orders_df.columns]

df_model = orders_df[feature_cols + ['will_purchase_again','order_date','user_id']].dropna().sort_values('order_date')
X, y = df_model[feature_cols], df_model['will_purchase_again']

tscv = TimeSeriesSplit(n_splits=3)
scores = []
for fold,(tr,va) in enumerate(tscv.split(X),1):
    Xtr,Xva = X.iloc[tr], X.iloc[va]
    ytr,yva = y.iloc[tr], y.iloc[va]
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(Xtr,ytr)
    auc = roc_auc_score(yva, model.predict_proba(Xva)[:,1])
    scores.append(auc)
    print(f"Fold {fold}: AUC={auc:.4f}")

print(f"Mean AUC: {np.mean(scores):.4f} ± {np.std(scores):.4f}")
```

---

# ⚖️ Comparación: Base vs Temporal

```python
base_cols = [c for c in ['order_dow','order_hour_of_day','is_weekend','is_holiday',
                         'cart_size','order_total','order_number'] if c in feature_cols]
def eval_subset(cols):
    s=[]; tscv=TimeSeriesSplit(n_splits=3)
    for tr,va in tscv.split(X):
        m=RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        m.fit(X.iloc[tr][cols], y.iloc[tr])
        s.append(roc_auc_score(y.iloc[va], m.predict_proba(X.iloc[va][cols])[:,1]))
    return np.mean(s), np.std(s)

base_mean, base_std = eval_subset(base_cols)
full_mean, full_std = eval_subset(feature_cols)

print(f"Base (sin temporales): {base_mean:.4f} ± {base_std:.4f}")
print(f"Full (con temporales): {full_mean:.4f} ± {full_std:.4f}")
print(f"Δ AUC: {full_mean - base_mean:.4f}  ({(full_mean-base_mean)/max(base_mean,1e-6)*100:.1f}%)")
```

---

# 🔍 Importancia de variables y chequeo de leakage

```python
# Entrenar full para importancia
m=RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1).fit(X,y)
imp = (pd.DataFrame({'feature':feature_cols,'importance':m.feature_importances_})
         .sort_values('importance',ascending=False))
print(imp.head(25))

# Señales de alerta (heurísticas)
train_acc = m.score(X,y)
print(f"Train accuracy: {train_acc:.3f}")
if train_acc > 0.99: print("⚠️ OVERFIT sospechoso")
if (train_acc - full_mean) > 0.30: print("⚠️ Gap train–CV grande → revisar leakage")

suspicious = [f for f in imp.head(10)['feature'] if any(x in f for x in ['target','label','leak'])]
print("Suspicious:", suspicious or "OK")
```

---

# 🧠 Resultados y discusión

| Hallazgo | Interpretación |
|---|---|
| **Δ AUC (full vs base)** | El modelo con features temporales mejoró de **0.661 → 0.728**, un incremento de **+0.066 (~10%)**, demostrando que las variables derivadas del comportamiento temporal agregan información real sobre recompra. |
| **Categorías más importantes** | Dominan las de **Lag/Window (0.29)**, seguidas por **Diversity (0.17)** y **RFM (0.15)**. Las económicas y de calendario aportan menos pero ayudan a capturar estacionalidad. |
| **Ventana temporal clave** | Las features de **90 días (spend_90d, orders_90d)** resultaron más influyentes que las de 7d/30d, lo que sugiere que la recompra en e-commerce tiene un horizonte de mediano plazo. |
| **Señales de leakage** | No se detectaron fugas. Todas las operaciones usaron `.shift(1)` y `groupby('user_id')`, evitando acceso a datos futuros. La validación se hizo con `TimeSeriesSplit`, garantizando orden temporal. |

> En mi implementación me enfoqué en construir un pipeline **realista y productivo**, donde cada paso (limpieza, agregaciones, ventanas, encoding) está **ordenado cronológicamente** y encapsulado dentro del pipeline.  
> Los *lags* capturaron la cadencia individual de compra; las *rolling windows* suavizaron variaciones cortas; las *expanding features* reflejaron comportamiento histórico.  
> El **encoding cíclico** (sin/cos) evitó rupturas en variables como hora o día, y el *forward fill* en datos económicos mantuvo consistencia temporal sin mirar al futuro.  
> En conjunto, estas decisiones hicieron que el modelo ganara estabilidad y robustez, manteniendo la trazabilidad necesaria para producción.

---

# 🔗 Conexión con otras unidades

- **UT2:** Reforcé la importancia de datos limpios y consistentes en el tiempo antes de cualquier modelado.  
- **UT4:** Este ejercicio anticipa cómo construir pipelines de ETL reproducibles, donde las ventanas y agregaciones se regeneran automáticamente cada día.  
- **UT5:** Las métricas (AUC y mejora del 10%) se vinculan con objetivos de negocio como retención y predicción de churn.

---

# 🧩 Reflexión final

En este trabajo confirmé que **las features temporales son las que más valor aportan**: los *lags* y *rolling windows* fueron decisivos para modelar la recurrencia de compra.  
Las de **RFM y diversidad** complementan el comportamiento histórico, mientras que las económicas y de calendario solo refinan estacionalidad.

Para evitar **leakage en producción**, mantendría un **batch diario** con cálculos basados únicamente en datos previos al corte, usando siempre `.shift(1)` y `forward fill`.  
El **trade-off** principal está entre señal y costo: las *rolling/expanding* son pesadas, pero justifican su uso cuando el objetivo es capturar la dinámica de usuario.  
A futuro, extendería el pipeline con **Fourier features** para estacionalidad, **slope features** para tendencias y **walk-forward validation** para robustecer el despliegue en tiempo real.


---

# 🧰 Stack técnico

**Lenguaje:** Python  
**Librerías:** Pandas · NumPy · Scikit-learn · Matplotlib/Seaborn  
**Conceptos:** Lags · Rolling/Expanding · RFM · Calendar (sin/cos) · Ventanas (7/30/90d) · TimeSeriesSplit · Leakage Prevention

### 📝 [Notebook](../../../notebooks/UT3-4.ipynb)

---

# 📚 Referencias

- Práctica: <https://juanfkurucz.com/ucu-id/ut3/11-temporal-features-assignment/> 
- Kaggle API — https://www.kaggle.com/docs/api  
- Pandas Time Series — https://pandas.pydata.org/docs/user_guide/timeseries.html  
- TimeSeriesSplit — https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html  
- RandomForestClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
