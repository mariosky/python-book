Metaheurísticas basadas en poblaciones
======================================

Como se discutió en la sección anterior, el control difuso propone una
alternativa heurística a los enfoques clásicos de control. Los controladores
difusos tienen como ventaja su flexibilidad y facilidad de interpretación. Sin
embargo, también observamos que el desempeño de un controlador difuso depende
de sus parámetros: los rangos de las variables, las funciones de membresía y la
base de reglas. El ajuste manual de estos parámetros puede ser un proceso muy
costoso, subjetivo y es dificil de realizar a gran escala.

En este capítulo proponemos el uso de **algoritmos genéticos** y de
**optimización por enjambre de partículas**, para abordar este tipo de
problemas. Estos algoritmos son métodos de optimización inspirados en procesos
naturales, como la selección natural y la inteligencia colectiva, que permiten
ajustar automáticamente los parámetros de un sistema a partir de su desempeño.

Metaheurísticas
---------------

Antes de entrar en detalle, conviene definir estas técnicas a partir del
concepto de **metaheurística**.

Una `**metaheurística** <https://en.wikipedia.org/wiki/Metaheuristic>`_
es una estrategia de alto nivel diseñada para guiar
procesos de búsqueda y optimización en problemas complejos, donde los métodos
exactos o deterministas son inprácticos o resultan demasiado costosos desde el
punto de vista computacional. Decimos que es de *alto nivel* porque la
estrategia no considera aspectos particulares del problema que ataca y, por lo
tanto, puede aplicarse a una amplia variedad de problemas distintos.

A diferencia de los algoritmos clásicos de optimización, las metaheurísticas no
requieren un modelo matemático explícito del problema (por ejemplo, derivadas,
convexidad o continuidad). En su lugar, tratan al sistema como una *caja negra*,
evaluando únicamente la calidad de una solución candidata mediante una función
objetivo.

En general, las metaheurísticas presentan las siguientes características:

- Exploran el espacio de soluciones de forma **estocástica** o parcialmente
  aleatoria.
- Balancean la **exploración** (búsqueda global) y la **explotación** (mejora
  local).
- Son **robustas** frente a funciones objetivo ruidosas, no diferenciables o
  multimodales.
- Pueden adaptarse a una amplia variedad de problemas sin cambios estructurales
  profundos.

Como ejemplos representativos de metaheurísticas se encuentran los
**algoritmos genéticos**, la **optimización por enjambre de partículas (PSO)**,
el **recocido simulado**, la **búsqueda tabú** y las **estrategias evolutivas**.

.. note::

   Algunos conceptos introducidos en esta sección pueden no resultar familiares
   en una primera lectura, como *espacio de búsqueda* o *función objetivo*. No es
   necesario dominarlos de inmediato: su significado se irá aclarando de forma
   natural a medida que avancemos en los ejemplos y aplicaciones prácticas.

.. note::

   En la literatura, el término *computación evolutiva* se utiliza a menudo como
   un paraguas para agrupar técnicas inspiradas en procesos de evolución natural,
   como los algoritmos genéticos, las estrategias evolutivas y la programación
   genética. En este libro adoptamos una clasificación más general basada en el
   concepto de **metaheurísticas basadas en poblaciones**, la cual permite incluir
   de manera natural tanto a los algoritmos genéticos como a técnicas
   relacionadas como PSO.

Metaheurísticas basadas en poblaciones
--------------------------------------

La característica principal de las metaheurísticas basadas en poblaciones es que
trabajan simultáneamente con **múltiples soluciones candidatas** y utilizan
mecanismos inspirados en procesos naturales o colectivos para explorar el
espacio de búsqueda.

Veamos un ejemplo concreto para que esta idea quede más clara.

Supongamos que debemos configurar un robot que cuenta con **20 parámetros
binarios**, es decir, cada uno puede estar encendido o apagado. Una
configuración particular puede representarse como una lista de ceros y unos en
Python:

.. code-block:: python

   r1 = [0, 1, 0, 1, 1, 1, 0, 1, 0, 1,
         0, 0, 1, 1, 1, 0, 1, 1, 0, 1]

Esta lista representa una **solución candidata**.

Para determinar si esta configuración es adecuada, necesitamos definir un
**objetivo**. Por ejemplo, podríamos buscar minimizar los errores del robot o
reducir el tiempo necesario para completar una tarea. Esta evaluación puede
realizarse mediante experimentos físicos o, más comúnmente, a través de una
simulación.

