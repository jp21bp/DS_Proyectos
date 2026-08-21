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
    * Porcentaje de 
    * segundo
    * tercero
8. [Suposiciones y Avisos](#suposiciones-y-avisos)



## Contexto del Proyecto
asasfsaf

asfsafaf

### Perspicacias, Recomendaciones y sus Enfoques
**ARPU y su tendencia ciclica**: la metrica ARPU (Promedio de Ingreso por Usuario) tiene un patron de oscilacion predecible en los meses del anio. Cada 3 meses se encuentra con ARPUs altos, seguidos por dos meses de bajo ARPU. El promedio ARPU de los meses altos es 41,940 Gs., mientras el promedio de los meses bajos es 39,384 Gs. Esta dinamica se utiliza en las recomendaciones para crear promociones en los meses con bajos ARPUs.  


**Categorias con alta y baja contribucion a los ingresos mensuales**: Existen 8 categorias, y cada producto disponible se encuentra en una de estas categorias. 'Carniceria' y 'Lacteos' tiene el impacto mas grande a los ingresos mensuales, con un valor de 27.13% y 15.61% respetivamente. De lo contrario, 'Conservas', 'Frutas y Verduras', y 'Galletitas y Snacks' tienen un imapcto minimo. Estas dinamicas se utilizan para crear combos de promociones sin asumir mayores perdidas. 


**Mayor perdidad de productos almacenados**: un 53.12% de los productos almacenados se desperdician anualmente. La categoria de 'Galletitas y Snack' tienen la mayores perdidas anuales, con un 68.22% del almacenamiento perdido. De lo contrario, la categoria 'Congelados' tiene un  Este hecho se puede considerar en la creacion de promociones para disminuir la cantidad de productos que se pierden sin venta. 



## Estructura de los Datos y su Verificaciones
4 tables dentro una base de datos se utilizo para realizar este analisis, sus formatos CSVs se pueden encontrar AQUI. Los componentes de cada tabla son los siguientes:

1. Tabla: categorias - llaves: id_categoria (primary), categoria (text), descripcion (text)
2. Tabla: clientes - llaves: id_cliente (primary), nombre (text), appelido (text), email (text), fecha_registro (text)
3. Tabla: productos - llaves: id_producto (primary), nombre (text), categoria (text), precio (smallint), stock (smallint)
4. Tabla: ventas - llaves: id_venta (primary), fecha (text), id_cliente (foreign), id_producto (foreign), cantidad (smallint)


## Resumen Ejecutivo

### Resumen de Descubrimientos
Esta microempresa de Paraguay es una representacion de las boedgas familiares comunes en el interior del pais. Debido a la escasez de electricidad, muchos de sus productos de ventas se pierden a traves del anio. Esto conlleva a una realidad donde la mayoria de los productos vendidos se desperdician. Adicionalmente, la cultura Paraguaya influye en la compra de los clientes, donde una reduccion en Abril se atribuye a Semana y las fiestas del fin del anio contribuyen un aumento en ARPU. Estas tradiciones tambien afectan los ingresos generales de la microempresa. Estos patrones se pueden analizar para crear cambios accionables que proveen mejoramientos a los KPIs de la empresa. 

### Tendencia de los Descubrimientos
**Meses con menos compras por clientes** : Los 4 meses de Abril, Agosto, y Octubre tienen un ARPU mucho menos del promedio, pero la microempresa tienen un promedio de cliente, implicando que los clientes compran menos cantidades de productos. 
**Una gran mayoria de productos se pierden**: un 53.12% de productos almacenados se pierden anualmente. Se detalla que la categoria 'Galletitas y Snacks' y el mes de Diciembre tienen las mas peridades a traves del anio. 
**'Carniceria' y 'Lacetos' aportan los mas ingresos mensuales**: Estas categorias obtienen los mas ingresos de sus ventas, produciendo un promedio de 27.13% y 15.61% del ingreso mensual, resptivamente. De lo contrario, 'Conservas', 'Frutas y Verduras', y 'Galletitas y Snack' son las categorias con menos aportes. 

## Detalles de las Perspicacias 
### ARPU picos en Marzo, Junio, Septiembre, y Diciembre
La metrica ARPU mide el ingreso promedio por cliente, y se notan algunas tendencias en su analisis mensual.

* **Junio tiene un aumento en la cantidad de clientes**: Este hecho señala un aumento en las transacciones y ventas del mes. Adicionalmente se registra un aumento en el ARPU, la cual se refleja en el max ingreso mensual dentro Junio. 

* **ARPU picos en Mar, Sep, y Dic**: Estos tres meses tambien tiene un aumento en su ARPU mensual, pero no se debe a un aumento en la cantidad de clientes como occurio en Junio. De lo contrario, estos meses tienen una cantidad promedio de clientes, la cual significa que cada cliente compra mas productos que lo normal. 

* **Octubre: cantidad vs ARPU**: Aunque Octubre tiene una cantidad de clientes un poco sobre el promedio, se registra una reduccion en el ARPU. Esta combinacion demuestra que Octubre tiene mas clientes quienes hacen menos compras. 


### Categoria 'Carniceria' Contribuye 27.13% de Ingresos Mensuales
De las 8 categorias de productos, existen un gran constraste entre los productos que generan mas ingreso a la micro-empresa. 

* **27.13% de Ingresos Mesuales Provienen de la Carniceria**: Productos de la cariniceria consistentemente proveen la mayoria de los ingresos mensuales. Esto demuestra que Paraguay es un pais que tiene la carne dentro su dieta cotidiana. 

* **Conservas vs Congelados**: Las conservas consiste de productos enlatados o envasados, pero los productos congelados tiene un promedio mas alto. Este hecho implica que los Paraguayos prefieren comprar comida visible y no dentro una lata, aunque la comida no sea fresca.

* **Lacteos son los segundos contribuyentes a los ingresos mensuales**: Integrando esta informacion con el alto consumo de carnes se deduce que Paraguay es un pais con un sector grande de ganaderia, donde la vacas pueden proveen a las categorias de carniceria e lacteos.


### Promedio Mensual de 53.12% de Productos Anuales Perdidos
Reconociendo las limitaciones electricas en pueblos de Paraguya, se esperaba que la mayoria de productos se desperdicien por falta de refrigeracion. El porcentaje de los productos que se pierden revelo datos alarmantes.

* **53.12% de Perdidas mensuales**: Un promedio de 53.12% de los productos almacenados se pierden anualmente al no venderse.

* **El Mes de Febrero tiene la mas perdidas**: Febrero pierde 58.1% de sus productos almacenados al no venderlos. 

* **'Galletitas y Snacks' son los productos con mas perdidas**: Esta categoria pierde 68.22% de sus productos a traves todo el anio. Esta cifra se empeora en Febrero y Diciembre, con perdidas de 80.06% y 83.89% respetivamente.


## Recomendaciones
### 1. Promociones de 'Carniceria' y 'Galletitas y Snack'
'Carniceria' era la categoria con mas ingresos mensuales (27.13% de ingresos) y la tercera mas popular (con 47.9% de perdidas anuales). De lo contrario, 'Galletitas y Snack' es la categoria con mas perdidas anuales (de 68.22% de su almacen). Considerando que las 'Galletitas y Snack' tiene una perdidad mas de 70% en Febrero, Junio, Noviembre, y Diciembre, esta promocion se puede activar durante estos meses para reduccir los productos perdidos y aumentar la venta de 'Carniceria'. 


### 2. Disminuir almacen de todos los productos por 15%
Considerando que ninguno de los productos llego al punto de agotamiento en ninguno de los meses, se puede deducir que todos los productos pueden dismiuir su perdidas al reducir su almacenamiento. Adicionalmente, el punto minimo de todas las peridads era un 19.27%, en la categoria 'Congelados' en el mes de Noviembre. Por ende, una reduccion de 15% no resultaria en agotamiento de esta categoria. Todas las otras perdidas no bajan de 24.31%, a traves todas las categorias y todos los meses. 

### 1. Ofrecer descuentos en Febrero y Noviembre
Estos meses obtuvieron una menor cantidad de clientes de lo promedio mensual, significando que los clientes hacen menos compras durante estos meses. Aunque la razon detras esta reduccion es desconocida, la micro empresa puede crear una iniciativa para atraer mas clientes durante estos meses. Una forma de crear motivacion es a traves de descuentos generales en sus productos, la cual atraeria a mas clientes para que ellos no pierden de esa oportunidad.



## KPIs
### 1. ARPU = Ingreso Promedio por Usuario
Total Ingreso / Numero de Clientes

Objetivo: aumentar el ARPU promedio de 40,314 Gs. a 45,000 Gs. mensuales. 


### 2. Porcentaje de Productos Perdidos
((Stock Disponible - Productos Vendidos)/Stock Disponible) * 100

Objetivo: Para disminuir la cantidad de productos desperdiciados, la meta sera de disminuir la perdidad de 53.12% anuales de todos los productos a 45%. 


### 3. Porcentage de Ingresos de Producto
(Ingresos de un Product/ Ingresos Totales) * 100

Enfoque: Aumentar la venta de la categoria que generen mas ingresos de un promedio de 27.13% a 30%. Esto se lograra a traves promociones con otras categoria que tengan un alto desperidicio

## Suposiciones y Avisos
dgonin


