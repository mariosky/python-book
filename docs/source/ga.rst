Metaheurísticas basadas en poblaciones
======================================

como se discutió en la sección anterior, el control difuso propone una
alternativa heurística a los enfoques clásicos de control. los controladores
difusos tienen como ventaja su flexibilidad y facilidad de interpretación. sin
embargo, también observamos que el desempeño de un controlador difuso depende
de sus parámetros: los rangos de las variables, las funciones de membresía y la
base de reglas. el ajuste manual de estos parámetros puede ser un proceso muy
costoso, subjetivo y es dificil de realizar a gran escala.

en este capítulo proponemos el uso de **algoritmos genéticos** y de
**optimización por enjambre de partículas**, para abordar este tipo de
problemas. estos algoritmos son métodos de optimización inspirados en procesos
naturales, como la selección natural y la inteligencia colectiva, que permiten
ajustar automáticamente los parámetros de un sistema a partir de su desempeño.

Metaheurísticas
---------------

antes de entrar en detalle, conviene definir estas técnicas a partir del
concepto de **metaheurística**.

una `**metaheurística** <https://en.wikipedia.org/wiki/metaheuristic>`_
es una estrategia de alto nivel diseñada para guiar
procesos de búsqueda y optimización en problemas complejos, donde los métodos
exactos o deterministas son inprácticos o resultan demasiado costosos desde el
punto de vista computacional. decimos que es de *alto nivel* porque la
estrategia no considera aspectos particulares del problema que ataca y, por lo
tanto, puede aplicarse a una amplia variedad de problemas distintos.

a diferencia de los algoritmos clásicos de optimización, las metaheurísticas no
requieren un modelo matemático explícito del problema (por ejemplo, derivadas,
convexidad o continuidad). en su lugar, tratan al sistema como una *caja negra*,
evaluando únicamente la calidad de una solución candidata mediante una función
objetivo.

en general, las metaheurísticas presentan las siguientes características:

- exploran el espacio de soluciones de forma **estocástica** o parcialmente
  aleatoria.
- balancean la **exploración** (búsqueda global) y la **explotación** (mejora
  local).
- son **robustas** frente a funciones objetivo ruidosas, no diferenciables o
  multimodales.
- pueden adaptarse a una amplia variedad de problemas sin cambios estructurales
  profundos.

como ejemplos representativos de metaheurísticas se encuentran los
**algoritmos genéticos**, la **optimización por enjambre de partículas (pso)**,
el **recocido simulado**, la **búsqueda tabú** y las **estrategias evolutivas**.

.. note::

   algunos conceptos introducidos en esta sección pueden no resultar familiares
   en una primera lectura, como *espacio de búsqueda* o *función objetivo*. no es
   necesario dominarlos de inmediato: su significado se irá aclarando de forma
   natural a medida que avancemos en los ejemplos y aplicaciones prácticas.

.. note::

   en la literatura, el término *computación evolutiva* se utiliza a menudo como
   un paraguas para agrupar técnicas inspiradas en procesos de evolución natural,
   como los algoritmos genéticos, las estrategias evolutivas y la programación
   genética. en este libro adoptamos una clasificación más general basada en el
   concepto de **metaheurísticas basadas en poblaciones**, la cual permite incluir
   de manera natural tanto a los algoritmos genéticos como a técnicas
   relacionadas como pso.

Metaheurísticas basadas en poblaciones
--------------------------------------

la característica principal de las metaheurísticas basadas en poblaciones es que
trabajan simultáneamente con **múltiples soluciones candidatas** y utilizan
mecanismos inspirados en procesos naturales o colectivos para explorar el
espacio de búsqueda.

veamos un ejemplo concreto para que esta idea quede más clara.

supongamos que debemos configurar un robot que cuenta con **20 parámetros
binarios**, es decir, cada uno puede estar encendido o apagado. una
configuración particular puede representarse como una lista de ceros y unos en
python:

