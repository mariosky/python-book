.. role:: python(code)
   :language: python


NumPy
*****

Cómputo numérico en Python
=================================

Durante más de cinco décadas, **Fortran** ha sido el lenguaje estándar 
del cómputo científico y de alto rendimiento. Bibliotecas clásicas como **BLAS** y 
**LAPACK**, escritas en Fortran, continúan siendo la referencia cuando queremos 
hecer operaciones vectoriales y matriciales. Incluso, herramientas comerciales 
como *MATLAB*, *Maple* o *Mathematica* se basan en estas librerías y tienen el 
objetivo de hacer su programación más amigable. La desventaja 
que tienen es que crean una dependencia del proveedor y vam en contra de 
la práctica de la **ciencia abierta** que nos interesa promoveer.

La tendencia actual es movernos hacia alternativas libres como 
**GNU Octave** o **SageMath**, y hacia lenguajes diseñados para el análisis 
numérico (*Julia*) o estadístico (*R*). En este panorama, **Python** se ha 
consolidado como uno de los lenguajes más utilizados gracias a su sencillez, 
su comunidad y su ecosistema científico. Muchas de las librerías científicas 
de  Python tienen en su núcleo a la librería **NumPy**.

NumPy nos proporciona:

* Un tipo de dato eficiente para arreglos **N-dimensionales** (``ndarray``).
* Operaciones vectorizadas implementadas en C/Fortran para mejorar el rendimiento.
* Funciones de **álgebra lineal**, transformadas de Fourier y generación 
  de números aleatorios.
* **Broadcasting**, para operar arreglos de diferentes formas.
* Integración con código en C, C++ y Fortran.
* Licencia abierta **BSD**, compatible con la ciencia abierta.

NumPy es la base de librerías como **SciPy**, **pandas**, 
**matplotlib**, **scikit-learn**, **JAX**, **PyTorch** y **TensorFlow**, 
especializadas en programación científica, análisis de 
datos y aprendizaje automático. Para simplificar la instalación y 
configuración de estas herramientas se han creado distribuciones de Python como 
**Enthought**, **Anaconda** y **SageMath**. 

En esta sección vamos a familiarizarnos con los **arreglos multidimensionales** 
de NumPy, ya que son la base para librerías que veremos posteriormente.


NumPy: el arreglo ``ndarray``
---------------------------------

Python incluye estructuras tipo secuencia como las listas, pero presentan 
dos limitaciones importantes para el cómputo numérico:

1. Pueden contener **elementos de distinto tipo**.
2. Sus sublistas pueden tener **longitudes diferentes**.

Por ejemplo::

.. code-block:: python

    >>> objetos = [[2, 3, 4],
    ...            [5, 5],
    ...            ['Hola, Mundo', 13],
    ...            [3]]

Aunque la lista es flexible, esta estructura no es muy adecuada para
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
  aceleración mediante rutinas BLAS/LAPACK.

Vamos a crear una lista compatible con un ``ndarray``::

.. code-block:: python

    >>> arreglo_nums = [[1, 2, 3],
    ...               [2, 2, 4],
    ...               [2, 3, 11],
    ...               [2, 1, 4]]


A partir de esta lista será posible crear un arreglo NumPy y realizar 
operaciones vectorizadas de forma eficiente, tal como se espera en la 
programación científica moderna.





Pandas
******

Matplotlib
**********


