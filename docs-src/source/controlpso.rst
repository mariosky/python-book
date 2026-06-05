Código fuente para los ejemplos de optimización de control difuso con PSO
=========================================================================

En este anexo se incluye el código fuente utilizado para optimizar un
controlador difuso (FIS) mediante **Particle Swarm Optimization (PSO)**. El
flujo de trabajo general es:

1. ``tunable_fuzzy.py`` construye un FIS **parametrizable** y genera un
   controlador callable.
2. ``evaluate_controller.py`` evalúa el controlador como una *caja negra* y
   devuelve un valor escalar (fitness), típicamente el **RMSE**.
3. ``pso.py`` ejecuta PSO (con DEAP) para minimizar el **RMSE** del controlador parametrizable.
4. ``best_controller.json`` guarda el mejor vector de parámetros encontrado, 
   también las ruta utilizadas para el entrenamiento.
5. ``show_controller.py`` carga el mejor controlador y permite visualizar una
   ruta específica (animación, gráficas y funciones de membresía).

Estructura de archivos
----------------------

El directorio del ejemplo contiene los siguientes archivos:

.. code-block:: bash

   fuzzy_code/
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

.. literalinclude:: fuzzy_code/tunable_fuzzy.py
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
- Penaliza escenarios donde el robot no llega a la meta o pierde la referencia.

.. literalinclude:: fuzzy_code/evaluate_controller.py
   :language: python
   :linenos:
   :caption: Evaluación del controlador como función objetivo (``evaluate_controller.py``)

``pso.py``
----------

Implementación del algoritmo **PSO** utilizando ``DEAP``. Su función es:

- Definir la representación de la partícula (posición/velocidad/mejor histórico).
- Definir el espacio de búsqueda (rangos mínimos y máximos por parámetro).
- Ejecutar el ciclo de optimización llamando a ``evaluate_controller.py``.
- Imprime el mejor vector de parámetros.

.. literalinclude:: fuzzy_code/pso.py
   :language: python
   :linenos:
   :caption: Optimización del FIS mediante PSO (``pso.py``)

``best_controller.json``
------------------------

Archivo de configuración que guarda el mejor controlador encontrado. Contiene
principalmente:

- ``params``: vector de parámetros (lista de ``float``) que define el FIS.
- (Opcional) rutas utilizadas, métricas y metadatos para reproducibilidad.

.. literalinclude:: fuzzy_code/best_controller.json
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

.. literalinclude:: fuzzy_code/show_controller.py
   :language: python
   :linenos:
   :caption: Visualización del mejor controlador (``show_controller.py``)

Ejemplo de uso
--------------

Para mostrar el mejor controlador sobre una ruta específica (por ejemplo, la
ruta con índice 2) y la ubicación del archivo con la configuración del FIS:

.. code-block:: bash

   python show_controller.py 2 --configure ./best_controller.json

Para ejecutar la optimización con PSO (puede tomar tiempo dependiendo del número
de partículas y generaciones):

.. code-block:: bash

   python pso.py

Código fuente para los ejemplos de Escalado Computacional
=========================================================

El siguiente archivo muestra la versión del algoritmo PSO donde la evaluación
de la aptitud de cada partícula se realiza en paralelo utilizando **tareas
remotas** de Ray. El resto del algoritmo se ejecuta de manera secuencial en un
solo proceso coordinador.

.. literalinclude:: fuzzy_code/pso_ray.py
   :language: python
   :linenos:
   :caption: Uso de Ray para ejecutar la evaluación distribuida (``pso_ray.py``)


A continuación se muestra el código completo del ejemplo de **PSO
multi-enjambre**, donde cada población se implementa como un **actor con estado**
(``SwarmAgent``). En este caso, Ray se utiliza tanto para ejecutar evaluaciones
*stateless* como para mantener poblaciones persistentes que evolucionan y
migran soluciones de manera coordinada.

.. literalinclude:: fuzzy_code/pso_agent.py
   :language: python
   :linenos:
   :caption: Uso de Ray para implementar PSO multi-enjambre (``pso_agent.py``)

