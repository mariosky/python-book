.. role:: python(code)
   :language: python


Programación Funcional
======================

A Python se le considera un lenguaje multiparadigma ya que tiene soporte para
varios estilos de programación.

.. rubric::  Programación procedural

En un inicio hemos seguido un paradigma de programación predominantemente
**imperativo**. Este es un estilo muy báscio pues nuestros programas capturan su
estado utilizando variables y estructuras, y el flujo de nuestro programa avanza
ejecutando instrucciones paso a paso utilizando estructuras de control.

Hasta este momento en el que estamos conociendo las características básicas del
lenguaje Python este estilo de programación es adecuado e incluso práctico ya
que los programas son muy básicos y no se requieren mecanismos de abstracción
que utilizaríamos en proyectos empresariales dónde necesitamos descomponer la
complejidad de un sistema. En este caso podemos utilizar variables globales ya
que no es mucho problema buscar en el código y ver qué modifica a qué.

.. code-block:: python

   >>> x = 0 # variable local
   >>> for i in range(5):
   ...     x+= i # se modifica variable local
   ...
   >>> x
   10

.. note:::

   Como vemos en este ejemplo, la variable ``x`` cambia de estado (valor) varias
   veces durante el transcurso del programa. Esta es una característica que trata de evitar la
   programación funcional.

.. rubric::  Programación procedural

Con la introducción de funciones y bloques, el paradigma de a programación sube
su nivel de abstracción. Ahora seguimos un paradigma **procedural**. Las
funciones nos permiten enfocarnos en su funcionalidad externa, representada por
su nombre, parámetros y valor de retorno. Podemos entonces ignorar los detalles
de su implementación interna y nos enfocamos en la funcionalidad a un nivel más
arriba.  Los bloques pueden contener variables locales las cuales no son
visibles desde bloques externos.  Podemos hacer una descomposición jerárquica de
nuestro programa y dividirlo en módulos (este tema lo veremos en otra sección).
En este paradigma se reduce bastante el uso de variables globales.

.. code-block:: python

   >>> def suma_enteros(n):
   ...     x = 0
   ...     for i in range(n):
   ...         x+=i
   ...     return x
   ...
   >>> suma_enteros(5)
   10

.. tip::

   Tal vez te diste cuenta que este método se podría simplificar
   utilizando algo como la *suma de Gauss*:

   .. math::

      \sum_{k=1}^{n} k = 1 + 2 + 3 + \dots + n = \frac{n(n+1)}{2}

.. rubric::  Programación Orientada a Objetos


Python nos permite encapsular el estado de un sistema en distintos objetos, cada
uno con su propio estado interno y comportamiento privado responsable de
manipular el estado interno del objeto.  En los ejercicios anteriores, ya
utilizamos a varios objetos, como las listas o las cadenas de texto. Estos
objetos tienen métodos, por ejemplo, :python:`list.append()` con los cuales
podemos modificar el estado del objeto.  En este caso agregando un elemento (o
un objeto) a la lista. Algo importante es que no podemos agregar directamente un
objeto a la lista, lo debemos hacer mediante alguno de sus métodos.  En Python
entonces, podemos definir nuestros propios tipos de objetos utilizando clases y
herencia.  El lenguaje también perimite de manera naturar utilizar polimorfismo.

.. code-block:: python

   >>> class Persona:
   ...     def __init__(self, nombre):
   ...         self.nombre = nombre
   ...     def saluda(self):
   ...         print(f"Hola, soy {self.nombre}")
   ...
   >>> ana = Persona("Ana")
   >>> ana.saluda()
   Hola, soy Ana

.. note::

   Aunque no hemos utilizado o mencionado conceptos de programación orientada a
   objetos (esto lo haremos en la sección correspondiente) este es un paradigma que
   Python implementa ampleamente.

.. rubric::  Programación funcional

Python nos permite utilizar algunas carácteristicas del paradigma funcional
aunque no lo podemos catalogar como un lenguaje funcional puro. Uno de las
principales características es tratar a las funciones como a cualquier objeto,
recordando lo de "las funciones son ciudadanos de primera clase":

.. code-block:: python

   >>> def triplíca(x):
   ...     return x*x*x
   ...
   >>> def llama_funcion(f, x):
   ...     return f(x)
   ...
   >>> print(llama_funcion(triplíca, 3))
   27
   >>>

En esta sección nos vamos a enfocar en las principales características de la
programación funcional y como se implementan en Python.

Programación Funcional
-----------------------

