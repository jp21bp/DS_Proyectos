"""
Este archivo creara y evaluara los modelos
"""

####### Importaciones
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


if os.getcwd().split('\\')[-1] != 'FeatEng':
    os.chdir('./4_DemandaForecasting/Datos/FeatEng')

##################################

##### Leyendo datos
df_org = pd.read_csv('ventas_productos_org.csv')
df_enc = pd.read_csv('ventas_productos_enc.csv')

##### Etiquetando datos
X = df_enc.drop(columns='cantidad')
y = df_enc['cantidad']

##### Separando datos
X_train, X_test, y_train, y_test = \
    train_test_split(X,y,test_size=0.2, random_state=42)

##### Buscando indices de df_org
idxs = y_test.index.to_list()
df_org_test = df_enc.iloc[idxs]

##### Haciendo reshapes
y_train = y_train.values.reshape(-1,1)
y_test = y_test.values.reshape(-1,1)

##### Normalizacion
scaler = StandardScaler()
y_train = scaler.fit_transform(y_train)
joblib.dump(scaler, './scaler.pkl')
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
    candidato = Lasso(alpha=(i/1000), max_iter=5000)
    error.append(
        np.mean(
            cross_val_score(
                candidato,
                X_train,
                y_train,
                scoring='neg_root_mean_squared_error',
                verbose=2,
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
    'n_estimators': range(10,300,50),
    'max_depth':range(5,11,5),
    'min_samples_split': range(1,6,1),
    'criterion': ('squared_error','absolute_error'),
    'max_features': ('auto', 'sqrt', 'log2'),
    'random_state': [42]
}
gs = GridSearchCV(rf, params, scoring='neg_root_mean_squared_error', cv = 3, verbose=2)
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
joblib.dump(lasso_reg, './model.pkl')



#################################################################
###### Creando visuales
    # Voy hacer predicciones de los top 5 sitios turisticos

##### Seleccionando datos adecuados
#### Seleccionando top 5 productos anuales
top_X = 5
top_X_productos = df_org\
    .groupby(by='nombre', as_index=False)\
    ['cantidad'].agg('sum')\
    .sort_values(by='cantidad', ascending=False)\
    ['nombre'][:top_X].values.tolist()

#### Seleccionando indices
idxs = df_org[df_org['nombre'].isin(top_X_productos)].index
df_org_topX = df_org.iloc[idxs]
df_enc_topX = df_enc.iloc[idxs]

df_org_topX.groupby(by='nombre',as_index=False)\
    ['mes'].agg('unique')

##### Modelo y prediccion
#### Cargando el modelo y scaler
modelo = gs.best_estimator_
# modelo = joblib.load('./model.pkl')
scaler = joblib.load('./scaler.pkl')
#### Invocando modelo
y_pred = modelo.predict(df_enc_topX.drop(columns='cantidad'))
#### Denormalizando
y_pred_denorm = scaler.inverse_transform(y_pred.reshape(-1,1))
#### Aregando preds a datos originales
df_org_topX['NUM_PRED'] = y_pred_denorm


##### Promedio de diferencia
df_org_topX['DIFF'] = abs(df_org_topX['cantidad'] - df_org_topX['NUM_PRED'])
diff_promedio = df_org_topX['DIFF'].mean().item()


##### Visuales
#### Seleccionando datos
df_visual = df_org_topX\
    .groupby(by=['mes', 'nombre'], as_index=False)\
    .agg(
        cantidad_verdadera = pd.NamedAgg(
            column='cantidad', aggfunc='mean'
        ),
        cantidad_pred = pd.NamedAgg(
            column='NUM_PRED', aggfunc='mean'
        )
    )
#### Configuracion inicial
ANCH = 8
ALT = 5
fig, ax  = plt.subplots(figsize=(ANCH,ALT))
meses = df_visual['mes'].unique()
colores = ["yellow", "purple", "cyan", "grey", "magenta", \
           "red", "black", "green", "orange", "blue"]
#### Graficando
for i in range(len(top_X_productos)):
    ax.plot(
        range(len(meses)),
        df_visual[df_visual['nombre']==top_X_productos[i]]['cantidad_pred'],
        label=top_X_productos[i],
        marker='o',
        color='orange',
        markerfacecolor = colores[i],
        markeredgecolor='black'
    )
    ax.plot(
        range(len(meses)),
        df_visual[df_visual['nombre']==top_X_productos[i]]['cantidad_verdadera'],
        label=top_X_productos[i],
        marker='o',
        color='blue',
        markerfacecolor = colores[i],
        markeredgecolor='black'
    )
        
    
plt.show()

