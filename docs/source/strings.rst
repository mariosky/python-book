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

Ya hemos visto que las cadenasd de caracteres son  secuencias inmutables parecidas a las 
tuplas y por lo tanto pueden utilizar los métodos que se aplican a estas. Pero además 
se incluyen muchas funciones útiles para operar sobre este tipo de datos. 
Veamos primero las funciones básicas para crear y leer cadenas de caracteres:

Operaciones básicas crear y codificar de caracteres
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. rubric:: :python:`str(objeto='', encoding='utf-8', errors='strict')`

Este método es un constructor que viene de fábrica y crea una cadena de caracteres a partir 
de un objeto. La sintáxis básica es la siguiente:

.. code-block:: python
    
    str(objeto='', encoding='utf-8', errors='strict')

<objeto>
    Es el objeto que queremos representar como una cadena de texto. En caso de que sea 
    un objeto definido por el usuario se intentará ejecutar el método :python:`__str__()` o 
    :python:`str()` que se deberíamos implementar o redefinir en su clase. 

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

.. rubric:: :python:`str.encode(encoding='utf-8', errors='strict')`

Con este método un objeto tipo cadena de caracteres se convierte en una cadena de bytes.
La sintáxis básica es muy similar a la del método :python:`str` pero en este caso solamente 
especificamos el tipo de codificación que queremos utilizar y el modo de gestión de errores. 
En caso de que el objeto este representado como una cadena de bytes, y busquemos hacer 
la conversión inversa utilizamos el método :python:`str.decode`. Veamos un ejemplo:

Vamos a crear una cadena de caractéres que incluye un acento. En este caso ``José``. Como 
estamos utilizando el valor literal de la cadena, el intérprete codifica la cadena como utf-8 y 
representa al carácter ``é`` correctamente. 

.. code-block:: python

    >>> nombre = 'José' 
    >>> nombre 
    'José' 

Si intentamos convertir la cadena a una cadena de bytes utilizando el método :python:`encode` 
con el tipo de codificación ``ascii`` obtenemos un error. Esto es porque el método ``encode`` 
no puede representar el caracter ``é`` en ``ascii``.

    >>> nombre_bytes = nombre.encode( 'ascii')
    Traceback (most recent call last):
    File "<python-input-2>", line 1, in <module>
        nombre_bytes = nombre.encode( 'ascii')
    UnicodeEncodeError: 'ascii' codec can't encode character '\xe9' in position 3: ordinal not in range(128)

Si ahora utilizamos el tipo de codificación ``Latin-1`` podemos representar el carácter ``é``:

    >>> nombre_bytes = nombre.encode( 'Latin-1')
    >>> nombre_bytes
    b'Jos\xe9'
    >>> str(nombre_bytes)
    "b'Jos\\xe9'"

Notamos que si imprimimos la cadena de bytes obtenemos una cadena de caracteres que incluye 
la representación del caracter ``é`` como ``\xe9``. Ahora vamos a suponer que por error, 
queremos convertir a una cadena utilizando ``str`` pero utilizando una codificación 
incorrecta:

    >>> str(nombre_bytes, encoding='utf-8')
    Traceback (most recent call last):
    File "<python-input-6>", line 1, in <module>
        str(nombre_bytes, encoding='utf-8')
        ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: unexpected end of data

Podemos, cambiar el tipo de gestión de errores a ``ignorar``:

    >>> str(nombre_bytes, encoding='utf-8', errors='ignore')
    'Jos'

Como vemos se ignora el caracter problemático. Enviemos la codificación correcta:

    >>> str(nombre_bytes, encoding='Latin-1', errors='ignore')
    'José'
    >>> 

En este ejemplo hemos visto como aunque Python utiliza por defecto una codificación estándar 
y que puede representar muchos tipos de caracteres, hay que tener cuidado al leer o escribir 
datos codificados en otros formatos. 

.. rubric:: :python:`string.split(separator, maxsplit)`

El método :python:`split` crea una nueva lista,  cortando en pedacitos la cadena original.
Los cortes se hacen utilizando un *separador*, por defecto el separador es uno o más espacios en blanco.
Veamos un ejemplo:

    >>> 'Hola, ¿qué tal?, esta es una    palabra   separada con algunos espacios.' 
    'Hola, ¿qué tal?, esta es una    palabra   separada con algunos espacios.'
    >>> texto = 'Hola, ¿qué tal?, esta es una    palabra   separada con algunos espacios.' 
    >>> texto.split()
    ['Hola,', '¿qué', 'tal?,', 'esta', 'es', 'una', 'palabra', 'separada', 'con', 'algunos', 'espacios.']

El objeto utiliza el espacio como separador. Fíjate como elimina múltiples espacios.

    >>> texto.split(',')
    ['Hola', ' ¿qué tal?', ' esta es una    palabra   separada con algunos espacios.']
    >>> texto.split(' ') # El separador es un espacio 
    ['Hola,', '¿qué', 'tal?,', 'esta', 'es', 'una', '', '', '', 'palabra', '', '', 'separada', 'con', 'algunos', 'espacios.']

En caso de incluir el caracter de espacio ` ` como separador, se agregan a la lista cadenas vacías.
Cuando veamos el tema de expresiones regulares vamos a ver como atacar este tipo de casos.

.. rubric:: :python:`string.join(iterable)`

Por otro lado, si tenemos una lista de cadenas de caracteres, podemos construir una sola cadena concatenando 
los elementos de la lista. En este caso, el objeto que realiza la operación es el caracter separador, que en 
esta operación se debería llamar caracter de unión: 

    >>> lista = texto.split()
    >>> lista
    ['Hola,', '¿qué', 'tal?,', 'esta', 'es', 'una', 'palabra', 'separada', 'con', 'algunos', 'espacios.']
    >>> '#'.join(lista) 
    'Hola,#¿qué#tal?,#esta#es#una#palabra#separada#con#algunos#espacios.'
    >>> 

.. rubric:: replace 

Podemos crear una nueva cadena de texto reemplazando uno o más caracteres del texto original: 
    >>> texto = 'Estudio en el Tec' 
    >>> texto = texto.replace('Tec', 'TecNM')  
    >>> texto
    'Estudio en el TecNM'

.. attention:: 
    Recuerda que debemos reasingar el texto generado por :python:`str.replace()` 
    al nombre ``texto`` ya que las cadenas de caracteres son **inmutables**.

Formato
^^^^^^^

Expresiones regulares
^^^^^^^^^^^^^^^^^^^^^

texto = "Hola    mundo   con   muchos   espacios"
palabras = texto.split()  # Sin argumento, split() usa espacios por defecto
print(palabras)
# Salida: ['Hola', 'mundo', 'con', 'muchos', 'espacios']

texto2 = "uno, , dos,, tres,,,"
palabras2 = texto2.split(",")
print(palabras2)
# Salida: ['uno', '', ' dos', '', ' tres', '', '', '']

import re
palabras3 = re.split(r"\s+", texto)
print(palabras3)
# Salida: ['Hola', 'mundo', 'con', 'muchos', 'espacios']

palabras4 = re.split(r",+", texto2)
print(palabras4)
# Salida: ['uno', ' dos', ' tres', '']`

Tokenización 
^^^^^^^^^^^^




