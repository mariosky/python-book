Escalado Computacional en Python
================================

En los capítulos anteriores hemos explorado diversas aplicaciones de Python
que, pueden llegar a requerir una **demanda considerable de
recursos computacionales**. Cuando el costo computacional de estas tareas
crece demasiado, el escalado deja de ser algo opcional y se convierte en una
necesidad. Algunas de las tareas con alta demanda de recursos son:

- **Optimización basada en poblaciones.**  

  Los algoritmos de optimización basados en poblaciones requieren evaluar de
  manera repetida el desempeño de un conjunto de soluciones candidatas. Esta
  evaluación puede resultar especialmente costosa cuando implica la ejecución
  de simulaciones o requieren modelos computacionales complejos. Un ejemplo es
  la evaluación del desempeño del controlador difuso del capítulo anterior.

- **Ajuste de los hiperparámetros de algoritmos de aprendizaje automático.**  

  Muchos algoritmos de aprendizaje automático requieren una etapa de
  entrenamiento computacionalmente intensiva, y su desempeño depende de los
  hiperparámetros utilizados. Cuando ajustamos estas combinaciones de
  parámetros debemos realizar muchos experimentos de prueba y validación lo
  cual incrementa de forma significativa el tiempo de cómputo. También
  necesitamos múltiples muestras de ejecuciones del algoritmo cuando realizamos
  **comparaciones estadísticas**.

- **Flujos de trabajo de aprendizaje automático.**  

  Más allá del entrenamiento de modelos, los flujos de trabajo completos de
  aprendizaje automático suelen incluir etapas de preprocesamiento de datos,
  extracción de características, entrenamiento y evaluación. En conjunto, estas
  operaciones pueden demandar una cantidad considerable de recursos de
  procesamiento, especialmente cuando se trabaja con conjuntos de datos grandes.

- **Análisis de datos.**  

  El procesamiento y análisis de grandes volúmenes de datos, por ejemplo, en
  tareas de clasificación de texto o análisis de sentimientos, puede superar
  fácilmente la capacidad de cómputo local, haciendo necesario recurrir a
  técnicas de cómputo distribuido.

Estos tareas comparten ciertas características que nos permiten escalarlas
utilizando **técnicas de procesamiento en paralelo**, ya que incluyen trabajos
que pueden realizarse de forma independiente. En particular, observamos los
siguientes casos:

- Es posible evaluar el desempeño de soluciones candidatas de manera
  independiente, sin necesidad de comunicación entre ellas.

- Es posible ejecutar metaheurísticas basadas en poblaciones utilizando
  múltiples poblaciones más pequeñas, las cuales pueden evolucionar de forma
  independiente durante varias iteraciones, para después intercambiar
  soluciones candidatas entre sí para incrementar la diversidad.

- Podemos ejecutar varios algoritmos de aprendizaje automático de manera
  simultánea, probando de forma independiente distintos valores de sus 
  parámetros.

- En tareas de análisis de datos, como el procesamiento de texto, es posible
  dividir el corpus en subconjuntos más pequeños para realizar operaciones de
  procesamiento independientes, cuyos resultados se integran posteriormente en
  un resultado final.

En conjunto, estos ejemplos nos muestran que es posible **escalar los
algoritmos dividiendo el trabajo en tareas independientes**, las cuales pueden
ejecutarse **en paralelo** en distintos procesadores o núcleos de cómputo.

Veamos ahora algunos **modelos comunes de paralelización de tareas**. Estos
modelos describen distintas formas de dividir y distribuir el trabajo cuando se
requiere escalar la ejecución de algoritmos computacionalmente costosos.

Colas de trabajo
----------------

Un modelo básico de escalado es la paralelización de tareas mediante el uso de
**colas de trabajo** y *workers* (trabajadores). En este enfoque, el sistema se
compone de varios elementos con responsabilidades bien definidas:

- **Worker.**  
  Es un componente de software que solicita tareas a una cola de mensajes y las
  ejecuta de manera independiente. El *worker* procesa cada tarea de forma
  asíncrona respecto al componente que la generó. En este modelo, la única
  comunicación y coordinación entre las partes ocurre **a través de la cola de
  mensajes**, por lo que no es necesario que el productor y el *worker* se coordinen
  en el tiempo.

