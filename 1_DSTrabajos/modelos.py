###### Creando modelos
    # Este archivo se enfocara en la creacion de los modelos

#### Importaciones de modulos
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


#### Leyendo los datos
print(os.chdir('1_DSTrabajos'))
df = pd.read_csv('datos_limpios.csv')


#### Ingineria de Variables
df.columns
df_variables = df[['titulo', 'len_desc', 'estado', 'ano', 'org', 'sueldo_promedio']]

#### Creando dummy datos
df_dum = pd.get_dummies(df_variables)
print(df_dum.columns)


#### Train test split
from sklearn.model_selection import train_test_split

X = df_dum.drop('sueldo_promedio', axis=1)
y = df_dum['sueldo_promedio'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#### OLS modelos
import statsmodels.api as sm

X_sm = sm.add_constant(X)
X_sm = X_sm.astype(float)
    # NEcesario convertir en float
model_ols = sm.OLS(y, X_sm)
summary = model_ols.fit().summary()
print(summary)
    # Escojer P valores < 0.05
        # PAra buscar cuales son significantes

#### Conviertiendo OLS summary en DataFrame
tabla_arr = summary.tables[1]
print(tabla_arr)
df_ols = pd.DataFrame(tabla_arr.data[1:], columns=tabla_arr.data[0])
df_ols = df_ols.rename(columns={'':'Variable'})
    # Primera columna es un vacio
df_ols.info()
for col in df_ols.columns.to_list()[1:]:
    df_ols[col] = df_ols[col].astype(float)
df_ols.info()
varaibles_sign = df_ols[df_ols['P>|t|'] < 0.05]['Variable']
varaibles_sign.shape



##### Formando linear regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

linear_reg = LinearRegression()
linear_reg.fit(X_train, y_train)
linear_reg_resultados = np.mean(
    cross_val_score(
        linear_reg, 
        X_train,
        y_train,
        scoring = 'neg_mean_absolute_error'
    )
)

print(linear_reg_resultados)


##### Lasso regression
#### Averiguando mejor param alpha
from sklearn.linear_model import Lasso
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
                scoring='neg_mean_absolute_error',
                cv=3
            )
        )
    )

plt.plot(alpha,error)
plt.show()

#### Esocjiendo el mejor alpha
err= tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha', 'error'])
alpha = df_err[df_err.error == max(df_err.error)]['alpha']
mejor_alpha = alpha.values[0]

#### Usando el mejor alpha
lasso_reg = Lasso(alpha=mejor_alpha)
lasso_reg.fit(X_train,y_train)
lasso_reg_resultados = np.mean(
    cross_val_score(
        lasso_reg,
        X_train,
        y_train,
        scoring = 'neg_mean_absolute_error', 
        cv= 3))





##### Creando un RF
#### Buscando los mejores parametros
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
rf = RandomForestRegressor()
params = {
    'n_estimators': range(10,300,10),
    'criterion': ('squared_error','absolute_error'),
    'max_features': ('auto', 'sqrt', 'log2')
}
gs = GridSearchCV(rf, params, scoring='neg_mean_absolute_error', cv = 3)

gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_




##### Prueba final con todos los modelos
tpred_linear_reg = linear_reg.predict(X_test)
tpred_lasso_reg = lasso_reg.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error as mae
mae(y_test, tpred_linear_reg)
mae(y_test, tpred_lasso_reg)
mae(y_test, tpred_rf)   # Tiene mejores resultados


##### Guardando el mejor modelo
import pickle, os
model_path = os.path.join('FlaskAPI', 'model_file.p')
model_pickle = {'model': gs.best_estimator_}
pickle.dump(model_pickle, open(model_path, 'wb'))


##### Aseugrando que el modelo guardado trabaja
with open(model_path, 'rb') as file:
    data = pickle.load(file)
    main_modelo = data['model']

prediccion = main_modelo.predict(
    X_test.iloc[3,:].values.reshape(1,-1)
)
prediccion
y_test[3]


sample = X_test.iloc[3,:].values.astype(float)
