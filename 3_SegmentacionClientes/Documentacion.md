# Table of Contents
1. [Contexto del Proyecto](#contexto-del-proyecto)
    * [Perspicacias, Recomendaciones y sus Enfoques](#perspicacias-recomendaciones-y-sus-enfoques)
2. [Estructura de los Datos y su Verificaciones](#estructura-de-los-datos-y-su-verificaciones)
3. [Resumen Ejecutivo](#resumen-ejecutivo)
    * [Resumen de Descubrimientos ](#resumen-de-descubrimientos)
    * [Tendencia de los Descubrimientos](#tendencia-de-los-descubrimientos)
4. [Detalles de las Perspicacias](#detalles-de-las-perspicacias)
    * Concentracion de 56.4% de Visitantes Internacionaless
    * Control Migratorio mas Populares
    * Los Meses con 21.7% de Turistas Anuales
    * Maximizando Ganancias y minimizando costos
5. [Modelos, Predicciones y sus Impactos](#modelos-predicciones-y-sus-impactos)
    * Los 6 tipos de visitantes internacionales
    * Predicciendo Movimiento Turistico 
6. [Recomendaciones](#recomendaciones)
    * Paquetes Promocionales Dirigidas al OCM
        - En cada OCM ver cuales son los turistas mas populares
    * Empleos de Corto- y Largo-Plazo
        - Febreo = menos empleados, julio = mas empleados
    * Aprovechando de Sitios sin Costo de Entradas
7. [KPIs](#kpis)
    * Aumento de clientes
        - (num_final - num_inicial)/ num_inicial
    * Ratio de Empleado por Turista
        - Num_Turs/ num_empleados
        - QUe sea consistente en al anio al cambiar cantidad de empleados por mes
    * Costo por viaje
        - C = entrada * num_turistas + gasolina *kms
8. [Suposiciones y Avisos](#suposiciones-y-avisos)



## Contexto del Proyecto

*** diff entre visitantes y touristas - pero ambos internacionales
asasfsaf

asfsafaf

### Perspicacias, Recomendaciones y sus Enfoques
asfafaf

assafaf

## Estructura de los Datos y su Verificaciones
assafasf

asfsagaga

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
### Concentracion de 56.4% de Visitantes Internacionales
Reconociendo que el Peru tiene una abundacia de sitios historicos y culturales, incluyendo una de las maravillas del mundo, se esperaba que haiga un porcentaje equilibrado de los ingresantes de todos los paises. El analisis demostro otras revelaciones.


* **Chile**: tiene 32.9% de **todos** los visitantes internacionales
* **Top 3 Paises**: ocupan 56.4% de visitantes internacionales
* **Top 10 Paises**: ocupan 82.5% de visitantes internacionales

Patrones Destacados:
* **Politica fronteriza impacta numero de visitantes internacionales**
    - 6 de los top 10 paises son Suramericanos y 5 de ellos son **vecinos directos** del Peru. Una gran mayoria de visitantes internacionales depende en las poltica al borde la fronter del Peru. 
* **Gran concentracion en 25 de los 198 paises**
    - El 95% de todos los visitantes internacionales provienen de los top 25, de los 198, paises. I.e., 177 paises no tienen un aporte significativo en los visitantes y no hay necesidad de tener un enfoque importante en ellos. 


### Control Migratorio entre los top 3 Paises
Considerando que Chile, EE.UU, y Ecuador ocupan mas de la mitad del total de visitantes, es importante considerara la Oficina de Control Migratorio (OCM) que utilizan para ingresar al Peru.

* El 79.47% de Chilenos entran por el OCM **Santa Rosa** en Tacna, Sur del Peru
* El 96.19% de Estado Unidenses usan el **Aeropuerto Internacional Jorge Chavez**
* El 67.54% de Ecuatorianos ingresan por el OCM **Cebaf-Tumbes** en Tumbes, Norte del Peru

Patrones Destacados:
* 81 OCMs ocupan solo un 4.36% de visitantes internacionales.
    - Existen 86 OCMs en Peru, con 81 de ellas agrupas bajo la misma variable 'OTRAS_OCM'. Solo 4.36% de visitantes internacionales entran por estas otras OCMs, implicando que no tienen un impacto significativo. 
    <h4 id="ocm"></h4>
* OCM y su pais vecino mas **cercano**
    - Cada OCM, excepto el Aeropuerto de Lima, tienen la mayoria de sus ingresantes viniendo del pais vecino mas cercano.
* Santa Rosa y Chilenos
    - Aunque **28.41%** de todos los visitantes internacionales vienen por OCM Santa Rosa, la mayoria de esos ingresantes vienen de Chile. Esto se deduce del hecho que 1/3 de todos los visitantes internacionales son chilenos, y 79.47% de ellos ingresan por Santa Rosa. 


### Los Meses con 21.7% de Turistas Anuales
Existen diferentes factores que afectan la cantidad de turistas en un mes, como el clima, eventos historicos, cambios polticos, etc. Algunos de estos factores tienen una temporada anual, impicando que la cantidad de turistas tambien tiene tendencias anuales. 

* Los meses de **Julio y Agosto** obtienen 21.7% de los turistas anuales.
* El mes de Febrero tiene la **menor** cantidad de turistas.
* **Machu Picchu**, incluyendo su ciudad, es el sitio mas visitado en todos los meses.

Patrones destacados:
* Tendencia estacional en todos los sitios turisticos
    - Existe una tendencia estacional en todos los sitios turisticos. En todos los sitios turisticos, Julio y Agosto reciben la mayor cantidad de turistas mientras Febrero tienen la menor cantidad. 
* Prominencia de Machu Picchu
    - Los top 5 sitios tienen algun enfoque con Machu Picchu. Algunos son servicios con destino a Machu Picchu, y otros son sitios en su alrededor. 


### 16 sitios gratis dentro 25 kms de Machu Picchu
Se esperaba que Machu Picchu, siendo una de las maravillas del mundo, es el sitio turistico mas popular. Tambien se encuentran una variedad de sitios turisticos cercanos con cero costo de ingreso, proveyendo una oportunidad que maximiza ganacias a una agencia turistica. 

* Existen 16 sitios **sin costo al ingresar** dentro 25 kilometeros de Machu Picchu.
* La mayoria de estos sitios se encuentran hacia el **Norte** y en rutas principales. 

## Modelos, Predicciones y sus Impactos
asfsafsa

### Modelo regresion
Prediciendo la cantidad de visitantes que espera dentro de un mes ayudaria en la optimizacion de recursos para un negocio. Dado el mes, departamento, y nombre del sitio turistico, el modelo de regresion predeci los numero de visitantes esperados en ese sitio turistico. 

Tres modelos candidatos se utilizaron con estos datos: Regresion lineal, regresion lasso, random forest. Con una metrica adecuada aplicada a todos los candidatos, el modelo regresion lineal obtuvo los mejores resultados. 




### Los 6 tipos de visitantes internacionales
KMeans es un algoritmo que agrupa puntos de datos en clusters, depediendo en su cercania entre uno al otro. Este proceso revelo los siguientes clusteres:

* Cluster 1: Los ingresantes por OCM Santa Rosa
* Cluster 2: Los visitantes Chilenos y Estadounidenses 
* Cluster 3: Los ingresantes por OCMs Aeropuerto internacional de Lima y Cebaf-Tumbres
* Cluster 4: Los ingresantes por otros OCMs no considerados
* Cluster 5: Los ingresantes por OCM Desaguadero
* Cluster 6: Los ingresantes por OCM Kasani

KMeans pricipalmente agrupo los visitantes internacionales por su OCM de entrada. Considerando que mayoria de visitantes de un OCM son ciudadanos del <a href="#ocm">pais mas cercano</a>, esta separacion es coherente con los datos. 

El segundo cluster se enfoca completamente en el pais de origen de los visitantes, especialmente de Chile y EE.UU. Reconociendo que estos dos paises forman [48.5% de todos los visitantes internacionales](#concentracion-de-564-de-visitantes-internacionales), se determina que este cluster es coherente con los datos. 

En practica, al llegar un visitante nuevo se puede determinar su similitud a otros visitantes -- como se puede utilizar estos clusteres para toma de decisiones

---- Targeted marketing? Ver recomendaciones


## Recomendaciones
Considerando las perspicacias y resultados de los modelos, se recomienda al **equipo de Marketing** de compania X los siguiente puntos:

### Targeted Marketing basado en Pais y OCM de Entrada
Los top 10 paises con visitantes internacionales ocupan 82.5% de **todos** los visitantes internacionales, con Chile obteniendo casi 1/3 de toda esa poblacion y 6 de los 10 paises siendo de Suramerica. Adicionalmente, se descubrio que a mayoria de ingresantes en cada OCM son del **vecino pais mas cercano**, creando un enlace entre punto de entrada y pais de origin. Este hecho fue fortalecido por los clusteres creados por el algoritmo KMeans, agrupando a todos los visitantes por el OCM de entrada. 

Por ende, se recomienda que el equipo de Marketing se enfoque en los siguiente targeted marketing:
* OCM Aeropuerto de Lima: Enfoque a un nivel internacional, sin enfocarse tanto en paises surmaericanos.
* OCM Santa Rosa: Enfoque en Chile.
* OCM Cebaf-Tumbes: Enfoque en Ecuador.
* OCM Desaguadero: Enfoque en Bolivia.
* Todos los otros OCMs: inversion minima y general. 

### Gestionar un Presupuesto que cambie Fluidamente por cada Mes
sdgsagag

### Incorporar Sitios sin Ingresos en Paquetes Promocionales para Machu Picchu
asgagsa


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





