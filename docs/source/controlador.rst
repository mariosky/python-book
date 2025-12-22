Código fuente para los ejemplos de control difuso
=================================================

El ejemplo FIS está compuesto por varios archivos Python que implementan y
prueban un sistema de inferencia difusa aplicado al control y simulación de un
vehículo sencillo. Los archivos incluidos son los siguientes:


``fuzzy_control.py``
--------------------

    Contiene la definición principal del controlador difuso. En este archivo se
    especifican las variables lingüísticas de entrada y salida, las funciones
    de membresía y el conjunto de reglas difusas que conforman el sistema de
    inferencia.

.. literalinclude:: fuzzy_code/fuzzy_control.py
  :language: python
  :linenos:
  :caption: Código de Sakai

``my_fis.py``
-------------

    Implementa la construcción y configuración del sistema FIS, sirviendo como
    módulo central que encapsula la lógica del sistema difuso y permite su
    reutilización desde otros scripts.

.. literalinclude:: fuzzy_code/my_fis.py
  :language: python
  :linenos:
  :caption: Código de Sakai

``angle.py``
------------

    Este script proporciona funciones auxiliares relacionadas con el cálculo y
    manejo de ángulos, utilizadas durante la simulación para determinar errores
    de orientación o referencias geométricas.

.. literalinclude:: fuzzy_code/angle.py
  :language: python
  :linenos:
  :caption: Código de Sakai

``path.py``
-----------

    Define la trayectoria o camino que debe seguir el sistema simulado. Este
    módulo se utiliza para generar puntos de referencia y evaluar el desempeño
    del controlador difuso respecto a la ruta deseada.

.. literalinclude:: fuzzy_code/path.py
  :language: python
  :linenos:
  :caption: Código de Sakai

``rear_wheel_sim.py``
---------------------

    Implementa la simulación del modelo cinemático del vehículo con rueda
    trasera, integrando el controlador difuso para calcular las acciones de
    control y evaluar su comportamiento dinámico.

.. literalinclude:: fuzzy_code/rear_wheel_sim.py
  :language: python
  :linenos:
  :caption: Código de Sakai
