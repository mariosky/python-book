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

El paradigma no tienen una definición estandarizada, pero normalmente un
lenguaje que sigue el paradigma funcional tiene o promueve las siguientes carácteristicas.

Principales características:

.. rubric::  Las funciones son objetos

Las funciones se pueden asignar a variables, pasar como argumentos y devolver
como resultado de otras funciones. Ya hemos visto varios ejemplos de esta funcionalidad.

.. rubric::  Las funciones no tienen efectos secundarios

Si seguimos la definición de una función matemática estas tienen algunas
propiedades importantes que nos permiten generalizar y establecer reglas para
verificar que las operaciones que realizamos con ellas son correctas (en un
contexto matemático). Hay dos carácteristicas que son
deseables también en las funciones que escribimos en nuestros programas (sean funcionales o no):

Para un mismo parámetro la función nos debería regresar exactamente el mismo
resultado. Incluso podríamos reemplazar directamente a la función (con el
parámetro correspondiente) por su valor de regreso y esto no debería tener
ningún efecto en el funcionamiento de nuestros programas. A esto se le llama transparencia
referencial.

Evaluar una función no debe modificar el comportamiento de otras funciones o el
suyo propio, no debe tener *efectos secundarios*. Decimos que una función tiene
efectos secundarios cuando modifica algún estado externo, por ejemplo, cuando
moficamos un archivo, una base de datos o una variable global.

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


Funciones puras
---------------

Funciones lambda
----------------

:python:`map()`, :python:`filter()`, :python:`reduce()`
-------------------------------------------------------

Listas por comprensión
----------------------

Expresiones Generadoras
-----------------------
