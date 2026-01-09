Metaheurísticas basadas en poblaciones
======================================

Como se discutió en la sección anterior, el control difuso propone una
alternativa heurística a los enfoques clásicos de control. Los controladores
difusos tienen como ventaja su flexibilidad y facilidad de interpretación. Sin
embargo, también observamos que el desempeño de un controlador difuso depende
de sus parámetros: los rangos de las variables, las funciones de membresía y la
base de reglas. El ajuste manual de estos parámetros puede ser un proceso muy
costoso, subjetivo y es difícil de realizar a gran escala.

En este capítulo proponemos el uso de **algoritmos genéticos** y de
**optimización por enjambre de partículas**, para abordar este tipo de
problemas. Estos algoritmos son métodos de optimización inspirados en procesos
naturales, como la selección natural y la inteligencia colectiva, que permiten
ajustar automáticamente los parámetros de un sistema a partir de su desempeño.

Metaheurísticas
---------------

Antes de entrar en detalle, conviene definir estas técnicas a partir del
concepto de **metaheurística**.

Una `metaheurística <https://en.wikipedia.org/wiki/metaheuristic>`_ es una
estrategia de alto nivel diseñada para guiar procesos de búsqueda y
optimización en problemas complejos, donde los métodos exactos o deterministas
son imprácticos o resultan demasiado costosos desde el punto de vista
computacional. Decimos que es de *alto nivel* porque la estrategia solo depende
de la representación y la función de aptitud, sin requerir aspectos analíticos
del problema que ataca (derivadas, convexidad, etc.) y, por lo tanto, puede
aplicarse a una gran variedad de problemas.

A diferencia de los algoritmos clásicos de optimización, las metaheurísticas no
requieren un modelo matemático explícito del problema (por ejemplo, derivadas,
convexidad o continuidad). En su lugar, tratan al sistema como una *caja negra*,
evaluando únicamente la calidad de una solución candidata mediante una función
de aptitud.

En general, las metaheurísticas presentan las siguientes características:

- Exploran el espacio de soluciones de forma **estocástica** o parcialmente
  aleatoria.
- Balancean la **exploración** (búsqueda global) y la **explotación** (mejora
  local).
- Son **robustas** frente a funciones de aptitud ruidosas, no diferenciables o
  multimodales.
- Pueden adaptarse a una amplia variedad de problemas sin cambios estructurales
  profundos.

Como ejemplos representativos de metaheurísticas se encuentran los
**algoritmos genéticos**, la **optimización por enjambre de partículas (PSO)**,
el **recocido simulado**, la **búsqueda tabú** y las **estrategias evolutivas**.

.. note::

   Algunos conceptos introducidos en esta sección pueden no resultar familiares
   en una primera lectura, como *espacio de búsqueda* o *función de aptitud*. No es
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
configuración particular puede representarse como una lista de unos y ceros:

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
solución**. A esta medida la llamaremos función de aptitud (*fitness*).

Supongamos que el valor de *fitness* puede ir de 0 a 20:

.. code-block:: pycon

   >>> fitness(r1)
   12

Ahora proponemos una segunda solución candidata modificando algunos parámetros:

.. code-block:: pycon

   r2 = [0, 0, 0, 1, 1, 0, 1, 1, 0, 1,
         0, 0, 1, 1, 1, 0, 1, 0, 0, 1]

   >>> fitness(r2)
   10

Esta es la esencia del problema: podemos generar soluciones candidatas y
evaluar su desempeño. Sin embargo, incluso en este caso aparentemente sencillo,
el **espacio de búsqueda** es considerable. El número total de configuraciones
posibles es:

.. code-block:: pycon

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
utilizaremos una lista de valores binarios (lo representamos como enteros).
Esta elección simplifica la explicación y nos permite centrarnos en el
funcionamiento general del algoritmo.

Para ilustrar la idea, utilizaremos un problema clásico de los algoritmos
genéticos conocido como **onemax**. En este problema, la función de aptitud
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
comprensión**.

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

.. code-block:: pycon
   
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

Ya que tenemos listas (con un orden establecido), podemos generar una lista que
incluya el *fitness* de cada individuo. Una opción más elaborada puede 
incluir definir una clase ``individuo`` que incluya el *fitness* y 
otros atributos. Aquí buscamos una solución más básica:

.. code-block:: pycon

    >>> fitness = [one_max(i) for i in population]
    >>> fitness
    [11, 10, 11, 8, 11, 10, 7, 13, 11, 7]
    >>>

Vamos a unir ambas listas utilizando ``zip``, 
por ejemplo podemos listar a cada individuo con su aptitud:

.. code-block:: pycon

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
*fitness* correspondiente a cada uno. Existen implementaciones más elaboradas
que definen una clase ``individuo`` para almacenar tanto el cromosoma como su
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
Una forma práctica de hacerlo es utilizando la función ``zip``, que
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

En cada torneo se eligen aleatoriamente ``k`` individuos sin reemplazo y gana el de
mayor *fitness*. Al repetir torneos para llenar la nueva población, un mismo
individuo puede ganar varias veces, por lo que el proceso global equivale a una
selección con reemplazo. Este procedimiento se repite tantas veces como individuos se
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
valor muy bajo puede hacer más lenta la convergencia del algoritmo. Por esta razón,
el tamaño del torneo se considera un **parámetro de diseño** del algoritmo
genético.

A continuación se muestra una implementación sencilla de selección por torneo
en:

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
       candidates.sort(key=lambda x: x[1], reverse=True)
       return candidates[0][0]

Esta función devuelve un individuo seleccionado mediante torneo. Para construir
una nueva población basta con repetir este proceso hasta obtener el número de
individuos deseado.

En el código anterior se utiliza una función ``lambda`` para ordenar a los
candidatos por el segundo elemento de la tupla, es decir, por el valor de
*fitness*.

Generación de la población seleccionada
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Los ganadores de los torneos son los **seleccionados para reproducirse** y
transmitir su material genético a la siguiente generación.

Es normal que algunos individuos ganen varios torneos; por lo tanto, pueden
aparecer más de una vez en la población seleccionada (se reproducen varias
veces). En términos de programación, es importante crear **copias** de los
individuos seleccionados, ya que si dejamos referencias, una modificación
posterior (por ejemplo, durante cruza o mutación) podría afectar a múltiples
entradas de la lista.

El código para crear la nueva población queda muy compacto utilizando listas
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

Una manera muy compacta de formar parejas consecutivas es utilizar
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
~~~~~~~~~~~~~~~~~

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

   def bit_flip_mutation(individual, pb_flip=0.01):
       """
       Mutación bit-flip sobre un individuo binario.

       individual : list
           Individuo a mutar.
       pb_flip : float
           Probabilidad de mutación por gen.
       """
       for i in range(len(individual)):
           if random.random() < pb_flip:
               individual[i] = 1 - individual[i]
       return individual

En esta función, cada bit del individuo tiene una probabilidad ``pb_flip`` de ser
invertido. Valores pequeños de ``pb_flip`` (por ejemplo, entre ``0.001`` y ``0.05``)
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

Aplicación del cruce y mutación a toda la población
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ahora que ya tenemos los operadores genéticos de **selección**, **cruce** y
**mutación**, podemos combinarlos para generar una nueva población a partir de
los individuos seleccionados. Esta población resultante es la nueva generación.
El número de generaciones es otro parámetro de diseño importante ``NGEN``. 

El proceso general es el siguiente:

1. Partimos de la selección de los mejores individuos de la población (obtenida, por ejemplo, mediante
   selección por torneo). Esta selección está conformada por copias de los mejores individuos.
2. Barajamos la población para evitar sesgos debidos al orden.
3. Formamos parejas consecutivas. Estas parejas son referencias a los individuos seleccionados previamente.
4. Con cierta probabilidad ``PB_CRUCE`` aplicamos el operador de cruce a cada pareja para generar descendientes.
5. Con cierta probabilidad ``PB_MUT`` aplicamos el operador de mutación a cada descendiente.

A continuación vemos implementación básica de este proceso. El script completo
lo podemos ver en anexos.

