"""
Este archivo sera la creacion de los modelos:
* Regression: para predecir num_visitantes dado el sitio, dept, y mes
"""

##### Importaciones
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
#### Regresion
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error,\
    root_mean_squared_error, r2_score
import joblib
    # Para hacer webapp con streamlit
import statsmodels.api as sm # OLS
from sklearn.linear_model import LinearRegression # Lin Regression
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Lasso #Lasso regresion
from sklearn.ensemble import RandomForestRegressor # RF
from sklearn.model_selection import GridSearchCV

#### Cambiando directorio (si es necesario)
if os.getcwd().split('\\')[-1] != '3_SegmentacionClientes': 
    os.chdir('3_SegmentacionClientes')


###################################################
###### Setup

##### Leyendo datos
df_2_original = pd.read_csv('Datos/FeatEng/visitantes_sitios_turisticos_original.csv')
df_2_encoded = pd.read_csv('Datos/FeatEng/visitantes_sitios_turisticos_encoded.csv')
df_2_encoded.info()
##### Etiquetando datos
X = df_2_encoded.drop(columns='NUMERO_VISITANTES')
y = df_2_encoded['NUMERO_VISITANTES']
##### Verificando datos importados
df_2_encoded['NUMERO_VISITANTES'].values.tolist()[:10]
df_2_original['NUMERO_VISITANTES'].values.tolist()[:10]


##### Separando datos
X_train, X_test, y_train, y_test = \
    train_test_split(X,y,test_size=0.2, random_state=42)


#### Buscando los indices de datos originales
idxs = y_test.index.to_list()
df_2_org_test = df_2_original.iloc[idxs]

##### Haciendo reshapes
# X_train = X_train.values.reshape(-1,1)
# X_test = X_test.values.reshape(-1,1)
y_train = y_train.values.reshape(-1,1)
y_test = y_test.values.reshape(-1,1)


##### Normalizacion
    # X todos son bool
    # y es int64, implicando que necesita scaler
scaler = StandardScaler()
y_train = scaler.fit_transform(y_train)
joblib.dump(scaler, './App/scaler.pkl')
y_test = scaler.transform(y_test)


##### Haciendo el accuracy score
def performance(nom, prediccion):
    mae = mean_absolute_error(y_test, prediccion)
    mse = mean_squared_error(y_test, prediccion)
    rmse = root_mean_squared_error(y_test, prediccion)
    r2 = r2_score(y_test, prediccion)
    return pd.DataFrame(
        {f'{nom}_metrics': [mae, mse, rmse, r2]},
        index=['MAE', 'MSE', 'RMSE', 'R2']
    )


#############################################
###### Modelos

##### OLS
#### Entrenando OLS
X_sm = sm.add_constant(X_train)
X_sm = X_sm.astype(float)
model_ols = sm.OLS(y_train, X_sm)
summary = model_ols.fit().summary()

#### Convirtiendo OLS summary en DF
tabla_arr = summary.tables[1]
df_ols = pd.DataFrame(tabla_arr.data[1:], columns=tabla_arr.data[0])
df_ols = df_ols.rename(columns={'':'Variable'})
for col in df_ols.columns.to_list()[1:]:
    df_ols[col] = df_ols[col].astype(float)
df_ols.info()
varaibles_sign = df_ols[df_ols['P>|t|'] < 0.05]['Variable']
varaibles_sign.head(20)




##### Linear regression
linear_reg = LinearRegression()
linear_reg.fit(X_train, y_train)
lr_y_pred = linear_reg.predict(X_test)
df_lr_results = performance('lin_reg', lr_y_pred)



##### Lasso regression
#### Buscando mejor alpha
alpha, error = [], []
for i in range(1,1000):
    alpha.append(i/1000)
    candidato = Lasso(alpha=(i/1000))
    error.append(
        np.mean(
            cross_val_score(
                candidato,
                X_train,
                y_train,
                scoring='neg_root_mean_squared_error',
                cv=3,
            )
        )
    )
