.. role:: python(code)
   :language: python

.. _datapy: 

Análisis de Datos con Python
=================================

NumPy
*****

Cómputo numérico en Python
--------------------------

Durante más de cincuenta años, `Fortran <https://fortran-lang.org/>`_  ha sido
el lenguaje estándar del cómputo científico y de alto rendimiento. Las
librerías `BLAS <https://es.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms>`_ (en realidad,
una especificación) y `LAPACK <https://es.wikipedia.org/wiki/LAPACK>`_,
escritas en Fortran, continúan siendo la referencia cuando se trata de hacer
operaciones vectoriales y matriciales. Incluso, herramientas comerciales como
`MATLAB <https://en.wikipedia.org/wiki/MATLAB>`_, se basan en estas librerías
pero ofreciendo una interfaz de programación más amigable. La desventaja es
que crean una dependencia del proveedor y van en contra de las prácticas de 
**ciencia abierta** que nos interesa promoveer.

La tendencia actual de la comunidad científica es migrar hacia alternativas de sofware libres como 
`GNU Octave <https://octave.org/>`_ o `SageMath <https://www.sagemath.org/>`_, 
y hacia lenguajes de programación abiertos, diseñados para el análisis 
numérico (`Julia <https://julialang.org/>`_) o estadístico (`R <https://www.r-project.org/>`_).
En este panorama, *Python* se ha 
consolidado como uno de los lenguajes más utilizados gracias a su sencillez, 
su comunidad y su creciente ecosistema científico. Este éxito se debe en gran medida al esfuerzo inicial  
de los autores de proyectos de código abierto
`SciPy <https://scipy.org/>`_, `Matplotlib <https://matplotlib.org/>`_, y `NumPy <https://numpy.org/>`_ .

NumPy, en particular, introdujo un tipo de dato fundamental: el arreglo
multidimensional ``ndarray``. Este arreglo (o matriz), junto con sus operaciones
vectorizadas permitió que Python alcanzara el rendimiento
necesario para aplicaciones científicas y de ingeniería.

NumPy nos proporciona:

* Un tipo de dato eficiente para arreglos *n-dimensionales* (``ndarray``).
* Operaciones vectorizadas implementadas en C/Fortran para mejorar el rendimiento.
* Funciones de *álgebra lineal*, transformadas de Fourier y generación 
  de números aleatorios. 
* *Broadcasting*, para operar arreglos de diferentes formas.
* Integración con código en C, C++ y Fortran.
* Licencia abierta *BSD*, compatible con la ciencia abierta.

.. tip::

        Si te interesa conocer más sobre la historia de la librería NumPy, no te pierdas el documental 
        *The early days of scientific Python with Travis Oliphant* disponible 
        en `YouTube <https://www.youtube.com/watch?v=-xhai2iu_QY>`_.

``ndarray``
-----------

Mientras que en Python contamos con colecciones de objetos tipo secuencia, como
las listas, éstas no tienen una estructura adecuada para realizar operaciones
numéricas generales. Por ejemplo, si tenemos la siguiente lista de listas:

.. code-block:: python

    >>> lista_objetos = [[1, 2, 3],
    ...                  [2, 2],
    ...                  ['Hola', 11],
    ...                  [2]]

Tenemos dos problemas importantes:

1. **Las sublistas tienen diferente tamaño.**  
   Unas tienen tres elementos, otras dos y una solo uno. Esto
   impide realizar operaciones posición por posición, como sumar todos los valores de
   la tercera columna ya que algunas sublistas no tienen el tercer
   elemento.

2. **Los elementos no son del mismo tipo.**  
   La tercera sublista contiene una cadena:

   .. code-block:: python

       ['Hola', 11]

   Esto hace imposible sumar todos los elementos de la primera posición, ya 
   Python no puede sumar enteros con cadenas de texto.

Estas limitaciones hacen que las listas de Python no sean una buena
representación para datos numéricos estructurados. Para análisis científico,
necesitamos estructuras que:

- tengan forma regular (todas las filas con el mismo número de columnas),  
- contengan datos homogéneos,  
- permitan operaciones vectorizadas eficientes.

Aquí es donde entra **NumPy** y su tipo de dato fundamental: el arreglo
multidimensional ``ndarray``.

Vamos a crear una lista compatible con un ``ndarray``:

.. code-block:: python

        >>> import numpy as np
        >>> listas  = [[2,3,4], [3,6,8], [2,3,4]]
        >>> listas
        [[2, 3, 4], [3, 6, 8], [2, 3, 4]]

