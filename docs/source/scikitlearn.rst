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
~~~~~~~~~~~~~~~~~~~~~~~

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

Como hay varios casos de datos categóricos a los que no se le asigna el tipo 
de dato correcto, cargaremos de nuevo los datos con el `dtype` correspondiente:

>>> df = pd.read_csv(
...     'penguins_size.csv',
...     dtype={
...         'species': 'category',
...         'island': 'category',
...         'culmen_length_mm': 'float64',
...         'culmen_depth_mm': 'float64',
...         'flipper_length_mm': 'float64',
...         'body_mass_g': 'float64',
...         'sex': 'category'
...     }
... )


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

Preparar los datos para el algoritmo de clasificación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un **clasificador** es un algoritmo cuyo objetivo es aprender un modelo a partir
de un conjunto de **datos de entrenamiento**
:cite:`tan2016introduction`. Los datos son objetos
representados mediante un vector de características y la categoría a la que
pertenece cada objeto.
Podemos representar a cada objeto como una tupla
:math:`(\vec{x}, y)`, donde :math:`\vec{x}` es el vector de características y
:math:`y` es la categoría asociada, también llamada **etiqueta** o **clase**.

En el caso de ``scikit-learn`` (y de la mayoría de las librerías de *machine
learning*) el conjunto de vectores de características se representa como una
matriz ``X``, mientras que las categorías correspondientes se representan como
un vector ``y``. Los métodos que implementan los algoritmos de clasificación
esperan, de manera estándar, recibir estos dos objetos como parámetros.

Por esta razón, una tarea común al preparar los datos consiste en **separar el
dataset** en ``X`` y ``y``. En este ejemplo, utilizaremos como clase objetivo
la columna ``species`` y el resto de las columnas como características
predictoras.

Vamos al código.

>>> X = df.drop(columns='species')
>>> y = df['species']

Podemos verificar las dimensiones de ambos objetos:

>>> X.shape
(333, 6)

>>> y.shape
(333,)

La matriz ``X`` contiene una fila por cada pingüino y una columna por cada
característica, mientras que el vector ``y`` contiene la clase asociada a cada
observación. Con estos datos ya estamos listos para entrenar nuestro primer
modelo de clasificación.
Como primer modelo de clasificación utilizaremos un **árbol de decisión**.
Este tipo de modelos es especialmente útil para comenzar, ya que su
funcionamiento es intuitivo y permite inspeccionar fácilmente las reglas que
aprende a partir de los datos.

En ``scikit-learn``, los árboles de decisión se encuentran en el módulo
``sklearn.tree``:

>>> from sklearn import tree
>>> clf = tree.DecisionTreeClassifier()
>>> clf = clf.fit(X, y)

¡Listo! En ``clf`` ya tenemos un modelo de clasificación entrenado y listo para
ser utilizado. Una de las principales ventajas de los **árboles de decisión**
es que permiten inspeccionar el modelo aprendido y, en muchos casos,
interpretar sus decisiones.

Para ello, podemos imprimir el árbol en formato de texto utilizando la función
``export_text``:

>>> from sklearn.tree import export_text
>>> feature_names = X.columns.tolist()
>>> r = export_text(clf, feature_names=feature_names)
>>> print(r)

.. warning::

   En este ejemplo entrenamos el modelo utilizando **todos los datos
   disponibles**, lo cual puede conducir a **sobreentrenamiento**
   (*overfitting*). Más adelante veremos cómo dividir los datos en conjuntos de
   entrenamiento y prueba para evaluar correctamente el desempeño del modelo.


Evaluación del modelo
~~~~~~~~~~~~~~~~~~~~~

Dado que entrenamos el modelo con todo el *dataset*, no tendría sentido
pedirle que clasifique un pingüino que **ya ha visto durante el entrenamiento**.
Por esta razón, en la práctica es habitual separar el conjunto de datos en dos
partes: un conjunto de **entrenamiento** y un conjunto de **prueba**.

Esta separación nos permite evaluar qué tan bien generaliza el modelo a datos
no vistos. Más adelante veremos cómo extender esta idea mediante técnicas más
robustas, como la **validación cruzada**, para reducir el riesgo de
sobreentrenamiento.


