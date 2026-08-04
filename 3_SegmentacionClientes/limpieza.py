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
import matplotlib.pyplot as plt

############################################################

##### Leyendo datos
#### Nombre de archivos
nom_1A = 'Llegada_excursionistas_internacionales.csv'
nom_1B = 'Llegada_turistas_internacionales.csv'
nom_1C = 'Llegada_visitantes_internacionales.csv'
nom_2A = 'Visitantes_sitios_turisticos_2019_2025.csv'
nom_3A = 'web_scrapped_inventario_recursos_turisticos.csv'

#### Paths
    # 1 = Ingresos internacionales
    # 2 = Ingresos a sitios turisticos
    # 3 = Lista de recursos de sitios turisticos
path_1A = os.path.join('Datos','VisitantesInternacionales', nom_1A)
path_1B = os.path.join('Datos','VisitantesInternacionales', nom_1B)
path_1C = os.path.join('Datos','VisitantesInternacionales', nom_1C)
path_2A = os.path.join('Datos','VisitantesSitios', nom_2A)
path_3A = os.path.join('Datos','WebScrapped', nom_3A)

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
###### Limapiando non-scrapped

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








############################################################
###### Limapiando scrapped

##### SEleccionando los datos 
    # Nos vamos a enfocar en 1C y 2A
#### Leyendo datos
df_3a = pd.read_csv(path_3A, sep=',', encoding='utf-8', header=0)

#### Resumen
df_3a.info()
df_3a.head()


############################################################

##### Revisando los mulos
#### Contando cantidad de veces aparecidos
df_3a.isnull().sum()

#### Investigando areas de nulos
### 'Latitud' y 'longitud'
    # Son variables continuos - no categorical
    # Detalla la latitud y longitud del sitio turistico
df_3a[['LATITUD', 'LONGITUD']].describe()
df_3a.boxplot(column='LATITUD');plt.show()
df_3a.boxplot(column='LONGITUD');plt.show()
    # CONLUSION: no se va a utilizar estos datos -> ignorar los nulos



### "tipo"
    # Es una variable categorical
    # Detalla como ingresar al sitio
df_3a['TIPO'].value_counts()
    # Las categorias de ingresos son pocos y estructuradas
len(df_3a['TIPO'].value_counts().to_list())
    # Hay muchos valores repetidos => solo hay 16 valores unicos
df_3a['TIPO'].isna()
    # Boolean de las filas que tienen "Nan" en la columna 'TIPO'
df_3a_tipo_nulos = df_3a[df_3a['TIPO'].isna()]
    # Enfocandose en datos solo donde 'TIPO' = 'NaN'
df_3a_tipo_nulos.info()
    # Verificacion de que todos 'tipo' son nulos
    # Existen 1531 sitios/registros
df_3a_tipo_nulos['NOMBRE DEL RECURSO'].value_counts()
    # Viendo cuales son los sitios que tienen 'tipo' nulo
    # Parece que la mayoria de recursos son eventos diferentes
len(df_3a_tipo_nulos['NOMBRE DEL RECURSO'].value_counts().to_list())
    # Existe 1524 valores unicos (recordar que son 1531 registros)
    # Parece que son diferentos eventos en diferentes lugares
    # Posiblemente ocurren una o dos veces al anio
df_3a_tipo_nulos['CATEGORÍA'].value_counts()
    # Son mayoramente 2 categorias: 'folclore' y 'acontecimientos programados'
        # Esto es mas evidencia de que son eventos
df_3a_tipo_nulos['NOMBRE DEL RECURSO'].str.contains(
    r'fiesta|festival|feria',
    case=False,
    na = False
).value_counts()
    # Viendo cuantos recursos tienen 'fiesta,festival,feria' en nombre
listas = []   # Creando dict para ver frecuencias de palabras
df_3a_tipo_nulos['NOMBRE DEL RECURSO'].apply(
    lambda fila: listas.extend(list(
        pd.Series(fila.lower().split())
        .value_counts(sort=True)
        .to_dict()
        .items()))
)   # Contando las palabras dentro cada fila
freq = {}    # Creando lista de frecuencias
for key,value in listas:    # Llenando dict de frecuencias
    freq[key] = freq.get(key,0) + value
pd.Series(freq)\
    .sort_values(axis=0, ascending=False)\
    .head(30)   # Creado DF de palabras mas comunes
    # Aparte de articulos ("de", "la", etc), las palabras comunes son:
        # danza, fiesta, festividad, patronal, festival, carnaval
    # CONCLUSION: los 'tipo' nulos son eventos publicos y no sitios 
        # Por eso no tienen un precio/detalla al poder ingresar
        # No se ingresa a un evento publico, solo se aparece uno



### 'observacion'
    # Es una variables categorical
    # Detalla explicaciones sobre como ingresar al sitio
    # Hipotesis: parece que esto solo se activa cuando 
len(df_3a['OBSERVACION'].value_counts())
    # Existen 2007 valores unicos 
    # Recorda: Existen 2190 no-nulos observaciones
    # Por ende, las observaciones son generalmente unicas
df_3a_obser_nulos =  df_3a[df_3a['OBSERVACION'].isna()]
    # Creando df de solo 'observacion' nulos
df_3a_obser_nulos.info()
    # Viendo info de neuvo DF
    # Recordar que existe relacion entre 'tipo' y 'observacion'
df_3a_obser_nulos['TIPO'].value_counts()
    # Se investiga que las observaciones nulas son generalmente cuando 'tipo' = 'libre'
    # CONCLUSION: las 'obseracion' nulas son cuando el ingreso al sitio es libre
        # En otras palabras, cuando el sitio es libre no es necesario dar mas explicaciones



#### Arreglando nulos
### Longitud y Latitud
    # Ignorar, no se utilizan en el enfoque de este proyecto
### 'TIPO'
    # La mayoria de 'tipo' nulos son eventos
        # danza, fiesta, festividad, patronal, festival, carnaval
    # Enfoques de proyecto:
        # Segmentos K: touristas internacionales
        # Probabilidad p_k: marketing probabilidad
        # Ingreso r_k: ingreso promedio por turista
        # Costo c_k: costo promeio por turista
    # Entonces: solo enfocarnos en sitios con ingresos
        # Se va a utilizar para prediccir r_k
        # Eliminar nulos
df_3a = df_3a.dropna(subset=['TIPO'])
df_3a.info()

### 'OBSERVACION'
    # Similar a 'TIPO'
    # Se va a utilizar para ver el ingreso para touristas internacionales
    # Generalmente, as observaciones nulos son de 'tipo' = 'libre'
    # Ende: sustituir nulos por 'libre'
df_3a['OBSERVACION'] = df_3a['OBSERVACION'].fillna('Libre')
df_3a.info()



############################################################

##### Revisando duplicaciones
#### Contando numero de duplicados
df_3a.duplicated().sum()

############################################################

##### Guardando datos limpios
path_save_3a = os.path.join('Datos','Limpios', 'inventario_recursos_turisticos.csv')

if not os.path.exists(path_save_3a):
    df_3a.to_csv(path_save_3a, index=False)
