Escalado Computacional en Python
================================

En los capítulos anteriores hemos explorado diversas aplicaciones de Python
que, en la práctica, pueden llegar a requerir una **demanda considerable de
recursos computacionales**. Cuando el costo computacional de estas tareas
crece, el escalado deja de ser una optimización opcional y se vuelve una
necesidad. Algunas de estas tareas son las siguientes:

- **Optimización basada en poblaciones.**  
  Los algoritmos de optimización basados en poblaciones requieren evaluar de
  manera repetida el desempeño de un conjunto de soluciones candidatas. Esta
  evaluación puede resultar especialmente costosa cuando implica la ejecución de
  simulaciones complejas, por ejemplo aquellas que involucran **integración
  numérica de sistemas dinámicos** o modelos computacionales de alto costo. En el
  ejemplo presentado en el capítulo anterior, la evaluación del desempeño de un
  controlador difuso requería un tiempo de cómputo considerable.

- **Ajuste de hiperparámetros en aprendizaje automático.**  
  Muchos algoritmos de aprendizaje automático requieren una etapa de
  entrenamiento computacionalmente intensiva, y su desempeño depende de manera
  crítica de los hiperparámetros utilizados. Explorar distintas combinaciones de
  estos parámetros mediante experimentos de prueba y validación puede incrementar
  de forma significativa el tiempo de cómputo requerido. Este tipo de evaluación
  también es necesario cuando se realizan **comparaciones estadísticas**, las
  cuales requieren una muestra obtenida a partir de múltiples ejecuciones del
  algoritmo.

- **Flujos de trabajo de aprendizaje automático.**  
  Más allá del entrenamiento de modelos, los flujos de trabajo completos de
  aprendizaje automático suelen incluir etapas de preprocesamiento de datos,
  extracción de características, entrenamiento y evaluación. En conjunto, estas
  operaciones pueden demandar una cantidad considerable de recursos de
  procesamiento, especialmente cuando se trabaja con conjuntos de datos grandes.

- **Análisis de datos.**  
  El procesamiento y análisis de grandes volúmenes de datos, por ejemplo, en
  tareas de clasificación de texto o análisis de sentimientos, puede superar
  fácilmente la capacidad de cómputo de una ejecución secuencial tradicional,
  haciendo necesario recurrir a técnicas de paralelización o escalado.

Estos ejemplos comparten características que permiten escalar los algoritmos
utilizando **técnicas de procesamiento en paralelo**, ya que incluyen tareas que
pueden realizarse de forma independiente. En particular, se observan los
siguientes casos:

- Es posible evaluar el desempeño de soluciones candidatas de manera
  independiente, sin necesidad de comunicación inmediata entre ellas.

- Es posible ejecutar metaheurísticas basadas en poblaciones utilizando
  múltiples poblaciones más pequeñas, las cuales pueden evolucionar de forma
  independiente durante varias iteraciones, para después intercambiar
  soluciones candidatas entre sí.

- Se pueden ejecutar varios algoritmos de aprendizaje automático de manera
  simultánea, probando de forma independiente distintos valores de sus 
  parámetros.

- En tareas de análisis de datos, como el procesamiento de texto, es posible
  dividir el corpus en subconjuntos más pequeños para realizar operaciones de
  procesamiento independientes, cuyos resultados se integran posteriormente en
  un resultado final.

En conjunto, estas observaciones muestran que es posible **escalar los
algoritmos dividiendo el trabajo en tareas independientes**, las cuales pueden
ejecutarse **en paralelo** en distintos procesadores o núcleos de cómputo.

Veamos varios modelos de paralelización de tareas:

Veamos ahora algunos **modelos comunes de paralelización de tareas**. Estos
modelos describen distintas formas de dividir y distribuir el trabajo cuando se
requiere escalar la ejecución de algoritmos computacionalmente costosos.

Colas de trabajo
----------------

Un modelo básico de escalado es la paralelización de tareas mediante el uso de
**colas de trabajo** y *workers*. En este enfoque, el sistema se compone de varios
elementos con responsabilidades bien definidas:

- **Worker.**  
  Es un componente de software que solicita tareas a una cola de mensajes y las
  ejecuta de manera independiente. El *worker* procesa cada tarea de forma
  asíncrona respecto al componente que la generó. En este modelo, la única
  comunicación y coordinación entre las partes ocurre **a través de la cola de
  mensajes**, por lo que no es necesario que el productor y el *worker* coincidan
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
-------------------------------------

Al paralelizar la ejecución de tareas, una decisión fundamental de diseño es
determinar **cómo se gestiona el estado del sistema**. En términos generales,
podemos distinguir entre dos enfoques: estado compartido y estado encapsulado.

En un modelo de **estado compartido**, múltiples tareas o componentes necesitan
compartir información entre ellas, o deben modificar/leer una memoria global.
Aunque este enfoque puede ser eficiente en ciertos escenarios, introduce
complejidad adicional, ya que es necesario coordinar el acceso concurrente al
estado global evitando inconsistencias.

Por el contrario, en un modelo de **estado encapsulado**, cada componente mantiene
su propio estado interno, y este no pueder ser modificado directamente por otros
componentes. La interacción ocurre únicamente mediante el intercambio de mensajes
o solicitudes explícitas. Este enfoque reduce la necesidad de sincronización y
facilita el razonamiento sobre el comportamiento del sistema.

En problemas como los abordados en este libro el estado suele tener una estructura
bien definida (por ejemplo, una población, un modelo o un subconjunto de datos),
lo que hace especialmente atractivo el uso de estado encapsulado.

El Modelo Actor
---------------

El **Modelo Actor** es una abstracción de programación que formaliza el uso de
estado encapsulado para la ejecución paralela y distribuida de tareas. En este
modelo, un *actor* es una entidad que:

- mantiene su propio estado interno,
- expone un conjunto de operaciones,
- y se comunica exclusivamente mediante el envío de mensajes.

Un actor no accede directamente al estado de otros actores. Toda interacción se
realiza de forma explícita, lo que elimina la necesidad de mecanismos de
sincronización complejos y facilita el escalado del sistema.

Este modelo resulta especialmente adecuado para los casos que nos interesan en
este capítulo. Por ejemplo:

- en optimización poblacional, un actor puede representar una población o *swarm*;
- en aprendizaje automático, un actor puede encapsular un modelo y su proceso de
  entrenamiento;
- en análisis de datos, un actor puede gestionar una partición del conjunto de
  datos.

En las siguientes secciones utilizaremos este modelo como base para implementar
ejemplos de escalado computacional en Python.



