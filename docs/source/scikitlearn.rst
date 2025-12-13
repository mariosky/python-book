.. role:: python(code)
   :language: python

.. _scikitlearn: 

Aprendizaje Automático con Scikit-learn
========================================

En este capítulo nos vamos a concentrar en la librería de código abierto
``scikit-learn``, una de las herramientas más utilizadas en Python para la
implementación de algoritmos de **Aprendizaje Automático**
(*machine learning*, *ML*), uno de los campos de las ciencias computacionales
con mayor impacto en la actualidad.

El aprendizaje automático es un área amplia y activa de investigación que,
por su profundidad teórica y variedad de enfoques, normalmente requiere uno o
varios cursos especializados. En este capítulo **no se pretende cubrir los
fundamentos matemáticos ni teóricos del área**, sino que se asume que el lector
cuenta con conocimientos básicos previos en temas como Minería de Datos,
Aprendizaje Automático o Inteligencia Artificial.

El enfoque principal será **la aplicación práctica de la librería
``scikit-learn`` en Python**, mostrando cómo utilizar sus componentes para
preprocesar los datos, entrenar, evaluar y utilizar modelos de aprendizaje
automático de manera eficiente. Pondremos especial atención en el flujo de
trabajo típico que sigue esta librería, así como en su integración con
herramientas vistas en capítulos anteriores, como NumPy y Pandas.

A lo largo del capítulo se presentarán ejemplos claros y reproducibles que
permitan al lector comprender cómo llevar modelos de aprendizaje automático
desde los datos hasta su uso en aplicaciones reales, haciendo énfasis en la
interpretación de resultados y en las buenas prácticas de uso de la librería.

El flujo de trabajo del Aprendizaje Automático
----------------------------------------------

Los algoritmos de aprendizaje automático forman parte de un proceso más amplio
que requiere un flujo de trabajo cuyo objetivo general es **extraer
conocimiento a partir de los datos**. En este proceso pueden intervenir muchas
técnicas, como aprendizaje automático, reconocimiento de patrones,
computación inteligente, estadística, procesamiento de lenguaje natural,
visualización de datos e ingeniería de software, entre otras.

Este flujo de trabajo tiene su origen en el proceso de **Extracción de
Conocimiento de Bases de Datos** (*Knowledge Discovery in Databases*, *KDD*).

Aunque el término *KDD* se utiliza con menor frecuencia en la literatura
industrial actual, el flujo de trabajo que propone sigue siendo la base
conceptual de los procesos modernos de ciencia de datos y aprendizaje
automático, incluidos los flujos de trabajo implementados con librerías
como ``scikit-learn``.

Veamos en qué consiste este proceso, según el esquema propuesto por
Brachman y Anand:

1. Como primer paso se debe *identificar el objetivo* del proceso de KDD.
   Por ejemplo, un proveedor de telefonía móvil podría estar interesado en
   identificar a aquellos clientes que no renovarán su contrato y se irán con
   la competencia. A esto se le conoce como la **tasa de cancelación de
   clientes** (en inglés *churn rate* o *attrition rate*), la cual es crucial
   para estimar el desempeño de la empresa.

2. El siguiente paso es *seleccionar y recolectar* los datos necesarios para
   el proceso. En nuestro ejemplo, podríamos requerir el historial de pagos de
   los clientes, datos sobre quejas y llamadas a soporte, servicios adicionales
   contratados o cancelados, entre otros. Esta información puede estar
   distribuida en diferentes bases de datos. También se pueden incluir datos
   recolectados por medio de sensores o sistemas externos, como lecturas de
   GPS, caídas de conexión o el número de aplicaciones instaladas por el
   cliente.

3. Es necesario *preprocesar* los datos para eliminar valores erróneos,
   datos faltantes, inconsistencias, cambios de formato, entre otros
   problemas. Este suele ser un proceso complejo y que puede demandar una
   cantidad considerable de recursos.

4. Dependiendo de los objetivos, los datos deben *transformarse* para
   facilitar su procesamiento. Por ejemplo, un documento de texto debe
   transformarse en una representación vectorial para permitir su análisis.
   De manera similar, una imagen puede convertirse en una representación
   simplificada que conserve sus características esenciales. En muchos casos
   también es necesario eliminar atributos que no aportan información
   relevante. Siguiendo nuestro ejemplo, podríamos descubrir que el número
   telefónico no es útil para distinguir el comportamiento del cliente,
   mientras que la marca y el modelo del dispositivo sí lo son.