.. code-block:: python
   :linenos:

    import random
    # Probabilidades y número de generaciones
    PB_CRUCE, PB_MUT, NGEN = 0.5, 0.1, 40

    # Población inicial (300 individuos, cromosomas de longitud 100)
    population = get_population(300, 100)

    # Desempeño de los individuos de la población
    fitness = [one_max(i) for i in population]

    for n in range(NGEN):
        # 1) Selección (con reemplazo) + copia para evitar referencias compartidas
        selected = [tournament_selection(population, fitness)[:] 
                for _ in range(len(population))]

        # 2) Parejas aleatorias
        random.shuffle(selected)
        pairs = list(zip(selected[::2], selected[1::2]))

        # 3) Cruce (in place) con probabilidad  PB_CRUCE por pareja
        for child1, child2 in pairs:
           if random.random() < PB_CRUCE:
               one_point_crossover(child1, child2)
               
        # 4) Mutación (in place) con probabilidad PB_MUT por individuo
        for individual in selected:
            if random.random() < PB_MUT:
                # Mutación Bit Flip con probabilidad pb_flip de 0.05   
                bit_flip_mutation(individual, pb_flip=0.05)

        # Reemplazamos la población anterior con la nueva
        population[:] = selected
        # Calculamos el fitness de la nueva generación 
        fitness = [one_max(i) for i in population]
        print(f'Gen:{n} Mejor:{max(fitness)}')

DEAP
****

En el script anterior, la única condición de paro es el número de
generaciones. Sin embargo, en problemas reales debemos considerar 
otras condiciones, por ejemplo:

- **Solución parcial:** podemos detener el algoritmo si se alcanza un
  valor para la función de aptitud (*fitness*) mayor a un umbral (o un error menor).
- **Estancamiento:** detener el algoritmo si el *fitness* no mejora durante un
  número fijo de generaciones (criterio de convergencia práctica).
- **Diversidad de la población:** monitorear si la población se vuelve demasiado
  homogénea. En ese caso, podríamos ajustar parámetros dentro del ciclo (por
  ejemplo, aumentar la probabilidad de mutación) para recuperar exploración.

Otro aspecto importante son las variantes que podríamos implementar para atacar
problemas más generales. Por ejemplo:

- Representaciones distintas a listas binarias (valores enteros o **continuos**).
- Operadores genéticos alternativos, como **cruce de dos puntos** o **cruce
  uniforme**.
- Mutaciones para variables continuas, como la **mutación gaussiana**.
- Esquemas de reemplazo con elitismo explícito, o selección con presión
  ajustable.

Una solución práctica para acceder a estas variantes es utilizar una librería
especializada que ya implemente los componentes más comunes. Una de las
bibliotecas más utilizadas en Python para algoritmos evolutivos es `DEAP`_.

Por ejemplo, el script anterior puede implementarse con DEAP de la siguiente
manera:

.. code-block:: python
   :linenos:

   import random
   from deap import base, creator, tools, algorithms

   creator.create("FitnessMax", base.Fitness, weights=(1.0,))
   creator.create("Individual", list, fitness=creator.FitnessMax)

   toolbox = base.Toolbox()

   toolbox.register("attr_bool", random.randint, 0, 1)
   toolbox.register("individual", tools.initRepeat, creator.Individual,
                    toolbox.attr_bool, n=100)
   toolbox.register("population", tools.initRepeat, list, toolbox.individual)

   def evalOneMax(individual):
       return sum(individual),

   toolbox.register("evaluate", evalOneMax)
   toolbox.register("mate", tools.cxTwoPoint)
   toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
   toolbox.register("select", tools.selTournament, tournsize=3)

   population = toolbox.population(n=300)

   NGEN = 40
   for gen in range(NGEN):
       offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
       fits = toolbox.map(toolbox.evaluate, offspring)

       for fit, ind in zip(fits, offspring):
           ind.fitness.values = fit

       population = toolbox.select(offspring, k=len(population))
       print(tools.selBest(population, k=1))

.. _DEAP: https://deap.readthedocs.io/en/master/

Vemos algunas diferencias importantes:

- En DEAP se define explícitamente una estructura ``Individual`` que incluye el
  cromosoma y su atributo ``fitness``. Este atributo es una **tupla**, lo cual
  permite abordar de forma natural problemas de **optimización multiobjetivo**.

- Los operadores genéticos (selección, cruce, mutación y evaluación) se
  registran en un objeto ``toolbox``, lo que facilita intercambiar componentes y
  experimentar con distintas configuraciones del algoritmo.

- El ciclo evolutivo se expresa mediante operaciones de **alto nivel** (por
  ejemplo, ``algorithms.varAnd``), lo que hace que el código sea más compacto,
  legible y reutilizable.