Python nos permite crear arreglos ``ndarray`` a partir de listas u otras secuencias de
Python. En este ejemplo, la secuencia contiene otras secuencias internas, ya que
tenemos una *lista de listas*. En estos casos NumPy interpreta esta estructura como un arreglo
bidimensional.

.. code-block:: python

        >>> arreglo_np = np.array(listas)
        >>> arreglo_np
        array([[2, 3, 4],
               [3, 6, 8],
               [2, 3, 4]])

Lo primero que notamos es que al desplegar el arreglo este se imprime con un formato
de matriz, donde cada sublista se convierte en un renglón del arreglo. 

Notación de cortes
------------------

Podemos acceder a los renglones o columnas de un arreglo bidimensional utilizando la
notación de cortes (*slicing*) de Python.   
NumPy extiende esta notación permitiendo especificar un corte para cada dimensión del
arreglo con la sintaxis ``arreglo[renglón, columna]``.

Por ejemplo, para imprimir toda la primer columna utilizamos:

>>> arreglo_np[:, 0]
array([2, 3, 2])

En este caso, indicamos que queremos todos los renglones ``:`` pero solo la
columna ``0``. Recuerda que el símbolo ``:`` representa un corte completo, es
decir, “todas las posiciones” en esa dimensión.

De la misma manera, podemos obtener un renglón completo utilizando la misma
notación de cortes. Ahora vamos a imprimir los primeros dos elementos del 
primer renglón:

.. code-block:: python

    >>> arreglo_np[0, :2]
    array([2, 3])

Vemos que es exactamente la misma notación de cortes (*slicing*) utilizada en listas
de Python, pero ahora aplicada a las dimensiones del arreglo bidimensional.
Esta manera de indexar es muy poderosa y la utilizaremos continuamente cuando
trabajemos con datos numéricos y operaciones matriciales en NumPy.

Copias y vistas
----------------
Algo muy importante al trabajar con arreglos ``ndarray`` es que, en la mayoría
de los casos, los cortes (*slices*) no generan una copia del arreglo, sino una
*vista* (*view*). Una vista comparte la misma memoria con el arreglo original,
por lo que cualquier modificación hecha a la vista afecta directamente al
arreglo original.

Veamos un ejemplo:

.. code-block:: python

    >>> a = np.array([1, 2, 3, 4, 5])
    >>> b = a[1:4]   # Regresa una vista
    >>> b
    array([2, 3, 4])

Modificamos la vista:

.. code-block:: python

    >>> b[0] = 99
    >>> b
    array([99, 3, 4])

El arreglo original también cambió:

.. code-block:: python

    >>> a
    array([1, 99, 3, 4, 5])

Esto sucede porque ``b`` no tiene sus propios datos, sino que es una referencia al
mismo bloque de memoria de ``a``. NumPy utiliza este comportamiento para
evitar copias innecesarias y mejorar el rendimiento.

Si necesitamos explícitamente una copia independiente del arreglo, debemos usar
``copy()``:

.. code-block:: python

    >>> c = a[1:4].copy()
    >>> c[0] = -5
    >>> c
    array([-5,  3,  4])
    >>> a
    array([1, 99, 3, 4, 5])  # El original ya no cambia

Funciones para crear arreglos 
-----------------------------

En ocasiones queremos crear arreglos con datos iniciales sin necesidad de
proporcionar explícitamente cada elemento. NumPy incluye varias funciones
con este propósito, entre ellas ``zeros()``, ``ones()`` y ``empty()``.

Podemos crear un arreglo lleno de ceros especificando su forma (*shape*) como
una tupla:

.. code-block:: python

    >>> np.zeros((3, 4))
    array([[0., 0., 0., 0.],
           [0., 0., 0., 0.],
           [0., 0., 0., 0.]])

De manera similar, ``ones()`` crea un arreglo en el que todos los elementos
son uno. El siguiente ejemplo crea un arreglo tridimensional:

.. code-block:: python

    >>> np.ones((2, 3, 4))
    array([[[1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.]],

           [[1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.]]])

La función ``empty()`` crea un arreglo con la forma indicada pero **sin
inicializar** sus valores; es decir, contiene lo que sea que hubiera en la
memoria en ese momento:

>>> np.empty((3,))
array([7.74860419e-304, 7.74860419e-304, 7.74860419e-304])

.. note::

        Es importante recordar que ``empty()`` no llena el arreglo con ceros;
        el contenido depende del estado de la memoria asignada y, por lo tanto,
        **no se debe utilizar cuando necesitemos valores iniciales
        confiables**.