5. En este paso se *selecciona la tarea de minería de datos* adecuada de
   acuerdo con el objetivo del proceso de KDD, por ejemplo clasificación,
   regresión o agrupamiento.

6. Se realiza un *análisis exploratorio*, en el cual se experimenta con
   distintos algoritmos de minería de datos o aprendizaje automático. Al
   seleccionar los algoritmos se deben considerar los tipos de datos
   disponibles, ya que algunos modelos no son adecuados para variables
   categóricas. También es necesario ajustar parámetros, evaluar el desempeño
   y comparar distintos enfoques.

7. En este paso se lleva a cabo el *aprendizaje automático* propiamente
   dicho, utilizando el o los algoritmos seleccionados anteriormente.

Este proceso produce los llamados *patrones ocultos*, los cuales describen la
estructura subyacente de los datos. Siguiendo nuestro ejemplo, el resultado
podría ser un conjunto de reglas que permitan decidir si un cliente cancelará
su suscripción. Una regla podría ser:

.. code-block:: bash

   SI el cliente tiene un promedio mayor a 7 días de retraso
      AND su promedio mensual de llamadas es menor que 10
   ENTONCES:
      el cliente cancelará el servicio

Los patrones son, en esencia, **modelos** ajustados a los datos. Estos modelos
no siempre se expresan en una forma directamente interpretable por los
humanos. Por ejemplo, el resultado de un algoritmo de agrupamiento puede ser
simplemente un conjunto de grupos de clientes que posteriormente deben ser
analizados e interpretados.

¿Qué es scikit-learn y para qué sirve?
--------------------------------------

Precisamente ``scikit-learn`` incluye herramientas para cada uno de los pasos
descritos anteriormente, lo que la convierte en un **ecosistema completo**
para implementar el flujo de trabajo del aprendizaje automático en Python.

Aunque es muy útil para proyectos de tamaño mediano, no incluye capacidades
para el procesamiento de datos masivos como las utilizadas en entornos de
*Big Data*, ni librerías para *deep learning* con aceleración en múltiples GPUs,
como ``PyTorch`` o ``TensorFlow``. Sin embargo, resulta muy atractiva para
abordar la mayoría de los problemas de aprendizaje automático convencional.

Sobre todo, ``scikit-learn`` es ideal para aprender los principios del
aprendizaje automático, ya que permite probar conceptos de manera rápida
utilizando una gran variedad de algoritmos listos para usarse. Además, la
librería está diseñada para ser **extensible**: los modelos y componentes que
se utilizan a lo largo del capítulo siguen una estructura bien definida, lo
que permite al usuario crear sus propios modelos y componentes de
preprocesamiento cuando las necesidades del problema así lo requieran.

En capítulos anteriores ya hemos trabajado con herramientas fundamentales como
NumPy, programación funcional y estructuras de datos, las cuales forman parte
del ecosistema sobre el que se construye ``scikit-learn``.

El flujo de trabajo básico en scikit-learn
------------------------------------------

En este capítulo haremos un recorrido por la librería siguiendo el flujo de
trabajo del aprendizaje automático, utilizando ejemplos con distintos
*datasets*, con el objetivo de mostrar de manera práctica cómo integrar las
diferentes etapas del proceso.

Comenzaremos por el **núcleo del proceso**, asumiendo un escenario ideal en el
que ya se ha realizado gran parte del trabajo previo. En este punto contamos
con datos preprocesados y limpios, listos para ser utilizados en el proceso de
aprendizaje automático. Bajo estas condiciones, el flujo de trabajo puede
simplificarse a los siguientes pasos básicos:

1. Cargar los datos.
2. Entrenar un modelo utilizando parámetros básicos.
3. Evaluar qué tan bien funciona el modelo antes de utilizarlo en un problema
   real.

Este es el caso más simple y directo. Más adelante iremos incorporando pasos
adicionales y desglosando con mayor detalle los componentes internos del
proceso, tal como ocurre en entornos reales de desarrollo y de investigación.

