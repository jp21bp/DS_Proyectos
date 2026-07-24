###### Creando modelos
    # Este archivo se enfocara en la creacion de los modelos

#### Importaciones de modulos
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


#### Leyendo los datos
print(os.chdir('1_DSTrabajos'))
df = pd.read_csv('datos_limpios.csv')


#### Ingineria de Variables
df.columns
df_variables = df[['titulo', 'len_desc', 'estado', 'ano', 'org', 'sueldo_promedio']]

#### Creando dummy datos
df_dum = pd.get_dummies(df_variables)
print(df_dum.columns)


#### Train test split
from sklearn.model_selection import train_test_split

X = df_dum.drop('sueldo_promedio', axis=1)
y = df_dum['sueldo_promedio'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#### OLS modelos
import statsmodels.api as sm

X_sm = sm.add_constant(X)
X_sm = X_sm.astype(float)
    # NEcesario convertir en float
model_ols = sm.OLS(y, X_sm)
summary = model_ols.fit().summary()
print(summary)
    # Escojer P valores < 0.05
        # PAra buscar cuales son significantes

#### Conviertiendo OLS summary en DataFrame
tabla_arr = summary.tables[1]
print(tabla_arr)
df_ols = pd.DataFrame(tabla_arr.data[1:], columns=tabla_arr.data[0])
df_ols = df_ols.rename(columns={'':'Variable'})
    # Primera columna es un vacio
df_ols.info()
for col in df_ols.columns.to_list()[1:]:
    df_ols[col] = df_ols[col].astype(float)
df_ols.info()
varaibles_sign = df_ols[df_ols['P>|t|'] < 0.05]['Variable']
varaibles_sign