plt.plot(alpha,error)
plt.show()
#### Escojiendo el mejor alpha
err= tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha', 'error'])
df_alpha = df_err[df_err.error == max(df_err.error)]['alpha']
mejor_alpha = df_alpha.values[0]
mejor_alpha
#### Usando el mejor alpha
lasso_reg = Lasso(alpha=mejor_alpha)
lasso_reg.fit(X_train,y_train)
lasso_y_pred = lasso_reg.predict(X_test)
df_lasso_results = performance('lasso', lasso_y_pred)
df_lasso_results



##### RF
#### Buscando los mejores parametros
rf = RandomForestRegressor()
params = {
    'n_estimators': range(10,300,10),
    'criterion': ('squared_error','absolute_error'),
    'max_features': ('auto', 'sqrt', 'log2')
}
gs = GridSearchCV(rf, params, scoring='neg_root_mean_squared_error', cv = 3)
gs.fit(X_train,y_train.reshape(-1))
gs.best_score_
gs.best_estimator_
#### Evaluando RF
rf_y_pred = gs.best_estimator_.predict(X_test)
df_rf_results = performance('rf', rf_y_pred)





##### Uniendo todos los resultados
df_resultados = pd.concat([
    df_lr_results, 
    df_lasso_results, 
    df_rf_results], axis=1)
df_resultados

##### Guardando el mejor modelo
# joblib.dump(gs.best_estimator_, './App/model.pkl')

#################################################################

# ##### Creando visual
'''
Este bloque no me srve pq y_test saco sitios aleatoriamentes
Pero para hacer un visual necesito un sitio con todos los meses
'''
#     # Se va hacer visualizacion de los top X sitios
#     # La prediccion sera los valores verdaderos vs las predicciones
# #### Haciendo predicciones con el modelo
# ### Cargando el modelo y scaler
# lin_reg = joblib.load('./App/model.pkl')
# scaler = joblib.load('./App/scaler.pkl')
# ### Invocando modelo
# y_pred = lin_reg.predict(X_test)
# y_pred.shape
# ### Agregado preds a los datos originales del test df_2_org_test
# df_2_org_test['PREDS'] = scaler.inverse_transform(y_pred.reshape(-1,1))

# #### Buscando los top X
# top_X = 5
# top_X_sitios = df_2_org_test\
#     .groupby(by='SITIO_TURISTICO', as_index=False)\
#     ['NUMERO_VISITANTES'].agg(['mean'])\
#     .sort_values(by='mean', ascending=False)\
#     ['SITIO_TURISTICO'][:top_X].values.tolist()
# top_X_sitios
# #### Creando visual
# ### Configuraciones inciales
# ANCH = 8
# ALT = 5
# fig = plt.figure(figsize=(ANCH,ALT))
# colores = ["yellow", "purple", "cyan", "grey", "magenta", \
#            "red", "black", "green", "orange", "blue"]
# meses = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN',\
#         'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
# ### Primer plot - valores verdaderos
# for i in range(len(top_X_sitios)):
#     plt.plot(
#         df_2_org_test[\
#             df_2_org_test['SITIO_TURISTICO'] == top_X_sitios[i]\
#         ]['ID_MES'],
#         df_2_org_test[\
#             df_2_org_test['SITIO_TURISTICO'] == top_X_sitios[i]\
#         ]['NUMERO_VISITANTES'],
#         label=top_X_sitios[i],
#         color='orange',
#         marker='o',
#         markerfacecolor = colores[i],
#         markeredgecolor='black'
#     )
# plt.show()

# top_X_sitios

#################################################################
###### Creando visuales
    # Voy hacer predicciones de los top 5 sitios turisticos

##### Seleccionando datos adecuados
#### Seleccionando top 5 sitios
top_X = 5
top_X_sitios = df_2_original.groupby(by='SITIO_TURISTICO', as_index=False)\
    ['NUMERO_VISITANTES'].agg('mean')\
    .sort_values(by='NUMERO_VISITANTES', ascending=False)\
    ['SITIO_TURISTICO'][:top_X].values.tolist()

#### Seleccionando los indices
idxs = df_2_original[df_2_original['SITIO_TURISTICO'].isin(top_X_sitios)].index
df_org_topX = df_2_original.iloc[idxs]
df_enc_topX = df_2_encoded.iloc[idxs].drop(columns='NUMERO_VISITANTES')