Clasificando pingüinos
----------------------

Para este primer ejemplo vamos a utilizar el *dataset* de los pingüinos, un
conjunto de datos sencillo y ampliamente utilizado con fines educativos en
aprendizaje automático.

El objetivo será **clasificar distintas especies de pingüinos** a partir de
características físicas medidas en cada individuo, como el tamaño del pico,
la longitud de las aletas y el peso corporal. Este tipo de problema es un
ejemplo clásico de **clasificación supervisada**, donde contamos con ejemplos
etiquetados que nos permiten entrenar y evaluar un modelo.

Este *dataset* es ideal para comenzar porque:

- Tiene un tamaño manejable.
- Contiene variables numéricas fáciles de interpretar.
- Permite visualizar claramente el flujo completo de trabajo del aprendizaje automático sin distraernos con detalles innecesarios.

A lo largo de esta sección seguiremos los pasos básicos descritos
anteriormente: cargar los datos, entrenar un modelo sencillo y evaluar su
desempeño antes de utilizarlo en un escenario real.

.. note::

   Este *dataset* es conceptualmente muy similar al clásico *dataset* de
   **Iris**, ampliamente utilizado en ejemplos introductorios de aprendizaje
   automático. En ambos casos se trata de un problema de **clasificación
   supervisada** con un número reducido de características numéricas y clases
   bien definidas. La principal diferencia es que el *dataset* de pingüinos
   resulta más cercano a problemas reales y evita algunas de las limitaciones
   conocidas del *dataset* de Iris.

Cargamos el *dataset*
~~~~~~~~~~~~~~~~~~~~

El *dataset* se encuentra en el repositorio público de GitHub de
`Allison Horst <https://github.com/allisonhorst/palmerpenguins>`_ y consiste en
dos archivos que contienen datos recolectados de **344 pingüinos** encontrados
en tres islas del Archipiélago Palmer, en la Antártida.

Los datos están disponibles bajo la licencia **CC-0**, de acuerdo con el
*Palmer Station LTER Data Policy* y el *LTER Data Access Policy for Type I data*
:cite:`gorman2014ecological`.

El primer archivo, llamado ``penguins``, es una versión simplificada de los
datos originales. El segundo archivo, ``penguins_raw``, contiene los datos
crudos tal como fueron capturados originalmente. En el repositorio original
los archivos se encuentran en formato del lenguaje **R**; para facilitar su
lectura en Python, podemos descargar los archivos en formato **CSV** desde el
sitio `Kaggle
<https://www.kaggle.com/datasets/parulpandey/palmer-archipelago-antarctica-penguin-data>`_
(requiere registro). Estos archivos también estarán disponibles en el
repositorio del libro.

Los archivos CSV que utilizaremos se llaman:

* ``penguins_size.csv`` (versión simplificada)
* ``penguins_iter.csv`` (versión cruda)

Para leer los archivos vamos a suponer que se encuentran en el mismo directorio
desde donde ejecutamos el intérprete de Python. Comenzaremos leyendo la versión
simplificada utilizando la librería ``pandas``:

>>> import pandas as pd
>>> df = pd.read_csv('penguins_size.csv')
>>> df.head()
  species     island  culmen_length_mm  culmen_depth_mm  flipper_length_mm  body_mass_g     sex
0  Adelie  Torgersen              39.1             18.7              181.0       3750.0    MALE
1  Adelie  Torgersen              39.5             17.4              186.0       3800.0  FEMALE
2  Adelie  Torgersen              40.3             18.0              195.0       3250.0  FEMALE
3  Adelie  Torgersen               NaN              NaN                NaN          NaN     NaN
4  Adelie  Torgersen              36.7             19.3              193.0       3450.0  FEMALE

Observamos que algunos registros contienen valores ``NaN``, los cuales
interpretaremos como **datos faltantes**. Este es un escenario común en
conjuntos de datos reales y lo abordaremos más adelante.

Ahora imprimimos información general sobre el *dataset* y los tipos de datos
de sus columnas:

>>> df.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 344 entries, 0 to 343
Data columns (total 7 columns):
 #   Column             Non-Null Count  Dtype
