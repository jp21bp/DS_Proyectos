# Datos de estos Proyectos

Todos estos proyectos fueron jalados de GitHub para que yo pueda acomodarme con proyectos DS. Ninguno de estos proyectos son mio

## Pasos Generales dentro un Proyecto
Existen los siguiente pasos generales dentro un proyecto:
1. Formulacion del Problema
2. Coleccion de Datos
3. Limpieza de Datos
4. EDA de Datos
5. Creacion de Modelos
6. Despliegue de Modelos
7. Documentacion de Analisis e Insights


### Paso 1: Formulacion del Problema
Existen varias maneras de formular un problema pero en general necesitan:
* Contexto del Negocio/Problema
    - Cual es el contexto del problema?
    - Cual es el problema?
    - Cual es el impoacto al negocio?
    - Quienes son los stakeholders?
    - Cuales son los antecedentes?
* Objetivo del Proyecto
    - Que se quiere lograr?
    - Tipo de problema: classificacion, regression, optimizacion, etc?
* Scope:
    - Cuales son los aspectos dentro del proyecto?
    - Cuales son los aspectos afuera del proyecto?
* Disponibilidad de Datos
    - Estructurados? No Estructurados? Incompletos?
* Restricciones
    - Alguna limitacion tecnica, financiera, ethica, etc.?
* Metricas de Exito
    - Como se mide el exito?
    - Cual KPI es importante?

#### Transformacion: problema de negocio -> problema de datos

https://levelup.gitconnected.com/crafting-effective-problem-statements-for-data-science-projects-60c979642194

Cuando se formula el problema, los siguientes paso los transformaran en problema de datos:
1. Frame la formulacion del problema
    * Converit problema general en especifico
    * Considera SMART
2. Romper en problemas matematicos mas pequenos
    * Al problema seleccionado, transformarlo en una ecuacion matematica de diferentes componentes
3. Convertir los problemas pequenos en problemas de datos
    * Identificar herramientas de datos en los componentes matematicos para solucionar el problema original
4. Encontrar las soluciones a los problemas de datos
    * Aplicar las herramientas

Ejemplo: 
1. Frame
    * Problema de negocio: " Quiero aumentar mis ganancias de mis clientes actuales"
    * Formulacion: "Aumentar x% ingresos de clientes actuales en los proximos y meses para reduccir reliance en nuevo clientes"
2. Problema matematicos
    * Ganacias = Ingresos - Egresos
        - Vamos asumir que no se puede cambiar egresos
    * Ingresos = num_clients * return_rate * conversion_rate * avg_purchase_value 
3. Problema de datos
    * num_clients:
        - Forecasting la acquision de clientes basado en datos historicas y datos del mercado
        - Segmentar los clientes para identificar las necesidades y preferencias de diferente grupos
    * return_rate:
        - Prediccir la probabilidad de un cliente regesando a la tienda dentro de *30 dias*
    * conversion_rate:
        - Predecir la probabilidad de convertir un cliente basado en los datos de interaccion (de un cliente arbritario) y sus datos de compras
        - Optimizar el diseno del website para aumentar el conversion_rate a traves de A/B testing y experimentacion
    * avg_purchase_value:
        - forecasting el purchase value futuristico usando tecnicas de prediccion de modelos *y* el customer lifetime value analysis
        - Crear un sist. de recomendaciones para persnalizar las recomendaciones de productos y upsell/cross-sell oportunidades basado en datos de compras previas y las preferencias del cliente



### Paso 2: Coleccion de datos
Existen varias forma de coleccionar datos, pero la mayoria de veces se van a tener que extraer de sitios publicos para poder procesarlas.

Esta extraccion generealmente se hace co SElenium





### Paso 3: Limpieza de Datos
La limpieza de datos generalmente consiste de 3 partes:
1. Arreglando nulls - eliminar o rellenar
    * Verificando la cantidad de nulos
        - df.isnull().sum()
        - df.isnull().sum()/len(df)*100
    * Eliminando nulos
        - df.dropna()
            * axis = 0/1
            * how = 'all'/ 'any'
            * thresh = x
            * subset = ['x','y','z'] 
    * Rellenando nulos
        - df.fillna()
            * Personalizado
            * method = 'ffill' / 'bfill'