El paradigma no tiene una definición estandarizada, las funciones siguen siendo
un mecanismo de modularidad y reutilización de código, pero desincentivando el
uso de los elementos imperativos que encontramos en el paradígma procedural.
Este estilo de programación surge de ambientes académicos, como una evolución
del cálculo lambda sobre el cual se inspira el diseño de Lisp y recientemente
teoría de categorías con el lenguaje Haskell (lenguaje funcional puro). Otros
lenguajes representativos con características funcinales son: Clojure, Scala y
Erlang/Elixir.  Normalmente un lenguaje que sigue el paradigma funcional tiene o
promueve las siguientes carácteristicas.

.. rubric::  Las funciones son objetos

Las funciones se pueden asignar a variables, pasar como argumentos y devolver
como resultado de otras funciones. Ya hemos visto varios ejemplos de esta funcionalidad.

.. rubric::  Funciones puras

Si seguimos la definición de una función matemática estas tienen algunas
propiedades importantes que nos permiten generalizar y establecer reglas para
verificar que las operaciones que realizamos con ellas son correctas (en un
contexto matemático). Hay dos carácteristicas que son
deseables también en las funciones que escribimos en nuestros programas (sean funcionales o no):

- Evaluar una función no debe modificar el comportamiento de otras funciones o el
  suyo propio, no debe tener *efectos secundarios*. Decimos que una función tiene
  efectos secundarios cuando modifica algún estado externo, por ejemplo, cuando
  moficamos un archivo, una base de datos o una variable global.

- Para un mismo parámetro la función nos debería regresar exactamente el mismo
  resultado. Incluso podríamos reemplazar directamente a la función (con el
  parámetro correspondiente) por su valor de regreso y esto no debería tener
  ningún efecto en el funcionamiento de nuestros programas. A esto se le llama transparencia
  referencial.


.. rubric::  Inmutabilidad como principio

La mutabilidad aunque es natural en los paradigmas inperativos y orientados a
objetos (de manera controlada en estos últimos) en los lenguajes funcionales se
trata de eliminar ya que se argumenta que es esta es la causa de muchos errores
o bichos (bugs) en estos otros paradigmas.

.. rubric::  Funciones de alto nivel

El la programación funcional es común que escribamos funciones generadoras cuyo
propósito sea precisamente generar nuevas funciones. Las funciones generadas
incluso pueden hacer referencia a objetos que se definieron en el contexto de la
función generadora (aunque esta función ya se ejecutó).  A este concepto se le
llama clausura (clousure). También se utilizan **funciones anónimas** cuyo propósito
es generar una función al mismo tiempo que se envía como argumento o se regresa
como resultado.

.. rubric::  Evita ciclos con recursividad

En lugar de promover los ciclos con estructuras como ``for`` o ``while``, en la
programación funcional se promuebe el uso de distintas variantes de
recursividad.


.. rubric::  Evaluación `Lazy`

Los lenguajes pueden realizar evaluación estricta (en inglés se les conoce com eager) o evaluación
no estricta (lazy). En la evaluación estricta, todos los componentes y subcomponentes
de una expresión son evaluados. En la evaluación no estricta, no se evaluan los términos
hasta que sea absolutamente necesario. Por ejemplo, la siguiente instrucción
en Python falla, debido que hay una división entre cero en el tercer elemento
de la lista:

.. code-block:: python

   >>> print(len([1,2,3/0]))
   Traceback (most recent call last):
   File "<python-input-10>", line 1, in <module>
      print(len([1,2,3/0]))
                     ~^~
   ZeroDivisionError: division by zero
   >>>

Si se utilizara evaluación no estricta, la instrucción no fallaría ya que
no es necesario realizar la división para conocer el tamaño de la lista.

Python utiliza evaluación no estrícta en el uso de operadores lógicos,
por ejemplo aquí no hay problema aunque también se incluye la división
entre cero en la instrucción:

.. code-block:: python

   >>> if True or 3/0: print('True')
   ...
   True

En los lenguejes funcionales que utilizan evaluación `lazy`, se pueden
definir estructuras como listas infinitas sin problema, por ejemplo, en
Haskell:


.. code-block:: haskell

   naturales = [0..]           -- lista infinita
   take 5 naturales            -- [0,1,2,3,4]

En el resto del capítulo vamos a ver ejemplos en Python del uso
de algunos elementos de programación funcional.

.. note::

   Este capitulo solo toca la superficie del tema, para más información te
   recomiendo otros libros:

Funciones lambda
----------------

Cuando queremos definir una función al mismo tiempo que la envíamos como
parámetro, la más práctico es que pasemos una función lambda. Las funciones lambda son
simplemente funciones anónimas que son utilizadas para enviarse como parámetro
y no tenemos la intención de rutilizar dicha función en otros contextos.

Veámoslo con un ejemplo. Vamos a suponer que tenemos una lista
de películas y los datos de cada película los guardamos simplmente en
una tupla:

.. code-block:: python

   >>> peliculas = [
   ...    ('1', 'How to Train Your Dragon', 2025, ('Action', 'Family', 'Fantasy'), '2h 5m', 80),
   ...    ('3', 'Prisoners', 2013, ('Drama', 'Thriller', 'Crime'), '2h 33m', 81),
   ...    ('10', 'The Substance', 2024, ('Drama', 'Horror', 'Science Fiction'), '2h 21m', 71),
   ...             ]

Si ordenamos la lista *in place* y luego la imprimimos, vemos que el órden se
establece ordenando por el primer elemento de la tupla y en este caso como son
cadenas de caracteres se ordenan lexicográficamente por el identificador.

.. code-block:: python

   >>> peliculas.sort()
   >>> for p in peliculas:
   ...    print(p)
   ...
   ('1', 'How to Train Your Dragon', 2025, ('Action', 'Family', 'Fantasy'), '2h 5m', 80)
   ('10', 'The Substance', 2024, ('Drama', 'Horror', 'Science Fiction'), '2h 21m', 71)
   ('3', 'Prisoners', 2013, ('Drama', 'Thriller', 'Crime'), '2h 33m', 81)


Si queremos ordenar la lista, por año debemos pasar como argumento una función
que tome como parámetro una lista y nos regrese el elemento sobre el cual queremos ordenar los elementos.

Esta función puede ser la siguiente:

.. code-block:: python

   >>> def select_año(pelicula):
   ...    return pelicula[2]
   ...

La función toma como argumento la tupla con la información de la película y nos regresa el tercer elemento.

.. code-block:: python

   >>> peliculas.sort(key=select_año)
   >>> for p in peliculas:
   ...    print(p)
   ...
   ('3', 'Prisoners', 2013, ('Drama', 'Thriller', 'Crime'), '2h 33m', 81)
   ('10', 'The Substance', 2024, ('Drama', 'Horror', 'Science Fiction'), '2h 21m', 71)
   ('1', 'How to Train Your Dragon', 2025, ('Action', 'Family', 'Fantasy'), '2h 5m', 80)

En lugar de tener que definir la función `select_año`, podemos enviar una función anónima
escrita de una manera mucho más compacta. Por ejemplo, para ordenar por
título, podriamos llamar a `peliculas.sort()` utilizando la palabra `lamda` de esta manera:

.. code-block:: python

   >>> peliculas.sort(key=lambda peliculas: peliculas[1])
   >>> for p in peliculas:
   ...    print(p)
   ...
   ('1', 'How to Train Your Dragon', 2025, ('Action', 'Family', 'Fantasy'), '2h 5m', 80)
   ('3', 'Prisoners', 2013, ('Drama', 'Thriller', 'Crime'), '2h 33m', 81)
   ('10', 'The Substance', 2024, ('Drama', 'Horror', 'Science Fiction'), '2h 21m', 71)

Las funciones lambda siguien esta sintaxis en Python:

.. code-block:: python

   lambda <lista de parámetros> : <cuerpo de la función>

<lista de parámetros>
   Es una lista opcional de parámetros separados por una coma.
   Al igual que en una función regular el símbolo de dos puntos `:` separa al
   cuerpo de la lísta de parámetros.

<cuerpo de la función>
   El cuerpo de la función debe ser solo una línea de código
   y es el valor que regresa la función.

Al ser una versión anónima y compacta de una función, es recomendable utilizarlas
para código que sea fácilmente entendible. En caso de requerir algo más elaborado
se recomienda utilizar una función convencional.

.. note::
   Recordemos que las funciones `lambda` son objetos, por lo que podemos regresarlas
   como valor de retorno de otra función o incluso ejecutarlas al mismo tiempo que las
   definimos:

   .. code-block:: python

      >>> def crea_suma():
      ...    return lambda a, b: a + b
      ...
      >>> crea_suma()(2,3)
      5
      >>> (lambda a, b: a + b)(2,3)
      5


