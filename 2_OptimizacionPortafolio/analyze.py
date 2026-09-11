import os
import pandas as pd
import numpy as np


path = os.path.join(
    os.getcwd(),
    '2_OptimizacionPortafolio',
    'DevelopedModels',
    'to_analyze'
)

os.chdir(path)

archivos = os.listdir(path)
resultados = None
first_flag = True
cols_nom_planilla = ['avg_val', 'avg_train', 'avg_val_change', 'avg_train_change']
for archivo in archivos: 
    if not archivo.endswith('.txt'): continue
    with open(archivo, 'r') as f:
        numero = archivo.split("_")[0]
        print('NUMERO', numero)
        cols_nom = [f'{numero}_{col}' for col in cols_nom_planilla]
        # print(cols_nom)
        f_avgs = []
        lineas_list = f.readlines()
        for linea in lineas_list[:10]:
            partes_list = linea.split(',')
            nums = []
            for parte in partes_list[:4]:
                num = float(parte.split(' ')[-1])
                # print(num)
                nums.append(num)
            f_avgs.append(nums)
            # print(f_avgs)
        tmp = pd.DataFrame(f_avgs, columns=cols_nom)
        print('concat')
        if first_flag:
            resultados = tmp
            first_flag= False
        else:
            resultados = pd.concat([resultados, tmp], axis=1)

resultados.to_csv('f_avgs.csv')


#### Analysis
df = pd.read_csv('f_avgs.csv')


FILTER1 = 'avg_val'
FILTER2 = 'avg_val_change'
for col in df.columns[df.columns.str.endswith(FILTER1)]:
    print(col)

df[df.columns[df.columns.str.endswith(FILTER2)]].iloc[10]