- **Productor.**  
  Cuando se requiere ejecutar una operación costosa, el productor crea un
  mensaje que representa la tarea y lo agrega a la cola de trabajo. Una vez
  enviada la tarea, el productor no espera su finalización inmediata y puede
  continuar realizando otras operaciones.

- **Cola de tareas.**  
  Es un servicio encargado de recibir las tareas en forma de mensajes y
  entregarlas a los *workers* que las solicitan. Típicamente, la entrega se
  realiza siguiendo una política FIFO (*First In, First Out*), es decir, el primero
  en llegar, es el primero en salir.

En algunos casos, si una tarea no se completa correctamente, la cola puede
reasignarla a otro *worker* para su ejecución. Una vez procesada la tarea, los
*workers* pueden depositar el resultado en otra cola de mensajes o notificar al
sistema que la ejecución ha finalizado.

Estado compartido y estado encapsulado
---------------------------------------

Al paralelizar la ejecución de tareas, una decisión fundamental de diseño es
determinar **cómo se gestiona el estado del sistema**. En términos generales,
podemos distinguir entre dos enfoques: estado compartido y estado encapsulado.

En un modelo de **estado compartido**, múltiples tareas o componentes necesitan
compartir información entre ellas, o deben modificar/leer una memoria global.
Aunque este enfoque puede ser eficiente en ciertos escenarios, introduce
complejidad adicional, ya que es necesario coordinar el acceso concurrente al
estado global evitando inconsistencias.

Por el contrario, en un modelo de **estado encapsulado**, cada componente mantiene
su propio estado interno, y este no puede ser modificado directamente por otros
componentes. La interacción ocurre únicamente mediante el intercambio de mensajes
o solicitudes explícitas. Este enfoque reduce la necesidad de sincronización y
facilita el razonamiento sobre el comportamiento del sistema.

En problemas como los abordados en este libro el estado suele tener una estructura
bien definida (por ejemplo, una población, un modelo o un subconjunto de datos),
lo que hace especialmente atractivo el uso de estado encapsulado.

.. note::

   **Recordatorio del concepto de estado**

   Recordemos que en la programación orientada a objetos, el *estado* de un
   objeto corresponde al conjunto de valores almacenados en sus atributos en un
   momento dado. Este estado puede modificarse a lo largo del tiempo mediante la
   ejecución de métodos del objeto.

   En este capítulo utilizamos el término *estado* en un sentido análogo: un
   componente con estado mantiene información persistente entre distintas etapas
   de la ejecución del algoritmo (por ejemplo, una población, un modelo entrenado
   o un conjunto de parámetros). Por el contrario, una función sin estado no
   conserva información entre ejecuciones y su resultado depende únicamente de
   sus entradas.

Funciones sin estado y actores con estado
-----------------------------------------

Además de la forma en que se gestiona el estado, es útil distinguir entre dos
modelos complementarios de ejecución al escalar algoritmos computacionales:
**funciones sin estado (*stateless*)** y **actores con estado (*stateful*)**.

Una **función sin estado** es aquella cuyo resultado depende únicamente de sus
parámetros de entrada y no modifica ni depende de un estado interno persistente.
Este tipo de funciones también se conoce como *funciones puras* en el contexto de
la programación funcional. Debido a esta propiedad, las funciones sin estado
pueden ejecutarse en paralelo de manera segura, ya que no requieren coordinación
ni sincronización entre ejecuciones.

Este modelo es especialmente adecuado para tareas como:

- la evaluación independiente de la aptitud (*fitness*) de una solución candidata,
- la ejecución de simulaciones,
- el procesamiento de datos por lotes.

Por otro lado, un **actor con estado** encapsula datos que persisten a lo largo
del tiempo y que se modifican conforme avanza la ejecución del algoritmo. Un
actor mantiene su propio estado interno y solo expone un conjunto de
operaciones para interactuar con él. 

Este enfoque resulta natural en algoritmos iterativos donde el estado evoluciona
progresivamente, como:

- metaheurísticas basadas en poblaciones,
- procesos de entrenamiento de modelos de aprendizaje automático,
- sistemas que requieren coordinación entre múltiples entidades.