:python:`map()`, :python:`filter()`, :python:`reduce()`
-------------------------------------------------------

:python:`map()`
^^^^^^^^^^^^^^^

El método :python:`map()` incluido de fábrica incorpora un estilo
funcional que es muy utilizado en Python. Veamos un ejemplo donde comparamos
un programa con un estilo *imperativo* versus la versón *funcional*:

Tenemos la tarea de producir una nueva lista que contenga solo los títulos de las
películas extraídos de la lista `peliculas` creada anteriormente. Una manera
imperativa para ralizar esta tarea sería la siguiente:

.. code-block:: python

   >>> peliculas
   [('1', 'How to Train Your Dragon', 2025, ('Action', 'Family', 'Fantasy'), '2h 5m', 80), ('3', 'Prisoners', 2013, ('Drama', 'Thriller', 'Crime'), '2h 33m', 81), ('10', 'The Substance', 2024, ('Drama', 'Horror', 'Science Fiction'), '2h 21m', 71)]
   >>> titulos = []
   >>> for p in peliculas:
   ...    titulos.append(p[1])
   ...
   >>> titulos
   ['How to Train Your Dragon', 'Prisoners', 'The Substance']
   >>>

Vamos a tratar de reconocer algunos elementos de este código que no concuerdan
con el paradigma funcional:

   - Declaramos a ``titulos``, recordemos que es un objeto mutable. Esto no es recomendado en el paradigma.
   - Tenemos un ciclo ``for`` que de manera explicita (imperativa) modificamos el estado (mutamos) de la lista. Esto
     es mejor que el estilo mucho más imperativo de utilizar un índice el cual vamos modificando en cada iteración.
   - Podemos decir que el bloque dentro del ciclo tiene 'efectos colaterales' ya que modifica el estado de la lista.


Ahora vamos a resolver el mismo problema pero siguiendo un estilo funcional. Una
manera de relizar esto es utilizando la función :python:`map()` la cual sirve
precisamente para este tipo de problemas. Esta función genera un objeto tipo
:python:`map` el cual es **iterable** pero **inmutable**. La función toma como primer
parámetro una función la cual se aplica de manera secuencial a al iterable que
se pasa como segundo parámetro y con esto se genera el objeto :python:`map` antes
mencionado.

Por ejemplo:

.. code-block:: python

   >>> map(int, ['1', '2', '3', '4'])
   <map object at 0x0000022FCEE461A0>
   >>> list(map(int, ['1', '2', '3', '4']))
   [1, 2, 3, 4]

En este ejemplo :python:`map()` toma al métod ``int`` y lo aplica a todos
los elementos de la lista. Vemos como la lista contiene enteros pero
expresado como cadenas de texto. La función regresa un objeto tipo :python:`map`.
Para visualizarlo podemos construir una lista a partir del objeto :python:`map`.

Utilicemos map para resolver el problema anterior:

.. code-block:: python

   >>> list(map(lambda p: p[1], peliculas))
   ['How to Train Your Dragon', 'Prisoners', 'The Substance']

Veamos las características funcionales de este código:
   - No utiliza objetos mutables para la generación de la lísta. En este caso no es
     necesario tener que definir la lista ``titulos``.
   - No utiliza ciclos para ir mutando el estado de la lista intermedia ``titulos``.
   - Utiliza la función :python:`map()` la cual recibe como parámetro una función anónima (las funciones son objetos).
   - Se sigue además un estilo declarativo muy compacto.

:python:`filter()`
^^^^^^^^^^^^^^^^^^^

De manera similar a :python:`map()`, la función toma como primer parámetro una función de prueba que sirver para filtrar
elementos del iterable que se recibe como segundo argumento. La función de prueba debe regresar verdadero para
que el elemento se incluya en el resultado. Por ejemplo, para regresar las películas más recientes
que el año 2023. Podemos hacer lo siguiente:

.. code-block:: python

   >>> list(filter(lambda p: p[2]>2023, peliculas))
   [('1', 'How to Train Your Dragon', 2025, ('Action', 'Family', 'Fantasy'), '2h 5m', 80), ('10', 'The Substance', 2024, ('Drama', 'Horror', 'Science Fiction'), '2h 21m', 71)]
   >>>

Podemos anidar las funciones:

.. code-block:: python

   >>> list(map(lambda p: p[1], filter(lambda p: p[2]>2023, peliculas)))
   ['How to Train Your Dragon', 'The Substance']



Listas por comprensión
----------------------

Expresiones Generadoras
-----------------------
