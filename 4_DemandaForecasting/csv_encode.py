'''
Este archivo va a guardar los datos en UTF-8, sin acentos

Para que pueden ser leidas por PSQL
'''

##### Importando modulos
import pandas as pd
from pandas.api.types import is_numeric_dtype
import os
import unicodedata

##### Cambiando directorio
if os.getcwd().split('\\')[-1] != 'Originales':
    os.chdir('4_DemandaForecasting/Datos/Originales')
    
##### Traversando todos los archivos
for file in os.listdir(os.getcwd()):
    if not file.endswith('.csv'): continue
    df = pd.read_csv(file)
    for col in df.columns:
        if is_numeric_dtype(df[col]): continue
        df[col] = df[col].apply(
            lambda fila: \
            ''.join(
                c for c in unicodedata.normalize('NFD',fila)\
                if unicodedata.category(c) != 'Mn'
            )
        )
    df.to_csv(f'../OriginalesEncodedUTF8/{file}')
