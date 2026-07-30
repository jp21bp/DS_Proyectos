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

############################################################

##### Leyendo datos
#### Nombre de archivos
nom_1A = 'Llegada_excursionistas_internacionales.csv'
nom_1B = 'Llegada_turistas_internacionales.csv'
nom_1C = 'Llegada_visitantes_internacionales.csv'
nom_2A = 'Visitantes_sitios_turisticos_2019_2025.csv'
nom_3A = 'Inventario_recursos_turisticos.csv'

#### Paths
    # 1 = Ingresos internacionales
    # 2 = Ingresos a sitios turisticos
    # 3 = Lista de recursos de sitios turisticos
path_1A = os.path.join('Datos','VisitantesInternacionales', nom_1A)
path_1B = os.path.join('Datos','VisitantesInternacionales', nom_1B)
path_1C = os.path.join('Datos','VisitantesInternacionales', nom_1C)
path_2A = os.path.join('Datos','VisitantesSitios', nom_2A)
path_3A = os.path.join('Datos','InventorioRecursosTuristicos', nom_3A)

#### Cambiando directorio (si es necesario)
os.chdir('3_SegmentacionClientes')

############################################################

# ##### Investigando Relacion entre 1A, 1B, y 1C
# #### Cargando datos
# df1 = pd.read_csv(path_1A, sep=';', encoding='latin-1', header=0)
# df2 = pd.read_csv(path_1B, sep=';', encoding='latin-1', header=0)
# df3 = pd.read_csv(path_1C, sep=';', encoding='latin-1', header=0)

# #### Viendo value counts de tipo de visitantes
#     # RAzon por esta columna: la diferencia en los nombre de los
#             # datos son entre "excursionista", "turista", y "visitante"
# df1['TIPO_VISITANTE'].value_counts()
# df2['TIPO_VISITANTE'].value_counts()
# df3['TIPO_VISITANTE'].value_counts()

# #### Resultados: 1C es la suma de 1A y 1B
#     # Entonces podemos enfocarnos en 1C dentro "Visitantes internacionles"
# del df1
# del df2
# del df3

############################################################

##### SEleccionando los datos 
    # Nos vamos a enfocar en 1C y 2A
#### Leyendo datos
df_1c = pd.read_csv(path_1C, sep=';', encoding='latin-1', header=0)
df_2a = pd.read_csv(path_2A, sep=';', encoding='latin-1', header=0)

#### Resumen
df_1c.info()
df_2a.info()

#### Ordenando por anio y mes
df_1c = df_1c.sort_values(by=['ANIO', 'ID_MES'], ascending=[True, True])
df_2a = df_2a.sort_values(by=['ANIO', 'ID_MES'], ascending=[True, True])

############################################################

##### Revisando los mulos
#### Contando cantidad de veces aparecidos
df_1c.isnull().sum()
    # Tiene nulos en 'BLOQUE', la cual no es necesario
df_2a.isnull().sum()
    # No tiene ningun nulo

#### Arreglando nulos
df_1c = df_1c.dropna(axis=1, how='any')
df_1c.info()


############################################################

##### Revisando duplicaciones
#### Contando numero de duplicados
df_1c.duplicated().sum()
    # 0 => nungun duplicado de filas completas
        # PERO si hay duplicados dentro columnas mismas
df_2a.duplicated().sum()
    # 0 => nungun duplicado de filas completas
        # PERO si hay duplicados dentro columnas mismas

############################################################

##### Guardando datos limpios
path_save_1c = os.path.join('Datos','Limpios', 'visitantes_internacionales.csv')
path_save_2a = os.path.join('Datos','Limpios', 'visitantes_sitios_turisticos.csv')

if not os.path.exists(path_save_1c): 
    df_1c.to_csv(path_save_1c, index=False)

if not os.path.exists(path_save_2a):
    df_2a.to_csv(path_save_2a, index=False)