En la práctica, ambos modelos suelen **combinarse**. Por ejemplo, un actor puede
coordinar la ejecución de múltiples funciones sin estado para realizar cálculos
costosos, manteniendo al mismo tiempo el estado global del algoritmo.

El Modelo Actor
---------------

Propuesto por Carl Hewitt en 1973, el **Modelo Actor** es una abstracción de
programación que formaliza el uso de estado encapsulado para la ejecución
concurrente de tareas. En este modelo, un *actor* es una entidad
que:

- mantiene su propio estado interno,
- expone un conjunto de operaciones,
- puede crear otros actores,
- y se comunica con otros actores **exclusivamente** mediante el envío de mensajes.

Un actor no accede directamente al estado de otros actores. Toda interacción se
realiza de forma explícita, lo que elimina la necesidad de mecanismos de
sincronización complejos y facilita el escalado del sistema.

Este modelo resulta especialmente adecuado para los casos que nos interesan en
este capítulo. Por ejemplo, en optimización poblacional, un actor puede representar
una población o *swarm*.

.. sidebar:: Sistemas reactivos y aplicaciones *cloud-native*

   En la literatura sobre sistemas distribuidos modernos, los modelos presentados
   en este capítulo suelen asociarse con el desarrollo de aplicaciones
   *cloud-native* y sistemas reactivos.

   De manera general, un sistema reactivo se caracteriza por estar compuesto por
   componentes desacoplados que se comunican mediante el intercambio de mensajes,
   pueden escalar de forma horizontal y están diseñados para tolerar fallos. En
   este contexto, el uso de funciones sin estado y componentes con estado
   encapsulado permite construir aplicaciones más flexibles y escalables.

   Las arquitecturas basadas en *workers*, colas de mensajes y actores son
   ejemplos de cómo estos principios se implementan en la práctica. Sin embargo,
   en este capítulo nos centramos en los **patrones computacionales y algorítmicos**
   subyacentes, independientemente de la infraestructura de despliegue utilizada.

Ray para Python Distribuido
---------------------------

Existen lenguajes de programación que adoptan los principios del Modelo Actor de
manera **inherente**, es decir, el modelo forma parte fundamental del lenguaje y
de su semántica. Un ejemplo clásico es *Erlang*, donde los procesos ligeros y el
paso de mensajes son el mecanismo principal para estructurar aplicaciones
concurrentes y distribuidas.

Otros lenguajes incorporan el Modelo Actor de forma más **específica y acotada**.
Por ejemplo, *Ruby* introduce el concepto de *Ractor* como una abstracción
explícita para encapsular estado y permitir concurrencia segura mediante el
intercambio de mensajes, sin que este modelo sea dominante en todo el lenguaje.

Finalmente, existen **librerías y frameworks especializados** que implementan el
Modelo Actor sobre lenguajes de propósito general. Un ejemplo representativo es
*Akka*, ampliamente utilizado en aplicaciones distribuidas, el cual proporciona
una infraestructura completa para definir actores, manejar mensajes y construir
sistemas tolerantes a fallos.

El el caso de Python existen varias librerías y *frameworks* para escalar
algoritmos en Python utilizando el modelo de *Colas de Trabajos* como Celery y
RabbitMQ las cuales son librerías maduras y ampliamente utilizadas. Y también
algunas librerías para el modelo Actor como *Thespian* o *Ray*. En este
capítulo utilizaremos el *framework* Ray, ya que nos permite implementar ambos
modelos. Ray en su núcleo, se basa en los dos conceptos fundamentales que ya
hemos visto:

- **Tareas (*tasks*).**  
  Las tareas representan la ejecución remota de funciones sin estado. Una tarea
  se define a partir de una función Python y puede ejecutarse en paralelo con
  otras tareas, ya sea en distintos núcleos de una misma máquina o en distintos
  nodos de un clúster. 

- **Actores (*actors*).**  
  Los actores encapsulan estado persistente y permiten definir objetos remotos
  que mantienen información a lo largo del tiempo.

En las secciones siguientes ilustraremos estos modelos mediante ejemplos
concretos utilizando el framework Ray. Comenzaremos con un ejemplo de
optimización por enjambre de partículas (PSO) donde el cálculo de la función de
aptitud se paraleliza mediante funciones sin estado, coordinadas desde un
script principal. Posteriormente, presentaremos una variante basada en múltiples
poblaciones, donde cada población se modela como un actor con estado encapsulado.

