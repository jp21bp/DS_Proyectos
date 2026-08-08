"""
Este archivo sera la creacion de los modelos:
* K-Mean: Para hacer cluster de los turistas
* Regression: para predecir num_visitantes dado el sitio, dept, y mes
"""

##### Importaciones
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
#### KMeans
from sklearn.cluster import KMeans, MiniBatchKMeans, BisectingKMeans
#### Regresion
from sklearn.model_selection import train_test_split
import statsmodels.api as sm # OLS
from sklearn.linear_model import LinearRegression # Lin Regression
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Lasso #Lasso regresion
from sklearn.ensemble import RandomForestRegressor # RF
from sklearn.model_selection import GridSearchCV

# import tensorflow as tf

#### Cambiando directorio (si es necesario)
if os.getcwd().split('\\')[-1] != '3_SegmentacionClientes': 
    os.chdir('3_SegmentacionClientes')


###################################################
###### K Means

##### Importando datos
#### Cargando
df_1_mod = pd.read_csv('Datos/FeatEng/visitantes_internacionales_mod.csv')
df_1_encoded = pd.read_csv('Datos/FeatEng/visitantes_internacionales_encoded.csv')

df_1_mod
df_1_encoded

##### Buscando optimo numero de clusters
#### Buscando inercias
inercias = []
for k in range(1,15):
    kmeans=KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_1_encoded)
    inercias.append(kmeans.inertia_)

#### Graficando inercias
fig = plt.figure(figsize=(8,5))
plt.plot(
    range(1,15),
    inercias,
    marker='o'
)
plt.show()

#### Eligiendo optimo numero de clusters
num_clus = 7


##### Haciendo los 3 diferentes KMeans
#### KMeans
m1 = KMeans(n_clusters=num_clus, random_state=42)
m1.fit(df_1_encoded.drop(columns='NUMERO_VISITANTES'))










