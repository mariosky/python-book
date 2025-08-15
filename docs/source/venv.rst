.. role:: python(code)
   :language: python

Ambientes Virtuales
===================

Python es un proyecto de código libre muy popular, lo que significa que muchos
desarroladores talentosos contribuyen a la comunidad de Python desarrollando
librerías y software también con licencias de código abierto. En caso de
necesitar una librería que no se incluya en la distribución actual de Python, es
muy probable que algún desarrollador en algún lugar del mundo ya haya
implementado una buena solución y que otros desarrolladores que utilizan dicha
herramienta colaboren para mantenerla al día. El desarrollo de librerías en
Python también puede tener el apoyo de empresas que invierten recursos para
mantener y agregarles nuevas funcionalidades. Pero, lamentablemente también
puede suceder que alguna librería no tenga suficientes usuarios o no haya tanto
interés en su desarrollo y sufra de abandono.

``pip``
*******

Los lenguajes modernos incluyen herramientas que permiten a los programadores
compartir fácilmente su código, e incluyen comandos para instalar cierta versión
anterior de una librería, o actualizar la versión actual a una versión más
reciente.  En el caso de Python, el programa preferido de instalación de módulos
es ``pip`` (`pip intalls packages`) ya partir de Python 3.4 se incluye dentro de
la distribución binaria del lenguaje.

Antes de empezar con el uso de ``pip``, vamos conocer otros componentes importantes
del ecosistema:

PyPI es el índice oficial de paquetes de la comunidad de programadores de
Python.  Funciona como un repositorio de acceso abierto que perimte a los
desarrolladores publicar, compartir y reutilizar sus contribuciones de software.

El sitio web principal es https://pypi.org, y es el punto de entrada
para explorar e instalar paquetes mediante herramientas como ``pip``.

El software que da vida a PyPI está construido sobre una plataforma llamada
Warehouse, que es el sistema backend desarrollado por la Python Packaging
Authority (PyPA) el grupo encargado de mantener herramientas como ``pip`` y
``wharehouse``. La plataforma es confiable y se considera en producción.

Como programador puedes iniciar tu búsqueda en el repositorio y ver los
detalles del módulo:

.. figure:: ./images/pypi.png
   :align: center
   :alt: La entrada en el repositorio https://pypi.org/ de la librería ``numpy``.

En esta página podemos ver información del módulo y también
el comando que debemos ejecutar para instalar la última versión (``release``).
En este caso, el comando:

.. code-block:: bash

   pip install numpy

Instalaría la última versión al momento de escribir esta sección: 2.3.1.
Como debe ser, la instalación de nuevas librerías se realiza desde la línea de
comandos.

``venv``
********

Si ejecutamos el comando de instalación de ``pip``, se instalará en la
distribución de Python de nuestra computadora. Esto puede ser práctico si
queremos probar alguna librería nueva rápidamente, pero no es recomendable
cuándo vayamos a incluir algún paquete en un proyecto de software que pensamos
mantener a largo plazo. Para esto es mejor crear una "ambiente virtual" de
desarrollo. Esto nos permitirá instalar nuevos paquetes en una localidad
aislada de la instalación global.

Un ambiente virtual nos permite crear proyectos a largo plazo utilizando
versiones de los paquetes posiblemente distintas a las instaladas en otros
proyectos o en la instalación global. Si yo hago un proyecto utilizando
el framework de "django" version 5.1, pero tengo un proyecto viejo con la
versión 4.1 que no he tenido tiempo de acutalizar. Si utilizo un ambiente
virtual para cada uno, no tengo problema. Además, dependiendo de las necesidades,
en un proyecto podría tener algunos paquetes que en el otro no necesito.

Entonces, antes de instalar cualquier cosa, primero vamos a crear un
ambiente virtual nuevo.

.. code-block:: bash
   :caption: Linux/Mac OS

   python3 -m venv ejemplo_venv
   source ejemplo_venv/bin/activate
   (ejemplo_venv) >

.. code-block:: bash
   :caption: Windows

   py -m venv ejemplo_venv
   ejemplo_env\Scripts\activate
   (ejemplo_venv) >

El módulo `venv` crea un nuevo ambiente llamado ``ejemplo_venv``,
esto es realmente un directorio que se crea en la ruta en la que ejecutamos el
comando.

Después procedemos a "activar" el ambiente. Esto se hace
ejecutando un script que se encuentra precisamente dentro del directorio
que contiene el ambiente. Este script dependerá del sistema operativo
y del intérprete de comandos que utilicemos, por ejemplo: `bash`, `fish`, etc.
O en Windows `PowerShell` o `Command Prompt`.

Una vez activado el ambiente el prompt nos muestra un indicador, en mi
caso muestra el ambiente entre paréntesis: ``(ejemplo_venv)``, esto
varía dependiendo del formato actual de tu intérprete de comandos.

.. note:

   Este directorio puede crearse en la raíz de un proyecto
   y normalmente se llama ``venv`` o ``.venv``. Esto es importante, por que
   algunas herramientas como `Visual Studio Code` buscan algún directorio
   que incluya un ambiente para activarlo de manera automática.