Estos ejemplos muestran cómo los modelos de funciones sin estado y actores con
estado pueden utilizarse de forma independiente o combinada para escalar
algoritmos costosos computacionalmente.

Funciones *stateless*
---------------------

Desde los primeros trabajos en el campo de la optimización basada en
poblaciones se han propuesto diversas arquitecturas y estrategias para
escalar este tipo de algoritmos. De hecho, estos métodos suelen considerarse
especialmente adecuados para el cómputo en paralelo. La razón principal es
que la parte más costosa del algoritmo consiste en evaluar las soluciones
candidatas, y dicha evaluación puede realizarse de manera independiente.

En particular, la evaluación de la aptitud presenta las siguientes
características:

- Cada evaluación recibe como entrada únicamente la representación de la
  solución candidata (normalmente un vector de parámetros) y produce como
  salida una medida de aptitud (*fitness*).

- Una función que realiza esta evaluación no requiere mantener información
  entre llamadas consecutivas; es decir, no depende de un estado interno
  persistente.

- Para dos soluciones candidatas idénticas, el valor de aptitud obtenido es
  siempre el mismo.

Debido a estas propiedades, las funciones de aptitud pueden considerarse
**funciones sin estado (*stateless*)**. Esto permite ejecutarlas en paralelo
sin introducir problemas de consistencia, ya que no requieren leer ni
modificar memoria compartida.

Como ejemplo, modificaremos el código del algoritmo PSO presentado en el
capítulo anterior para que la evaluación de las soluciones candidatas se
realice en paralelo. Primero, recordemos la versión secuencial:

.. code-block:: python

   # Fragmento del algoritmo original
   for g in range(GEN):
       for part in pop:
           part.fitness.values = toolbox.evaluate(part)

En este fragmento, el algoritmo itera sobre cada elemento de la población
(en este caso, cada partícula) y evalúa su aptitud de manera secuencial.
Este ciclo se repite durante un número fijo de generaciones. El costo
computacional total del algoritmo puede estimarse, de forma aproximada, como
el producto del número de generaciones por el tamaño de la población.

En la versión secuencial, el programa se bloquea esperando a que cada llamada
a ``toolbox.evaluate(part)`` finalice antes de continuar con la siguiente
evaluación.

Al utilizar una librería de cómputo distribuido, el mismo ciclo de evaluación
toma una forma distinta:

.. code-block:: python

   futures_fitness_values = [
       remote_ev_controller.remote(list(particle))
       for particle in pop
   ]
   results = ray.get(futures_fitness_values)

De nuevo, se recorre la población para evaluar cada partícula. Sin embargo,
en lugar de devolver directamente el resultado de la evaluación, cada llamada
a una función remota devuelve una **referencia** y estas no bloquean la ejecución
mientras realizan el cálculo. 

La lista ``futures_fitness_values`` contiene referencias especiales a los
resultados que estarán disponibles en el futuro. Este tipo de referencias se
conoce comúnmente como **futures** o **promesas** (*promises*). En Ray, estas
referencias se denominan ``ObjectRef``.

De manera conceptual, cada llamada a la función remota puede entenderse como
una tarea que se agrega a una cola de trabajo. Cuando un *worker* toma una de
estas tareas y completa su ejecución, el resultado se almacena y queda
asociado a la referencia correspondiente.

Esta ejecución es **asíncrona**, ya que no importa el orden en el que se
realicen las evaluaciones. Dado que las funciones de aptitud son *stateless*,
el resultado no depende de la intercalación de las tareas.

No obstante, en este punto del algoritmo es necesario esperar a que todas las
evaluaciones de la población hayan concluido antes de continuar. Esto ocurre
en la segunda línea del fragmento anterior. La instrucción
``ray.get(futures_fitness_values)`` bloquea la ejecución hasta que todos los
resultados estén disponibles. Una vez completada esta llamada, la variable
``results`` contiene los valores de aptitud de todas las partículas, y el
algoritmo puede continuar con la siguiente etapa.