Tipos de datos
--------------

Es importante considerar el tipo de dato (`dtype
<https://numpy.org/doc/stable/user/basics.types.html>`_) de los elementos del
arreglo. Podemos imprimir el tipo de dato asignado por el constructor ``array``
con el atributo ``dtype``:

>>> arreglo_np.dtype
dtype('int64')

Tambien podemos especificar explícitamente el tipo de dato en el contructor:

>>> arreglo_8 = np.array(listas, dtype=np.int8)
>>> arreglo_8
array([[2, 3, 4],
       [3, 6, 8],
       [2, 3, 4]], dtype=int8)

En este caso utilizamos enteros con signo de 8 bits, lo que 
nos permite representar enteros de ``-120`` a ``127``. Si 
se intentara incluir un entero fuera de este rango, el 
constructor lanzaría una excepción.

Rank y Shape
------------

Veamos que pasa si enviamos una lista heterogénea al constructor de `ndarray`:

>>> objetos = [[1, 3.4], ['Hola'], [2, 3, 4]]
>>> arreglo = np.array(objetos)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: setting an array element with a sequence. The requested array has 
an inhomogeneous shape after 1 dimensions. The detected shape was (3,) + inhomogeneous part.

NumPy intenta crear un arreglo bidimensional, pero las sublistas no tienen la
misma longitud; por lo tanto, la estructura no es rectangular y se produce un
error. Aunque normalmente no es útil, podemos construir un arreglo unidimensional
de elementos tipo ``object``:

>>> arreglo = np.array(objetos, dtype=object)
>>> arreglo
array([list([1, 3.4]), list(['Hola']), list([2, 3, 4])], dtype=object)

Este no es un arreglo muy útil para cómputo numérico. 
Mejor vamos a crear un arreglo unidimensional de enteros:

>>> enteros = np.array([1,3,4,5,7])
>>> enteros
array([1, 3, 4, 5, 7])
>>> enteros.dtype
dtype('int64')

Comparemos la dimension de los arreglos utilizando el atributo `ndim`:

>>> enteros.ndim
1

>>> arreglo_np.ndim
2

El número de dimensiones se conoce en NumPy como el *rank* (rango) del arreglo.

Otro atributo importante es la forma (*shape*) del arreglo, que indica el número
de elementos en cada dimensión:

>>> arreglo_np.shape
(3, 3)
>>> enteros.shape
(5,)

Para un arreglo bidimensional, el primer valor de la tupla corresponde al número
de renglones y el segundo al número de columnas. Una forma útil de recordarlo es
pensar en cómo se asignan los asientos en el cine: primero se indica la fila
(renglón) y después el número de asiento (columna).

Operaciones en arreglos 
-----------------------

Para esta sección consideremos la siguiente lista de calificaciones, donde cada alumno tiene
tres evaluaciones: examen, tarea y participación. Todas las calificaciones están en el
rango de 0 a 10.

+----+----------------+--------+--------+----------+
| id | nombre         | tarea  | examen | proyecto |
+====+================+========+========+==========+
| 1  | Joe            | 8.5    | 9.0    |  5.0     |
+----+----------------+--------+--------+----------+
| 2  | Ana            | 10.0   | 5.0    | 9.0      |
+----+----------------+--------+--------+----------+
| 3  | Tom            | 6.5    | 10.0   | 8.0      |
+----+----------------+--------+--------+----------+
| 4  | Zoe            | 8.0    | 4.0    | 9.0      |
+----+----------------+--------+--------+----------+

Vamos a almacenar las evaluaciones en un arreglo de NumPy, en este punto 
vamos a dejar fuera tanto el ``id`` como el ``nombre`` del alumno. Dejamos fuera 
estos datos ya que NumPy está optimizado para operar sobre
datos numéricos homogéneos, por lo que mezclar identificadores o cadenas de
caracteres en el mismo arreglo rompería esta regla y haría menos eficientes las operaciones
vectorizadas.

.. note::

        Más adelante podremos conservar estos datos *DataFrames* en pandas,
        pero el arreglo principal de NumPy debe permanecer exclusivamente numérico para
        que su uso sea óptimo.

Creamos ahora el arreglo ``evaluaciones`` utilizando únicamente los datos
numéricos. Cada renglón corresponde a un alumno y cada columna a una de las
tres evaluaciones (tarea, examen y proyecto):

