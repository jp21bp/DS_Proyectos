# Table of Contents
1. [Contexto del Proyecto](#contexto-del-proyecto)
    * [Hallazgos Insights, Recomendaciones y sus Enfoques](#hallazgos-insights-recomendaciones-y-sus-enfoques)
2. [Estructura de los Datos y su Verificaciones](#estructura-de-los-datos-y-su-verificaciones)
3. [Resumen Ejecutivo](#resumen-ejecutivo)
    * [Resumen de Descubrimientos ](#resumen-de-descubrimientos)
    * [Tendencia de los Descubrimientos](#tendencia-de-los-descubrimientos)
4. [Detalles de las Hallazgos Insights](#detalles-de-los-hallazgos-insights)
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

### Hallazgos Insights, Recomendaciones y sus Enfoques
asfafaf

assafaf

## Estructura de los Datos y su Verificaciones
SPLAC es un indice financiero que consiste de las 40 empresas suramericanas tamano y liquidez mas alta. Estas companias varian a traves del tiempo, entonces las empresas seleccionadas fuerons las que estaban dentro de estas 40 empresas el 31 de Agosto, 2026. Reconociendo que no todas estas companias empezaron al mismo tiempo, se aplico un filtracion para seleccionar a la companias que estaban activos el 28 de Febrero del 2006. Esta fecha se escojio para poder incluir la crisis del 2008 dentro los datos. 

La informacion historica se descargaron de YFinance, con los siguiente detalles:
* Fechas (Post-Filtracion): 28/2/2006 - 28/8/2026
* Companias (Post-Filtracion): AMXB.MX, AXIA3.SA, BBAS3.SA, BIMBOA.MX, BSAC, CEMEXCPO.MX, CENCOSUD.SN, CIB, FEMSAUBD.MX, GCARSOA1.MX, GGB, ISA.CL, PAC, PBR, RENT3.SA, SCCO, SQM, VALE, VIV, WALMEX.MX, WEGE3.SA
* Indicadores: Cierre Ajustado, Cierre, Alto, Bajo, Apertura, y Volumen.


## Resumen Ejecutivo
### Resumen de Descubrimientos
Las estrategias de portafolio se evaluaron a traves las siguientes metricas financieras: retorno esperado (E(R)), Volatilidad (Std(R)), ratio Sharpe, Downside Deviation (DD), ratio Sortino, Max Drawdown (MD), Porcentaje de retornos positivos (% Pos.(R)), y ratio de Ganancias/Perdidas (P/L Ratio). Diferentes sectores de las empresas suramericanas tienen momentos donde son mas fuertes o mas debiles que los otros sectores. A pesar de esta variacion, el **sector Industrial** ha obtenido mas exitos y rendimientos que todos los demas, indicando que es un buen sector para hacer inversiones. 

Por otro lado, las estrategias desarrolladas con ML modelos ofrecen una alternativa competitiva a modelos tradicionales. En promedio, los retornos acumulados (al escalar volatilidad) con estrategias de ML obtuvieron **229.17%** de la inversion inicial, mientras que las estrategias sin ML obtuvieron un **172.23%**. Adicionalmente, los ratio Sharpe tambien confirmar esta diferencia, con las estrategias ML obteniendo un promedio de **0.707** mientras que las estrategias sin ML obtuvieron **0.566**.

Por lo contrario, las estragias sin ML superan a las estrategias ML en las siguientes categorias: Volatilidad (0.068 vs 0.075) y Porcentaje de retornos positivos (52.86% vs 51.83%). Diferentes metricas tienen diferentes niveles de importancias a cada usuario, senalando que la mejor estrategia depende en las preferencias del usuario. 


### Tendencia de los Descubrimientos
**Fuerza del Sector Industrial**: Teniendo una inversion fija en las empresas dentro el sector Industrial tiene **1.37 veces**(al escalar volatilidad) y **2.17 veces**(sin escalar volatilidad) mejores redimiento acumulado que los otros sectores: financiero, materiales, y consumo basico. 

**Impacto de COVID**: Todas las estrategias sintieron el impacto economico de la pandemia, la cual occurio entro el mes de **Marzo 2020**. A pesar de su influencia negativa, todas las estrategias tambien empezaron a resaltar y superar la pandemia empezando en **Abril 2020**. 

**Referencia del Benchmark**: El benchmark que se utilizo fue el indice SPLAC del sector financiero en SurAmerica. Las comparaciones revelan que **todas** las inversiones directas (en las 40 empresas utilizado por el SPLAC) resultan en mejores resultados que una inversion directa en el indice. 



## Detalles de las Hallazgos Insights 
### Ratio Sharpe de 0.966 en el Sector Industrial
Dentros las estrategias de asignacion fija, enfocandose en el sector industrial construyo el portafolio mas fuerte entre todos las estrategias sin ML. 

* **Ratio Sharpe**: esta estrategia obtuvo el ratio sharpe **mas alto de 0.966 y 0.929** (sin escalar la volatilidad).
* **Retorno Esperado**: al igual, esta estrategia obtiene los mejores retornos esperados annuales, con 0.184 y 0.055 (sin escalar la volatilidad)

### Impacto de COVID
La pandemia del COVID se sinitio en todos aspectos globales, incluyendo al sector financiero.

* **Todas las estrategia**, sea con o sin ML, pueden capturar los impactos drasticos del COVID 19
* Las estrategias **con volatilidad escalada** fueron **menos afectados** por estos impactos, al tener una caida mas mesurada y con menos perdidas.
* Todas las estrategias, incluyendo el benchmark, pudieron re-saltar sus perdidas al terminar la pandemia. 

### Debilidad del Benchmark
En benchmark indice SPLAC obtuvo los mejores resultados detro el primer año del rango de fechas, pero a traves del tiempo fue superado por todos los otros modelos. Considerando que **todos** los otros modelos le superan al indice, se identifica que este benchmark no tiene las mejores estrategias para manejar los movimientos de las 40 mejores empresas de suramerica. 


## Modelos, Predicciones y sus Impactos
Existen varias formas para crear un modelo que capture las dependencias temporales dentro un conjunto de datos. En este caso, dos estrategias principales se estudiaron: ventanas deslizantes y ventanas expansivas. Adicionalmente, diferentes combinaciones de las siguientes **metricas financieras**, de cada accion, se investigaron: Precio de Cierre (P), Retornos Logaritmicos (LR), TEMA (T), HLC3 (H), y OBV (O). 

### Modelos con Ventanas Deslizantes
En esta estrategia las ventanas de los datos de deslizaban anualmente, senalando que solo los datos dentro de dos anos se utilizaban para entranar el modelo. Se crearon tres diferentes modelos con esta estrategia. La arquitecturas eras iguales, pero los datos procesados tenian las siguientes diferecias: datos 1 usaban los indicadores P y RL; datos 2 usaban los indicadores T, H, y O; datos 3 usaban todos los inicadores. 



### Modelos con Ventanas Expansivas
En esta estrategia las ventanas se expandia anualmente para capturar todos los datos desde el comienzo (disponible) hasta el dia antes de cuando empieza los datos de pruebas. Similar a la otra estrategia, se crearon tres diferentes modelos con arquitecturas iguales pero diferentes indicadores en cada conjunto. 


### Resultados
Los modelos de las ventanas deslizantes obtuvieron un **promedio ratio Sharpe de 0.695 y 0.645**(al escalar la volatilidad) mientras los moelos de las ventanas expansivas tenian **0.809 y 769**(al escalar la volatilidad). En otras palabras, la segunda estrategia predice pesas (de las acciones) que resultan en portafolios con ratio Sharpes mas altos. 

Por lo contrario, se registra que en ambas estrategias los modelos que utilizaban todos los indicadores obtuvieron un ratio Sharpe **mas que 1.39 (ventanas deslizantes) y 1.19 (ventas expansivas) veces** de que todos los demas. Incluso, el modelo con ventana deslizante que utilizaba todos los indicadores obtuvo mejores resultados que los modelos de ventanas expansivas que no utilizaban todos los indicadores. 

Adicionalmente, el **modelo con ventanas expansivas** tiene mejores resultados al **no escalar la volatailidad** (con un ratios de 0.905 y 1.254). De lo contrario, el **modelo con ventanas deslizante** tiene los mejores resultados cuando **si se escala la volatilidad** (con ratios de 0.844 y 1.252).

## Recomendaciones
### Estrategia Adecuada le Corresponde al Usuario
Todas las estrategias presentadas se destacan con 10 diferentes metricas, pero ninguna estrategia es la mejor en todas estas metricas. Para desarrollar la mejor estrategia de recomienda identificar las caracteristicas y preferencias del usuario.

Las estrategias de **asignacion fija tiene los mejores ratios** (con y sin escalar la volatilidad), pero tiene uno de los mas MD con -0.436. Un usuario que intenta minimizar los asustes que tiene al enfrentarse con una caida de precios no va a preferir esta estrategia. 

Por otro lado, un usuario puede priorizar el ratio de la ganancias a perdidas ("P/L Ratio"), teniendo en cuenta qque es posible sacrificar un optimo ratio Sharpe. Existe diferentes combinaciones que se pueden formar al considerar las metas del usuario. 

### Enfoque en el Sector Industrial
El sector Industrial tiene una gran corrida, obteniendo alrededor de **250% retorno compuesto** en la inversion inicial. En corto plazo, se recomienda invertiendo una gran mayoria de los recursos en el sector industrial, siempre y cuando se diversifique con otras acciones. A largo plazo, se recomienda seguir investigando los movimientos del sector, considerando que un cambio del mercado pueda empezar a fortalecer otro sector. 



### ML con Mejores Resultados
Se registra que los ML modelos, en ambas estrategias de ventanilla (deslizante y expansiva), obtuvieron mejores rendimientos al utilizar **todos los indicadores**. Se recomienda coleccionar mas indicadores para mejorar las predicciones de los modelos.

Adicionalmente se nota que las **ventanas expansivas obtuvieron mejores resultados las ventanas deslizantes**. Este patron ayudaria a capturar cambios historicamente drasticos, senalando al modelo que cambie sus predicciones. En otra palabras, teniendo mas informacion historica de las acciones mejora los rendimientos del modelo.


## KPIs
### Ratio Sharpe
(Retoros Esperados)/(Volatilidad de Retornos)

Objetivo: aumentar el ratio Sharpe del portafolio actual por 67%. Para adquerir estos resultados se utilizaran los 4 mejores modelos para determinar los pesos del las acciones que tengan los mejores rendimientos sin aumentar la volatilidad. 

### Retorno Compuesto
\prod{i=1}^t (1 + retorno_simple_i)

Enfoque: mejorar el retorno compuesto del portafolio. Esto se modificar por si mismo al mejorar los rendimientos del portafolio. 

### Drawdown Maximo
(Pico Maximo - Valle Minima)/(Pico Maxima)

Enfoque: Esta metrica afecta el bienestar psicologico del usuario ya que es la bajada mas alta dentro la historia de los retornos. Aunque una bajada del pasado no se puede borrar, si se puede utilizar como una referencia para evitar. 

## Suposiciones y Avisos
Este analisis desrrollo las siguientes asunciones:

* El "Cierre Ajustado" del YFinance refleja el valor de las acciones que es utilizado por los inversionistas.
* Los datos del mercado bursatil no tienen estacionaridad y son naturalmente impredecibles. 