##### Modelo y prediccion
#### Cargando el modelo y scaler
rf = joblib.load('./App/model.pkl')
scaler = joblib.load('./App/scaler.pkl')
#### Invocando modelo
y_pred = rf.predict(df_enc_topX)
#### Denormalizando
y_pred_denorm = scaler.inverse_transform(y_pred.reshape(-1,1))
#### Aregando preds a datos originales
df_org_topX['NUM_PRED'] = y_pred_denorm

##### Promedio de diferencia
df_org_topX['DIFF'] = abs(df_org_topX['NUMERO_VISITANTES'] - df_org_topX['NUM_PRED'])
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
        df_org_topX[df_org_topX['SITIO_TURISTICO']==top_X_sitios[i]]['NUM_PRED']/exp,
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
    )
plt.show()


##########################################################################################
    # Hypothesis testing #
##### Seleccionando datos adecuados
#### Seleccionando top 5 sitios
top_X = 5
top_X_sitios = df_2_original.groupby(by='SITIO_TURISTICO', as_index=False)\
    ['NUMERO_VISITANTES'].agg('mean')\
    .sort_values(by='NUMERO_VISITANTES', ascending=False)\
    ['SITIO_TURISTICO'][:top_X].values.tolist()

#### Seleccionando los indices
idxs = df_2_original[df_2_original['SITIO_TURISTICO'].isin(top_X_sitios)].index
df_org_topX = df_2_original.iloc[idxs]
df_enc_topX = df_2_encoded.iloc[idxs].drop(columns='NUMERO_VISITANTES')


##### Modelo y prediccion
#### Cargando el modelo y scaler
rf = joblib.load('./App/model.pkl')
scaler = joblib.load('./App/scaler.pkl')
#### Invocando modelo
y_pred = rf.predict(df_enc_topX)
#### Denormalizando
y_pred_denorm = scaler.inverse_transform(y_pred.reshape(-1,1))
#### Aregando preds a datos originales
df_org_topX['NUM_PRED'] = y_pred_denorm

##### Hipotesis
        # Vm = Visitantes del modelo
        # Va = Visitantes actuales
    # HO = Modelo no captura los visitantes de los sitios turisticos
        # Vm - Va != 0
    # HA = Modelo si captura los visitantes de los sitios turisticos
        # Vm - Va = 0
from scipy import stats
##### Prueba de hipotesis
    # Determinar normalidad de todos sitios (valores actuales y del modelo)
    # Usar Shapiro-Wilk por su baja cantidad de muestra

for sitio in top_X_sitios:
    # Extrayendo datos
    num_actual = df_org_topX[df_org_topX['SITIO_TURISTICO'] == sitio]['NUMERO_VISITANTES']
    num_predecido = df_org_topX[df_org_topX['SITIO_TURISTICO'] == sitio]['NUM_PRED']
    # Prueba de normalidad
    _, num_act_pvalor = stats.shapiro(num_actual.values)
    _, num_pred_pvalor = stats.shapiro(num_predecido.values)
    # Formalizando
    num_act_normal = True if num_act_pvalor > 0.05 else False
    num_pred_normal = True if num_pred_pvalor > 0.05 else False
    print(f'Sitio {sitio} Normalidad - valores actuales {num_act_normal}; valores predecidos {num_pred_normal}')
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
            print(f'T-test p-valor {t_pvalor}: se acepta la hipotesis nula, las dos muestras son diferentes')
        else:
            print(f'T-test p-valor {t_pvalor}: no se rechaza la hipotesis nula, las dos muestras no son diferentes')
    else: 
        _, w_pvalor = stats.wilcoxon(
            num_actual.values,
            num_predecido.values,
            alternative='two-sided'
        )
        if t_pvalor < 0.05:
            print(f'Wilcoxon p-valor {t_pvalor}: se acepta la hipotesis nula, las dos muestras son diferentes')
        else:
            print(f'Wilcoxon p-valor {t_pvalor}: no se rechaza la hipotesis nula, las dos muestras no son diferentes')

    # Resultados:
        # Los valores del modelo y los valores actuales no son diferentes
        # I.e., el modelo es una buena representacion para predecir los numero de visitantes

