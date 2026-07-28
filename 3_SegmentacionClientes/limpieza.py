"""
Limpieza de Datos

Este archivo se va a encarga de limpiar y concatenar datos.

Existen los siguientes directorios y datos:
1. Visitantes Internacionales
    * A: Excursionistas
    * B: Turistas
    * C: Visitantes
2. Visitantes en sitios Turisticos
    * A: Visitantes en sitios
3. Listo de Recursos Turisticos
    * A: Lista
"""

##### Importacion de Datos
import os
import pandas as pd
import numpy as np



##### Leyendo datos
#### Nombre de archivos
nom_1A = 'Llegada_excursionistas_internacionales.csv'
nom_1B = 'Llegada_turistas_internacionales.csv'
nom_1C = 'Llegada_visitantes_internacionales.csv'
nom_2A = 'Visitantes_sitios_turisticos_2019_2025.csv'
nom_3A = 'Inventario_recursos_turisticos.csv'

#### Paths
path_1A = os.path.join('Datos','VisitantesInternacionales', nom_1A)
path_1B = os.path.join('Datos','VisitantesInternacionales', nom_1B)
path_1C = os.path.join('Datos','VisitantesInternacionales', nom_1C)
path_2A = os.path.join('Datos','VisitantesSitios', nom_2A)
path_3A = os.path.join('Datos','InventorioRecursosTuristicos', nom_3A)

#### Cargando datos
os.chdir('3_SegmentacionClientes')
df = pd.read_csv(path_1A, sep=';', encoding='latin-1', header=0)
df.info()

#### Investigando los datos
### Ordenar por ANIO
df = df.sort_values(by='ANIO')
df[['ANIO','MES']].iloc[[0,-1]]

### Investigando si 1C es la suma de 1A y 1B
df[(df['ANIO']==2023) & (df['MES']=='AGOSTO')]


# df['MES'].value_counts().count()
# df['BLOQUE'].isnull().sum()