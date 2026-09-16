"""
Este se encarga de crear un Pipeline y el hypothesis testing
"""

#### Importing modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import os, joblib


#### Paths
data_path = os.path.join(
    os.getcwd(),
    'Datos',
    'FeatEng'
)

pickle_path = os.path.join(
    os.getcwd(),
    'App'
)

#### Reading data
df_2_original = pd.read_csv(f'{data_path}/visitantes_sitios_turisticos_original.csv')
df_2_encoded = pd.read_csv(f'{data_path}/visitantes_sitios_turisticos_encoded.csv')
model = joblib.load(f'{pickle_path}/model.pkl')
scaler = joblib.load(f'{pickle_path}/scaler.pkl')


###################################################
    # Creating Pipeline #
#### Separating data
X = df_2_original[['ID_MES', 'DEPARTAMENTO', 'SITIO_TURISTICO']]
y = df_2_original['NUMERO_VISITANTES']

#### Creating OneHotEncoder
### Initialize
OHE = OneHotEncoder(
    handle_unknown='ignore',
    sparse_output=False
)
### Fitting
encoder = OHE.fit(X)

#### Creating Pipeline
pipeline = Pipeline([
    ('encoder', encoder),
    ('model', model)
])

#### Saving pipeline
joblib.dump(pipeline, f'{pickle_path}/pipeline.pkl')

#######################################
    # Hypothesis testing #
#### Selecting the top 5 tourist sites
top_X = 5
top_X_sitios = df_2_original.groupby(by='SITIO_TURISTICO', as_index=False)\
    ['NUMERO_VISITANTES'].agg('mean')\
    .sort_values(by='NUMERO_VISITANTES', ascending=False)\
    ['SITIO_TURISTICO'][:top_X].values.tolist()

#### Selecting the indices of the top 5 sites
idxs = df_2_original[df_2_original['SITIO_TURISTICO'].isin(top_X_sitios)].index
df_org_topX = df_2_original.iloc[idxs]
X_top5 = df_org_topX.drop(columns = 'NUMERO_VISITANTES')
y_top5 = df_org_topX['NUMERO_VISITANTES']

#### Running pipeline
y_pred_top5 = 




