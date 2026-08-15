"""
Este documento sirvera como los insights pos-EDA de 'ventas_productos'

Tendencias generales del conjunto:
* Columnas:
    - id_venta: cada transaccion es un id diferente
    - cliente_id: cada cliente tiene un diferente is
    - cantidad: la cantidad de un producto (dentro una transaccion) 
            que se vendio
    - stock: cantidad de un producto almacenado
    - nombre: nombre de un producto
    - categoria: categoria de un producto
    - precio: precio de una unidad de un producto
    - fecha: la fecha de una transaccion

Metricas de este proyecto:
* Porcentaje de productos perdidos
    - ((stock - productos_sold)/stock) * 100
* Popularidad de producto X
    - prod_X_sold / total_prod_sold
* ARPU 
    - total revenue / num_customers
* Transacion value
    - total revenue / num_transactions

"""
##### Importacion de modulos
import pandas as pd
import os

##### Cambiando directorio
if os.getcwd().split('\\')[-1] != 'PostSQL':
    os.chdir('./4_DemandaForecasting/Datos/PostSQL')

##### Cargando datos
df = pd.read_csv('ventas_productos.csv')

###############################################
####### Arreglo de datos inciales

##### Columna: Fecha
#### Creando columnas: dia, mes
df['dia'] = df['fecha'].apply(lambda fila: int(fila.split('/')[0]))
df['mes'] = df['fecha'].apply(lambda fila: int(fila.split('/')[1]))
#### Ordenando datos por fecha
df = df.drop(columns='fecha')\
    .sort_values(by=['mes','dia'], ascending=[True, True])\
    .reset_index(drop=True)


df.groupby(by=['mes','nombre'], as_index=False)\
    [['cantidad','stock']].agg(['sum', 'mean'])













