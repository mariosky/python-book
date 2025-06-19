.. role:: python(code)
   :language: python

Procesamiento de Texto
======================

Una de las especialidades de Python es el procesamiento de texto. El 
lenguaje es incluye en la librería estándar herramientas para la manipulación 
básica de las cadenas de caracteres y manipulación avanzadad utilizando expresiones regulares. 
Además existen librerías avalnzadas para el procesamiento del lenguaje 
natural. Desde la clásica NLTK a las más moderna spaCY. Además utiliza de manera 
nativa el formato unicode. En esta sección daremos un repazo rápido a estas 
herramientas. Aunque el lenguaje no es el más rápido para el procesamiento 
el ecosistema compensa esta desventaja, además se puede utilizar cómputo 
distribuido y multiprocesamiento en caso de ser necesario.

Operaciones básicas con cadenas de caracteres
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ya hemos visto que las cadenasd de caracteres son  secuencias inmutables parecidas a las 
tuplas y por lo tanto pueden utilizar los métodos que se aplican a estas. Pero además 
se incluyen muchas funciones útiles para operar sobre este tipo de datos. 
Veamos algunos ejemplos:

.. rubric:: str

Este método es un constructor que viene de fábrica y convierte a un objeto 
a su representación en forma de cadena de texto. La sintáxis básica es la 
siguiente:

.. code-block:: python
    
    str(objeto='', encoding='utf-8', errors='strict')

<objeto>
    Es el objeto que queremos convertir en una cadena de texto. En caso de que sea 
    un objeto definido por el usuario se intentará ejecutar el método :python:`__str__()` o 
    :python:`str()` que se debemos implementar o redefinir en su clase. 

<encoding>
    En el caso de que el objeto este representado como una cadena de bytes, debemos 
    especificar el tipo de codificación (encoding) que usa. Por defecto se utiliza el popular 'utf-8'. 
    Esto es útil por ejemplo, cuándo recibimos texto de una fuente externa como un archivo o una base de datos, 
    las cuales pueden enviar el texto codificado como bytes.

<errors>
    En caso de converión desde bytes, especificamos que tan estricta va a ser la gestión de los errores o que acción se realiza en caso de error. 
    En esta tabla se muestrán algunas opciones:

+------------------------+-------------------------------------------------------------+
| Modo                   | Descripción                                                 |
+========================+=============================================================+
| ``'strict'``           | Lanza un ``UnicodeDecodeError`` si hay bytes inválidos.     |
+------------------------+-------------------------------------------------------------+
| ``'ignore'``           | Ignora los errores y omite los caracteres problemáticos.    |
+------------------------+-------------------------------------------------------------+
| ``'replace'``          | Reemplaza errores con el carácter de reemplazo ``�``.       |
+------------------------+-------------------------------------------------------------+
| ``'backslashreplace'`` | Reemplaza errores con secuencias ``\xNN`` o ``\uNNNN``.     |    
+------------------------+-------------------------------------------------------------+
| ``'namereplace'``      | Reemplaza con el nombre Unicode del carácter:               |
|                        | ``\N{REPLACEMENT CHARACTER}``.                              |
+------------------------+-------------------------------------------------------------+


.. code-block:: python

    >>> nombre = 'José' 
    >>> nombre_bytes = nombre.encode( 'ascii')
    Traceback (most recent call last):
    File "<python-input-2>", line 1, in <module>
        nombre_bytes = nombre.encode( 'ascii')
    UnicodeEncodeError: 'ascii' codec can't encode character '\xe9' in position 3: ordinal not in range(128)
    >>> nombre_bytes = nombre.encode( 'Latin-1')
    >>> nombre_bytes
    b'Jos\xe9'
    >>> str(nombre_bytes)
    "b'Jos\\xe9'"
    >>> str(nombre_bytes, encoding='utf-8')
    Traceback (most recent call last):
    File "<python-input-6>", line 1, in <module>
        str(nombre_bytes, encoding='utf-8')
        ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: unexpected end of data
    >>> str(nombre_bytes, encoding='utf-8', errors='ignore')
    'Jos'
    >>> str(nombre_bytes, encoding='Latin-1', errors='ignore')
    'José'
    >>> 


.. rubric:: split

.. rubric:: join 

.. rubric:: replace 

Formato
^^^^^^^

Expresiones regulares
^^^^^^^^^^^^^^^^^^^^^

Tokenización 
^^^^^^^^^^^^




