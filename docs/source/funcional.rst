.. role:: python(code)
   :language: python


Programación Funcional
======================

A Python se le considera un lenguaje multiparadigma ya que tiene soporte para
varios estilos de programación. 

En un inicio hemos seguido un paradigma de programación predominantemente
**imperativo**. Este es un estilo muy báscio pues nuestros programas capturan su
estado utilizando variables y estructuras, y el flujo de nuestro programa avanza
ejecutando instrucciones paso a paso utilizando instrucciones de control. En
esta etapa de reconocimiento del lenguaje este estilo es apropiado ya hasta
práctico ya que los programas son muy básicos y no se requieren mecanismos de
abstracción para descomponer la complejidad. Se pueden utilizar variables
globales ya que no es un problema buscar y ver qué modifica a qué. 

.. code-block:: python 

   >>> x = 0 # variable local
   >>> for i in range(5):
   ...     x+= i # se modifica variable local
   ... 
   >>> x
   10


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


Aunque no hemos utilizado o mencionado conceptos de programación orientada a
objetos.  Python nos permite encapsular en objetos su estado y comportamiento.
Vimos a varios objetos como las listas. Las cuales tienen métodos, por ejemplo,
:python:`list.append()` con los cuales podemos modificar el estado del objeto.
En este caso agregando un elemento (o un objeto).  Podemos definir nuestros
propios tipos de objetos utilizando clases y herencia.  El lenguaje perimite de
manera naturar utilizar polimorfismo.

Programación Funcional
--------------------------


Programación Funcional




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
