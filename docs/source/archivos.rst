.. role:: python(code)
   :language: python


Manejo de Archivos
==================

La mayoría de lenguajes de programación utiliza el concepto de "streams" para
implementar la funcionalidad general de entrada y salida de datos desde y hacia
los distintos dispositivos disponibles para nuestros programas.  Un **stream**
es un flujo secuencial de datos que puede venir de: un archivo, un dispositivo
de la red, la terminal e incluso de un buffer en momoria.  Una característica
importante de los "streams" es que accede a este flujo de de datos de forma
secuencial, sin necesidad de cargar todo el contenido en memoria.

Aunque python no utiliza la matoría de las veces directamente el término "streams",
utiliza el modelo de streams internamante mediante el módulo :python:`io`. Este
módulo nos proveé de la funcionalidad básica de entrada/salida (I/O) implementando tres
subtipos: texto, binario y datos crudos ("raw"). En lugar de streams,
Python le llama :python:`file` (archivo) a los objetos concretos. Conceptulamente
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