- El objeto ``toolbox`` incluye otras estructuras y utilidades que simplifican
  la construcción de algoritmos evolutivos más complejos.

- Es posible implementar de manera sencilla problemas de **maximización** y
  **minimización**, simplemente ajustando la definición del objeto ``Fitness``.

- La librería proporciona herramientas para recopilar **estadísticas del
  proceso evolutivo**, como promedios, máximos, mínimos y desviaciones estándar
  del *fitness* por generación.

- Además de algoritmos genéticos, DEAP implementa otros métodos de búsqueda
  basados en poblaciones, como **optimización por enjambre de partículas
  (PSO)**.

PSO
---

Veamos ahora **PSO (Particle Swarm Optimization)**, un algoritmo bioinspirado
propuesto por J. Kennedy y R. Eberhart en 1995 :cite:`eberhart1995new`.

Este algoritmo ataca problemas de **optimización continua** de una manera
conceptualmente distinta a los algoritmos genéticos. Mientras que los
algoritmos genéticos se inspiran en la selección natural y operan mediante
operadores discretos como selección, cruce y mutación, PSO se basa en el
comportamiento colectivo observado en sistemas naturales como parvadas de aves
o bancos de peces. En lugar de recombinar soluciones, PSO ajusta de manera
iterativa un conjunto de **partículas** que se desplazan en el espacio de
búsqueda siguiendo reglas simples de movimiento.

Cada partícula representa una solución candidata y mantiene información tanto
de su **mejor posición individual** como de la **mejor posición encontrada por
el grupo**. A partir de estas referencias, las partículas actualizan su
velocidad y posición, logrando un balance entre exploración global y
explotación local.

La velocidad de cada partícula se actualiza únicamente a partir de
la atracción hacia su mejor posición individual y la mejor posición global del
enjambre. 

Tenemos:

- :math:`x_i(t)` la posición de la partícula :math:`i` en la iteración :math:`t`,
- :math:`v_i(t)` su velocidad,
- :math:`p_i` la mejor posición encontrada por la partícula (*personal best*),
- :math:`g` la mejor posición encontrada por el enjambre (*global best*).

En esta versión simplificada (sin término de inercia), la ecuación de
actualización de la velocidad se define como:

.. math::

   v_i(t+1) = c_1 r_1 \big(p_i - x_i(t)\big)
              + c_2 r_2 \big(g - x_i(t)\big)

y la actualización de la posición como:

.. math::

   x_i(t+1) = x_i(t) + v_i(t+1)

donde:

- :math:`c_1` es el **coeficiente cognitivo**, que mide cuánto confía la partícula
  en su propia experiencia,
- :math:`c_2` es el **coeficiente social**, que mide la influencia del enjambre,
- :math:`r_1, r_2 \sim \mathcal{U}(0,1)` son números aleatorios uniformes que
  introducen variabilidad estocástica en el movimiento.

En esta versión elemental del algoritmo, cada partícula se mueve directamente
hacia una combinación de su mejor solución conocida y la mejor solución global.

Estas ecuaciones reflejan el comportamiento colectivo del enjambre: cada
partícula es atraída tanto por su experiencia individual como por el
conocimiento compartido del grupo. 

.. note::

    Una de las mejoras a este algoritmo básico es agregar un término de inercia
    que permite regular mejor el balance entre **exploración** y
    **explotación** del espacio de búsqueda.

Vamos a utilizar el ejemplo básico de la documentación de la librería ``DEAP``
para discutir su implementación. De la descripción del algoritmo
vemos que ahora necesitamos almacenar información adicional para cada
partícula. Su posición, velocidad y mejor *fitness* hasta el momento. También
debemos almacenar información de la mejor partícula hasta el momento. 
Para esto ``DEAP`` utiliza una nueva estructura ``Particle``:

.. code-block:: python
    :linenos:

    import operator
    import random

    import numpy
    import math

    from deap import base
    from deap import benchmarks
    from deap import creator
    from deap import tools

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Particle", list, fitness=creator.FitnessMax, speed=list, 
        smin=None, smax=None, best=None)

En este caso importamos la librería ``benchmarks`` que incluye el problema de optimización 
a resolver. Vemos que es un problema de maximización. 