Datos de entrenamiento y prueba
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vamos a volver a crear el modelo, pero ahora separando el *dataset* en dos
conjuntos aleatorios: **entrenamiento** y **prueba**. El parámetro
``test_size`` indica el porcentaje de datos que se reservarán para la prueba. El
tamaño del conjunto de entrenamiento será el complemento.

Aunque la partición es aleatoria, con el parámetro ``random_state`` definimos
la semilla para obtener experimentos repetibles:

>>> from sklearn.model_selection import train_test_split
>>> X_train, X_test, y_train, y_test = train_test_split(
...     X, y, test_size=0.20, random_state=12
... )

Ahora entrenamos de nuevo con los datos de entrenamiento ``X_train`` y
``y_train``:

>>> from sklearn import tree
>>> clf = tree.DecisionTreeClassifier(random_state=12)
>>> clf = clf.fit(X_train, y_train)

Podemos probar clasificando alguno de los pingüinos de prueba. Cuando el modelo
se entrena utilizando un ``DataFrame`` de ``pandas``, es recomendable realizar
las predicciones utilizando el mismo tipo de estructura. 
Como vimos anteriormente, aunque seleccionemos solo una fila podemos conservar el
``DataFrame`` utilizando ``iloc[[i]]``:

>>> X_test.iloc[[0]]
    island  culmen_length_mm  culmen_depth_mm  flipper_length_mm  body_mass_g  sex
56     0.0              39.0             17.5              186.0       3550.0  1.0

>>> clf.predict(X_test.iloc[[0]])
array([0.])

Veamos si la predicción es correcta:

>>> y_test.iloc[0]
2.0

En este caso el clasificador no funcionó correctamente. Sin embargo, para evaluar
el desempeño del modelo es necesario repetir este proceso para **todos** los
registros del conjunto de prueba, utilizando una métrica apropiada.

Evaluación con una métrica
~~~~~~~~~~~~~~~~~~~~~~~~~~~

La forma más directa de evaluar un clasificador consiste en **predecir todas
las etiquetas del conjunto de prueba** y compararlas contra las etiquetas
reales.

Comenzamos obteniendo las predicciones del modelo para los datos de prueba:

>>> y_pred = clf.predict(X_test)
>>> y_pred
array([2., 0., 2., 0., 2., 1., 2., 0., 1., 2., 0., 0., 0., 2., 0., 2., 0.,
       2., 1., 0., 2., 0., 2., 2., 0., 0., 1., 2., 2., 1., 0., 0., 0., 2.,
       2., 1., 2., 0., 2., 1., 2., 2., 2., 2., 2., 0., 0., 2., 2., 0., 2.,
       1., 1., 0., 0., 1., 1., 0., 1., 2., 2., 0., 2., 1., 2., 2., 0.])

Exactitud (*accuracy*)
^^^^^^^^^^^^^^^^^^^^^

Vamos a evaluar nuestro modelo de clasificación utilizando la métrica de
**exactitud** (*accuracy*), la cual mide el porcentaje de ejemplos que fueron
clasificados correctamente:

.. math::

   \text{accuracy} = \frac{\#\text{aciertos}}{\#\text{ejemplos}}

En ``scikit-learn`` esta métrica se encuentra disponible en el módulo
``sklearn.metrics``:

>>> from sklearn.metrics import accuracy_score
>>> accuracy_score(y_test, y_pred)
0.9850746268656716

El modelo alcanza una exactitud cercana al **98 %**, lo cual indica que clasifica
correctamente la gran mayoría de los ejemplos del conjunto de prueba.

Preprocesamiento y modelos con *pipelines*
*****************************************

Hasta ahora hemos aplicado el preprocesamiento de los datos y el entrenamiento
del modelo como pasos separados. En problemas reales, este enfoque puede
volverse difícil de mantener, especialmente cuando el preprocesamiento es más
complejo o cuando se prueban distintos modelos.

Para resolver este problema, ``scikit-learn`` proporciona el concepto de
*pipeline*, que permite **encadenar varias etapas del flujo de trabajo** en un
solo objeto. De esta manera, el preprocesamiento y el modelo se tratan como una
unidad coherente.

Un *pipeline* típico incluye:

- una o más etapas de **transformación de datos**, y
- una etapa final de **aprendizaje automático**.

Veamos cómo utilizar un *pipeline* sencillo con el mismo *dataset* de los
pingüinos, incorporando ahora una transformación adicional para el
**tratamiento de valores faltantes**.

Hasta este punto eliminamos manualmente los registros con valores nulos para
simplificar los ejemplos. Sin embargo, en problemas reales esta estrategia no
siempre es adecuada, ya que puede implicar la pérdida de información valiosa.
Una de las principales ventajas de los *pipelines* es que el tratamiento de
valores faltantes puede **integrarse directamente como una etapa más del flujo
de trabajo**, garantizando que el mismo preprocesamiento se aplique de forma
consistente durante el entrenamiento y la predicción.

Para ello utilizaremos el objeto ``SimpleImputer``, el cual permite reemplazar
valores faltantes siguiendo una estrategia definida, como el promedio, la
mediana o el valor más frecuente.

En este ejemplo:

- imputaremos las variables numéricas utilizando la **mediana**, y
- codificaremos las variables categóricas mediante ``OrdinalEncoder``.

Primero definimos las columnas numéricas y categóricas:

>>> numeric_features = [
...     'culmen_length_mm',
...     'culmen_depth_mm',
...     'flipper_length_mm',
...     'body_mass_g'
... ]
>>> categorical_features = ['island', 'sex']

Es importante notar que los *pipelines* en ``scikit-learn`` se aplican
únicamente a las variables de entrada ``X``. La clase objetivo ``y`` no forma
parte del *pipeline* y se proporciona directamente al método ``fit``.

Esta separación refleja el flujo conceptual del aprendizaje automático: el
preprocesamiento se aplica a los datos observables, mientras que las etiquetas
se utilizan como referencia para el aprendizaje del modelo.

Ahora construimos los transformadores correspondientes:

>>> from sklearn.impute import SimpleImputer
>>> from sklearn.preprocessing import OrdinalEncoder
>>> from sklearn.compose import ColumnTransformer
>>> from sklearn.pipeline import Pipeline

>>> numeric_transformer = SimpleImputer(strategy='median')
>>> categorical_transformer = Pipeline(steps=[
...     ('imputer', SimpleImputer(strategy='most_frequent')),
...     ('encoder', OrdinalEncoder())
... ])

A continuación combinamos ambos tipos de variables utilizando un
``ColumnTransformer``:

>>> preprocessor = ColumnTransformer(
...     transformers=[
...         ('num', numeric_transformer, numeric_features),
...         ('cat', categorical_transformer, categorical_features)
...     ]
... )

Finalmente, integramos el preprocesamiento y el modelo de clasificación en un
solo *pipeline*:

>>> from sklearn.tree import DecisionTreeClassifier

>>> pipeline = Pipeline(steps=[
...     ('preprocess', preprocessor),
...     ('classifier', DecisionTreeClassifier(random_state=0))
... ])

Entrenamos el *pipeline* utilizando los datos de entrenamiento originales,
**incluyendo valores nulos**:

>>> pipeline.fit(X_train, y_train)

Finalmente calculamos la exactitud del modelo creado a partir del pipeline:

>>> y_pred = pipeline.predict(X_test)
>>> from sklearn.metrics import accuracy_score
>>> accuracy_score(y_test, y_pred)
0.9855072463768116

Aunque este valor de exactitud es alto, es importante recordar que el *dataset*
es relativamente pequeño y que el modelo utilizado es capaz de ajustarse con
facilidad a los datos. En problemas reales, es recomendable complementar esta
evaluación con otras métricas y técnicas, como la validación cruzada, para
obtener una estimación más robusta del desempeño del modelo.

Un ejemplo breve con redes neuronales
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``scikit-learn`` también incluye implementaciones básicas de redes neuronales,
útiles con fines educativos y para problemas de tamaño pequeño. En particular,
podemos utilizar ``MLPClassifier`` (Perceptrón Multicapa) como clasificador.

La idea es exactamente la misma que en el ejemplo anterior: reutilizamos el
mismo preprocesamiento (imputación + codificación) y sustituimos el modelo
final por una red neuronal.

>>> from sklearn.neural_network import MLPClassifier
>>> from sklearn.pipeline import Pipeline

>>> nn_pipeline = Pipeline(steps=[
...     ('preprocess', preprocessor),
...     ('classifier', MLPClassifier(hidden_layer_sizes=(20,),
...                                 max_iter=2000,
...                                 random_state=0))
... ])

Entrenamos el modelo con los datos de entrenamiento:

>>> nn_pipeline.fit(X_train, y_train)

Y evaluamos su desempeño en el conjunto de prueba usando exactitud
(*accuracy*):

>>> y_pred = nn_pipeline.predict(X_test)
>>> from sklearn.metrics import accuracy_score
>>> accuracy_score(y_test, y_pred)
0.6811594202898551

Este resultado nos puede sorprender por ser tan bajo, pero muestra una realidad
del aprendizaje automático: no todo se resuelve utilizando el mejor algoritmo.
De hecho, según el principio *No free lunch* no hay un algoritmo que sea el
mejor en todos los casos. En este caso, el resultado se puede explicar por 
varias razones:

- El *dataset* tiene muy pocos registros y las clases están bien separadas. 
  La red no alcanza a ajustarse a los datos,en el caso de los árboles de 
  decisión que hacen "cortes" rectos aquí es más fácil.
- El preprocesamiento no fue adecuado (este normalmente es el caso)
- Los parámetros (hiperparámtros) de la red no son los adecuados.
  
Veamos el caso del preprocesamiento.

Es importante notar que, en este ejemplo, utilizamos ``OrdinalEncoder`` para
codificar las variables categóricas. Esta codificación introduce una relación
numérica artificial entre categorías que no tienen un orden inherente.

Mientras que modelos como los árboles de decisión son poco sensibles a esta
representación, las **redes neuronales sí se ven fuertemente afectadas** por la
forma en que se codifican las variables categóricas. En estos casos, suele ser
preferible utilizar *encoders* como ``OneHotEncoder``, que evitan introducir
datos ordinales.

El menor desempeño observado en este ejemplo resalta la importancia de realizar
un preprocesamiento adecuado en función del algoritmo utilizado. Mejorar este
resultado quedará como ejercicio para el lector.

.. rubric:: Ejercicio

En el ejemplo con redes neuronales utilizamos el mismo *pipeline* que en el
caso del árbol de decisión, incluyendo la codificación de variables categóricas
mediante ``OrdinalEncoder``. Como observamos, el desempeño del modelo fue
considerablemente menor.

1. Modifica el *pipeline* para utilizar ``OneHotEncoder`` en lugar de
   ``OrdinalEncoder`` para las variables categóricas.

2. Entrena nuevamente el modelo de red neuronal utilizando ``MLPClassifier`` y
   evalúa su desempeño en el conjunto de prueba.

3. Compara los resultados obtenidos con los del árbol de decisión y reflexiona
   sobre cómo la representación de los datos influye en el desempeño del
   modelo.

Este ejercicio ilustra la importancia del preprocesamiento y muestra que
distintos modelos pueden requerir distintas representaciones de los datos para
obtener buenos resultados.

Resumen del capítulo
~~~~~~~~~~~~~~~~~~~~

En este capítulo presentamos una introducción práctica al **aprendizaje
automático con ``scikit-learn``**, enfocándonos en el flujo de trabajo completo
más que en los detalles teóricos de los algoritmos.

A lo largo del capítulo:

- Revisamos el flujo general del aprendizaje automático y su relación con el
  proceso de *Knowledge Discovery in Databases* (KDD).
- Trabajamos con un *dataset* real de pingüinos, utilizando ``pandas`` para su
  exploración y preparación inicial.
- Construimos y entrenamos un primer **modelo de clasificación** utilizando
  árboles de decisión.
- Introdujimos buenas prácticas como la separación de datos en conjuntos de
  entrenamiento y prueba, así como la evaluación del modelo mediante una
  métrica sencilla.
- Mostramos cómo integrar **preprocesamiento y modelos** mediante
  *pipelines*, incluyendo el tratamiento de valores faltantes.
- Exploramos de manera breve el uso de **redes neuronales** dentro del mismo
  flujo de trabajo, destacando la importancia del preprocesamiento y de la
  representación de los datos.
- Discutimos que la elección del modelo y del preprocesamiento depende del
  problema y de los datos disponibles, y que modelos más complejos no garantizan
  mejores resultados.

El objetivo principal de este capítulo no fue mostrar todas las capacidades de
``scikit-learn``, sino proporcionar una **visión clara del flujo de
trabajo básico** del aprendizaje automático en Python.





