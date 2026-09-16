"""
Este archivo es el backend
Servira las predicciones del modelo
"""

#### Import libraries
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib, os

#### tmp
import pandas as pd
data_path = os.path.join(
    os.getcwd(),
    '3_SegmentacionClientes',
    'Datos', 
    'FeatEng'
)

df_2_original = pd.read_csv(f'{data_path}/visitantes_sitios_turisticos_original.csv')
df_2_encoded = pd.read_csv(f'{data_path}/visitantes_sitios_turisticos_encoded.csv')




#### Path
deploy_path = os.path.join(
    os.getcwd(),
    '3_SegmentacionClientes',
    'App'
)

#### Read model and scaler
modelo = joblib.load(f'{deploy_path}/model.pkl')
scaler = joblib.load(f'{deploy_path}/scaler.pkl')

#### Initialize API
app = FastAPI(title='Model API')

#### Setup data entry validation
# class 