.. note:

   Para desactivar un ambiente utilizamos el comando ``deactivate``.
   Cada que iniciemos una nueva sesión en la línea de comandos debemos
   activar el ambiente.

Una vez activado el ambiente podemos ver el listado de módulos instalados
actualmente:

En mi computadora actual:

.. code-block:: bash

   (ejemplo_venv) PS C:\Users\Mario> py -m pip list
   Package Version
   ------- -------
   pip     24.3.1

Esto es muy distinto a la cantidad de paquetes en la instalación global de
Python o de otros ambientes que tengo en la máquina. Digamos que este es
un ambiente nuevo y vacio. Aunque tenemos muchos módulos como parte
de la instalación estándar. Vamos instalando algún nuevo módulo.

La instalación de la ultima versión de un nuevo paquete (o módulo) y sus dependencias en PyPI
se hace con el parámetro ``install`` aquí te muestro algunas variantes:

.. code-block:: bash

   python -m pip install algúnPaquete
   python -m pip install algúnPaquete==2.2.4    # instala la versión especificada
   python -m pip install "algúnPaquete>=2.2.4"  # la versión o superior
   python -m pip install "algúnPaquete>=1,<2"   # rangos

En  caso de que el módulo ya se encuentre instalado se puede actualizar:

.. code-block:: bash

   python -m pip install --upgrade algúnPaquete

Y para desinstalar:

.. code-block:: bash

   python -m pip uninstall algúnPaquete

Vamos a instalar la úlima versión de la librería `numpy`
que nos va a permitir trabajar con matrices y arreglos multidimensionales:

.. code-block:: bash

   (ejemplo_venv) PS C:\Users\Mario> py -m pip install numpy
   Collecting numpy
   Using cached numpy-2.3.1-cp313-cp313-win_amd64.whl.metadata (60 kB)
   Downloading numpy-2.3.1-cp313-cp313-win_amd64.whl (12.7 MB)
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.7/12.7 MB 12.3 MB/s eta 0:00:00
   Installing collected packages: numpy
   Successfully installed numpy-2.3.1

   [notice] A new release of pip is available: 24.3.1 -> 25.1.1
   [notice] To update, run: python.exe -m pip install --upgrade pip
   (ejemplo_venv) PS C:\Users\Mario>

Si te fijas, ``pip`` utilizó una versión almacenada en un directorio local de
los metadatos de la librería (``Using cached ..``). Bajó los archivos y los
instaló correctamente. Se utilizó una versión en caché porque ya habíamos
instalado la librería en otro ambiente.

Vamos a entrar al intérprete y vamos a revisar que se instaló el paquete
correctamente:

.. code-block:: python

   >>> import numpy as np
   >>> arr = np.array([[1, 2, 3],[4, 5, 6]])
   >>> print(arr)
   [[1 2 3]
   [4 5 6]]
   >>>

``pip freeze``
**************

Ya que tenemos una o más librerías para nuestro proyecto, estas se
consideran requerimientos para el proyecto. El ambiente una vez creado
se considera como un recurso efímero que solo sirve para la instalación
local:

   - Si queremos ejecutar nuestro proyecto en otra máquina, **no copiamos**
     el ambiente, lo reconstruímos.

   - Tampoco debemos mantener el directorio
     de ambiente en sistemas de control de vesiones como ``git``, ya que es
     un recurso independiente de nuestro código.

Una manera básica de reconstruir un ambiente es utilizando el comando
``pip`` para que nos de un listado de los paquetes incluidos en el ambiente
en este momento. Este listado lo guardamos en un archivo que después podemos
utilizar para recrear el ambiente instalando todos los paquetes necesarios.
Veamos un ejemplo.

Primero instalaré un paquete con dependencias para que el ejemplo se vea mejor:
.. code-block:: bash

   (ejemplo_venv)> py -m pip install requests

Una vez de instalar la librería request, vamos a ejecutar el comando ``freeze``
que nos da un listado de los paquetes del ambiente actual:

.. code-block:: bash

   > py -m pip freeze
   certifi==2025.7.9
   charset-normalizer==3.4.2
   idna==3.10
   numpy==2.3.1
   requests==2.32.4
   urllib3==2.5.0

Vemos que está ``numpy==2.3.1`` y ``requests==2.32.4``. Se incluyen además
otras dependencias, cada una con su versión.

Vamos a ejecutar el comando de nuevo pero esta vez la salida del comando
la vamos a guardar en un archivo al que llamaremos ``requirements.txt``.
Este nombre es común dentro de los proyectos de Python.

.. code-block:: bash

   > py -m pip freeze > requirements.txt

El archivo de requirements.txt si es muy importante y debemos manternerlo
como parte de nuestro proyecto. Si otro programador desea instalar nuestro
proyecto, deba bajar el código fuente y el archivo de ``requirements-txt``
para instalar las dependencias. Esto se hace con el comando ``pip``:

.. code-block:: bash

   > py -m pip install -r .\requirements.txt

Utilizamos el parámetro ``-r`` para indicar que instale la lista
de paquetes que se encuentra en el archivo ``requirements.txt``.
Si ejecutamos el comando en el ambiente actual, el comando nos
dira que ya están instalados los paquetes.