Debemos agregar una función para crear de manera aleatoria las partículas de tamaño ``size``. Tanto la posición 
como la velocidad incluyen limites mínimos y máximos para evitar que las particulas 
se salgan del espacio de búsqueda. En este caso los valores aleatorios son contínuos y 
se generan dentro del rango ``smin`` y ``smax``:

.. code-block:: python
    :linenos:

    def generate(size, pmin, pmax, smin, smax):
        part = creator.Particle(random.uniform(pmin, pmax) for _ in range(size)) 
        part.speed = [random.uniform(smin, smax) for _ in range(size)]
        part.smin = smin
        part.smax = smax
        return part

``DEAP`` nos permite incluir un método para actualizar a la partícula en cada iteración. 
En este caso lo hacemos de manera básica utilizando las reglas de actualización vistas
anteriormente:

.. code-block:: python
    :linenos:

    def updateParticle(part, best, phi1, phi2):
        u1 = (random.uniform(0, phi1) for _ in range(len(part)))
        u2 = (random.uniform(0, phi2) for _ in range(len(part)))
        v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
        v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
        part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
        for i, speed in enumerate(part.speed):
            if abs(speed) < part.smin:
                part.speed[i] = math.copysign(part.smin, speed)
            elif abs(speed) > part.smax:
                part.speed[i] = math.copysign(part.smax, speed)
        part[:] = list(map(operator.add, part, part.speed))

El método de actualización recibe los parámetros ``phi1`` y ``phi2`` que
corresponden a los coeficientes *cognitivo* y *social* de PSO. Los vectores
``u1`` y ``u2`` son los factores estocásticos. Por último se restringe la
partícula al espacio de búsqueda.

Se registran los elementos en el ``toolbox``:

.. code-block:: python
    :linenos:

    toolbox = base.Toolbox()
    toolbox.register("particle", generate, size=2, pmin=-6, pmax=6, smin=-3, smax=3)
    toolbox.register("population", tools.initRepeat, list, toolbox.particle)
    toolbox.register("update", updateParticle, phi1=2.0, phi2=2.0)
    toolbox.register("evaluate", benchmarks.h1)

El *benchmark* utilizado es ``h1`` y el ejemplo trabaja en dos dimensiones
(``size=2``). Los valores ``phi1=2.0`` y ``phi2=2.0`` se utilizan comúnmente en
ejemplos introductorios y son una elección estándar en múltiples referencias de
PSO.

.. note::

   En este ejemplo, el espacio de búsqueda se limita a ``[-6, 6]`` y la velocidad
   a ``[-3, 3]``. En problemas reales, estos rangos deben elegirse con base en la
   interpretación física o numérica de los parámetros que se están optimizando.

Finalmente, el ciclo del algoritmo propuesto por la documentación es el siguiente:

.. code-block:: python
    :linenos:

     def main():
        pop = toolbox.population(n=5)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        logbook = tools.Logbook()
        logbook.header = ["gen", "evals"] + stats.fields

        GEN = 1000
        best = None

        for g in range(GEN):
            for part in pop:
                part.fitness.values = toolbox.evaluate(part)
                if not part.best or part.best.fitness < part.fitness:
                    part.best = creator.Particle(part)
                    part.best.fitness.values = part.fitness.values
                if not best or best.fitness < part.fitness:
                    best = creator.Particle(part)
                    best.fitness.values = part.fitness.values
            for part in pop:
                toolbox.update(part, best)

            # Gather all the fitnesses in one list and print the stats
            logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
            print(logbook.stream)

        return pop, logbook, best

    if __name__ == "__main__":
        main()

En este caso se lleva un registro del avance del algoritmo mediante los objetos
``stats`` y ``logbook``. El ciclo es conceptualmente parecido al que vimos en
algoritmos genéticos: se evalúa a la población y se registra su desempeño. La
diferencia principal es que en PSO **no se generan descendientes** por cruza y
mutación; en su lugar, se mantienen las partículas y se **actualiza su posición**
iterativamente con base en la información de su mejor solución personal y la
mejor solución global del enjambre.

Optimización del Controlador Difuso con PSO
-------------------------------------------

En secciones anteriores diseñamos un **controlador difuso base** para el
problema de seguimiento de ruta. Si bien este controlador es funcional, su
desempeño depende de múltiples parámetros, como la forma y los rangos de las
funciones de membresía.

