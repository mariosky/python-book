Código fuente para los ejemplos de optimización de control difuso con PSO
=========================================================================

En este anexo se incluye el código fuente utilizado para optimizar un
controlador difuso (FIS) mediante **Particle Swarm Optimization (PSO)**. El
flujo de trabajo general es:

1. ``tunable_fuzzy.py`` construye un FIS **parametrizable** y genera un
   controlador callable.
2. ``evaluate_controller.py`` evalúa el controlador como una *caja negra* y
   devuelve un valor escalar (fitness), típicamente el **RMSE**.
3. ``pso.py`` ejecuta PSO (con DEAP) para minimizar ese fitness.
4. ``best_controller.json`` guarda el mejor vector de parámetros encontrado.
5. ``show_controller.py`` carga el mejor controlador y permite visualizar una
   ruta específica (animación, gráficas y funciones de membresía).

Estructura de archivos
----------------------

El directorio del ejemplo contiene los siguientes archivos:

.. code-block:: bash

   pso_code/
   ├── tunable_fuzzy.py
   ├── evaluate_controller.py
   ├── pso.py
   ├── show_controller.py
   └── best_controller.json

.. note::

   Este anexo documenta los archivos específicos de la optimización con PSO.
   La simulación del robot tipo bicicleta y la generación de rutas (por ejemplo
   ``rear_wheel_sim.py`` y ``path.py``) se describen en el anexo anterior de la
   simulación y se reutilizan sin cambios.

``tunable_fuzzy.py``
--------------------

Este archivo define el **FIS ajustable**. Su responsabilidad es:

- Construir el sistema de inferencia difusa a partir de parámetros (por ejemplo,
  un vector de ``float``).
- Proveer una función ``get_controller(params)`` que regresa un controlador
  callable con interfaz:

.. math::

   (e_{th}, e) \;\longrightarrow\; \omega

- (Opcional) incluir funciones para visualizar las funciones de membresía.

.. literalinclude:: pso_code/tunable_fuzzy.py
   :language: python
   :linenos:
   :caption: FIS parametrizable para optimización (``tunable_fuzzy.py``)

``evaluate_controller.py``
--------------------------

Este script implementa la **función objetivo** (*fitness*). En la práctica:

- Recibe un vector de parámetros (o ``None`` para usar el controlador base).
- Construye el controlador difuso mediante ``tunable_fuzzy.get_controller``.
- Ejecuta la simulación sobre un conjunto fijo de rutas.
- Calcula el desempeño (por ejemplo, RMSE del error lateral).
- Penaliza escenarios donde el robot no llega a la meta o diverge.

.. literalinclude:: pso_code/evaluate_controller.py
   :language: python
   :linenos:
   :caption: Evaluación del controlador como función objetivo (``evaluate_controller.py``)

``pso.py``
----------

Implementación del algoritmo **PSO** utilizando ``DEAP``. Su función es:

- Definir la representación de la partícula (posición/velocidad/mejor histórico).
- Definir el espacio de búsqueda (rangos mínimos y máximos por parámetro).
- Ejecutar el ciclo de optimización llamando a ``evaluate_controller``.
- Guardar el mejor vector de parámetros encontrado en ``best_controller.json``.

.. literalinclude:: pso_code/pso.py
   :language: python
   :linenos:
   :caption: Optimización del FIS mediante PSO (``pso.py``)

``best_controller.json``
------------------------

Archivo de configuración que guarda el mejor controlador encontrado. Contiene
principalmente:

- ``params``: vector de parámetros (lista de ``float``) que define el FIS.
- (Opcional) rutas utilizadas, métricas y metadatos para reproducibilidad.

.. literalinclude:: pso_code/best_controller.json
   :language: json
   :linenos:
   :caption: Mejor controlador encontrado (``best_controller.json``)

``show_controller.py``
----------------------

Script de **visualización y diagnóstico**. Este archivo:

- Carga ``best_controller.json``.
- Construye el controlador difuso con esos parámetros.
- Ejecuta la simulación sobre una ruta específica (por índice).
- Muestra animación y gráficas del seguimiento.
- Despliega las funciones de membresía resultantes.

.. literalinclude:: pso_code/show_controller.py
   :language: python
   :linenos:
   :caption: Visualización del mejor controlador (``show_controller.py``)

Ejemplo de uso
--------------

Para mostrar el mejor controlador sobre una ruta específica (por ejemplo, la
ruta con índice 2):

.. code-block:: bash

   python show_controller.py 2

Para ejecutar la optimización con PSO (puede tomar tiempo dependiendo del número
de partículas y generaciones):

.. code-block:: bash

   python pso.py

Sugerencia de reproducibilidad
------------------------------

Si se desea hacer el experimento reproducible, conviene registrar:

- semilla aleatoria (``seed``),
- número de partículas,
- número de iteraciones,
- límites del espacio de búsqueda,

y guardarlos junto con ``params`` en ``best_controller.json``.