Para poder utilizar esta infraestructura de cómputo distribuido es necesario
instalar la librería Ray y sus dependencias. Una vez hecho esto, Ray puede
ejecutarse de manera local, utilizando automáticamente los núcleos de CPU
disponibles en la máquina.

El primer paso consiste en definir una función remota. Para ello basta con
importar el módulo ``ray`` y decorar la función que se desea ejecutar de forma
distribuida utilizando el decorador ``@ray.remote``:

.. code-block:: python

   import ray
   from evaluate_controller import evaluate_controller

   @ray.remote
   def remote_ev_controller(particle):
       return evaluate_controller(particle)

En este ejemplo, la función remota ``remote_ev_controller`` simplemente invoca
a la función local ``evaluate_controller`` para evaluar una solución candidata.
Es importante notar que **no es necesario modificar la lógica de evaluación
existente**: Ray se encarga de ejecutar la función en un *worker* disponible y
de gestionar la comunicación de los resultados.

A partir de este punto, cada llamada a
``remote_ev_controller.remote(...)`` crea una tarea independiente que puede
ejecutarse en paralelo con otras evaluaciones.

.. note::

   **Ejecución en clúster**

   Aunque en los ejemplos de este capítulo utilizamos Ray en modo local, el
   mismo código puede ejecutarse sin cambios en un entorno distribuido.
   Ray permite crear *clústeres* formados por varias máquinas físicas en una
   red local o por máquinas virtuales en la nube.

   Desde el punto de vista del programador, el modelo de programación es el
   mismo: las funciones remotas, los *workers* y las referencias a resultados
   se utilizan de manera idéntica. La diferencia radica únicamente en la
   infraestructura subyacente sobre la cual se ejecutan las tareas.

A continuación se muestran los resultados impresos de la ejecución del algoritmo
secuencial y del algoritmo distribuido (utilizando Ray). En ambos casos se
imprime el resumen estadístico por generación y el tiempo total de ejecución
medido con el comando ``time``.

Ejecución secuencial
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   (base)> time python pso.py
   gen  evals  avg     std     min       max
   0    50     9.80625 1.35624 0.312589  10
   1    50     9.80706 1.35057 0.353079  10
   2    50     10      0       10        10
   3    50     9.4191  2.29927 0.299577  10
   4    50     9.41963 2.29719 0.304851  10
   5    50     8.83545 3.15362 0.268492  10
   6    50     9.41942 2.298   0.284945  10
   7    50     9.22013 2.64468 0.244499  10
   8    50     8.83136 3.16469 0.227427  10
   9    50     9.02514 2.9246  0.224242  10
   10   50     8.63399 3.38564 0.225814  10
   11   50     9.21839 2.65056 0.224037  10
   12   50     8.43915 3.57639 0.224305  10
   13   50     8.43975 3.57501 0.224878  10
   14   50     8.43744 3.58027 0.223422  10
   15   50     8.63654 3.37933 0.224132  10
   16   50     8.24333 3.7494  0.222354  10
   17   50     8.05008 3.89985 0.224733  10
   18   50     7.85437 4.04011 0.222289  10
   19   50     7.46457 4.27742 0.224036  10
   (0.22228923395729627,) (0.22228923395729627,) (10.0,) (10.0,)
   python pso.py  504.70s user 7.01s system 100% cpu 8:26.91 total

Ejecución distribuida con Ray
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   (base) > time python pso_ray.py
   gen  evals  avg     std     min       max
   0    50     9.80543 1.36197 0.271625  10
   1    50     9.61276 1.89707 0.280407  10
   2    50     9.80485 1.36607 0.242367  10
   3    50     9.80578 1.35951 0.289244  10
   4    50     9.60888 1.91607 0.204239  10
   5    50     9.80572 1.35997 0.285893  10
   6    50     9.80547 1.36173 0.273391  10
   7    50     10      0       10        10
   8    50     9.60917 1.91469 0.221329  10
   9    50     9.80477 1.36661 0.238504  10
   10   50     9.60828 1.91905 0.203851  10
   11   50     10      0       10        10
   12   50     9.6083  1.91892 0.202428  10
   13   50     9.60891 1.91593 0.210575  10
   14   50     9.60819 1.91945 0.20373   10
   15   50     10      0       10        10
   16   50     9.80411 1.37123 0.205466  10
   17   50     9.60842 1.91836 0.206088  10
   18   50     9.41338 2.32192 0.20295   10
   19   50     9.41237 2.32592 0.187824  10
   (0.18782377160030547,) [0.8161546994505915, 0.540860845936098, 0.4939122355299173, 0.4528654762091597, 0.048719238941010434, 0.38885999252028464]
   python pso_ray.py  3.91s user 6.51s system 20% cpu 50.445 total

