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

Con la introducción de funciones y bloques, el paradigma de a progrmación sube
su nivel. Ahora seguimos un paradigma **procedural**. Las funciones nos permiten
enfocarnos en su funcionalidad externa, representada por su nombre, parámetros y
valor de retorno e ignorar los detalles de su implementación. Los bloques pueden
contener variables locales las cuales no son visibles desde bloques externos.
Podemos hacer una descomposición jerárquica de nuestro programa y dividirlo en
módulos (este tema lo veremos en otra sección). En este paradigma se reduce
bastante el uso de variables globales.

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


Python nos permite encapsular en objetos su estado y comportamiento.
Vimos a varios objetos como las listas. Las cuales tienen métodos, por ejemplo,
:python:`list.append()` con los cuales podemos modificar el estado del objeto.
En este caso agregando un elemento (o un objeto).  Podemos definir nuestros
propios tipos de objetos utilizando clases y herencia.  El lenguaje perimite de
manera naturar utilizar polimorfismo.

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
A
.. rubric::  Programación funcional


Python nos permite utilizar algunas carácteristicas del paradigma funcional aunque 
no lo podemos catalogar como un lenguaje funcional puro. Uno de las principales 
características es tratar a las funciones como objetos, recordemos lo de 
"las funciones son ciudadanos de primera clase":

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

En esta sección nos vamos a enfocar en las principales características
de la programación funcional que se implementan en Python como parte del
lenguaje.

Programación Funcional
-----------------------




Principales características:

.. rubric::  Las funciones son objetos

.. rubric::  Promueve las funciones sin efectos secundarios

.. rubric::  Inmutabilidad como principio

.. rubric::  Funciones de alto nivel

.. rubric::  Evita ciclos


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
