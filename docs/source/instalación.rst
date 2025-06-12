Instalación de Python
======================

En caso de que no tengas instalado y configurado Python en tu sistema, aquí están
unas guías para tu sistema operativo. Para hacer estas instalaciones
utilizaremos la línea de comandos porque es la manera más práctica de mostrarlo
en texto y es una de las maneras más prácticas de instalación para los
programadores. El sistema operativo que recomiendo para programar en Python es
Linux o macOS, precisamente porque están más orientados a la línea de comandos
y hay muchas herramientas para este estilo de trabajo. También se puede
utilizar Windows, pero hay algunos programas o librerías que corren nativamente
en Linux o macOS y no tienen soporte oficial en Windows. Por ejemplo, Redis.

Python en tu sistema
----------------------

Dependiendo de tu sistema operativo o los programas que tengas previamente
instalados, es probable que haya varias instalaciones de Python en tu
computadora. Por ejemplo, algunas versiones de Linux y macOS utilizan Python
como parte de las herramientas del sistema operativo, por lo que tienen alguna versión preinstalada. Para
complicar las cosas, de seguro va a incluir una versión más vieja, como la 2.x, la cual
es una versión completamente distinta y no compatible con las versiones
modernas del lenguaje. Para tratar de evitar confusiones, en las versiones modernas se
utiliza el nombre de ``python3`` para el intérprete. La versión dos (viejita) se llama
simplemente ``python``.

Además, para los programadores, es recomendable el uso de ambientes virtuales de
desarrollo. En caso de que no hayas escuchado el término, son herramientas que
nos permiten tener instalaciones aisladas del lenguaje; estos ambientes incluyen
sus propias copias de versiones compatibles de las librerías y código utilizados
por el proyecto. Por último, también es posible programar utilizando
contenedores, los cuales son en sí una instalación aislada no solo del lenguaje,
sino también de los programas incluidos en el sistema operativo. Este tipo de
instalaciones avanzadas las veremos más adelante. En esta sección instalaremos
una versión de Python para uso general por parte de los usuarios del sistema.

Windows
-------

En caso de que no tengas instalada la aplicación *Terminal*, te recomiendo que la instales
cuanto antes. Puedes instalarla desde la `Microsoft Store <https://apps.microsoft.com/detail/9n0dx20hk701>`_.
Esta es una versión más moderna y rápida que el tradicional programa de Command Prompt
(console.exe), además esta versión es de `código abierto <https://github.com/microsoft/terminal>`_.

Estos pasos para instalar Python funcionan para las versiones 10 y 11 de
Windows. Para seguir practicando el uso de la terminal, vamos a utilizar la
herramienta WinGet, esta herramienta nos permite gestionar aplicaciones desde
la línea de comandos, parecido a lo que hacen los programas ``apt`` en
distribuciones de Linux Debian o el programa ``brew`` en macOS.

Veamos si está instalado WinGet ejecutando el siguiente comando en Terminal:

.. code-block:: bash

   winget -v

Se debería desplegar la versión del programa winget en tu computadora. Si el
comando no es reconocido debemos instalar
`WinGet <https://learn.microsoft.com/es-es/windows/package-manager/winget/>`_.
Una vez instalado *winget*, podemos consultar las versiones de Python
disponibles:

.. code-block:: bash

   winget search --id Python.Python

Lo que nos arroja las versiones disponibles:

.. code-block:: bash

   Nombre      Id                 Versión   Origen
   ------------------------------------------------
   Python 2    Python.Python.2    2.7.18150 winget
   Python 3.0  Python.Python.3.0  3.0.1     winget
   ...
   Python 3.13 Python.Python.3.13 3.13.2    winget

Vamos a instalar la versión 3.13.2, la más reciente al día de hoy. Para esto
utilizaremos el comando
`install <https://learn.microsoft.com/es-es/windows/package-manager/winget/install#arguments>`_,
pasaremos el identificador del paquete (``--id Python.Python.3.13``) de manera
exacta (``-e``). Queremos instalar Python para todos los usuarios de nuestro
equipo, por lo que agregaremos el parámetro ``--scope machine``. Para ejecutar el
comando es importante ejecutar el programa de *Terminal* como usuario
**Administrador**.

