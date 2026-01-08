.. role:: python(code)
   :language: python


Manejo de Archivos
==================

La mayoría de lenguajes de programación utiliza el concepto de "streams" para
implementar la funcionalidad general de entrada y salida de datos desde y hacia
los distintos dispositivos disponibles para nuestros programas.  Un **stream**
es un flujo secuencial de datos que puede venir de: un archivo, un dispositivo
de la red, la terminal e incluso de un buffer en memoria.  Una característica
importante de los "streams" es que accede a este flujo de datos de manera
incremental, lo que resulta esencial cuando los archivos son grandes o no caben
completamente en memoria.

Aunque python no utiliza la mayoría de las veces directamente el término "streams",
utiliza el modelo de streams internamante mediante el módulo :python:`io`. Este
módulo nos proveé de la funcionalidad básica de entrada/salida (I/O) implementando tres
subtipos: texto, binario y datos crudos ("raw"). En lugar de streams,
Python le llama :python:`file` (archivo) a los objetos concretos. Conceptualamente
le podemos llamar "streams" u objetos ``file-like``.

Los "streams" de Python incluyen los modos de acceso de ``solo lectura``, ``solo escritura``
y ``lectura escritura``. Además del acceso secuencial también se incluye el acceso aleatorio.

Texto
*****

Un "stream" de texto se especializa en leer y escribir objetos tipo :python:`str`.
En caso de leer o escribir a un origen o destino de datos tipo "bytes", es necesario
especificar de manera opcional el encoding, recordando que el encoding por defecto de Python
es ``utf-8``. Para crear un "stream" de texto se utiliza el método incluido :python:`open()`,
por ejemplo:

.. code-block:: python

   archivo = open("archivo.txt", "r", encoding="utf-8")

Como primer argumento enviamos una cadena con el nombre del archivo que vamos a abrir,
se puede incluir la ruta.

El segundo argumento indica el método de acceso: ``'r'`` para
solo lectura (valor por defecto) y ``'w'`` para solo escritura (si existe el archivo se sobre escribe). Para
agregar datos al final del archivo utilizamos ``'a'`` modo **append**. Para lectura y
escritura utilizamos ``'r+'``.

Como tercer argumento indicamos el encoding. De manera similar a lo visto en la sección de cadenas de
texto (ver :ref:`encode <encoding>`).

El procesamiento del texto también se encarga internamente de uniformizar como ``\n`` los saltos de línea leidos. Los
saltos se representan internamente como ``\n`` en Unix y ``\r\n`` en Windows.
Al escribir se convierten los saltos de línea de ``\n`` a la representación
específica del sistema operativo que estemos utilizando.

El método :python:`open()` regresa un objeto tipo `TextIOWrapper`_, que es una forma de stream de texto.

.. _TextIOWrapper: https://docs.python.org/3/library/io.html#io.TextIOWrapper

.. code-block:: python

   with open("archivo.txt", "r", encoding="utf-8") as archivo:
      for línea in archivo:  # lectura línea por línea = stream
         print(línea)

Es una buena práctica utilizar la palabra reservada :python:`with` cuando
abrimos objetos tipo :python:`file`. Este bloque nos protege ya que cierra el
stream al terminar el bloque sin importar si se lanzó alguna excepción, sin
necesidad de incluir un bloque ``try-finally``.

También podemos abrir un stream de texto en memoria:

.. code-block:: python

   >>> import io
   >>> buffer = io.StringIO()
   >>> buffer.write("Hola ") # Agregamos texto al buffer
   10
   >>> print("Mundo", file=buffer) # print agrega un salto de línea
   >>> buffer.seek(0) # Nos posicionamos al inicio del buffer
   0
   >>> buffer.read() # Leemos el buffer
   'Hola Mundo\n'

Binario
*******

Para crear un "stream" binario también utilizamos el método :python:`open()`
pero ahora incluimos la letra ``b`` en el parámetro de modo:

.. code-block:: python

   >>> f = open("imagen.png","rb")
   >>> imagen = f.read()
   >>> imagen
   b\'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x07X\x00\x00\x04\xc4\x08\xfb\xb

Este "stream" trabaja con objetos ``bytes-like`` por lo que no se realiza ningún
procesamiento adicionale de encoding, salto de línea o decoding. Podemos
utilizar este "stream" para todo tipo de archivos binarios como imágenes, video,
etc., o para operar sobre texto con una representación binaria.