.. code-block:: python

    >>> import numpy as np

    >>> evaluaciones = np.array([
    ...     [8.5,  9.0,  5.0],
    ...     [10.0, 5.0,  9.0],
    ...     [6.5, 10.0,  8.0],
    ...     [8.0,  4.0,  9.0]
    ... ])
    >>> evaluaciones
    array([[ 8.5,  9. ,  5. ],
           [10. ,  5. ,  9. ],
           [ 6.5, 10. ,  8. ],
           [ 8. ,  4. ,  9. ]])

Podemos inspeccionar la forma (*shape*) del arreglo para confirmar su estructura:

.. code-block:: python

    >>> evaluaciones.shape
    (4, 3)

Esto nos indica que tenemos **4 alumnos** y **3 evaluaciones** por alumno.

También podemos verificar el tipo de dato que le asignó NumPy:

.. code-block:: python

    >>> evaluaciones.dtype
    dtype('float64')

Sobre estos arreglos ahora si podemos aplicar operaciones vectorizadas. 
En el caso de las evaluaciones podemos calcular: promedios, máximos, mínimos,  
normalización y muchas otras operaciones de análisis numérico.
Veamos algunos ejemplos.

Para empezar, podemos ver las calificaciones de ``Joe`` y calcular su promedio utilizando
*slicing*. Recordemos que ``Joe`` corresponde al primer renglón del arreglo
(índice ``0``):

.. code-block:: python

    >>> evaluaciones[0, :]
    array([8.5, 9. , 5. ])

También podemos acceder al primer renglón del arreglo utilizando únicamente un
índice:

.. code-block:: python

    >>> evaluaciones[0]
    array([8.5, 9. , 5. ])

Cuando proporcionamos solo un índice a un arreglo bidimensional, NumPy asume
que nos referimos al renglón completo correspondiente a ese índice. Por lo
tanto, ``evaluaciones[0]`` es equivalente a escribir ``evaluaciones[0,:]``.

Ahora, para calcular el promedio de sus evaluaciones, simplemente aplicamos el
método ``mean`` sobre su renglón:

.. code-block:: python

    >>> evaluaciones[0, :].mean()
    7.5

NumPy realiza esta operación de manera vectorizada, sin necesidad de escribir
ciclos explícitos. Esta es una de las razones por las que es tan eficiente para
el análisis numérico.

Operaciones elemento por elemento
---------------------------------

Cuando utilizamos operaciones aritméticas sobre arreglos, la operación se realiza
para cada elemento (*element-wise*) y se regresa un nuevo arreglo con el
resultado. NumPy aplica estas operaciones de manera vectorizada, sin necesidad
de escribir ciclos explícitos.

Por ejemplo, supongamos que debido al buen desempeño de todos los alumnos se
decide subir un punto a todas las calificaciones:

.. code-block:: python

    >>> evaluaciones + 1
    array([[ 9.5, 10. ,  6. ],
           [11. ,  6. , 10. ],
           [ 7.5, 11. ,  9. ],
           [ 9. ,  5. , 10. ]])

La operación ``+ 1`` se aplica a cada elemento del arreglo y NumPy regresa un
nuevo arreglo con los valores actualizados. El operador de adición es un alias
de la función ``numpy.add``. Esta función toma dos arreglos como operandos y
aplica la operación elemento a elemento. Cuando realizamos:

.. code-block:: python

    >>> evaluaciones + 1

el valor ``1`` se interpreta como un arreglo muy pequeño cuya forma es
compatible con la operación. NumPy realiza un proceso llamado *broadcasting*,
que consiste en ampliar de manera conceptual el arreglo más pequeño para que
coincida con la forma del arreglo más grande, sin copiar datos innecesariamente.

En otras palabras, NumPy "extiende" el escalar ``1`` para que actúe sobre cada
elemento de ``evaluaciones``, gráficamente la extensión virtual se vería así:

.. figure:: ./images/punto_extra.png
   :align: center
   :alt: Ejemplo de *broadcasting* en NumPy.

.. attention::
   Hay un detalle en nuestra operación. Al hacer la operación en todo el arreglo 
   varias evaluaciones superan la calificación máxima de diez. Resolveremos este problema 
   como ejercicio.


Siguiendo con el ejemplo, ahora vamos a suponer que deseamos aplicar una ponderación distinta a cada
actividad. Por ejemplo, podríamos asignar un 40% a la tarea, 40% al examen y
20% al proyecto:

