.. _prefacio:

Prefacio
========

A principios del año 2025, Python :cite:`van2007python` es el lenguaje de
programación más popular de acuerdo con el índice de
`TIOBE <https://www.tiobe.com>`_, el cual además le otorgó el reconocimiento de
“lenguaje de programación del año 2024”. Este premio se concede al lenguaje que
presenta el mayor incremento en su calificación durante un año, y en este caso
Python creció un 9.3\% tan solo en 2024
(`https://www.tiobe.com/tiobe-index/ <https://www.tiobe.com/tiobe-index/>`_).

Actualmente, Python no tiene rival en varios campos de la computación
:cite:`srinath2017python`, particularmente en análisis de datos, aprendizaje
automático :cite:`hao2019machine` y desarrollo de aplicaciones de aprendizaje
profundo. Una de las razones principales de este éxito es la facilidad con la
que puede aprenderse y utilizarse el lenguaje. Al ser interpretado, Python
permite probar y modificar código sin necesidad de un proceso de compilación,
lo que favorece un desarrollo rápido y exploratorio. Entre sus desventajas se
encuentra un rendimiento generalmente menor en comparación con lenguajes
compilados como C++ o Rust, así como el hecho de que muchos errores se detectan
únicamente en tiempo de ejecución.

¿Por qué uso Python?
--------------------

En mi caso, llegué al lenguaje atraído por sus *frameworks* para el desarrollo de
aplicaciones web a principios de los años dos mil. Un ejemplo temprano fue el
framework `CherryPy <https://cherrypy.dev/>`_, con el cual desarrollé algunas
aplicaciones web de manera relativamente sencilla para la época. Posteriormente
surgieron frameworks más conocidos y utilizados en la actualidad, como
`Django <https://www.djangoproject.com/>`_ y
`FastAPI <https://fastapi.tiangolo.com/>`_.

Aunque probé otros lenguajes de *scripting* populares para estas tareas, como
`tcl <https://www.tcl.tk/>`_, `PHP <https://www.php.net/>`_ y posteriormente
`Ruby <https://www.ruby-lang.org/en/>`_, la sintaxis de Python me resultó más
amigable y fácil de entender. Con el paso del tiempo, comenzaron a surgir
numerosas librerías y herramientas innovadoras para el desarrollo de
aplicaciones científicas :cite:`langtangen2009primer`, las cuales no encontraba
con el mismo nivel de madurez en otros lenguajes. Esto me llevó a adoptar Python
para una variedad cada vez mayor de proyectos.

Por ejemplo, alrededor de 2008 Python era el único lenguaje soportado por Google
App Engine, lo que permitía ejecutar código de alto desempeño en la nube de
forma relativamente sencilla. Otro proyecto interesante fue
`PiCloud <https://www.crunchbase.com/organization/picloud>`_, un servicio que
permitía ejecutar código de manera transparente en la nube a partir de un
programa local, simplemente importando una librería. Este tipo de plataformas
representó una de las primeras aproximaciones a lo que hoy se conoce como
computación
`Serverless <https://es.wikipedia.org/wiki/Serverless_computing>`_.

.. tip::

   Si te interesa conocer más sobre la historia del lenguaje, no te pierdas el
   documental *The Story of Python and how it took over the world | Python: The
   Documentary*, disponible en
   `YouTube <https://www.youtube.com/watch?v=GfH4QL4VqJ0>`_.

¿A quién va dirigido este libro?
--------------------------------

Es común que programadores se interesen por Python al enfrentar un proyecto o
problema específico para el cual ya existe una librería o una base de código que
resuelve una parte importante del problema central. Algunos ejemplos incluyen
el uso de APIs de inteligencia artificial generativa, el
`procesamiento de imágenes <https://pillow.readthedocs.io/en/latest/index.html>`_,
la interacción con servicios en la
`nube <https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html>`_,
la construcción de
`rastreadores web <https://www.crummy.com/software/BeautifulSoup/>`_ o la
simulación de sistemas mediante
`ecuaciones diferenciales ordinarias <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html>`_.
Python ofrece librerías, ejemplos y comunidades activas para abordar este tipo
de problemas.

Si este es tu caso, este libro está pensado para ti. Su objetivo es facilitar
que programadores con experiencia previa se pongan al día de manera eficiente
con el lenguaje, y que cuenten con una guía para resolver distintos tipos de
problemas de ingeniería en los que Python puede ser una herramienta clave.

