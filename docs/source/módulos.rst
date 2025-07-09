.. role:: python(code)
   :language: python

Módulos y Paquetes
==================

La descomposición de un programa en componentes independientes, no solo nos
permite dividir y en cierto modo reducir la complejidad de nuestro sistema.
También nos permite definir una frontera física sobre el código que implementa
cada componente creando una unidad básica de gestión. De tal manera que el
módulo puede estar protegido para que solo lo editen los programadores
responsables y  también se pueden controlar más facilmente las versiones y
cambios que se realicen en el módulo.

En Python un **módulo** se utiliza como la unidad física básica de
descomposición, ya que un módulo en Python es simplemente un archivo con
extensión ``.py``. En este archivo programamos la definición de los objetos que
componen el módulo los cuales queremos reutilizar en otros componentes o
programas.

Un módulo también puede ejecutarse como si fuera un script independiente e
incluye instrucciones que se ejecutan cuándo el módulo es incluido en otro
componente o programa o cuando se ejecuta directamente por el intérprete.

Veamos un ejemplo. Vamos a suponer que sumar (y restar) dos números es una
operación muy complicada que además utilizamos en varias partes de nuestro
programa. Decidimos crear un módulo dónde se incluyan estas dos funciones pues
consideramos que son parte del mismo problema y tienen mucha relación.
Definimos entonces el módulo ``aritmética.py`` con este código:

.. code-block:: python
   :caption: ``aritmética.py``.

   pi =  3.141592653589793 # Variable global

   def suma(a: int, b:int) -> int:
      return a + b

   def resta(a: int, b:int) -> int:
      return suma(a,-b)

Ahora podemos utilizar este módulo ejecutando el intérprete en la misma
ruta dónde está nuestro programa.

.. code-block:: python

   Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import aritmética
   >>> aritmética.suma(5,8)
   13
   >>> aritmética.resta(5,8)
   -3

Todos los módulos incluyen una variable global llamada ``__name__``:

.. code-block:: python

   >>> import aritmética
   >>> aritmética.__name__
   'aritmética'
   >>> __name__
   '__main__'

Como vemos, en caso de que módulo se haya ejecutado como un script
este tendrá el nombre de :python:`'__main__'`. Esto lo podemos utilizar
para ejecutar de manera selectiva código que queremos que se
ejecute en caso de que el módulo se ejecute como script:

.. code-block:: python
   :caption: ``aritmética.py``.

   pi =  3.141592653589793 # Variable global

   def suma(a: int, b:int) -> int:
      return a + b

   def resta(a: int, b:int) -> int:
      return suma(a,-b)

   if __name__ == "__main__":
      import sys
      suma(int(sys.argv[1]), int(sys.argv[2]))

Ahora ejecutemos el módulo ``aritmetica.py`` como script:

.. code-block:: bash

   $ python .\aritmética.py 12 900
   912

Los módulos contienen variables globales, que siguiendo
los principios del encapsulamiento, solo deberían ser para
uso privado del módulo. Sin embargo, es la tendencia en Python,
si sabemos lo que estamos haciendo, podemos modificar y leer estas
variables desde código externo al módulo.

.. code-block:: python

   >>> import aritmética
   >>> print(aritmética.pi)
   3.141592653589793
   >>> aritmética.pi = 3.1416
   >>> print(aritmética.pi)
   3.1416

Otras variantes de :python:`import`
***********************************

Hay distintas variantes de la instrucción :python:`import`, que afectan
la manera en la que se incluyen en el módulo actual los elementos importados.

Podemos incluir directamente en el espacio de nombres algunos de los
objetos definidos en el módulo externo, en esta versión el módulo no
se incluye al espacio de nombres:

.. code-block:: python

   >>> from aritmética import suma, resta
   >>> aritmética # No está definido localmente
   Traceback (most recent call last):
   File "<python-input-1>", line 1, in <module>
      aritmética
   NameError: name 'aritmética' is not defined
   >>> suma(2,3) # Se agrega la función 'suma()' al espacio de nombres local
   5

Podemos importar todos las definiciones con ``*``. Esto no es recomendable ya que se
podría ocultar o redefinir cierto nombre del espacio local.

.. code-block:: python

   >>> from aritmética import *
   >>> pi
   3.141592653589793

Podemos darle un alias local al nombre del módulo:

.. code-block:: python

   >>> import aritmética as m
   >>> m.pi
   3.141592653589793

Por último, podemos darle un alias a los nombres importados, de
nuevo, tenemos que tener cuidad de no acultar algún nombre:

.. code-block:: python

   >>> sum([1,2,3,4]) # Utilizamos la función 'built-in' sum()
   10
   >>> from aritmética import suma as sum
   >>> sum([1,2,3,4]) # Redefinimos así que ya no funciona
   Traceback (most recent call last):
   File "<python-input-4>", line 1, in <module>
      sum([1,2,3,4])
      ~~~^^^^^^^^^^^
   TypeError: suma() missing 1 required positional argument: 'b'
   >>> sum(2,3) # Cambió a sumar dos números.
   5

Encontrando al Módulo importado
*******************************

Como hemos visto, un módulo no es más que un archivo con extensión ``.py``.
Cuando ejecutamos la instrucción :python:`import` el intérprete de Python incia
una búsqueda para encontrar el archivo o módulo que especificamos.  El primer
lugar dónde se busca en el los módulos ``built-in``, estos nombres se encuentran
en la tupla :python:`sys.builtin_module_names`. Incluye módulos que se utilizan
bastante como :python:`array, math, sys, time, itertools`.  Al no encontrar el
nombre del módulo, busca un archivo en los directorios incluidos en la variable
:python:`sys.path`. Esta lista se incializa a partir de los siguientes datos:

   - El directorio dónde se encuentra el script desde dónde se llamó el :python:`import`. En caso de que no se esté corriendo un script, se busca en el directorio actual.

   - En las rutas especificadas en la variable de entorno ``PYTHONPATH``. De manera similar a ``PATH``.

   - El valor por defecto especificado al momento de la instalación. Es común buscar en el  directorio ``site-packages``.

El