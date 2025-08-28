---
title: EDA Titanic con pandas
date: 2025-01-01
---

# EDA Titanic

## Cómo cargué los datos
- Origen: dataset de Kaggle (`train.csv`).
- Librerías: `pandas`, `matplotlib`, `seaborn`.

## Visualizaciones destacadas

### 1) Supervivencia por sexo y clase
![Survival por clase y sexo](assets/img/titanic_survival.png)

**Observaciones:**
- Mayor supervivencia en mujeres.
- Primera clase con mejores chances de sobrevivir.

### 2) Distribución de tarifas (Fare) por clase
![Boxplot Fare](assets/img/titanic_fare.png)

**Observaciones:**
- Pasajeros de primera clase pagaron más y tenían más chances de sobrevivir.
- Outliers claros en tarifas muy altas.

## Hallazgos iniciales
- Sexo y clase social son factores clave en la supervivencia.
- `Age` tiene muchos valores faltantes → requiere imputación.
- Variables socioeconómicas influyen en el desenlace.

## Próximos pasos
- Feature engineering: `FamilySize`, `Title`, `IsAlone`.
- Imputar `Age` usando mediana por grupo.
- Probar un modelo baseline de clasificación.