Este "stream" nos brinda una lectura y escritura por bloques (buffers) por
lo que es más eficiente y práctico. Este es el método recomendado para el
procesamiento de datos binarios. Para ver con mayor detalle los métodos
disponibles podemos ver la documentación de  `BytesIO`_

.. _BytesIO: https://docs.python.org/3/library/io.html#io.BytesIO

Binario sin buffer
******************

Este "stream" binario no utiliza bloques y nos permite tener
un acceso a bajo nivel y control total del acceso.

.. note::

   En la práctica, la mayoría de las aplicaciones no requieren acceso binario
   sin buffer. Este tipo de stream se utiliza principalmente en sistemas de bajo
   nivel, drivers o implementaciones muy específicas.

Operaciones sobre archivos
**************************

Una de las operaciones más básicas es escribir datos en un archivo de texto:


.. code-block:: python

   >>> a = open("archivo.txt", "w", encoding="utf-8")
   >>> a.write("Esta es la primera línea\n")
   25
   >>> a.write("Esta es la segunda\n")
   19
   >>> a.close()

Una vez cerrado el archivo no podemos realizar operaciones en él:


.. code-block:: python

   >>> a.write("Esto es un error")
   Traceback (most recent call last):
   File "<python-input-4>", line 1, in <module>
      a.write("Esto es un error")
      ~~~~~~~^^^^^^^^^^^^^^^^^^^^
   ValueError: I/O operation on closed file.

Puedes comprobar que el archivo se grabó correctamente abriendolo en un editor de texto.

Ahora vamos a abrir el archivo para leerlo completo:


.. code-block:: python

   >>> a = open("archivo.txt", "r",encoding="utf-8")
   >>> a.read()
   'Esta es la primera línea\nEsta es la segunda\n'



Como estamos leyendo un "stream" una vez que consumimos todo el
flujo, estamos en el final del archivo y ya no podemos leer más:

.. code-block:: python

   >>> a.read()
   ''

Podemos posicionarnos al inicio del archivo con el método :python:`seek()`

.. code-block:: python

   >>> a.seek(0)
   0
   >>> a.read()
   'Esta es la primera línea\nEsta es la segunda\n'

También se puede recorrer el archivo línea por línea:

.. code-block:: python

   >>> a.seek(0)
   0
   >>> for línea in a:
   ...     print(línea)
   ...
   Esta es la primera línea

   Esta es la segunda

Hay dos saltos de línea ya que el método :python:`print()` agrega un salto y las
líneas del archivo incluyen un salto también. Podemos eliminar los
saltos utilizando el método :python:`str.rstrip()` teniendo cuidado de
cubrir los saltos de línea de Unix y Windows: :python:`línea.rstrip('\n\r')`.

En archivos de texto, el método :python:`seek()` solo puede dar saltos relativos
al inicio del archivo o moverse al final. En los archivos binarios se pueden
utilizar saltos a partir de otras posiciones.

Para probar esto vamos a crear un "buffer" binario:

.. code-block:: python

   >>> import io
   >>> b = io.BytesIO(b"0123456789abcdef\x00\x01")
   >>> b.seek(4)  # Avanzamos al cuarto byte
   4
   >>> b.read(2)  # Leemos dos bytes
   b'45'
   >>> b.tell()  # Vemos la posición actual
   6
   >>> b.seek(-2, 2) # Retrocedemos dos bytes con respecto al final del archivo
   16
   >>> b.read(1) # Leemos un byte
   b'\x00'

El método :python:`seek()` toma como primer argumento el "offset" y como segundo argumento
enviamos el punto de referencia: un valor de ``0`` indica el inicio del archivo o buffer,
``1`` indíca la posición actual y el valor ``2`` hace referencia al final del archivo.

Resumen del capítulo
--------------------

En este capítulo vimos cómo Python implementa el manejo de archivos y entrada/salida
mediante el concepto de *streams* u objetos ``file-like``. Aprendimos a:

- Abrir y cerrar archivos de texto y binarios de forma segura utilizando el
  administrador de contexto ``with``.
- Leer y escribir datos de manera secuencial sin cargar todo el contenido en memoria.
- Trabajar correctamente con codificaciones de texto y evitar errores comunes
  relacionados con Unicode.
- Utilizar streams en memoria para simular archivos y facilitar pruebas.
- Entender las diferencias entre streams de texto, binarios y de bajo nivel.

Estas herramientas son fundamentales para el procesamiento de datos, la manipulación
de archivos de gran tamaño y la integración con sistemas externos. En capítulos
posteriores las utilizaremos como base para el análisis de datos, el procesamiento
de texto avanzado y el cómputo distribuido.