En este punto no es necesario conocer los detalles internos de la simulación;
basta con obtener una medida de desempeño que nos indique **qué tan buena es una
solución**. A esta medida la llamaremos *fitness* o función objetivo.

Supongamos que el valor de *fitness* puede ir de 0 a 20:

.. code-block:: python

   >>> fitness(r1)
   12

Ahora proponemos una segunda solución candidata modificando algunos parámetros:

.. code-block:: python

   r2 = [0, 0, 0, 1, 1, 0, 1, 1, 0, 1,
         0, 0, 1, 1, 1, 0, 1, 0, 0, 1]

   >>> fitness(r2)
   10

Esta es la esencia del problema: podemos generar soluciones candidatas y
evaluar su desempeño. Sin embargo, incluso en este caso aparentemente sencillo,
el **espacio de búsqueda** es considerable. El número total de configuraciones
posibles es:

.. code-block:: python

   >>> 2 ** 20
   1048576

Es decir, poco más de un millón de soluciones candidatas. En principio, podríamos
evaluar todas y encontrar la solución óptima. No obstante, si cada evaluación de
``fitness()`` toma un minuto, este enfoque resultaría computacionalmente
inviable.

En una metaheurística basada en poblaciones, el proceso es distinto. En lugar de
evaluar todas las soluciones posibles, se comienza con un **conjunto inicial de
soluciones candidatas** y se inicia un proceso de búsqueda guiado por una
heurística específica, manteniendo un balance entre **exploración** y
**explotación**.

En este contexto:

- **Exploración** implica probar configuraciones muy distintas entre sí, con el
  objetivo de cubrir diferentes regiones del espacio de búsqueda.
- **Explotación** consiste en refinar las mejores soluciones encontradas hasta el
  momento, realizando cambios pequeños en su vecindad.

Por ejemplo, si una solución alcanza un valor de ``fitness()`` cercano a 18, una
estrategia de explotación buscaría mejorarla modificando solo algunos parámetros,
con la esperanza de encontrar una solución aún mejor en su entorno cercano.

Otro concepto importante en este tipo de metaheurísticas es el **componente
estocástico**. Normalmente, el conjunto inicial de soluciones candidatas se
genera de manera aleatoria, y el balance entre **exploración** y
**explotación** también se logra introduciendo decisiones probabilísticas en
las distintas etapas del algoritmo.

Este uso controlado del azar permite evitar búsquedas demasiado rígidas y
favorece la exploración de nuevas regiones del espacio de búsqueda, sin perder
de vista las mejores soluciones encontradas hasta el momento.

Con estas ideas fundamentales ya contamos con los elementos necesarios para
construir un algoritmo concreto. Como siguiente paso, vamos a dar solución a
este problema implementando un **algoritmo genético básico**.

Algoritmo genético básico
-------------------------

Como primer paso, vamos a definir la función ``fitness()``. En las
metaheurísticas basadas en poblaciones, esta función es uno de los componentes
clave y debe adaptarse específicamente al problema de optimización que se desea
resolver.

El otro elemento fundamental es la **representación de las soluciones
candidatas**. En este ejemplo, dicha representación se define desde un inicio:
utilizaremos una lista de valores binarios (enteros en Python). Esta elección
simplifica la explicación y nos permite centrarnos en el funcionamiento general
del algoritmo.

Para ilustrar la idea, utilizaremos un problema clásico de los algoritmos
genéticos conocido como **OneMax**. En este problema, la función objetivo
consiste simplemente en maximizar la cantidad de unos presentes en la solución
candidata. En términos prácticos, la solución óptima es aquella en la que todos
los parámetros binarios están activados.

Una implementación básica de esta función de aptitud es la siguiente:

.. code-block:: python

   def one_max(solution):
       return sum(solution)

   r = [1, 0, 0, 0, 1, 1]
   one_max(r)

El algoritmo genético inicia con una **población inicial**, compuesta por un
conjunto de *individuos*. Cada individuo se representa mediante un
*cromosoma*, el cual codifica una posible solución al problema.

En la práctica, esta población suele generarse de manera aleatoria. Para ello,
definimos funciones auxiliares que crean individuos y poblaciones completas.
Este es también un buen momento para reforzar el uso de **listas por
comprensión** en Python.

.. code-block:: python

   import random

   def create_individual(size):
       return [random.randint(0, 1) for _ in range(size)]

   def get_population(n, size):
       return [create_individual(size) for _ in range(n)]