.. code-block:: bash

   winget install -e --id Python.Python.3.13 --scope machine

Para revisar que el intérprete se instaló correctamente, debemos de cerrar la
terminal y abrirla de nuevo para que se cargue la configuración. Una vez hecho
esto, ejecutamos el intérprete con el comando ``python``:

.. code-block:: bash

   PS C:\Users\Usuario> python
   Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

Linux
-----

Python se incluye en la mayoría de las distribuciones de Linux. Puedes
consultar `distrowatch.com <https://distrowatch.com/>`_ para ver la versión
exacta incluida en tu distribución específica de Linux. Por ejemplo, actualmente uso
la versión Ubuntu LTS 24.04, la cual incluye la versión 3.12.3. Utilizar la
versión que se incluye en los repositorios oficiales tiene la ventaja de que
son versiones relativamente recientes y la mayoría de los programas y librerías
son compatibles. Dicho esto, en ocasiones queremos probar la última
funcionalidad del lenguaje; en ese caso podemos instalar la última versión desde
repositorios no oficiales. Veamos las dos opciones:

Instalación utilizando APT
~~~~~~~~~~~~~~~~~~~~~~~~~~

Antes de instalar, podemos revisar si el intérprete está instalado
y es una versión reciente:

.. code-block:: bash

   python3 --version

Si se imprime una versión mayor a 3.12.1, es una versión reciente y
para la mayoría de los ejercicios del libro es más que suficiente.

En caso de que requieras actualizar a la última versión del intérprete disponible
para tu versión de Ubuntu, podemos seguir los siguientes pasos:

Como primer paso, actualizamos el índice local del repositorio de paquetes de
Ubuntu para asegurarnos de instalar la última versión disponible:

.. code-block:: bash

   sudo apt update

Ahora podemos actualizar nuestro sistema:

.. code-block:: bash

   sudo apt -y upgrade

El parámetro ``-y`` nos permite confirmar con anticipación la instalación
de las nuevas versiones.

Si solo queremos actualizar el intérprete y sus dependencias, podemos
ejecutar el comando:

.. code-block:: bash

   sudo apt install python3

Una vez actualizado el sistema, podemos ver la versión del intérprete con:

.. code-block:: bash

   python3 --version

Ahora vamos a actualizar el programa ``pip``, con el que
gestionamos los *paquetes* o librerías de terceros:

.. code-block:: bash

   python3 -m pip install --upgrade pip

Instalación utilizando el PPA de deadsnakes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para instalar la última versión de Python en Ubuntu, vamos a utilizar el
`repositorio <https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa>`_ del equipo
*deadsnakes*, en el cual se incluyen versiones más recientes que en la
distribución oficial. Para esto, agregamos el repositorio a nuestro sistema con
los siguientes comandos:

.. code-block:: bash

   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt update

Una vez agregado el repositorio no oficial, podemos instalar la versión más
reciente. Vamos a instalar otras herramientas para desarrollo utilizando dev
para incluir los encabezados de C para compilar librerías y venv para instalar
las herramientas de ambientes virtuales de Python que utilizaremos más
adelante:

.. code-block:: bash

   sudo apt install python3.13 python3.13-venv

Para ejecutar la nueva versión, debemos especificar la versión:

.. code-block:: bash

   python3.13

Para instalar ``pip`` para el nuevo intérprete:

.. code-block:: bash

   python3.13 -m ensurepip --upgrade

Y por último, actualizamos ``pip``:

.. code-block:: bash

   python3.13 -m pip install --upgrade pip

MacOS
-----

Para instalar Python en MacOS, puedes bajar la última versión de `python.org <https://www.python.org/downloads/>`_
y seguir las instrucciones para instalarlo utilizando la aplicación.
