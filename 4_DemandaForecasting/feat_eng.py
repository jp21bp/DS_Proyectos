"""
Este archivo va a crear los datos necesarios para hacer modelos.

Se nota que todas las metricas utilizadas dependen en la variable "cantidad".
Esta variable es la cantidad de un producto vendido en una transaccion.
Por ende, esta columna va a ser la variable dependiente de este modelo.
Input: variables de registros de cada transaccion/venta

"""

##### Importacion de Datos
import os
import pandas as pd
import numpy as np

if os.getcwd().split('\\')[-1] != 'PostSQL':
    os.chdir('./4_DemandaForecasting/Datos/PostSQL')


############################################################

#### Leyendo datos
df = pd.read_csv('ventas_productos.csv')

##### Fechas y Datetime
#### Transformanco fechas a DateTime
df['fecha'] = pd.to_datetime(
    df['fecha'],
    format='%d/%m/%Y',
    dayfirst=True,
    errors='coerce'
)
#### Verificando que todos los datos son del anio 2024
print(df['fecha'].dt.year.unique().tolist())
#### Creando columnas: dia, semana, mes
df['dia'] = df['fecha'].dt.day
df['dia_semana'] = df['fecha'].dt.weekday + 1
df['semana'] = df['fecha'].dt.isocalendar().week
df['mes'] = df['fecha'].dt.month
#### Ordenando datos por fecha
df = df.drop(columns='fecha')\
    .sort_values(by=['mes','dia'], ascending=[True, True])\
    .reset_index(drop=True)


##### Borrando variables no necesarias
df = df.drop(columns=['id_venta', 'cliente_id', 'stock'])
#### Razones por drops:
    # id_venta: cada registro es una venta
    # cliente_id: no importa la persona quien hizo la venta
    # stock: el stock no se saben al hacer una compra

    
##### Funcion para verificar Correlacion de OHE DF
def ohe_corr(df_enc):
    df_1_enc_corr= df_enc.corr().round(2)
    coords = list(zip(*np.where(
        (df_1_enc_corr > 0.8) &\
        (df_1_enc_corr < 1.0)
    )))
    cells_info = [
        (
            df_1_enc_corr.index[row], 
            df_1_enc_corr.columns[col], 
            df_1_enc_corr.iat[row, col]
        ) for row, col in coords
    ]
    for i, (col1, col2, num) in enumerate(cells_info):
        if col1 != col2: 
            print(cells_info[i])
    return cells_info

############################################################

df.info()
##### Hacer OHE
df_enc = pd.get_dummies(
    df, 
    columns=['nombre', 'categoria'],
    drop_first=False
)

##### VErificando correlaciones 
ohe_corr(df_enc)
    # Semana y Mes

##### Eliminando columnas con alta correlacion
df_enc = df_enc.drop(columns='semana')
df = df.drop(columns='semana')

##### Arreglando 'mes' columna
    # Como el primer 'mes' = 1 esta incompleto, se borra
df_enc = df_enc[df_enc['mes']!=1]
df = df[df['mes']!=1]

##### Verificacion
ohe_corr(df_enc)


##### normalizacion de non-OHE cols
norm_cols = ['precio', 'dia', 'dia_semana', 'mes']
for col in norm_cols:
    df_enc[col] = (df_enc[col] - df_enc[col].mean())/df_enc[col].std()

##### Guardando datasets
df.to_csv('../FeatEng/ventas_productos_org.csv')
df_enc.to_csv('../FeatEng/ventas_productos_enc.csv')






