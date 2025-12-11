.. role:: python(code)
   :language: python

.. _datapy: 

Análisis de Datos con Python
=================================

NumPy
*****

Cómputo numérico en Python
--------------------------

Durante más de cinco décadas, `Fortran <https://fortran-lang.org/>`_  ha sido
el lenguaje estándar del cómputo científico y de alto rendimiento. Bibliotecas
clásicas como la especificación
`BLAS <https://es.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms>`_ y
`LAPACK <https://es.wikipedia.org/wiki/LAPACK>`_, escritas en Fortran, continúan
siendo la referencia cuando queremos hecer operaciones vectoriales y
matriciales. Incluso, herramientas comerciales como `MATLAB <https://en.wikipedia.org/wiki/MATLAB>`_,
se basan en estas librerías con el objetivo de hacer su
programación más amigable. La desventaja que tienen es que crean una
dependencia del proveedor y vam en contra de la práctica de la **ciencia
abierta** que nos interesa promoveer.

La tendencia actual es movernos hacia alternativas libres como 
`GNU Octave <https://octave.org/>`_ o `SageMath <https://www.sagemath.org/>`_, 
y hacia lenguajes diseñados para el análisis 
numérico (`Julia <https://julialang.org/>`_) o estadístico (`R <https://www.r-project.org/>`_).
En este panorama, *Python* se ha 
consolidado como uno de los lenguajes más utilizados gracias a su sencillez, 
su comunidad y su ecosistema científico. Muchas de las librerías científicas 
de Python tienen en su núcleo a la librería `NumPy <https://numpy.org/>`.

.. tip::

        Si te interesa conocer más sobre la historia de la librería NumPy, no te pierdas el documental 
        *The early days of scientific Python with Travis Oliphant* disponible 
        en `YouTube <https://www.youtube.com/watch?v=-xhai2iu_QY>`_.

NumPy nos proporciona:

* Un tipo de dato eficiente para arreglos *n-dimensionales* (``ndarray``).
* Operaciones vectorizadas implementadas en C/Fortran para mejorar el rendimiento.
* Funciones de *álgebra lineal*, transformadas de Fourier y generación 
  de números aleatorios. 
* *Broadcasting*, para operar arreglos de diferentes formas.
* Integración con código en C, C++ y Fortran.
* Licencia abierta *BSD*, compatible con la ciencia abierta.

realizar operaciones sobre sus elementos: las listas son de distintos tamaños y tienen
objetos de distintos tipos. Por ejemplo, no podemos sumar todos los números en
la primera posición o en la tercera. En el primer caso no podemos sumar la
cadena 'Hola' y en el segundo hay dos listas que no tienen un elemento en la
tercera posición. 

NumPy introduce el **arreglo homogéneo multidimensional** (``ndarray``), 
en los cuales:

* Todos sus elementos son del **mismo tipo** (casi siempre numérico).
* Todas sus dimensiones tienen el **mismo tamaño**.
* El almacenamiento en memoria es **contiguo**, lo cual permite 
  una ejecución más rápida mediante el uso de BLAS/LAPACK.

Vamos a crear una lista compatible con un ``ndarray``::

.. code-block:: python

        >>> import numpy as np
        >>> listas  = [[2,3,4], [3,6,8], [2,3,4]]
        >>> listas
        [[2, 3, 4], [3, 6, 8], [2, 3, 4]]

Podemos crear arreglos ``ndarray`` a partir de listas u otras secuencias de
Python.  Cuando la secuencia contiene otras secuencias internas, como aquí, que
tenemos una *lista de listas*, NumPy interpreta esta estructura como un arreglo
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
ValueError: setting an array element with a sequence. The requested array has an inhomogeneous shape after 1 dimensions. The detected shape was (3,) + inhomogeneous part.

NumPy intenta crear un arreglo bidimensional, pero las sublistas no tienen la
misma longitud; por lo tanto, la estructura no es rectangular y se produce un
error. Aunque normalmente no es útil, podemos construir un arreglo unidimensional
de elementos tipo ``object``:

>>> arreglo = np.array(objetos, dtype=object)
>>> arreglo
array([list([1, 3.4]), list(['Hola']), list([2, 3, 4])], dtype=object)

Este no es un arreglo muy útil para cómputo numérico. 
Mejor vamos a crear un arreglo unidimensional
más común:

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

>>> np.empty((3,))
array([7.74860419e-304, 7.74860419e-304, 7.74860419e-304])

.. note::

        Es importante recordar que ``empty()`` no llena el arreglo con ceros;
        el contenido depende del estado de la memoria asignada y, por lo tanto,
        **no se debe utilizar cuando necesitemos valores iniciales
        confiables**.

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

También podemos verificar el tipo de dato que NumPy asignó:

.. code-block:: python

    >>> evaluaciones.dtype
    dtype('float64')

A partir de este punto podremos aplicar operaciones vectorizadas sobre las
calificaciones: promedios, máximos, mínimos, normalización y muchas otras
operaciones típicas del análisis numérico.

slicing

Podemos ver las calificaciones de ``Joe`` y calcular su promedio utilizando
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

También podemos verificar el tipo de dato que NumPy asignó:

.. code-block:: python

    >>> evaluaciones.dtype
    dtype('float64')

A partir de este punto podremos aplicar operaciones vectorizadas sobre las
calificaciones: promedios, máximos, mínimos, normalización y muchas otras
operaciones típicas del análisis numérico.

slicing

Podemos ver las calificaciones de ``Joe`` y calcular su promedio utilizando
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

Operaciones básicas

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
nuevo arreglo con los valores actualizados. El arreglo original no se modifica,
a menos que asignemos el resultado a una variable:

.. code-block:: python

    >>> nuevas = evaluaciones + 1
    >>> nuevas
    array([[ 9.5, 10. ,  6. ],
           [11. ,  6. , 10. ],
           [ 7.5, 11. ,  9. ],
           [ 9. ,  5. , 10. ]])

El operador de adición es un alias de la función ``numpy.add``. Esta función
toma dos arreglos como operandos y aplica la operación elemento a elemento.
Cuando realizamos:

.. code-block:: python

    >>> evaluaciones + 1

el valor ``1`` se interpreta como un arreglo muy pequeño cuya forma es
compatible con la operación. NumPy realiza un proceso llamado *broadcasting*,
que consiste en ampliar de manera conceptual el arreglo más pequeño para que
coincida con la forma del arreglo más grande, sin copiar datos innecesariamente.

En otras palabras, NumPy "extiende" el escalar ``1`` para que actúe sobre cada
elemento de ``evaluaciones``:

.. code-block:: python

    >>> np.add(evaluaciones, 1)
    array([[ 9.5, 10. ,  6. ],
           [11. ,  6. , 10. ],
           [ 7.5, 11. ,  9. ],
           [ 9. ,  5. , 10. ]])

Este proceso de *broadcasting* es fundamental en NumPy, pues permite realizar
operaciones aritméticas entre arreglos de diferentes formas de manera muy
eficiente. Más adelante estudiaremos este mecanismo con mayor detalle.


Pandas
******

Matplotlib
**********
