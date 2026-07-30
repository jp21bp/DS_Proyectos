# DS3: Segmentacion de Clientes

Este proyecto consiste en identificando las diferentes segmentacion de clientes touristas en Peru

Buen segmentacion:
https://github.com/martabuaf/Customer-Segmentation/blob/main/clustering_methods.py


## Pasos del Proyecto

### Paso 1 - Formulacion del Problema

Problema Asignado: El departamento de tourismo en el Peru quiere entender la diversidad de touristas para disenar estrategias de marketing que mejoren las experiencias y la geston de presupesto. Actualmente, el marketing es general y amplio, resultando en oportunidades perdidas al no considerar las peculiardades de diferentes touristas. Al segmentar los touristas se busca crear perfiles de visitores distinctos para ayudar en la toma de decisiones.


Analisis:
* Contexto del Negocio:
    - Contexto: el marketing es general y no personalizado
    - Problema: no existe perfiles distinctos para los diferente tipos de touristas
    - Impacto: el departamento pierde dinero y oportunidades
    - Stakeholders: Peru como pais y su economia
    - Antecedentes: ------
* Objetivo del Proyecto:
    - Objetivo: Se quiere lograr una segmentacion especifica de los touristas para crear perfiles distinctos y hacer targeted marketing
    - Tipo: Clustering
* Scope:
    - Dentro:
        * Enfoque de touristas hacia el Peru
    - Afuera:
        * Tourismo nacional: Peruanos visitando otras partes del Peru
* Disponibilidad de Datos:
    - Dimesionalidades:
        * Registros/instances = Touristas
            - Necesario para hacer cluster de touristas
        * Variables/feats = cualquiera
    - Sitios:
        * https://www.datosabiertos.gob.pe/group/ministerio-de-comercio-exterior-y-turismo
        * https://datosturismo.mincetur.gob.pe/appdatosTurismo/index.html
        * https://horaciochacon.github.io/peruopen/
        * https://datosturismo.mincetur.gob.pe/
* Restricciones:
    - Ninguna limitaciones considerando que los datos son publicos
* Metricas de Exito:
    - Perfiles distinctos para diferentes touristas
    - Recomendaciones para: campanas de marketing, productos para ofrecer, gestion de recursos.


Transformacion:
1. Frame:
    - Problema de negocio: Proveer recomendaciones para campanas de market que optimicen los ingresos a traves de la creacion de perfiles de touristas distinctos
    - Formulacion:
        * S: Mejorar los ingresos de marketing por un x% al implementar targeted campanas de marketing
        * M: Cambio de x% en el pre-test y post-test
        * A: Si, considerando acesbilidad a los datos necesarios
        * R: Relevante al caso
        * T: Este aumento se tiene que refeleccionar dentro de 3 meses despues de targeted marketing campanas
2. Problemas matematicos
    - Ganacias = Ingresos $R$ - Costos $C$
    - $R = \sum_{k=1}^K R_k$
    - $C = \sum_{k=1}^K C_k$
    - $R_k = N_k \cdot p_k \cdot r_k$
    - $C_k = N_k \cdot c_k$
3. Convertir problemas
    - Segmentos $K$ y tamano de cada segmento $N_k$:
        * Utilizar KMeans para encontrar $K$ segmentos
        * Data:
    - Probabilidad que un tourista en segmento $k$ interactue con el marketing $p_k$: 
        * Binary classificacion sin signmoid activacion de historical campaign response rates
        * Data: 
    - Ingreso de campana efectiva $r_k$: 
        * Regresion de trasaction data
        * Data:
    - Costo del marketing $c_k$:
        * Regresion de marketing spending records
        * Data:


Latex:
* Variables Generales:
    - $K$ = numero de clusters/segmentos de touristas
    - $N_k$ = numero de touristas dentro segmento $k$
    - $p_k$ = probabilidad que un tourista dentro segmente $k$ responda positivamente a una campana de marketing
    - $r_k$ = ingreso promedio de un tourista en segmento $k$ si responden al marketing
    - $c_k$ = costo de marketing para un tourista en segmento $k$
* Variable de Decision:
$$ 
y_k = 
\begin{cases} 
1 & \text{target segment } k \\
0 & \text{otherwise}
\end{cases}
$$
* Funcion de Ingresos (del segmento $k$): $R_k = N_k \cdot p_k \cdot r_k$
* Funcion de Costos (del segmento $k$): $C_k = N_k \cdot c_k$
* Objetivo de Optimizacion: Maximizar las ganancias
$$
\max_{y_k \in {0,1}} \sum_{k=1}^K y_k \cdot \left[ N_k \cdot p_k \cdot r_k - N_k \cdot c_k \right]
$$
* Restricciones de Presupuesto: $ \sum_{k=1}^K y_k \cdot N_k \cdot c_k \leq B$
* Workflow:
    1. Segmentacion
        - Utilizar KMeans para encontrar $K$ segmentos
    2. Estimacion de Parametros (valores iguales para todos segmentos $k$):
        - $p_k$: de historical campaign response rates
            * Idea: despues de avergiuar k segments en 2025, hacer un trend histrico y ver como cada segmento aumento a traves de ano
                - Ej: 2023 = 1.0 M y 2024 = 1.2M => p_k = (1.2-1.0)/1.0 = 0.2
        - $r_k$: de trasaction data
            * Idea: precio de cada sitio?
        - $c_k$: marketing spending records
            * Idea: costo de mantenimiento de cada sitio?
    3. Optimizacion
        - Resolver el binary integer programming problema para ver cual de los segmentos hacer targeted marketing
    4. Prediccion:
        - Utilizar modelos de clasificacion para mejorar $p_k$ para campanas de marketing en el futuro
    

Antecedentes:
* [Tourist Profiles](https://thetourism.institute/understanding-tourism-markets/tourist-profiles-guide-profiling-tourism-markets/)
    - "Understanding the originating market means understanding why someone in Frankfurt or Dhaka or Sydney would choose to spend their hard-earned holiday in your city. That motivation is shaped by their **economy, culture, climate, holiday calendar, and even their political relationship with the host country**."
    - Variables importantes: 
        * Tiempo de llegada (horas y fechas)
        * Duracion de visita
        * Informacion demografica
        * Proposito de la visita
        * Seasnality and travel patterns
        * Spending and economic contribution
        * Sureys de satisfaccion