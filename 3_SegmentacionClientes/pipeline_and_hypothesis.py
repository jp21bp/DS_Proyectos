"""
Este se encarga de crear un Pipeline y el hypothesis testing
"""

#### Importing modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import stats
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import os, joblib


#### Paths
data_path = os.path.join(
    os.getcwd(),
    '3_SegmentacionClientes',
    'Datos',
    'FeatEng'
)

pickle_path = os.path.join(
    os.getcwd(),
    'App'
)

#### Reading data
df_2_original = pd.read_csv(f'{data_path}/visitantes_sitios_turisticos_original.csv')
df_2_encoded = pd.read_csv(f'{data_path}/visitantes_sitios_turisticos_encoded.csv')
model = joblib.load(f'{pickle_path}/model.pkl')
scaler = joblib.load(f'{pickle_path}/scaler.pkl')

set(df_2_original['SITIO_TURISTICO'].values)

###################################################
    # Creating Pipeline #
#### Separating data
X = df_2_original[['ID_MES', 'DEPARTAMENTO', 'SITIO_TURISTICO']]
y = df_2_original['NUMERO_VISITANTES']

dicc = df_2_original.groupby('DEPARTAMENTO')['SITIO_TURISTICO'].apply(list).to_dict()
for k,v in dicc.items():
    print(f"'{k}':{v},")

#### Creating OneHotEncoder
### Initialize
OHE = OneHotEncoder(
    handle_unknown='ignore',
    sparse_output=False
)
### Fitting
encoder = OHE.fit(X)

#### Creating Pipeline
pipeline = Pipeline([
    ('encoder', encoder),
    ('model', model)
])

#### Saving pipeline
joblib.dump(pipeline, f'{pickle_path}/pipeline.pkl')

#######################################
    # Hypothesis testing #
#### Selecting the top 5 tourist sites
top_X = 5
top_X_sitios = df_2_original.groupby(by='SITIO_TURISTICO', as_index=False)\
    ['NUMERO_VISITANTES'].agg('mean')\
    .sort_values(by='NUMERO_VISITANTES', ascending=False)\
    ['SITIO_TURISTICO'][:top_X].values.tolist()

#### Selecting the indices of the top 5 sites
idxs = df_2_original[df_2_original['SITIO_TURISTICO'].isin(top_X_sitios)].index
df_org_topX = df_2_original.iloc[idxs]
X_top5 = df_org_topX.drop(columns = 'NUMERO_VISITANTES')
y_top5 = df_org_topX['NUMERO_VISITANTES']

#### Running pipeline
y_pred_top5_normalized = pipeline.predict(X_top5)

#### Denormalizing
y_pred_top5= scaler.inverse_transform(
    y_pred_top5_normalized.reshape(-1,1)
)

#### Adding predictions to whole DF
df_org_topX['PREDICTION'] = y_pred_top5