---  ------             --------------  -----
 0   species            344 non-null    object
 1   island             344 non-null    object
 2   culmen_length_mm   342 non-null    float64
 3   culmen_depth_mm    342 non-null    float64
 4   flipper_length_mm  342 non-null    float64
 5   body_mass_g        342 non-null    float64
 6   sex                334 non-null    object
dtypes: float64(4), object(3)
memory usage: 18.9+ KB

Las columnas del *dataset* incluyen los siguientes atributos:

* ``species``: especie del pingüino (Chinstrap, Adélie o Gentoo)
* ``culmen_length_mm``: longitud del culmen (mm)
* ``culmen_depth_mm``: profundidad del culmen (mm)
* ``flipper_length_mm``: longitud de la aleta (mm)
* ``body_mass_g``: masa corporal (g)
* ``island``: nombre de la isla (Dream, Torgersen o Biscoe)
* ``sex``: sexo del pingüino

Eliminamos registros con valores nulos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Más adelante veremos las herramientas de `sci-kit learn` para tratar los casos
de valores nulos. En estre primer ejercicio simplemente vamos a eliminar estos
registros. Primero vemos cuales renglones *incluyen* valores nulos en alguna de
sus columnas:

>>> df.isnull().any(axis=1)
0      False
1      False
2      False
3       True
4      False
       ...
339     True
340    False
341    False
342    False
343    False
Length: 344, dtype: bool

Podemos utilizar este vector de boleanos (mascara boleane) pare filtrar aquellos que 
*no tienen valores nulos*   y 
copiarlos en un nuevo `DataFrame`. Como esta es la idea, mejor vamos a utilizar 
directamente `notnull()` para quedarnos con los que cumplen con la condición (`True`). Es
importante observar que ahora tenemos que utilizar el cuantificador `all(axis=1)` porque 
queremos *no nulo* en todas las columnas.

>>> df = df[df.notnull().all(axis=1)]
>>> df.isnull().all(axis=1).sum()
0

Preprocesamiento mínimo
~~~~~~~~~~~~~~~~~~~~~~~

Los algoritmos de clasificación en ``scikit-learn`` requieren que tanto las
**características** como la **clase objetivo** estén representadas mediante
valores numéricos.

En nuestro *dataset*, la clase corresponde a la **especie del pingüino**, la
cual está representada como texto. Además, como vimos anteriormente, la columna
``sex`` es una variable categórica. Para poder entrenar un modelo, es necesario
codificar este tipo de datos.

Para realizar esta codificación utilizaremos la librería
``sklearn.preprocessing``, en particular el *encoder* ``OrdinalEncoder``, el
cual transforma variables categóricas asignando un valor numérico ordinal a
cada categoría:

>>> from sklearn.preprocessing import OrdinalEncoder
>>> encoder = OrdinalEncoder()
>>> df[['species', 'island', 'sex']] = encoder.fit_transform(
...     df[['species', 'island', 'sex']]
... )
>>> df.head()
   species  island  culmen_length_mm  culmen_depth_mm  flipper_length_mm  body_mass_g  sex
0      0.0     2.0              39.1             18.7              181.0       3750.0  2.0
1      0.0     2.0              39.5             17.4              186.0       3800.0  1.0
2      0.0     2.0              40.3             18.0              195.0       3250.0  1.0
4      0.0     2.0              36.7             19.3              193.0       3450.0  1.0
5      0.0     2.0              39.3             20.6              190.0       3650.0  2.0

.. warning::

   Es importante recordar que los datos ordinales implican la existencia de una
   **secuencia u orden inherente** entre las categorías, lo cual **no ocurre en
   este caso**. Aunque ``scikit-learn`` puede trabajar con este tipo de
   codificación, algunos algoritmos de aprendizaje automático pueden interpretar
   erróneamente estos valores como si existiera una relación de orden o
   magnitud entre ellos.

   En la mayoría de los casos, especialmente en problemas reales, es preferible
   utilizar *encoders* alternativos como ``OneHotEncoder`` o ``TargetEncoder``,
   los cuales evitan introducir supuestos de orden que no están presentes en los
   datos originales.

.. note::

   Como vimos anteriormente, estas transformaciones también pueden realizarse con ``pandas``; aquí se
   presentan utilizando ``scikit-learn`` para mantener un flujo de trabajo
   coherente con el entrenamiento de modelos.

