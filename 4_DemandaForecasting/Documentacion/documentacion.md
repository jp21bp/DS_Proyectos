# Table of Contents
1. [Contexto del Proyecto](#contexto-del-proyecto)
    * [Perspicacias, Recomendaciones y sus Enfoques](#perspicacias-recomendaciones-y-sus-enfoques)
2. [Estructura de los Datos y su Verificaciones](#estructura-de-los-datos-y-su-verificaciones)
3. [Resumen Ejecutivo](#resumen-ejecutivo)
    * [Resumen de Descubrimientos ](#resumen-de-descubrimientos)
    * [Tendencia de los Descubrimientos](#tendencia-de-los-descubrimientos)
4. [Detalles de las Perspicacias](#detalles-de-las-perspicacias)
    * [ARPU picos en Marzo, Junio, Septiembre, y Diciembre](#arpu-picos-en-marzo-junio-septiembre-y-diciembre)
    * [Categoria 'Carniceria' Contribuye 27.13% de Ingresos Mensuales](#categoria-carniceria-contribuye-2713-de-ingresos-mensuales)
    * [Promedio Mensual de 53.12% de Productos Anuales Perdidos](#promedio-mensual-de-5312-de-productos-anuales-perdidos)
5. [Recomendaciones](#recomendaciones)
    * [Promociones de 'Carniceria' y 'Galletitas y Snack'](#1-promociones-de-carniceria-y-galletitas-y-snack)
    * [Disminuir almacen de todos los productos por 15%](#2-disminuir-almacen-de-todos-los-productos-por-15)
    * [Ofrecer descuentos en Febrero y Noviembre](#3-ofrecer-descuentos-en-febrero-y-noviembre)
6. [KPIs](#kpis)
    * [ARPU = Ingreso Promedio por Usuario](#1-arpu--ingreso-promedio-por-usuario)
    * [Porcentaje de Productos Perdidos](#2-porcentaje-de-productos-perdidos)
    * [Porcentage de Ingresos de Producto](#3-porcentage-de-ingresos-de-producto)
7. [Suposiciones y Avisos](#suposiciones-y-avisos)



## Contexto del Proyecto
Bodega Ña Maria es una microempresa en el interior de Paraguay y la microempresaria sostiene a su familia con las ventas y ganancias. La dueña ha notado que hay meses con más ingresos y otros con menos, pero le gustaría concretar los detalles sobre cuándo ocurren y cuál es la **diferencia entre los meses altos y bajos**. También menciona que generalmente termina botando la mayoría de sus productos, pero no sabe cuántos menos comprar sin que los clientes se queden sin productos. 

Paraguay es un país con un sector de ganadería fuerte, contribuyendo a su alto consumo de carnes. Maria reconoce que los productos de **carnes traen un alto porcentaje de ingresos**, y también le gustaría saber cómo los otros productos contribuyen a las ganancias mensuales. 

El siguiente análisis revela los meses con bajos ingresos y cómo crear promociones específicas durante esos meses para generar más ingresos. Adicionalmente, se destacan los productos con más pérdidas mensuales y cómo poder convertirlas en ganancias en vez de botarlas.

<br><br><br>

### Perspicacias, Recomendaciones y sus Enfoques
**ARPU y su tendencia cíclica**: La métrica ARPU (Promedio de Ingreso por Usuario) tiene un patrón de oscilación predecible en los meses del año. Cada 3 meses se encuentra con ARPU altos, seguidos por dos meses de bajo ARPU. El promedio ARPU de los meses altos es 41,940 Gs., mientras el promedio de los meses bajos es 39,384 Gs. Esta dinámica se utiliza en las recomendaciones para crear promociones en los meses con bajo ARPU.  


**Categorías con alta y baja contribución a los ingresos mensuales**: Existen 8 categorías, y cada producto disponible se encuentra en una de estas categorías. 'Carnicería' y 'Lácteos' tienen el impacto más grande en los ingresos mensuales, con un valor de 27.13% y 15.61%, respectivamente. De lo contrario, 'Conservas', 'Frutas y Verduras' y 'Galletitas y Snacks' tienen un impacto mínimo. Estas dinámicas se utilizan para crear combos de promociones sin asumir mayores pérdidas. 


**Mayor pérdida de productos almacenados**: un 53.12% de los productos almacenados se desperdician anualmente. La categoría de 'Galletitas y Snack' tiene las mayores pérdidas anuales, con un 68.22% del almacenamiento perdido. De lo contrario, la categoría 'Congelados' tiene un  Este hecho se puede considerar en la creación de promociones para disminuir la cantidad de productos que se pierden sin venta. 

<br><br>
Las queries de SQL se encuentran AQUÍ

El análisis de datos se encuentra AQUÍ



## Estructura de los Datos y su Verificaciones
4 tablas dentro de una base de datos se utilizaron para realizar este análisis; sus formatos CSVs se pueden encontrar AQUÍ. Los componentes de cada tabla son los siguientes:

1. Tabla: categorias - llaves: id_categoria (primary), categoria (text), descripcion (text)
2. Tabla: clientes - llaves: id_cliente (primary), nombre (text), apellido (text), email (text), fecha_registro (text)
3. Tabla: productos - llaves: id_producto (primary), nombre (text), categoria (text), precio (smallint), stock (smallint)
4. Tabla: ventas - llaves: id_venta (primary), fecha (text), id_cliente (foreign), id_producto (foreign), cantidad (smallint)


## Resumen Ejecutivo

### Resumen de Descubrimientos
Esta microempresa de Paraguay es una representación de las bodegas familiares comunes en el interior del país. Debido a la escasez de electricidad, muchos de sus productos de ventas se pierden a través del año. Esto conlleva una realidad donde la mayoría de los productos vendidos se desperdician. Adicionalmente, la cultura Paraguaya influye en la compra de los clientes, donde una reducción en abril se atribuye a Semana Santa y las fiestas del fin del año contribuyen a un aumento en ARPU. Estas tradiciones también afectan los ingresos generales de la microempresa. Estos patrones se pueden analizar para crear cambios accionables que proveen mejoramientos a los KPIs de la empresa. 

### Tendencia de los Descubrimientos
**Meses con menos compras por clientes** : Los 4 meses de abril, agosto y octubre tienen un ARPU mucho menos del promedio, pero la microempresa tiene un promedio de cliente, implicando que los clientes compran menos cantidades de productos. 
**Una gran mayoría de productos se pierden**: un 53.12% de productos almacenados se pierden anualmente. Se detalla que la categoria 'Galletitas y Snacks' y el mes de diciembre tienen las mayores pérdidas a través del año. 
**'Carniceria' y 'Lacetos' aportan los más ingresos mensuales**: Estas categorías obtienen los más ingresos de sus ventas, produciendo un promedio de 27.13% y 15.61% del ingreso mensual, respectivamente. De lo contrario, 'Conservas', 'Frutas y Verduras', y 'Galletitas y Snack' son las categorías con menos aportes. 

## Detalles de las Perspicacias 
### ARPU picos en marzo, junio, septiembre y Diciembre
La métrica ARPU mide el ingreso promedio por cliente, y se notan algunas tendencias en su análisis mensual.

* **Junio tiene un aumento en la cantidad de clientes**: Este hecho señala un aumento en las transacciones y ventas del mes. Adicionalmente, se registra un aumento en el ARPU, el cual se refleja en el máximo ingreso mensual dentro de junio. 

* **ARPU picos en Mar, Sep y Dic**: Estos tres meses también tiene un aumento en su ARPU mensual, pero no se debe a un aumento en la cantidad de clientes como ocurrió en junio. De lo contrario, estos meses tienen una cantidad promedio de clientes, la cual significa que cada cliente compra más productos que lo normal. 

* **Octubre: cantidad vs. ARPU**: Aunque octubre tiene una cantidad de clientes un poco sobre el promedio, se registra una reducción en el ARPU. Esta combinación demuestra que octubre tiene más clientes que hacen menos compras. 

![ARPUs por Mes](arpu.png)

<br><br><br>

### Categoría 'Carniceria' Contribuye 27.13% de Ingresos Mensuales
De las 8 categorías de productos, existe un gran contraste entre los productos que generan más ingresos a la microempresa. 

* **27.13% de Ingresos Mesuales Provienen de la Carniceria**: Los productos de la carnicería consistentemente proveen la mayoría de los ingresos mensuales. Esto demuestra que Paraguay es un país que tiene la carne dentro de su dieta cotidiana. 

* **Conservas vs Congelados**: Las conservas consisten en productos enlatados o envasados, pero los productos congelados tienen un promedio más alto. Este hecho implica que los Paraguayos prefieren comprar comida visible y no dentro de una lata, aunque la comida no sea fresca.

* **Lácteos son los segundos contribuyentes a los ingresos mensuales**: Integrando esta información con el alto consumo de carnes, se deduce que Paraguay es un país con un sector grande de ganadería, donde las vacas pueden proveer a las categorías de carnicería y lácteos.


![Categorias e Ingresos Mensuales](categorias_ingresos.png)

<br><br><br>

### Promedio Mensual de 53.12% de Productos Anuales Perdidos
Reconociendo las limitaciones eléctricas en pueblos de Paraguay, se esperaba que la mayoría de productos se desperdiciaran por falta de refrigeración. El porcentaje de los productos que se pierden reveló datos alarmantes.

* **53.12% de Pérdidas mensuales**: Un promedio de 53.12% de los productos almacenados se pierden anualmente al no venderse.

* **El Mes de Febrero tiene las más pérdidas**: Febrero pierde 58.1% de sus productos almacenados al no venderlos. 

* **'Galletitas y Snacks' son los productos con más pérdidas**: Esta categoria pierde 68.22% de sus productos a través de todo el año. Esta cifra se empeora en febrero y diciembre, con pérdidas de 80.06% y 83.89%, respectivamente.

![Promedio de Perdidas](perdidas.png)

<br><br><br>

## Recomendaciones
### 1. Promociones de 'Carniceria' y 'Galletitas y Snack'
'Carniceria' era la categoría con más ingresos mensuales (27.13% de ingresos) y la tercera más popular (con 47.9% de pérdidas anuales). De lo contrario, 'Galletitas y Snack' es la categoría con más pérdidas anuales (de 68.22% de su almacén). Considerando que las 'Galletitas y Snack' tienen una pérdida de más del 70% en febrero, junio, noviembre y diciembre, esta promoción se puede activar durante estos meses para reducir los productos perdidos y aumentar la venta de 'Carniceria'. 

<br><br><br>

### 2. Disminuir almacén de todos los productos por 15%
Considerando que ninguno de los productos llegó al punto de agotamiento en ninguno de los meses, se puede deducir que todos los productos pueden disminuir sus pérdidas al reducir su almacenamiento. Adicionalmente, el punto mínimo de todas las pérdidas era un 19.27%, en la categoría 'Congelados' en el mes de noviembre. Por ende, una reducción de 15% no resultaría en agotamiento de esta categoría. Todas las otras pérdidas no bajan de 24.31%, a través de todas las categorías y todos los meses. 

<br><br><br>

### 3. Ofrecer descuentos en febrero y noviembre
Estos meses obtuvieron una menor cantidad de clientes de lo promedio mensual, significando que los clientes hacen menos compras durante estos meses. Aunque la razón detrás de esta reducción es desconocida, la microempresa puede crear una iniciativa para atraer más clientes durante estos meses. Una forma de crear motivación es a través de descuentos generales en sus productos, lo cual atraería a más clientes para que ellos no pierdan esa oportunidad.



## KPIs
### 1. ARPU = Ingreso Promedio por Usuario
Total Ingreso / Número de Clientes

Objetivo: Aumentar el ARPU promedio de 40,314 Gs. a 45,000 Gs. mensuales. 

<br><br><br>

### 2. Porcentaje de Productos Perdidos
((Stock Disponible - Productos Vendidos)/Stock Disponible) * 100

Objetivo: Para disminuir la cantidad de productos desperdiciados, la meta será disminuir la pérdida de 53.12% anuales de todos los productos a 45%. 
<br><br><br>

### 3. Porcentaje de Ingresos de producto
(Ingresos de un Producto/ Ingresos Totales) * 100

Enfoque: Aumentar la venta de la categoría que genere más ingresos de un promedio de 27.13% a 30%. Esto se logrará a través de promociones con otras categorías que tengan un alto desperdicio.

## Suposiciones y Avisos
Este análisis tiene las siguientes suposiciones:

* Para mantener confidencialidad, estos datos son una combinación de datos encontrados en línea (de Argentina) y datos de clientes personales (de Paraguay).
* Para simplificar el análisis, los costos y las devoluciones de productos no se consideran. 
* La cantidad de almacén en cada producto es el valor anual, el cual se divide equitativamente en cada mes.
* Los productos que no se venden al fin del mes se desperdician. 