En este experimento se observa una reducción significativa en el tiempo total de
ejecución al paralelizar la evaluación de la población. En el caso secuencial,
el tiempo total fue de aproximadamente 8.45 minutos, mientras que con Ray fue de
aproximadamente 50.4 segundos.

.. note::

   Los tiempos dependen del número de núcleos disponibles, de la carga de la
   máquina y del costo relativo de la función de evaluación. En particular, si
   la evaluación es muy rápida, el *overhead* de crear tareas y transferir datos
   puede reducir el beneficio del paralelismo.

Funciones remotas que invocan funciones remotas
------------------------------------------------

Otra alternativa que podríamos considerar en este caso particular es escalar
el **método de evaluación del controlador**, paralelizando las simulaciones
internas necesarias para calcular su desempeño. Recordemos que, para evaluar
un controlador, se ejecutan varias simulaciones independientes y se calcula
el promedio del error obtenido.

Desde el punto de vista conceptual, esta estrategia también es válida: cada
simulación es independiente de las demás y, por lo tanto, puede ejecutarse en
paralelo. En términos prácticos, esto implicaría que, en lugar de paralelizar
la evaluación de múltiples controladores, paralelizamos las simulaciones que
componen la evaluación de un solo controlador.

Por ejemplo, el siguiente fragmento de código muestra cómo podrían lanzarse
varias simulaciones en paralelo utilizando tareas remotas:

.. code-block:: python

   futures = []
   for ax, ay in paths:
       goal = [ax[-1], ay[-1]]
       reference_path = path.CubicSplinePath(ax, ay)

       future = remote_sim.remote(
           reference_path,
           goal,
           controller=controller,
       )
       futures.append(future)

En este caso, cada llamada a ``remote_sim.remote(...)`` ejecuta una simulación
independiente, y las referencias a los resultados se almacenan en la lista
``futures``. Posteriormente, sería posible sincronizar todas las simulaciones
mediante una llamada a ``ray.get(futures)`` para obtener los resultados y
calcular el promedio del error.

Sin embargo, en este problema específico, esta estrategia **no produce una
mejora significativa en el tiempo total de ejecución**. La razón es que cada
simulación individual tiene un costo computacional relativamente bajo, por lo
que el *overhead* asociado a la creación de tareas y a la comunicación de datos
domina el tiempo total.

Este ejemplo ilustra un punto importante: **no todo paralelismo es igualmente
efectivo**. En general, resulta más conveniente paralelizar las partes del
algoritmo cuyo costo computacional es alto en comparación con el *overhead* del
sistema distribuido. En el caso del PSO, esto suele lograrse paralelizando la
evaluación de múltiples soluciones candidatas, en lugar de paralelizar los
componentes internos de una sola evaluación.


PSO Multipoblaciones con Agentes
--------------------------------



.. code-block:: bash 

    time python pso_agent.py
    2026-01-05 16:53:13,151	INFO worker.py:2007 -- Started a local Ray instance.
    Ronda 00 | Mejor: 0.214788
    Ronda 01 | Mejor: 0.209654
    Migrando
    Ronda 02 | Mejor: 0.177159
    Ronda 03 | Mejor: 0.172730
    Migrando
    Ronda 04 | Mejor: 0.156348
    Ronda 05 | Mejor: 0.152842
    Migrando
    Ronda 06 | Mejor: 0.149235
    Ronda 07 | Mejor: 0.148310
    Migrando
    Mejor global: 0.148310 | [0.014552263021165864, 0.09644121641148923, 0.5106944656555066, 0.5283209236361381, 0.01189209106007404, 0.40691584824379534]
    python pso_agent.py  7.15s user 9.41s system 11% cpu 2:25.43 total