.. code-block:: python

    >>> ponderacion = np.array([0.40, 0.40, 0.20])
    >>> ponderacion
    array([0.4, 0.4, 0.2])

Si multiplicamos el arreglo ``evaluaciones`` por el arreglo ``ponderacion``, NumPy
aplica la operación elemento a elemento. En este caso los arreglos tienen formas
compatibles: ``evaluaciones`` es de forma ``(4, 3)`` y ``ponderacion`` es de forma
``(3,)``. De nuevo NumPy utiliza *broadcasting* para extender la ponderación a cada renglón:

.. figure:: ./images/ponderacion.png
   :align: center
   :alt: Ejemplo de *broadcasting* en NumPy.

.. code-block:: python

    >>> evaluaciones * ponderacion
    array([[3.4 , 3.6 , 1.  ],
           [4.  , 2.  , 1.8 ],
           [2.6 , 4.  , 1.6 ],
           [3.2 , 1.6 , 1.8 ]])

En este caso, la ponderación se aplica correctamente a cada una de las tres
actividades para todos los alumnos. Este tipo de operación es muy eficiente,
porque NumPy no hace copias adicionales; simplemente extiende de manera
conceptual el arreglo ``ponderacion`` para que sea compatible con ``evaluaciones``.

Como ejemplo, vamos a suponer que no agregamos una ponderación para la evaluación del proyecto:

>>> ponderacion = np.array([0.40, 0.40])
>>> ponderacion.shape
(2,)

En este caso no podemos hacer la multiplicación elemento por elemento, ya 
que no es posible obtener dos arreglos compatibles (con la misma forma) 
estirando alguno de ellos:

.. figure:: ./images/incompatibles.png
   :align: center
   :alt: Ejemplo de *broadcasting* en NumPy.

``numpy.newaxis``
-----------------

En algunos casos debemos agregar una dimensión adicional a nuestros arreglos
para que estos sean compatibles. Veamos un ejemplo. 

De nuevo vamos dar un punto extra a los alumnos, pero solo a algunos.
Para especificar a que alumnos daremos un punto extra utilizaremos un 
arreglo de una dimensión con cuatro elementos, indicando el valor que 
sumaremos al las evaluaciones de cada alumno:

>>> puntos_extra = np.array([1,0,0,1])
>>> puntos_extra
array([1, 0, 0, 1])
>>> puntos_extra.shape
(4,)

Gráficamente podemos observar que el arreglo ``evaluaciones`` no es compatible 
con ``puntos_extra``:


.. figure:: ./images/punto_alumno.png
   :align: center
   :alt: Ejemplo de *broadcasting* en NumPy.

Podemos ver gráficamente una manera de solucionar este problema:

.. figure:: ./images/newaxis.png
   :align: center
   :alt: Ejemplo de *broadcasting* en NumPy.


Para obtener el promedio ponderado final de cada alumno sumamos los valores de
cada renglón. NumPy puede hacerlo de manera vectorizada:

.. code-block:: python

    >>> (evaluaciones * ponderacion).sum(axis=1)
    array([8. , 7.8, 8.2, 6.6])

Esto lo hacemos aplicando la función suma a los elementos del eje
correspondiente. Al utilizar ``axis=1`` indicamos que la suma debe realizarse a
lo largo de cada renglón, es decir, sumamos las actividades de cada alumno para
obtener su promedio ponderado.

Esto produce un arreglo unidimensional donde cada entrada corresponde al
promedio ponderado de un alumno.

- Joe obtiene **8.0**  
- Ana obtiene **7.8**  
- Tom obtiene **8.2**  
- Zoe obtiene **6.6**

Nótese que no necesitamos escribir ciclos; NumPy realiza la operación de manera
eficiente mediante operaciones vectorizadas y *broadcasting*.

De manera análoga, si deseamos calcular el promedio de calificación por
actividad (tarea, examen y proyecto), debemos sumar a lo largo del eje ``0``,
es decir, por columnas. Después dividimos entre el número de alumnos o, de
forma más conveniente, utilizamos directamente la función ``mean``:

.. code-block:: python

    >>> evaluaciones.mean(axis=0)
    array([8.25, 7.0 , 7.75])

Esto nos da:

- promedio de **tarea**: 8.25  
- promedio de **examen**: 7.0  
- promedio de **proyecto**: 7.75  

Aquí ``axis=0`` indica que la operación se aplica columna por columna, lo que
corresponde a obtener el promedio de cada actividad considerando a todos los
alumnos.

Ejemplo: Cuantización Vectorial
-------------------------------

