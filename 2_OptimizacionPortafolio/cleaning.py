"""
This file will clean the raw data downloaded.
"""

##### Importing libraries
import pandas as pd
import os 

##### Data path
data_path = os.path.join(
    os.getcwd(),
    '2_OptimizacionPortafolio',
    'Data'
)

##### Reading data
df = pd.read_csv(
    f'{data_path}/raw_splac.csv',
    parse_dates=['Date'],
    index_col='Date',
)

df.index
##### 
df.info()
df.columns.nlevels
df.head()

df['Date'].dtype

#######################################
    # Nulls #











