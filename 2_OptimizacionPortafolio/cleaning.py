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
    f'{data_path}/raw_top40.csv',
    parse_dates=['Date'],
    index_col='Date'
)


#######################################
    # Nulls #
#### Forward fill (for weekends) before full null-analysis
df = df.ffill()

#### Capturing 2008 crisis and build up
    # Erasing all companies with NaN after 2006-3-31
df_erase = df[df.index > "2006-3-31"].isna().sum()
df = df.drop(columns=df_erase[df_erase > 0].index.to_list())

#### Creating dataframe where ALL rows have some value
df = df[df.notna().all(axis=1)]

##########################################
    # Duplicates #
#### Counting number of duplicates
df[df.duplicated()].shape
    # There are 47 repeated rows

#### Delete duplicates 
df = df.drop_duplicates()


##########################################
    # Saving #
df.to_csv(
    f'{data_path}/clean_top40.csv',
    index=True,
    encoding='utf-8')