.. code-block:: python

   r1 = [0, 1, 0, 1, 1, 1, 0, 1, 0, 1,
         0, 0, 1, 1, 1, 0, 1, 1, 0, 1]

esta lista representa una **solución candidata**.

para determinar si esta configuración es adecuada, necesitamos definir un
**objetivo**. por ejemplo, podríamos buscar minimizar los errores del robot o
reducir el tiempo necesario para completar una tarea. esta evaluación puede
realizarse mediante experimentos físicos o, más comúnmente, a través de una
simulación.

en este punto no es necesario conocer los detalles internos de la simulación;
basta con obtener una medida de desempeño que nos indique **qué tan buena es una
solución**. a esta medida la llamaremos *fitness* o función objetivo.

supongamos que el valor de *fitness* puede ir de 0 a 20:

.. code-block:: python

   >>> fitness(r1)
   12

ahora proponemos una segunda solución candidata modificando algunos parámetros:

.. code-block:: python

   r2 = [0, 0, 0, 1, 1, 0, 1, 1, 0, 1,
         0, 0, 1, 1, 1, 0, 1, 0, 0, 1]

   >>> fitness(r2)
   10

esta es la esencia del problema: podemos generar soluciones candidatas y
evaluar su desempeño. sin embargo, incluso en este caso aparentemente sencillo,
el **espacio de búsqueda** es considerable. el número total de configuraciones
posibles es:

.. code-block:: python

   >>> 2 ** 20
   1048576

es decir, poco más de un millón de soluciones candidatas. en principio, podríamos
evaluar todas y encontrar la solución óptima. no obstante, si cada evaluación de
``fitness()`` toma un minuto, este enfoque resultaría computacionalmente
inviable.

en una metaheurística basada en poblaciones, el proceso es distinto. en lugar de
evaluar todas las soluciones posibles, se comienza con un **conjunto inicial de
soluciones candidatas** y se inicia un proceso de búsqueda guiado por una
heurística específica, manteniendo un balance entre **exploración** y
**explotación**.

en este contexto:

- **exploración** implica probar configuraciones muy distintas entre sí, con el
  objetivo de cubrir diferentes regiones del espacio de búsqueda.
- **explotación** consiste en refinar las mejores soluciones encontradas hasta el
  momento, realizando cambios pequeños en su vecindad.

por ejemplo, si una solución alcanza un valor de ``fitness()`` cercano a 18, una
estrategia de explotación buscaría mejorarla modificando solo algunos parámetros,
con la esperanza de encontrar una solución aún mejor en su entorno cercano.

otro concepto importante en este tipo de metaheurísticas es el **componente
estocástico**. normalmente, el conjunto inicial de soluciones candidatas se
genera de manera aleatoria, y el balance entre **exploración** y
**explotación** también se logra introduciendo decisiones probabilísticas en
las distintas etapas del algoritmo.

este uso controlado del azar permite evitar búsquedas demasiado rígidas y
favorece la exploración de nuevas regiones del espacio de búsqueda, sin perder
de vista las mejores soluciones encontradas hasta el momento.

con estas ideas fundamentales ya contamos con los elementos necesarios para
construir un algoritmo concreto. como siguiente paso, vamos a dar solución a
este problema implementando un **algoritmo genético básico**.

Algoritmo genético básico
-------------------------

como primer paso, vamos a definir la función ``fitness()``. en las
metaheurísticas basadas en poblaciones, esta función es uno de los componentes
clave y debe adaptarse específicamente al problema de optimización que se desea
resolver.

el otro elemento fundamental es la **representación de las soluciones
candidatas**. en este ejemplo, dicha representación se define desde un inicio:
utilizaremos una lista de valores binarios (enteros en python). esta elección
simplifica la explicación y nos permite centrarnos en el funcionamiento general
del algoritmo.

para ilustrar la idea, utilizaremos un problema clásico de los algoritmos
genéticos conocido como **onemax**. en este problema, la función objetivo
consiste simplemente en maximizar la cantidad de unos presentes en la solución
candidata. en términos prácticos, la solución óptima es aquella en la que todos
los parámetros binarios están activados.

