"""
Creacion de datos para el modelo

# Etapas:
        # 1. Ver correlacion 
        # 2. Escojer columnas
        # 3. Condensar datos en columnas que no importan
        # 4. Verificar correlacion final
        # 5. Hacer one hot encoding (y normalizacion)
        # 6. Guardar
"""


##### Importacion de Datos
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.preprocessing import LabelEncoder

############################################################

##### Leyendo datos
#### Rutas de archivos
fpath_1 = 'Datos/Limpios/visitantes_internacionales.csv'
fpath_2 = 'Datos/Limpios/visitantes_sitios_turisticos.csv'
fpath_3 = 'Datos/Limpios/inventario_recursos_turisticos.csv'

#### Cambiando directorio (si es necesario)
os.chdir('3_SegmentacionClientes')

#### Cargando datos
df_1 = pd.read_csv(fpath_1)
df_2 = pd.read_csv(fpath_2)
df_3 = pd.read_csv(fpath_3)

### Borrando columnas no necesarias
## Datos 1
df_1 = df_1.drop(columns=['FECHA_CORTE', 'MES', 'TIPO_VISITANTE'])
## Eliminando columnas no necesarias
df_2 = df_2.drop(columns=['ï»¿FECHA_CORTE','MES'])
## Filtracion de filas
df_2 = df_2[df_2['TIPO_VISITANTE'] == 'EXTRANJERO']
## Borrando columna no necesaria
df_2 = df_2.drop(columns=['TIPO_VISITANTE'])
## DAtos 3
df_3 = df_3.drop(columns=[
    'URL', 'FECHA_DE_CORTE', 'TIPO', 'OBSERVACION'
])



############################################################
##### Datos 1
    # Cols: ANIO, ID_MES, ID_PAIS, PAIS, ID_CONTINENTE,
            # CONTINENTE, ID_OCM, OCM, DEPARTAMENTO_OCM,
            # NUMERO_VISITANTES
    # Estos datos se van a utilizar para hacer k-means en paises
        # Datos necesarios:
            # ID_MES, PAIS, CONTINENTE, OCM, NUMERO_VISITANTES
            # Entonces se tendra que codensar todas otras col

#### Etapa 1: Correlacion
df_1[['ANIO', 'ID_MES', 'ID_PAIS', 'ID_CONTINENTE', 'ID_OCM', 'NUMERO_VISITANTES']].corr().round(4)
    # Ninguno de los |valores| >0.18 => no hay correlacion

#### Etapa 2: Escojer columnas
    # 'ID_MES', 'ID_PAIS', 'ID_CONTINENTE', 'ID_OCM', 'NUMERO_VISITANTES'

#### Etapa 3: Condensar datos
df_1_mod = df_1[['ANIO', 'ID_MES', 'ID_PAIS', 'ID_CONTINENTE', 'ID_OCM', 'NUMERO_VISITANTES']]\
    .groupby(by=['ID_MES', 'ID_PAIS', 'ID_CONTINENTE', 'ID_OCM'], as_index=False)\
    ['NUMERO_VISITANTES'].sum()

#### Etapa 4: Verificar correlacion final
df_1_mod.corr().round(4)
    # Ninguno de los |valores| >0.18 => no hay correlacion

#### Etapa 5: Hacer OHE (y normalizacion)
### OHE
df_1_encoded = pd.get_dummies(df_1_mod, columns=['ID_MES', 'ID_PAIS', 'ID_CONTINENTE', 'ID_OCM'], drop_first=False)
### Normalizacion
df_1_encoded['NUMERO_VISITANTES'] =(
    (
        df_1_encoded['NUMERO_VISITANTES'] -\
        df_1_encoded['NUMERO_VISITANTES'].mean()
    ) / df_1_encoded['NUMERO_VISITANTES'].std()
)


#### Etapa 6: Guardar ambos datasets
df_1_mod.to_csv('Datos/FeatEng/visitantes_internacionales_mod.csv', index=False)
df_1_encoded.to_csv('Datos/FeatEng/visitantes_internacionales_encoded.csv', index=False)


############################################################
##### Datos 2
    # Cols: ANIO, ID_MES, DEPARTAMENTO,
            # SITIO_TURISTICO, NUMERO_VISITANTES
    # Esto se puede utilizar para hacer un regression
            # en los numero de visitantes por sitio
            # dado el mes

#### 1. Ver correlacion 
### Hacer label encoder
df_le = df_2.copy()
vars_categoricales = ['DEPARTAMENTO', 'SITIO_TURISTICO']
for col in vars_categoricales:
    le = LabelEncoder()
    df_le[col] = le.fit_transform(df_le[col])
### Correlacion
df_le.corr().round(4)
    # Ninguno de los |valores| > 0.177 => no correlacion

#### 2. Escojer columnas
    # Voy utilizar ['ID_MES', 'DEPARTAMENTO', 'SITIO_TURISTICO', 'NUMERO_VISITANTES']

#### 3. Condensar datos en columnas que no importan
df_2_mod = df_le.groupby(by=[
        'ID_MES', 
        'DEPARTAMENTO', 
        'SITIO_TURISTICO'
    ], as_index=False)\
    ['NUMERO_VISITANTES'].sum()

#### 4. Verificar correlacion final
df_2_mod.corr().round(4)
    # Ninguno de los |valores| > 0.2129 => no correlacion


#### 5. Hacer one hot encoding
### OHE
df_2_encoded = pd.get_dummies(df_2_mod, columns=['ID_MES', 'DEPARTAMENTO', 'SITIO_TURISTICO'], drop_first=False)
### Normalizacion
df_2_encoded['NUMERO_VISITANTES'] =(
    (
        df_2_encoded['NUMERO_VISITANTES'] -\
        df_2_encoded['NUMERO_VISITANTES'].mean()
    ) / df_2_encoded['NUMERO_VISITANTES'].std()
)

#### 6. Guardar
df_2_mod.to_csv('Datos/FeatEng/visitantes_sitios_turisticos_mod.csv',index=False)
df_2_encoded.to_csv('Datos/FeatEng/visitantes_sitios_turisticos_encoded.csv',index=False)


############################################################
##### Datos 3
    # Cols: DEPARTAMENTO, PROVINCIA, DISTRITO, CODIGO DEL RECURSO,
            # NOMBRE DEL RECURSO, CATEGORIA, TIPO_CATEGORIA, 
            # SUBTIPO_CATEGORIA, LATITUS, LONGITUS, INGRESO
    # No se van a usar, considerando que 'INGRESO' es algo 
            # fijo y establecido por gobierno, no es algo
            # que depende en las otras columnas

