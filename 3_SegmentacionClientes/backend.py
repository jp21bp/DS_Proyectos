"""
Este archivo es el backend
Servira las predicciones del modelo
"""

#### Import libraries
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib, os, uvicorn

#### tmp
import pandas as pd
data_path = os.path.join(
    os.getcwd(),
    'Datos', 
    'FeatEng'
)

df_2_original = pd.read_csv(f'{data_path}/visitantes_sitios_turisticos_original.csv')
df_2_encoded = pd.read_csv(f'{data_path}/visitantes_sitios_turisticos_encoded.csv')




#### Path
deploy_path = os.path.join(
    os.getcwd(),
    'App'
)

#### Read model and scaler
try:
    pipeline = joblib.load(f'{deploy_path}/pipeline.pkl')
    scaler = joblib.load(f'{deploy_path}/scaler.pkl')
except Exception as e:
    raise RuntimeError(f'Loading error: {e}')

#### Initialize API
app = FastAPI(title='Model API')

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#### Setup data entry validation
class DataInput(BaseModel):
    feat1: int
    feat2: str
    feat3: str

@app.get('/')
def homepage():
    print('GET ROOT')
    return {'home': 'page'}

@app.post('/predict')
def predict(data: DataInput):
    try:
        input = [[data.feat1, data.feat2, data.feat3]]
        prediction_norm = pipeline.predict(input)
        prediction = scaler.inverse_transform(
            prediction_norm.reshape(1,-1)
        )
        print(prediction[0][0])
        return {'page': int(prediction[0][0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)