una implementación básica de esta función de aptitud es la siguiente:

.. code-block:: python

   def one_max(solution):
       return sum(solution)

   r = [1, 0, 0, 0, 1, 1]
   one_max(r)

el algoritmo genético inicia con una **población inicial**, compuesta por un
conjunto de *individuos*. cada individuo se representa mediante un
*cromosoma*, el cual codifica una posible solución al problema.

en la práctica, esta población suele generarse de manera aleatoria. para ello,
definimos funciones auxiliares que crean individuos y poblaciones completas.
este es también un buen momento para reforzar el uso de **listas por
comprensión** en python.

.. code-block:: python

   import random

   def create_individual(size):
       return [random.randint(0, 1) for _ in range(size)]

   def get_population(n, size):
       return [create_individual(size) for _ in range(n)]

con estas funciones podemos generar una población inicial de ``n`` individuos,
cada uno con un cromosoma de longitud ``size``.

en implementaciones más completas, las bibliotecas especializadas incluyen
mecanismos más elaborados para la creación de poblaciones, así como operadores
aleatorios adaptados a distintos tipos de representación. 

inicializamos la población, en este caso vamos a crear la población con 10 individuos de 
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

los algoritmos genéticos se basan en la selección natural, en dónde los
individuos de la población más aptos, tienen mayor probabilidad de
reproducirse. para esto debemos primero evaluar el desempeño de cada individuo.

ya que tenemos listas (con un órden establecido), podemos generar una lista que
incluya el fitness de cada individuo. una opción más elaborada puede 
incluir definir una clase ``individuo`` que incluya su fitness y 
otros elementos. aquí buscamos una solución más básica:

>>> fitness = [one_max(i) for i in population]
>>> fitness
[11, 10, 11, 8, 11, 10, 7, 13, 11, 7]
>>>

vamos a unir ambas listas utilizando ``zip``, 
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

los algoritmos genéticos se inspiran en el principio de **selección natural**:
los individuos más aptos dentro de una población tienen mayor probabilidad de
reproducirse y transmitir sus características a la siguiente generación.

para poder aplicar este principio, el primer paso consiste en **evaluar el
desempeño de cada individuo** de la población mediante la función de aptitud
(*fitness*).

dado que ya contamos con una población representada como una lista de
individuos, podemos generar fácilmente una lista que contenga el valor de
``fitness`` correspondiente a cada uno. existen implementaciones más elaboradas
que definen una clase ``individuo`` para almacenar tanto el cromosoma como su
aptitud y otros atributos, pero por ahora utilizaremos una solución más simple
y explícita.

por ejemplo, utilizando listas por comprensión:

.. code-block:: python

   fitness = [one_max(i) for i in population]
   fitness

el resultado es una lista de valores que representa la aptitud de cada
individuo:

.. code-block:: python

   [11, 10, 11, 8, 11, 10, 7, 13, 11, 7]

en este punto resulta útil **asociar cada individuo con su valor de fitness**.
una forma práctica de hacerlo es utilizando la función ``zip`` de python, que
permite recorrer ambas listas de manera simultánea:

.. code-block:: python

   for individual, fit in zip(population, fitness):
       print(individual, fit)

la salida muestra claramente cada cromosoma junto con su aptitud:

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

esta información será fundamental en los siguientes pasos del algoritmo
genético, donde utilizaremos la aptitud de los individuos para **seleccionar**
aquellos que participarán en los procesos de cruce y mutación.

Selección por torneo
~~~~~~~~~~~~~~~~~~~~

una de las técnicas más sencillas y utilizadas para seleccionar a los mejores
individuos de una población es la **selección por torneo**.

la idea es la siguiente: se eligen aleatoriamente ``k`` individuos de la
población y se comparan sus valores de *fitness*. el individuo con mejor
desempeño gana el torneo y es seleccionado para formar parte de la siguiente
generación. este procedimiento se repite tantas veces como individuos se
necesiten.