Con estas funciones podemos generar una población inicial de ``n`` individuos,
cada uno con un cromosoma de longitud ``size``.

En implementaciones más completas, las bibliotecas especializadas incluyen
mecanismos más elaborados para la creación de poblaciones, así como operadores
aleatorios adaptados a distintos tipos de representación. 

Inicializamos la población, en este caso vamos a crear la población con 10 individuos de 
tamaño 20.

>>> population = get_population(10, 20)
>>> population
[[0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1],
 [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0],
 [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
 [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
 [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0],
 [1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
 [0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
 [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
 [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
 [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0]]

Los algoritmos genéticos se basan en la selección natural, en dónde los
individuos de la población más aptos, tienen mayor probabilidad de
reproducirse. Para esto debemos primero evaluar el desempeño de cada individuo.

Ya que tenemos listas (con un órden establecido), podemos generar una lista que
incluya el fitness de cada individuo. Una opción más elaborada puede 
incluir definir una clase ``Individuo`` que incluya su fitness y 
otros elementos. Aquí buscamos una solución más básica:

>>> fitness = [one_max(i) for i in population]
>>> fitness
[11, 10, 11, 8, 11, 10, 7, 13, 11, 7]
>>>

Vamos a unir ambas listas utilizando ``zip``, 
por ejemplo podemos listar a cada individuo con su aptitud:

>>> for i in zip(population, fitness):
...     print(i)
...
([1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1], 11)
([1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0], 10)
([1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1], 11)
([1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0], 8)
([1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1], 11)
([1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0], 10)
([0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0], 7)
([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0], 13)
([0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1], 11)
([1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], 7)

Evaluación de la población
~~~~~~~~~~~~~~~~~~~~~~~~~~

Los algoritmos genéticos se inspiran en el principio de **selección natural**:
los individuos más aptos dentro de una población tienen mayor probabilidad de
reproducirse y transmitir sus características a la siguiente generación.

Para poder aplicar este principio, el primer paso consiste en **evaluar el
desempeño de cada individuo** de la población mediante la función de aptitud
(*fitness*).

Dado que ya contamos con una población representada como una lista de
individuos, podemos generar fácilmente una lista que contenga el valor de
``fitness`` correspondiente a cada uno. Existen implementaciones más elaboradas
que definen una clase ``Individuo`` para almacenar tanto el cromosoma como su
aptitud y otros atributos, pero por ahora utilizaremos una solución más simple
y explícita.

Por ejemplo, utilizando listas por comprensión:

.. code-block:: python

   fitness = [one_max(i) for i in population]
   fitness

El resultado es una lista de valores que representa la aptitud de cada
individuo:

.. code-block:: python

   [11, 10, 11, 8, 11, 10, 7, 13, 11, 7]

En este punto resulta útil **asociar cada individuo con su valor de fitness**.
Una forma práctica de hacerlo es utilizando la función ``zip`` de Python, que
permite recorrer ambas listas de manera simultánea:

.. code-block:: python

   for individual, fit in zip(population, fitness):
       print(individual, fit)

La salida muestra claramente cada cromosoma junto con su aptitud:

.. code-block:: text

   [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1] 11
   [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0] 10
   [1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1] 11
   [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0] 8
   [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1] 11
   [1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0] 10
   [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0] 7
   [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0] 13
   [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1] 11
   [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0] 7

Esta información será fundamental en los siguientes pasos del algoritmo
genético, donde utilizaremos la aptitud de los individuos para **seleccionar**
aquellos que participarán en los procesos de cruce y mutación.

Selección por torneo
~~~~~~~~~~~~~~~~~~~~

Una de las técnicas más sencillas y utilizadas para seleccionar a los mejores
individuos de una población es la **selección por torneo**.

La idea es la siguiente: se eligen aleatoriamente ``k`` individuos de la
población y se comparan sus valores de *fitness*. El individuo con mejor
desempeño gana el torneo y es seleccionado para formar parte de la siguiente
generación. Este procedimiento se repite tantas veces como individuos se
necesiten.

En este capítulo utilizaremos torneos de tamaño ``k = 2``; es decir, en cada
torneo compiten únicamente dos individuos y se selecciona el mejor de ellos.
Este esquema es simple, eficiente y suele ofrecer buenos resultados en la
práctica.

El parámetro ``k`` juega un papel importante en el comportamiento del algoritmo:

- Si ``k`` es pequeño, la selección es **menos elitista**, lo que favorece la
  diversidad de la población y la exploración del espacio de búsqueda.
- Si ``k`` es grande, la selección se vuelve **más elitista**, ya que los
  individuos con mejor *fitness* tienen una probabilidad mucho mayor de ser
  seleccionados.

Un valor de ``k`` demasiado alto puede provocar que la población pierda
diversidad rápidamente y se **estanque en óptimos locales**, mientras que un
valor muy bajo puede ralentizar la convergencia del algoritmo. Por esta razón,
el tamaño del torneo se considera un **parámetro de diseño** del algoritmo
genético.

A continuación se muestra una implementación sencilla de selección por torneo
en Python:

.. code-block:: python

   import random

   def tournament_selection(population, fitness, k=2):
       """
       Selección por torneo.

       population : list
           Lista de individuos.
       fitness : list
           Lista con los valores de fitness correspondientes.
       k : int
           Tamaño del torneo.
       """
       candidates = random.sample(list(zip(population, fitness)), k)
       candidates.sort(key=lambda x: x[1], reverse=True)
       return candidates[0][0]

Esta función devuelve un individuo seleccionado mediante torneo. Para construir
una nueva población basta con repetir este proceso hasta obtener el número de
individuos deseado.

En el código anterior se utiliza una función ``lambda`` para ordenar a los
candidatos por el segundo elemento de la tupla, es decir, por el valor de
*fitness*.

La selección por torneo tiene varias ventajas prácticas: es fácil de
implementar, no requiere normalizar los valores de *fitness* y se adapta bien a
funciones objetivo ruidosas o no estacionarias. Por estas razones, es una opción
muy común en implementaciones de algoritmos genéticos tanto académicas como
aplicadas.

Generación de la población seleccionada
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

El siguiente paso es generar una lista de individuos seleccionados mediante
torneos. Los ganadores se eligen para reproducirse y transmitir su material
genético a la siguiente generación.

Es normal que algunos individuos ganen varios torneos; por lo tanto, pueden
aparecer más de una vez en la población seleccionada. En términos de programación,
es importante crear **copias** de los individuos seleccionados, ya que si dejamos
referencias, una modificación posterior (por ejemplo, durante cruza o mutación)
podría afectar a múltiples entradas de la lista.

El código para crear la nueva población queda muy compacto utilizando listas
por comprensión. El *slicing* ``[:]`` crea una copia superficial de la lista:

.. code-block:: python

   selected = [tournament_selection(population, fitness)[:] for _ in range(len(population))]

En este ejemplo, el número de torneos se elige igual al tamaño de la población,
de modo que la población seleccionada conserve el mismo número de individuos.

Emparejamiento para cruza
~~~~~~~~~~~~~~~~~~~~~~~~~

Una vez que tenemos la población seleccionada, debemos decidir cómo formar
**parejas** para aplicar el operador de cruza. Una estrategia simple consiste en:

1. barajar (*shuffle*) la población seleccionada para evitar sesgos debidos al orden,
2. formar parejas consecutivas.

Esta estrategia asume que el tamaño de la población es par. Si es impar, una
opción sencilla es descartar al último individuo, o bien copiarlo directamente
a la siguiente generación (*elitismo*).

Una manera muy compacta de formar parejas consecutivas en Python es utilizar
*slicing* junto con ``zip``:

.. code-block:: python

   import random

   random.shuffle(selected)
   pairs = list(zip(selected[::2], selected[1::2]))

Cruce de un punto
~~~~~~~~~~~~~~~~~

El cruce más básico es el **cruce de un solo punto**. En este operador se
selecciona un punto de corte al azar y se intercambian segmentos de los padres
para generar un par de descendientes.

.. code-block:: python

   def one_point_crossover(p1, p2):
       """
       Cruce de un punto entre dos individuos binarios.
       """
       assert len(p1) == len(p2)
       point = random.randint(1, len(p1) - 1)
       c1 = p1[:point] + p2[point:]
       c2 = p2[:point] + p1[point:]
       return c1, c2

En este caso nos aseguramos primero de que ambos individuos (listas) tienen la
misma longitud. Elegimos el punto de corte con la librería ``random`` y, usando
*slicing*, concatenamos los segmentos para construir los descendientes. La
función regresa una tupla con dos hijos.

Aplicación del cruce a toda la población
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A partir de las parejas generadas, podemos construir una nueva población
aplicando el operador de cruza a cada par:

.. code-block:: python

   children = []
   for p1, p2 in pairs:
       c1, c2 = one_point_crossover(p1, p2)
       children.extend([c1, c2])