En la documentación oficial de NumPy se describe un ejemplo del uso de arreglos 
para un caso del mundo real de *Cuantización Vectorial*. Veamos podemos aplicar este 
concepto a nuestros estudiantes.

Ejemplo: Cuantización Vectorial de Colores RGB
---------------------------------------------

En la documentación oficial de NumPy se describe un ejemplo del uso de arreglos 
para un caso del mundo real de *Cuantización Vectorial*. Vamos a adaptar esta
idea al caso de colores en formato RGB.

Cada color se puede representar como un vector en :math:`\mathbb{R}^3` con tres
componentes: rojo (R), verde (G) y azul (B). Por ejemplo, el color rojo puro
sería el vector ``[255, 0, 0]``.

Supongamos que tenemos una pequeña “imagen” formada por 6 píxeles, cada uno con
un color RGB:

.. code-block:: python

    >>> import numpy as np

    >>> imagen = np.array([
    ...     [123,  20,  18],   # píxel 0
    ...     [200, 180, 170],   # píxel 1
    ...     [ 10, 220,  30],   # píxel 2
    ...     [  5,  10, 200],   # píxel 3
    ...     [250, 250, 250],   # píxel 4
    ...     [ 80,  80,  80]    # píxel 5
    ... ], dtype=float)
    >>> imagen
    array([[123.,  20.,  18.],
           [200., 180., 170.],
           [ 10., 220.,  30.],
           [  5.,  10., 200.],
           [250., 250., 250.],
           [ 80.,  80.,  80.]])

Ahora definimos una pequeña *paleta* de colores prototipo. Estos serán los
colores “permitidos” después de la cuantización:

.. code-block:: python

    >>> paleta = np.array([
    ...     [255,   0,   0],   # rojo
    ...     [  0, 255,   0],   # verde
    ...     [  0,   0, 255],   # azul
    ...     [255, 255, 255]    # blanco
    ... ], dtype=float)
    >>> paleta
    array([[255.,   0.,   0.],
           [  0., 255.,   0.],
           [  0.,   0., 255.],
           [255., 255., 255.]])

Queremos asignar cada píxel de la imagen al color de la paleta *más cercano*
usando la distancia euclidiana.

Primero calculamos la diferencia entre cada píxel y cada color de la paleta.
Utilizamos *broadcasting* para evitar ciclos explícitos:

.. code-block:: python

    >>> dif = imagen[:, np.newaxis, :] - paleta[np.newaxis, :, :]
    >>> dif.shape
    (6, 4, 3)

El arreglo ``dif`` tiene forma ``(6, 4, 3)``:

- 6 píxeles,
- 4 colores en la paleta,
- 3 componentes (R, G, B).

Calculamos ahora la distancia euclidiana a lo largo del último eje:

.. code-block:: python

    >>> distancias = np.linalg.norm(dif, axis=2)
    >>> distancias
    array([[134.71451295, 265.85334303, 267.76482219, 358.91224554],
           [253.62373706, 272.99267389, 282.17902119, 125.99603168],
           [330.64331235,  47.16990566, 314.84122983, 334.47720401],
           [320.31234756, 316.30681308,  56.1248608 , 354.33035433],
           [353.58874416, 353.58874416, 353.58874416,   8.66025404],
           [208.38665984, 208.38665984, 208.38665984, 303.10889132]])

Cada renglón corresponde a un píxel y cada columna a un color de la paleta.

Para saber qué color asignar a cada píxel, tomamos el índice del menor valor
en cada renglón:

.. code-block:: python

    >>> asignacion = distancias.argmin(axis=1)
    >>> asignacion
    array([0, 3, 1, 2, 3, 0])

Con esta información construimos la versión cuantizada de la imagen, donde cada
píxel se reemplaza por su color prototipo más cercano:

.. code-block:: python

    >>> imagen_cuantizada = paleta[asignacion]
    >>> imagen_cuantizada
    array([[255.,   0.,   0.],
           [255., 255., 255.],
           [  0., 255.,   0.],
           [  0.,   0., 255.],
           [255., 255., 255.],
           [255.,   0.,   0.]])

Hemos realizado una versión sencilla de *cuantización vectorial* de colores:
cada vector RGB original se ha aproximado por el color de la paleta más
cercano. Este mismo patrón se usa en problemas reales de compresión de imágenes
y reducción de colores, y ilustra muy bien la potencia de las operaciones
vectorizadas y el *broadcasting* en NumPy.


Pandas
******

Matplotlib
**********