en este capítulo utilizaremos torneos de tamaño ``k = 2``; es decir, en cada
torneo compiten únicamente dos individuos y se selecciona el mejor de ellos.
este esquema es simple, eficiente y suele ofrecer buenos resultados en la
práctica.

el parámetro ``k`` juega un papel importante en el comportamiento del algoritmo:

- si ``k`` es pequeño, la selección es **menos elitista**, lo que favorece la
  diversidad de la población y la exploración del espacio de búsqueda.
- si ``k`` es grande, la selección se vuelve **más elitista**, ya que los
  individuos con mejor *fitness* tienen una probabilidad mucho mayor de ser
  seleccionados.

un valor de ``k`` demasiado alto puede provocar que la población pierda
diversidad rápidamente y se **estanque en óptimos locales**, mientras que un
valor muy bajo puede hacer más lenta la convergencia del algoritmo. por esta razón,
el tamaño del torneo se considera un **parámetro de diseño** del algoritmo
genético.

a continuación se muestra una implementación sencilla de selección por torneo
en python:

.. code-block:: python

   import random

   def tournament_selection(population, fitness, k=2):
       """
       selección por torneo.

       population : list
           lista de individuos.
       fitness : list
           lista con los valores de fitness correspondientes.
       k : int
           tamaño del torneo.
       """
       candidates = random.sample(list(zip(population, fitness)), k)
       candidates.sort(key=lambda x: x[1], reverse=true)
       return candidates[0][0]

esta función devuelve un individuo seleccionado mediante torneo. para construir
una nueva población basta con repetir este proceso hasta obtener el número de
individuos deseado.

en el código anterior se utiliza una función ``lambda`` para ordenar a los
candidatos por el segundo elemento de la tupla, es decir, por el valor de
*fitness*.

Generación de la población seleccionada
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

los ganadores de los torneos son los **seleccionados para reproducirse** y
transmitir su material genético a la siguiente generación.

es normal que algunos individuos ganen varios torneos; por lo tanto, pueden
aparecer más de una vez en la población seleccionada (se reproducen varias
veces). en términos de programación, es importante crear **copias** de los
individuos seleccionados, ya que si dejamos referencias, una modificación
posterior (por ejemplo, durante cruza o mutación) podría afectar a múltiples
entradas de la lista.

el código para crear la nueva población queda muy compacto utilizando listas
por comprensión. el *slicing* ``[:]`` crea una copia superficial de la lista:

.. code-block:: python

   selected = [tournament_selection(population, fitness)[:] for _ in range(len(population))]

.. note::

   En este ejemplo utilizamos *slicing* (``[:]``) para crear copias de los
   individuos seleccionados. Dado que los cromosomas están representados como
   listas simples de valores inmutables (enteros), esta copia superficial es
   suficiente.

   En representaciones más complejas —por ejemplo, cuando los individuos
   contienen estructuras anidadas— es recomendable utilizar el módulo
   ``copy`` de Python y, en particular, la función ``copy.deepcopy`` para
   evitar efectos secundarios no deseados durante los operadores de cruza o
   mutación. Por ejemplo, para un solo individuo:

    .. code:: python

       import copy
       individual_copy = copy.deepcopy(individual)

En este ejemplo, el número de torneos se elige igual al tamaño de la población,
de modo que la población seleccionada conserve el mismo número de individuos.

Cruce de parejas
~~~~~~~~~~~~~~~~

Una vez que tenemos la población seleccionada, debemos decidir cómo formar
**parejas** para aplicar el operador de cruce. Una estrategia simple consiste en:

1. Barajar (*shuffle*) la población seleccionada para evitar sesgos impuestos por el orden,
2. Formar parejas consecutivas.

Esta estrategia asume que el tamaño de la población es par. Si es impar, una
opción sencilla es descartar al último individuo, o bien copiarlo directamente
a la siguiente generación (de manera *elitista*).

Una manera muy compacta de formar parejas consecutivas en Python es utilizar
*slicing* junto con ``zip``:

.. code-block:: python

   import random

   random.shuffle(selected)
   pairs = list(zip(selected[::2], selected[1::2]))

Cruce de un punto
~~~~~~~~~~~~~~~~~

El cruce más básico en un algoritmo genético es el **cruce de un solo punto**.
En este operador se selecciona un punto de corte al azar y se intercambian
segmentos de los padres para generar un par de descendientes.

A continuación se muestra una implementación que realiza el cruce
**modificando directamente a los individuos originales** (*in place*):

.. code-block:: python

   import random

   def one_point_crossover(ind1, ind2):
       """
       Cruce de un punto entre dos individuos binarios.

       ind1 : list
           Primer individuo (padre).
       ind2 : list
           Segundo individuo (padre).
       
       La modificación se realiza *in place*.
       """
       assert len(ind1) == len(ind2)
       point = random.randint(1, len(ind1) - 1)
       ind1[point:], ind2[point:] = ind2[point:], ind1[point:]
       return ind1, ind2

En este caso, primero verificamos que ambos padres (listas) tengan la misma
longitud. El punto de corte se elige de manera aleatoria utilizando la librería
``random``. A partir de este punto, los segmentos finales de los individuos se
intercambian utilizando *slicing*.

La función **modifica directamente** a los individuos originales y regresa una
tupla con referencias a ambos descendientes.

.. note::

   Esta versión del operador de cruza asume que los individuos ya son copias
   independientes dentro de la población. Si se aplicara directamente sobre
   individuos que aún están referenciados en generaciones anteriores, podrían
   producirse efectos secundarios no deseados.

   En caso de requerir un comportamiento no destructivo, es preferible crear
   copias explícitas de los padres antes de aplicar el cruce.

Mutación
^^^^^^^^

El operador de **mutación** introduce pequeñas modificaciones aleatorias en los
individuos de una población. Su propósito principal es **mantener diversidad
genética** y evitar que el algoritmo genético se estanque prematuramente en
óptimos locales.

Mientras que la cruza combina información genética existente, la mutación
permite explorar nuevas configuraciones que no estaban presentes en la
población original. Por esta razón, aunque la mutación suele aplicarse con una
probabilidad baja, juega un papel fundamental en el equilibrio entre
**exploración** y **explotación** del espacio de búsqueda.

En nuestro caso, dado que los individuos están representados como listas
binarias, utilizaremos la mutación más sencilla: la **mutación *bit-flip***.
Este operador invierte el valor de uno o más bits del cromosoma, cambiando un
``0`` por un ``1`` o viceversa.

Una implementación básica de mutación *bit-flip* es la siguiente:

.. code-block:: python

   import random

   def bit_flip_mutation(individual, p=0.01):
       """
       Mutación bit-flip sobre un individuo binario.

       individual : list
           Individuo a mutar.
       p : float
           Probabilidad de mutación por gen.
       """
       for i in range(len(individual)):
           if random.random() < p:
               individual[i] = 1 - individual[i]
       return individual

En esta función, cada bit del individuo tiene una probabilidad ``p`` de ser
invertido. Valores pequeños de ``p`` (por ejemplo, entre ``0.001`` y ``0.05``)
son comunes en la práctica, ya que una tasa de mutación demasiado alta puede
convertir el algoritmo en una búsqueda casi aleatoria.

Al igual que en el operador de cruza, esta función modifica al individuo
**directamente** (*in place*). Por lo tanto, es importante asegurarse de que los
individuos sobre los que se aplica la mutación no estén compartiendo referencias
con generaciones anteriores.

Con la incorporación de los operadores de **selección**, **cruza** y
**mutación**, ya contamos con los elementos esenciales de un algoritmo genético
básico. En la siguiente sección integraremos estos componentes en un ciclo
completo de evolución generacional.

Aplicación del cruce y mutación toda la población
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ahora que tenemos los elementos necesarios podemos crear una nueva población 
a partir de la copia de indivuos seleccionados:




