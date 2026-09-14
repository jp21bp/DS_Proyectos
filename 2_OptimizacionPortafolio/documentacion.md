# Table of Contents
1. [Contexto del Proyecto](#contexto-del-proyecto)
    * [Perspicacias, Recomendaciones y sus Enfoques](#perspicacias-recomendaciones-y-sus-enfoques)
2. [Estructura de los Datos y su Verificaciones](#estructura-de-los-datos-y-su-verificaciones)
3. [Resumen Ejecutivo](#resumen-ejecutivo)
    * [Resumen de Descubrimientos ](#resumen-de-descubrimientos)
    * [Tendencia de los Descubrimientos](#tendencia-de-los-descubrimientos)
4. [Detalles de las Perspicacias](#detalles-de-las-perspicacias)
    * primero
    * segundo
    * tercero
    * cuarto
5. [Modelos, Predicciones y sus Impactos](#modelos-predicciones-y-sus-impactos)
    * modelo 1
    * modelo 2
6. [Recomendaciones](#recomendaciones)
    * primero
    * segundo
    * tercero
    * cuarto
7. [KPIs](#kpis)
    * primero
    * segundo
    * tercero
8. [Suposiciones y Avisos](#suposiciones-y-avisos)



## Contexto del Proyecto
asasfsaf
** ML - Machine Learning
asfsafaf

### Perspicacias, Recomendaciones y sus Enfoques
asfafaf

assafaf

## Estructura de los Datos y su Verificaciones
SPLAC es un indice financiero que consiste de las 40 empresas suramericanas tamano y liquidez mas alta. Estas companias varian a traves del tiempo, entonces las empresas seleccionadas fuerons las que estaban dentro de estas 40 empresas el 31 de Agosto, 2026. Reconociendo que no todas estas companias empezaron al mismo tiempo, se aplico un filtracion para seleccionar a la companias que estaban activos el 28 de Febrero del 2006. Esta fecha se escojio para poder incluir la crisis del 2008 dentro los datos. 

La informacion historica se descargaron de YFinance, con los siguiente detalles:
* Fechas (Post-Filtracion): 28/2/2006 - 28/8/2026
* Companias (Post-Filtracion): AMXB.MX, AXIA3.SA, BBAS3.SA, BIMBOA.MX, BSAC, CEMEXCPO.MX, CENCOSUD.SN, CIB, FEMSAUBD.MX, GCARSOA1.MX, GGB, ISA.CL, PAC, PBR, RENT3.SA, SCCO, SQM, VALE, VIV, WALMEX.MX, WEGE3.SA
* Indicadores: Cierre Ajustado, Cierre, Alto, Bajo, Apertura, y Volumen.


## Resumen Ejecutivo
assaas

afsagsag

### Resumen de Descubrimientos
asafasf

asgsagsa

### Tendencia de los Descubrimientos
asfsfsa

asgsagsag

## Detalles de las Perspicacias 
asfsfsa

asgsagsag

### Ratio Sharpe de 0.966 en el Sector Industrial
Dentros las estrategias de asignacion fija, enfocandose en el sector industrial construyo el portafolio mas fuerte entre todos las estrategias sin ML. 

* **Ratio Sharpe**: esta estrategia obtuvo el ratio sharpe mas alto de 0.966 y 0.929 (sin escalar la volatilidad).
* **Retorno Esperado**: al igual, esta estrategia obtiene los mejores retornos esperados annuales, con 0.184 y 0.055 (sin escalar la volatilidad)

### Impacto de COVID
La pandemia del COVID se sinitio en todos aspectos globales, incluyendo al sector financiero.

* **Todas las estrategia**, sea con o sin ML, pueden capturar los impactos drasticos del COVID 19
* Las estrategias **con volatilidad escalada** fueron **menos afectados** por estos impactos, al tener una caida mas mesurada y con menos perdidas.
* Todas las estrategias, incluyendo el benchmark, pudieron re-saltar sus ganancias al terminar la pandemia. 

### Tercero
asfsfsa

asgsagsag

### Cuarto
asfsfsa

asgsagsag

## Modelos, Predicciones y sus Impactos
Existen varias formas para crear un modelo que capture las dependencias temporales dentro un conjunto de datos. En este caso, dos estrategias principales se estudiaron: ventanas deslizantes y ventanas expansivas. Adicionalmente, diferentes combinaciones de las siguientes metricas financieras, de cada accion, se investigaron: Precio de Cierre (P), Retornos Logaritmicos (RL), TEMA (T), HLC3 (H), y OBV (O). 

### Modelos con Ventanas Deslizantes
En esta estrategia las ventanas de los datos de deslizaban anualmente, senalando que solo los datos dentro de dos anos se utilizaban para entranar el modelo. Se crearon tres diferentes modelos con esta estrategia. La arquitecturas eras iguales, pero los datos procesados tenian las siguientes diferecias: datos 1 usaban los indicadores P y RL; datos 2 usaban los indicadores T, H, y O; datos 3 usaban todos los inicadores. 



### Modelos con Ventanas Expansivas
En esta estrategia las ventanas se expandia anualmente para capturar todos los datos desde el comienzo (disponible) hasta el dia antes de cuando empieza los datos de pruebas. Similar a la otra estrategia, se crearon tres diferentes modelos con arquitecturas iguales pero diferentes indicadores en cada conjunto. 


### Resultados
Los modelos de las ventanas deslizantes obtuvieron un **promedio ratio Sharpe de 0.695 y 0.645**(al escalar la volatilidad) mientras los moelos de las ventanas expansivas tenian **0.809 y 769**(al escalar la volatilidad). En otras palabras, la segunda estrategia predice pesas (de las acciones) que resultan en portafolios con ratio Sharpes mas altos. 

Por lo contrario, se registra que en ambas estrategias los modelos que utilizaban todos los indicadores obtuvieron un ratio Sharpe **mas que 1.39 (ventanas deslizantes) y 1.19 (ventas expansivas) veces** de que todos los demas. Incluso, el modelo con ventana deslizante que utilizaba todos los indicadores obtuvo mejores resultados que los modelos de ventanas expansivas que no utilizaban todos los indicadores. 

Adicionalmente, el **modelo con ventanas expansivas** tiene mejores resultados al **no escalar la volatailidad** (con un ratios de 0.905 y 1.254). De lo contrario, el **modelo con ventanas deslizante** tiene los mejores resultados cuando **si se escala la volatilidad** (con ratios de 0.844 y 1.252)

## Recomendaciones
asfasfa

### Estrategia Corresponde al Usuario
Todas las estrategias presentadas se destacan con 10 diferentes metricas, pero ninguna estrategia es la mejor en todas estas metricas. La estrategia mas adecuada para desenvolver depende en las caracteristicas del usuario. 

### Enfoque en el Sector Industrial
El sector Industrial tiene una gran corrida, obteniendo alrededor de **250% retorno cumulativo** en la inversion inicial. En corto plazo, se recomienda invertiendo una gran mayoria de los recursos en el sector industrial, siempre y cuando se diversifique con otras acciones. A largo plazo, se recomienda seguir investigando los movimientos del sector, considerando que un cambio del mercado pueda empezar a fortalecer otro sector. 

### Utilizacion de mas Indicadores
Se registra que los ML modelos, en ambas estrategias de ventanilla (deslizante y expansiva), obtuvieron mejores rendimientos al utilizar **todos los indicadores**. 

sdgsagag

### Tercero
asgagsa

### Cuarto
ggagag

## KPIs
sgaga

### Primero
dgdgaga

### Segundo
sdagaga

### Tercero
asgasgsa

## Suposiciones y Avisos
dgonin


