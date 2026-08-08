"""
Este archivo sera la creacion de los modelos:
* K-Mean: Para hacer cluster de los turistas
* Regression: para predecir num_visitantes dado el sitio, dept, y mes
"""

##### Importaciones
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import os
import matplotlib.pyplot as plt
#### KMeans
from sklearn.cluster import KMeans, MiniBatchKMeans, BisectingKMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
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
df_1_original = pd.read_csv('Datos/FeatEng/visitantes_internacionales_original.csv')
df_1_encoded = pd.read_csv('Datos/FeatEng/visitantes_internacionales_encoded.csv')
#### Eliminando columnas no necesarias
# df_1_encoded = df_1_encoded.drop(columns=['NUMERO_VISITANTES'])
df_1_encoded = df_1_encoded.drop(columns=['CONTINENTE'])

#### Renombrando Aeropuerto
#### Cambiando AIJC abbreviacion
tmp = df_1_original[df_1_original['OCM']=='AEROPUERTO INTERNACIONAL JORGE CHÁVEZ'].index
df_1_original.loc[tmp, 'OCM'] = 'AIJCH'
del tmp

##### Buscando optimo numero de clusters
    # Elbow metodo
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
num_clus = 6


##### Haciendo los 3 diferentes KMeans
#### KMeans <-> 'CLUSTER_1'
m1 = KMeans(n_clusters=num_clus, random_state=42)
m1.fit(df_1_encoded)
df_1_original['CLUSTERS_KMEANS'] = m1.labels_

#### MiniBatchKMeans <-> 'CLUSER_2'
m2 = MiniBatchKMeans(n_clusters= num_clus, random_state=42)
m2.fit(df_1_encoded)
df_1_original['CLUSTERS_MINIBATCH'] = m2.labels_

#### BisectingKMeans <-> 'CLUSTER_3'
m3 = BisectingKMeans(n_clusters=num_clus, random_state=42)
m3.fit(df_1_encoded)
df_1_original['CLUSTERS_BISECTING'] = m3.labels_ 


##### Evaluacion de los 3 clustering algs
#### Correlacion
cluster_corr = df_1_original[['CLUSTERS_KMEANS','CLUSTERS_MINIBATCH','CLUSTERS_BISECTING']].corr()
    # Resultados: Ningun |valor| > 0.121
    # Ende: No hay correlacion entre los diferentes clusteres
#### Silhouette scores, mayor es mejor
m1_ss = silhouette_score(df_1_encoded, m1.labels_)
m2_ss = silhouette_score(df_1_encoded, m2.labels_)
m3_ss = silhouette_score(df_1_encoded, m3.labels_)
#### Davie-Bouldin, menor es mejor
m1_db = davies_bouldin_score(df_1_encoded, m1.labels_)
m2_db = davies_bouldin_score(df_1_encoded, m2.labels_)
m3_db = davies_bouldin_score(df_1_encoded, m3.labels_)
#### Creando DF de resultados
resultados={
    'corr_c1':cluster_corr['CLUSTERS_KMEANS'].values.tolist(),
    'corr_c2':cluster_corr['CLUSTERS_MINIBATCH'].values.tolist(),
    'corr_c3':cluster_corr['CLUSTERS_BISECTING'].values.tolist(),
    'silhouette': [m1_ss, m2_ss, m3_ss],
    'davies': [m1_db, m2_db, m3_db]
}
df_resultados = pd.DataFrame(resultados, index=['clusters_kmeans', 'clusters_minibatch', 'clusters_bisecting'])
df_resultados
    # 'Kmeans' tuvo los mejores resultados

df_1_original = df_1_original.drop(columns=['CLUSTERS_MINIBATCH','CLUSTERS_BISECTING'])

##### Examinando los clusteres establecidos
df_1_original['CLUSTERS_KMEANS'].value_counts()
    # Existen 6 clusters: 0 - 5
clus_eda={}

for clus in range(df_1_original['CLUSTERS_KMEANS'].value_counts().shape[0]):
    df_clus = df_1_original[df_1_original['CLUSTERS_KMEANS']==clus].drop(columns='CLUSTERS_KMEANS')
    tmp = []
    for col in df_clus.columns:
        tmp_ds = df_clus[col]
        if is_numeric_dtype(tmp_ds):
            tmp.append(tmp_ds.mean())
        else:
            tmp.append(tmp_ds.value_counts().shape[0])
    clus_eda.update({f'cluster_{clus}': tmp})

tmp = []
for col in df_1_original.drop(columns='CLUSTERS_KMEANS').columns:
    tmp_ds = df_1_original[col]
    if is_numeric_dtype(tmp_ds):
        tmp.append(tmp_ds.mean())
    else:
        tmp.append(tmp_ds.value_counts().shape[0])
clus_eda.update({f'valores_distintos': tmp})

df_clu_eda = pd.DataFrame(clus_eda, index=df_clus.columns).round(2)
df_clu_eda

##### Analisis de clusters
df_1_original[df_1_original['CLUSTERS_KMEANS']==5]['OCM'].value_counts()
'CHILE' in df_1_original[df_1_original['CLUSTERS_KMEANS']==5]['PAIS'].values.tolist()

###########################################
##### Insights de KMeans
"""
Parece que KMeans obtuvo los mejores resultados con 6 clusters.

Los 6 clusteres se dividen en la siguiente manera
Cluster 1
* OCM = Santa Rosa
* Todos los: Meses, Paises, Continentes
* I.e., el simple hecho de llegar al OCM Santa Rosa automaticamente crea un grupo
    - Esto tiene coherencia con EDA, considerando que 32.9% de los visitantes internacionales
            son chilenos y 80.3% de ellos entran por Santa Rosa
Cluster 2
* OCM = Cebaf - Tumbes, AIJC
* PAIS = Chile, EE.UU
* CONTINENTE = Sur america y Norte america
* Todos los Meses
* I.e., el simple hecho de ser Chileno o Estadounidense automaticamente los ponene en un grupo
    - Tiene coherencia con EDA, considerando que ambos paises son 48% de todos visitantes internacionales
Cluster 3
* OCM = AIJCH, Cebaf - Tumbes
* Todos los: Meses, Paises, Continentes
* I.e., el hecho de venir de los OCMs AIJCH y Cebaf-Tumbes es un grupo
Cluster 4
* OCM = Otros
* Todos los: Meses, Paises, Continentes
* I.e., el hecho de venir de los 'OTROS' OCMs es un grupo
Cluster 5
* OCM = Desaguadero
* Todos los: Meses, Paises, Continentes
* I.e., el hecho de venir de los 'DESAGUADERO' OCMs es un grupo
Cluster 6
* OCM = Kasani
* Todos los: Meses, Paises, Continentes
* I.e., el hecho de venir de los 'KASANI' OCMs es un grupo
"""