El ajuste manual de estos parámetros puede resultar complicado, costoso en
tiempo y altamente dependiente de la experiencia del diseñador. En esta
sección abordamos este problema utilizando una **metaheurística basada en
poblaciones**, específicamente **optimización por enjambre de partículas
(PSO)**, para ajustar automáticamente los parámetros del controlador difuso.

El objetivo no es obtener el controlador “perfecto”, sino ilustrar cómo
**técnicas de cómputo inteligente pueden combinarse** para resolver problemas
complejos de manera práctica.

Parametrización del controlador difuso
--------------------------------------

Para poder optimizar el controlador, primero es necesario **hacer explícitos
los parámetros ajustables** del sistema difuso. En nuestro caso, estos
parámetros corresponden a valores que definen la forma y el ancho de las
funciones de membresía de las variables difusas.

En lugar de codificar estos valores directamente en el código, se utiliza un
vector de parámetros reales:

.. math::

   \mathbf{p} = [p_1, p_2, \dots, p_n]

Cada partícula del algoritmo PSO representa una posible configuración del
controlador difuso, es decir, un conjunto particular de parámetros que definen
las funciones de membresía.

El archivo ``tunable_fuzzy.py`` implementa esta idea, permitiendo construir un
FIS a partir de un vector de parámetros.

.. note::

   En esta implementación, el controlador difuso sigue utilizando únicamente
   las variables de error geométrico ``e`` y ``e_{th}``. No se introduce
   conocimiento adicional del modelo ni de la velocidad del robot.

Normalización de variables difusas
----------------------------------

Un paso clave para facilitar la optimización es la **normalización de las
variables difusas**. En lugar de trabajar directamente con unidades físicas
(metros, radianes), los errores se escalan a rangos adimensionales fijos, por
ejemplo:

.. math::

   e, e_{th} \in [-1, 1]

Esto tiene varias ventajas:

- Reduce la sensibilidad del algoritmo a la escala de las variables.
- Permite reutilizar la misma estructura del FIS en distintos escenarios.
- Facilita la búsqueda en el espacio de parámetros por parte del PSO.

La normalización se realiza fuera del FIS, manteniendo el controlador como una
*caja negra* desde el punto de vista del optimizador.

Definición de la función de aptitud 
-----------------------------------

Para evaluar la calidad de un controlador difuso necesitamos definir una
**función de aptitud**. En este trabajo utilizamos como métrica
el **error cuadrático medio (RMSE)** del error lateral a lo largo de
una o varias rutas de referencia.

La función de evaluación sigue el siguiente esquema:

1. Construir el controlador difuso a partir del vector de parámetros.
2. Ejecutar la simulación para un conjunto fijo de rutas.
3. Calcular el RMSE del error lateral.
4. Penalizar configuraciones que no alcanzan la meta o divergen.

Desde el punto de vista del optimizador, el proceso completo se ve como una
función:

.. math::

   \mathbf{p} \;\longrightarrow\; \text{RMSE}

El archivo ``evaluate_controller.py`` implementa esta lógica y actúa como
interfaz entre el simulador y el algoritmo PSO.

.. note::

   El simulador puede terminar anticipadamente si el error crece demasiado o si
   el robot no alcanza la meta. Esto reduce el costo computacional durante la
   optimización.

Optimización mediante PSO
-------------------------

Una vez definida la función de aptitud, el problema se reduce a minimizarla en un
espacio continuo de parámetros. Para ello utilizamos **PSO**, una
metaheurística inspirada en el movimiento colectivo de enjambres.

Cada partícula representa un controlador difuso distinto. Durante el proceso:

- Las partículas exploran el espacio de parámetros.
- Cada partícula recuerda su mejor solución histórica.
- El enjambre comparte información sobre la mejor solución global encontrada.

La implementación se basa en la librería ``DEAP`` y se encuentra en el archivo
``pso.py``.

El resultado del proceso es un vector de parámetros que produce el mejor
desempeño observado durante la optimización. Este resultado se guarda en un
archivo de configuración:

.. code-block:: text

   best_controller.json

Este archivo permite **reproducir y analizar** el controlador optimizado sin
necesidad de volver a ejecutar el algoritmo PSO.