#### Enacting hypothesis test
for sitio in top_X_sitios:
    # Extracting data
    num_actual = df_org_topX[df_org_topX['SITIO_TURISTICO'] == sitio]['NUMERO_VISITANTES']
    num_predecido = df_org_topX[df_org_topX['SITIO_TURISTICO'] == sitio]['PREDICTION']
    # Prueba de normalidad
    _, num_act_pvalor = stats.shapiro(num_actual.values)
    _, num_pred_pvalor = stats.shapiro(num_predecido.values)
    # Formalizando
    num_act_normal = True if num_act_pvalor > 0.05 else False
    num_pred_normal = True if num_pred_pvalor > 0.05 else False
    print(f'Sitio {sitio} Normalidad - valores actuales {num_act_normal}; valores predecidos {num_pred_normal}')
    print(f'Site {sitio} Normality - actual values {num_act_normal}; predicted values {num_pred_normal}')
    # Prueba de hipotesis
    if num_act_normal and num_pred_normal:
        # Ambos necesitan ser normales para usar ttest
        var_igual = True if num_actual.std() == num_predecido.std() else False
        _, t_pvalor = stats.ttest_ind(
            num_actual.values,
            num_predecido.values,
            equal_var=var_igual,
            alternative='two-sided'
        )
        if t_pvalor < 0.05:
            print(f'T-test p-valor {t_pvalor}: se acepta la hipotesis alternativa, las dos muestras son diferentes')
            print(f'T-test p-valor {t_pvalor}: the alternative hypothesis is accepted, the two samples are different')
        else:
            print(f'T-test p-valor {t_pvalor}: se acepta la hipotesis nula, las dos muestras no son diferentes')
            print(f'T-test p-valor {t_pvalor}: the null hypothesis is accepted, the two samples are not different')
    else: 
        _, w_pvalor = stats.wilcoxon(
            num_actual.values,
            num_predecido.values,
            alternative='two-sided'
        )
        if t_pvalor < 0.05:
            print(f'Wilcoxon p-valor {t_pvalor}: se acepta la hipotesis alternativa, las dos muestras son diferentes')
            print(f'Wilcoxon p-valor {t_pvalor}: the alternative hypothesis is accept, the two samples are different')
        else:
            print(f'Wilcoxon p-valor {t_pvalor}: se acepta la hipotesis nula, las dos muestras no son diferentes')
            print(f'Wilcoxon p-valor {t_pvalor}: the null hypothesis is accepted, the two samples are not different')
    # Resultados:
        # Los valores del modelo y los valores actuales no son diferentes
        # I.e., el modelo es una buena representacion para predecir los numero de visitantes

############################################################
    # Visual #
##### Calculating difference
df_org_topX['DIFF'] = abs(df_org_topX['NUMERO_VISITANTES'] - df_org_topX['PREDICTION'])
diff_promedio = int(df_org_topX['DIFF'].mean().item())

##### Visuales
#### Configuracion inicial
ANCH = 8
ALT = 5
exp = 10000
fig, ax  = plt.subplots(figsize=(ANCH,ALT))
meses = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN',\
         'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
colores = ["yellow", "purple", "cyan", "grey", "magenta", \
           "red", "black", "green", "orange", "blue"]
#### Graficando
for i in range(len(top_X_sitios)):
    ax.plot(
        range(len(meses)),
        df_org_topX[df_org_topX['SITIO_TURISTICO']==top_X_sitios[i]]['NUMERO_VISITANTES']/exp,
        label = top_X_sitios[i],
        marker='o',
        color = "#c0960cff",
        markerfacecolor = colores[i],
        markeredgecolor='black'
    )
    ax.plot(
        range(len(meses)),
        df_org_topX[df_org_topX['SITIO_TURISTICO']==top_X_sitios[i]]['PREDICTION']/exp,
        label = top_X_sitios[i],
        marker='o',
        color = 'blue',
        markerfacecolor = colores[i],
        markeredgecolor='black'
    )
ax.set_xticks(range(len(meses)))
ax.set_xticklabels(meses)
ax.set_xlabel('MES', fontweight='bold')
ax.set_ylabel(f'VISITANTES (x{exp})', fontweight='bold')
ax.set_title(f'{diff_promedio} Turistas de Diferencia Promedio entre \nla Preddicion y Valores Actuales',
             fontweight='bold')
ax.set_ylim(0, max(df_org_topX['NUMERO_VISITANTES'])/exp + 2)
# Crear elementos personalizados para la leyenda
custom_lines = [
    Line2D([0], [0], color='blue', linestyle='-', lw=2),   
    Line2D([0], [0], color="#c0960cff", linestyle='-', lw=2),
]
for i in range(len(top_X_sitios)):
    custom_lines.append(
        Line2D([0], [0], color=colores[i], marker='o', lw=0, markersize=4)  # Puntos rojos
    )

# Agregar leyenda personalizada
ax.legend(
    custom_lines, 
    ['PREDICCIONES', 'VALORES ACTUALES'] + top_X_sitios, 
    loc='upper left',
    bbox_to_anchor =(-0.1, 1.035), 
    fontsize=7.5, 
    framealpha=1.0
    )
plt.show()



