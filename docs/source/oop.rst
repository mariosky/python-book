.. role:: python(code)
   :language: python

Programación Orientada a Objetos en Python
==========================================

Como ya hemos visto, Python *no* es un lenguaje orientado a objetos (OO) puro.
Podemos programar scripts en los cuales  no es necesario utilizar el paradigma
explicitamente.  Aunque los tipos de datos, estructuras e incluso las funciones
son objetos, no es necesario implementar una clase principal o métodos miembro
para poder escribir un programa. Incluso parecería que la implementación del
paradigma es un agregado de último momento. Un parche. Esta impresión radica (en
mi opinión) en la sintáxis para expresar algunos elementos,
como los constructores, el páso de una referencia (:python:`self`) en la
definición métodos miembro, entre otras.

Un aspecto crucial de la Programción Orientada a Objetos es el tipado estrícto.
Esto ocasiona que tengamos que utilizar mecanismos elaborados para hacer
cosas que en un lenguaje dinámico se hacen muy fácilmente. Por ejemplo,
el polimorfismo, plantillas o el uso de interfaces. Un programador
experimentado sabe que todas estas 'libertades' pueden traer problemas, pero al
mismo tiempo nos permiten el desarrollo de programas *sin tanto verbo* (del inglés verbose).

Por esta razón, creo que Python puede no ser el mejor lenguaje para aprender
Programación Orientada a Objetos (POO), ya que muchos de los temas o elementos de
programación no tienen una aplicación directa.  Por otro lado, el hecho de que
el paradigma sea *opcional* evita que se establezcan reglas de acción para
solucionar problemas de una manera más o menos estándar, ya que hay varias
formas de hacer todo. Entonces, creo que esta sección no debería ser
tan extensa como en los libros de otros lenguajes ya que los elementos de POO
en Python no son tan extensos. El enfoque estará en ver y enteder las
diferencias entre paradigmas en términos de programación.

.. note::
    A lo largo del libro veremos que si hay un estilo de programación en Python,
    pero al igual que el lenguaje es algo libre e híbrido.

Ámbitos y espacios de nombres en Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
La documentación oficial de Python aborda este importante tema en la sección
de definición de  `clases <https://docs.python.org/es/3.13/tutorial/classes.html#python-scopes-and-namespaces>`_.
En este libro vamos a seguir la misma estructura ya que es una manera interesante
de abordar las diferencias entre los paradigmas procedural/funcional y el orientado a objetos.
Entender muy bien estos conceptos nos hará mejores programadores independientemente
del paradigma que utilicemos. Primero es importante definir que es un espacio de nombres y
después el ámbito de visibilidad que hay entre ellos.

Iniciemos una nueva sesión del interprete y como primera instrucción vamos a
ejecutar el método incluido de fábrica :python:`dir()`.
Cuando invocamos esta función sin argumentos, nos regresa una lista
de cadenas que representan los nombres definidos en el ámbito actual:

   >>> dir()
   ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']

Estos son los **nombres** disponibles **en ese punto del programa**. Entre estos nombres
encontramos: variables internas, módulos cargados automáticamente y
otros elementos del contexto de ejecución. Es comprender esta idea fundamental:

.. note::

   En todo momento, nuestro programa opera dentro de un **ámbito limitado** de nombres.

   La función dir() nos permite asomarnos a ese ámbito y conocer qué
   identificadores están definidos y disponibles en este momento.

Vamos a crear algunos nombres adicionales en este ámbito.

   >>> entero = 1234
   >>> nombre = 'Ana'

Como es de esperarse estos nombres se agregan al ámbito actual:
   >>> dir()
   ['__annotations__', '__builtins__', 'entero',  'nombre']
   # El resultado se recortó para que no ocupe tanto espacio.

Incluso podemos agregar una función:

   >>> def genera_correo(n):
   ...     dominio = 'gmail.com'
   ...     print(dir())
   ...     return f'{n}@{dominio}'
   ...
   >>> dir()
   ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'entero', 'genera_correo', 'nombre']

Esta función incluye la variable local :python:`dominio` y el argumento :python:`n`. Es importante notar que estos dos nombres,
**no están disponibles en el ámbito actual**.

Como demostración en la función :python:`genera_correo(n)` se imprime el resultado de :python:`dir()`:

   >>> genera_correo('juan')
   ['dominio', 'n']
   'juan@gmail.com

Ahora, como es de esperarse, solo se imprimen los nombres :python:`['dominio',
'n']`.  Estos dos nombres están ocultos, no se pueden modificar ni leer desde
fuera. Solo las instrucciones dentro del ámbito pueden hacerlo.  Este es un
principio importante de la programación estructurada y la programación orientada
a objetos:

**Ocultación de la información (information hiding)**

   Es un principio por el cual se separan los detalles de implementación de los
   detalles de uso, de modo que los componentes de un programa solo acceden a lo
   que necesitan saber, y no a los mecanismos internos de otros componentes

En este ejemplo, si necesitamos crear un correo electrónico, solo podemos ver
el nombre de la función y su parámetro. Pero no tenemos control sobre lo que sucede
dentro, los detalles de implementación. Esto puede permitir a los programadores
mejorar la implementación interna sin afectar al resto del programa. Por ejemplo,
vamos a mejorar un poco la implementación:

   >>> def genera_correo(n, dominio='gmail.com'):
   ...    return f'{n}@{dominio}'
   ...

Ahora podemos enviar como segundo parámetro el dominio del correo y por defecto
se pasa :python:`'gmail.com'` de esta manera, algunas
partes del programa seguiran llamando a la función de la manera anterior sin
que les afecte el nuevo cambio. Y en otras partes se puede utilizar de la nueva manera.


   >>> genera_correo('juan')
   'juan@gmail.com'
   >>> genera_correo('juan','hotmail.com')
   'juan@hotmail.com'

Al ocultar los detalles de implementación evitamos que los usuarios de nuestras funciones
dependan de las decisiones que tomemos internamente y que no les afecten los cambios.

En el caso de variables locales como las de la función anterior. Se crean al momento de
llamar a la función y se eliminan cuando la función regresa o se lanza alguna excepción.
También hay ambitos de nombres que tienen una vida más duradera, por ejemplo, los
nombres de fabrica (``builtins``), se crean al iniciar el intérprete y nunca se destruyen.