Visualización y análisis del controlador optimizado
---------------------------------------------------

Una vez obtenido el mejor conjunto de parámetros, es posible:

- visualizar las funciones de membresía resultantes,
- ejecutar la simulación para rutas individuales,
- comparar visualmente el desempeño frente al controlador base.

El script ``show_controller.py`` cumple esta función y permite seleccionar la
ruta a evaluar como parámetro de entrada.

Este paso es importante desde un punto de vista pedagógico: aunque el proceso
de optimización es automático, **la interpretación del resultado sigue siendo
humana**.

Limitaciones
------------

El enfoque presentado ilustra varias ideas clave:

- El control difuso es **heurístico** y altamente parametrizable.
- Las metaheurísticas permiten automatizar el ajuste de sistemas complejos.
- El resultado no es necesariamente óptimo ni único.
- El costo computacional puede ser elevado.

En este capítulo hemos dejado deliberadamente fuera varios aspectos, como la
optimización multiobjetivo, la selección automática de reglas o la adaptación
en línea del controlador. Estos temas quedan como trabajo futuro o ejercicios
avanzados.

Control inteligente y cómputo suave
-------------------------------------------

El controlador difuso optimizado mediante PSO es un ejemplo representativo de
**computación inteligente** o **cómputo suave** (*soft computing*): una
combinación de técnicas aproximadas, interpretables y adaptativas que permiten
resolver problemas para los cuales los enfoques clásicos resultan poco
prácticos.

Más que reemplazar a la teoría de control tradicional, estas técnicas la
complementan, ofreciendo herramientas flexibles para enfrentar incertidumbre,
no linealidades y complejidad creciente.

En el siguiente capítulo abordaremos el problema del **alto costo computacional**
asociado a este tipo de métodos, utilizando técnicas de **cómputo distribuido**.

Las metaheurísticas basadas en poblaciones son **altamente paralelizables**, ya
que la evaluación de cada individuo o partícula puede realizarse de manera
independiente. Esta característica las hace particularmente adecuadas para
aprovechar arquitecturas de cómputo modernas, como sistemas multinúcleo,
clusters o entornos distribuidos.

Con esta motivación, implementaremos una variante de **PSO multi-enjambre**, en
la cual varios enjambres evolucionan en paralelo e intercambian información de
forma controlada. Este enfoque permite reducir el tiempo total de optimización y,
al mismo tiempo, mejorar la exploración del espacio de búsqueda.

Resumen del capítulo
--------------------

En este capítulo se introdujeron las **metaheurísticas basadas en poblaciones**
como una estrategia práctica para resolver problemas de optimización donde los
métodos exactos resultan inviables. A diferencia de enfoques deterministas, las
metaheurísticas tratan al sistema como una *caja negra* y evalúan soluciones
candidatas únicamente mediante una **función de aptitud** (*fitness*), incorporando
componentes estocásticos para balancear **exploración** y **explotación** del
espacio de búsqueda.

A partir de un ejemplo con parámetros binarios, se explicó el concepto de
**espacio de búsqueda** y por qué evaluar todas las configuraciones puede ser
computacionalmente prohibitivo. Con esta motivación se construyó un
**algoritmo genético básico**, describiendo sus componentes esenciales:
representación de individuos, evaluación de la población, **selección por
torneo**, **cruce de un punto** y **mutación bit-flip**, así como un ciclo
generacional que produce nuevas poblaciones de manera iterativa.

Posteriormente se presentó la librería **DEAP** como una alternativa para
implementar algoritmos evolutivos de forma más estructurada y reutilizable,
mostrando cómo registrar operadores en un ``toolbox`` y cómo expresar el proceso
evolutivo con funciones de alto nivel. Finalmente, se introdujo **PSO (Particle
Swarm Optimization)** como un método bioinspirado orientado a optimización
continua, explicando su intuición (mejor posición personal y global), sus
ecuaciones de actualización de velocidad y posición, y un ejemplo de
implementación con DEAP.

El capítulo cierra conectando estas técnicas con la **optimización de
controladores difusos**, motivando la parametrización del controlador y el uso
de PSO para ajustar automáticamente funciones de membresía y otros parámetros a
partir de métricas de desempeño, y preparando el terreno para abordar el costo
computacional y la paralelización en capítulos posteriores.