########################################################3
    # Creando Pipeline #
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.pipeline import Pipeline


#### Cargando datos
df_2_original = pd.read_csv('Datos/FeatEng/visitantes_sitios_turisticos_original.csv')
df_2_encoded = pd.read_csv('Datos/FeatEng/visitantes_sitios_turisticos_encoded.csv')

#### Cargando el modelo y scaler
rf = joblib.load('./App/model.pkl')
scaler = joblib.load('./App/scaler.pkl')

#### OHE
X = df_2_original[['ID_MES', 'DEPARTAMENTO', 'SITIO_TURISTICO']]
y = df_2_original['NUMERO_VISITANTES']

### Creando encoder
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
encoder = ohe.fit(X)

### Implementacion
enc = encoder.transform(X)
(enc == df_2_encoded.drop(columns = 'NUMERO_VISITANTES')).sum().sum()
(df_2_encoded.drop(columns = 'NUMERO_VISITANTES') == enc).all(axis=1).all()
    # confirmacion que OHE: original -> encoded

#### Pipe de OHE
pip1 = Pipeline([
    ('encoder', encoder),
])

enc2 = pip1.transform(X)
(enc2 == enc).all(axis=1).all()
    # Confirmacion ue trabaja


###### Model prediccion
#### SEleccionanado top X
top_X = 5
top_X_sitios = df_2_original.groupby(by='SITIO_TURISTICO', as_index=False)\
    ['NUMERO_VISITANTES'].agg('mean')\
    .sort_values(by='NUMERO_VISITANTES', ascending=False)\
    ['SITIO_TURISTICO'][:top_X].values.tolist()

#### Seleccionando los indices
idxs = df_2_original[df_2_original['SITIO_TURISTICO'].isin(top_X_sitios)].index

#### usando rf.predict
df_org_idxs = df_2_original.iloc[idxs].drop(columns = 'NUMERO_VISITANTES')
df_enc_idxs = df_2_encoded.iloc[idxs].drop(columns = 'NUMERO_VISITANTES')

idxs_enc = encoder.transform(df_org_idxs)

(idxs_enc == df_enc_idxs).all().all()   # Confirmacion que son iguales

pred_idxs_enc = rf.predict(idxs_enc)
pred_df_enc = rf.predict(df_enc_idxs)

(pred_idxs_enc == pred_df_enc).all().all()  # son iguales

#### Predicciones usando pipeline

pipeline = Pipeline([
    ('encoder', encoder),
    ('model', rf)
])

pipe_org = pipeline.predict(df_org_idxs)
pipe_enc = rf.predict(df_enc_idxs)

(pipe_org == pipe_enc).all().all()


dir(pipeline)

pipeline.get_feature_names_out()

new = pipeline.predict(X.iloc[idxs])


encoder.get_feature_names_out()
encoder.feature_names_in_
encoder.n_features_in_
encoded = ohe.transform(X)

nuevo = ohe.transform(X.iloc[0].values.reshape(1,-1))

new = ohe.transform(np.array([np.int64(3),'AMAZONAS', 'RUMIPUNKU'],dtype=object).reshape(1,-1))

X.iloc[0].values.reshape(1,-1)


df_2_encoded_tmp = df_2_encoded.drop(columns='NUMERO_VISITANTES')

tmp = pd.DataFrame(
    encoded,
    columns=df_2_encoded_tmp.columns
)

(tmp == df_2_encoded_tmp).all(axis=1).sum()


new = ohe.transform()






idxs = df_2_original[df_2_original['SITIO_TURISTICO'].isin(top_X_sitios)].index
test_tmp = tmp.iloc[idxs]
test_df=df_2_encoded_tmp.iloc[idxs]

p1 = rf.predict(test_tmp)
p2 = rf.predict(test_df)

p1_dn = scaler.inverse_transform(p1.reshape(-1,1))
p2_dn = scaler.inverse_transform(p2.reshape(-1,1))

p1_dn == p2_dn