2. Revisando duplicaciones - genrealmente eliminacion (con axis=0)
    * duplicados_bool = df.duplicated()
        - Boolean con num de filas para ver si hay duplicacion
    * duplicados_df = df[df.duplicated()]
        - Muestra solo filas duplicadas
    * duplicados_nombre = df.duplicated(subset=['Nombre'])
        - Verificar duplicacion en columnas especificas
    * df_sin_duplicados = df.drop_duplicates()
        - Eliminar duplicados 
3***. (Generalmente despues de feature engineering) Transformacion de datos - estandardizacion, one-hot encoding de vars categoricas/cualitativas, log-transform, etc. 
    * df.get_dummy()
        - One hot encoding
    * df_std = (df - df.mean()) / df.std(ddof=0)
    * df[numeric_cols] = np.log(df[numeric_cols])
    * df["Education"] = df['Education'].replace({"Basic": 0, "2n Cycle": 1, "Graduation": 2, "Master": 3, "PhD": 4})
        - Transformando de cateogical a cuant
        - Pero NO ES one hot encoding







### Paso 4: EDA
* Cargar datos
* Hacer resumen holistico
    - df.describe()
    - df.info()
* Identificar variables cuant y cual
    - Cuant: cuant_vars = df._get_numeric_data().columns.values
    - Cual: cual_vars = list(set(df.columns) - set(cuant_vars))
* Investigando correlaciones
    - sns.heatmap(df.corr(), annot = True, cmap = 'coolwarm', center = 0)
* Hacer los histogramas (con variables cuant)
    - sqrt_vars = sqrt(len(cuant_vars))
    - fig, axs = plt.subplots(sqrt_vars, sqrt_vars, figsize=(20,20))
    - palette = cmap(np.linspace(start = 0, stop = 1, num = 5))
    - for ax, col, color in zip(axs.flat, cuant_vars, cycle(palette)):
        fig = sns.histplot(df[col], ax=ax, color=color); fig.grid()
* Histogramas (con variables cual) = Barplots
    - sqrt_vars = sqrt(len(cuanl_vars))
    - fig, axs = plt.subplots(sqrt_vars, sqrt_vars, figsize=(20,8))
    - for ax, col, color in zip(axs.flat, cuanl_vars, cycle(palette)):
        sns.barplot(x= df[column].value_counts().index, y = df[column].value_counts().values, ax = ax, color = color)
* Boxplots
    - df.boxplot(columns=cuant_vars, rot=90)
        * Generalmente hacer estandardizacion para que esten juntos
    - sqrt_vars = sqrt(len(cuant_vars))
    - fig, axs = plt.subplots(sqrt_vars, sqrt_vars, figsize=(20,20))
    - palette = cmap(np.linspace(start = 0, stop = 1, num = 5))
    - for ax, col, color in zip(axs.flat, cuant_vars, cycle(palette)):
        fig = sns.boxplot(data = df[f"{column}"], ax = ax, color = color); fig.grid()
* Decidir si guardar/eliminar outliers
    - Se utilizaria "df.describe()" para ver los quantiles
* Feature engineering (ejemplos)
    - df["Age"] = datetime.datetime.now().year - df["Year_Birth"]
    - df["Family Members"] = df["Marital_Status"] + df["Kidhome"] + df["Teenhome"]
    - df["Total_Spent"] = df["MntWines"] + df["MntFruits"] + df["MntMeatProducts"] + df["MntFishProducts"] + df["MntSweetProducts"] + df["MntGoldProds"]
    - df["Total_Purchases"] = df["NumDealsPurchases"] + df["NumWebPurchases"] + df["NumCatalogPurchases"] + df["NumStorePurchases"]
    - df["Accepted_Promos"] = df["AcceptedCmp1"] + df["AcceptedCmp2"] + df["AcceptedCmp3"] + df["AcceptedCmp4"] + df["AcceptedCmp5"]
* Eliminar columnas que no aportan informacion
    - drop_columns = ["ID", "Year_Birth"]
    - df = df.drop(drop_columns, axis = 1)
* Matriz de correlacion
* Normalizacion de datos





Buena segmentacion:
https://github.com/martabuaf/Customer-Segmentation/blob/main/clustering_methods.py