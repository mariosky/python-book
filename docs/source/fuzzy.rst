.. role:: python(code)
   :language: python

.. _fuzzy: 

Sistemas Difusos
================

«El agua sigue muy fría, está helada, súbele mucho más al calentón»
«El servicio y la comida de este restaurante fueron muy buenos, debemos dejar una
buena propina», «Vas lento, acelera un poco». 


Por ejemplo, ¿qué porcentaje de la cuenta podría considerarse una propina *muy buena*? 
Un 5\% claramente no lo es; un 10\% suele considerarse “normal” (sin considerar ciudades como Nueva York en la actualidad o países como Japón), 
mientras que en algunas ciudades un 15\% o incluso un 18\% podrían ya considerarse *muy buenos*.

Estas son algunas de las frases que podemos escuchar y entender perfectamente
en algún contexto dado. La pregunta es: ¿podemos representar esto
numéricamente?. 

Por ejemplo, ¿qué porcentaje de la cuenta podría considerarse una propina *muy
buena*? Un 5\% claramente no lo es; un 10\% suele considerarse “normal” (sin
considerar ciudades como Nueva York en la actualidad o países como Japón),
mientras que en algunas ciudades un 15\% o incluso un 18\% podrían ya
considerarse *muy buenos*.

No existe un límite exacto y universal: la interpretación depende del contexto,
la cultura y la experiencia previa. De manera similar, términos como frío, muy
frío, lento o rápido no tienen fronteras numéricas bien definidas. Cuando
utilizamos el lenguaje natural, los números precisos y los operadores lógicos
convencionales (como mayor que, menor que o igual a) resultan insuficientes
para capturar este tipo de conocimiento impreciso.

Ante esta limitación, Lotfi A. Zadeh propuso, en la década de los sesenta, una
extensión de la lógica clásica conocida como lógica difusa (*fuzzy logic*).
En lugar de exigir pertenencia absoluta a un conjunto (verdadero o falso),
la lógica difusa introduce el concepto de funciones de pertenencia,
variables difusas y términos lingüísticos, permitiendo modelar grados de
pertenencia intermedios.

Por ejemplo, retomando el caso de una propina *muy buena*, a continuación se
muestra una posible asignación del grado de pertenencia (un valor entre cero y
uno) para los porcentajes mencionados anteriormente:

Grado de pertenencia a *muy buena*:

- 5\%  → 0.0  
- 10\% → 0.4  
- 15\% → 0.8  
- 18\% → 1.0  

Gracias a este enfoque, es posible representar computacionalmente conceptos
vagos o subjetivos, como *temperatura alta*, *velocidad moderada* o *servicio
excelente*, de una forma más cercana al razonamiento humano. Los sistemas
difusos han sido ampliamente utilizados en áreas como el control automático,
la inteligencia artificial, los sistemas expertos y la toma de decisiones,
especialmente cuando los modelos matemáticos precisos son difíciles de obtener
o simplemente no existen.

En las siguientes secciones estudiaremos los fundamentos de los sistemas
difusos y su implementación utilizando Python, comenzando con las funciones de
pertenencia y avanzando gradualmente hacia sistemas de inferencia difusa
completos.

Funciones de Membresía
**********************

Las funciones de membresía son un elemento fundamental de la lógica difusa.
Continuando con el ejemplo de la propina, hasta el momento hemos asignado
únicamente algunos valores discretos de porcentaje a su grado de pertenencia
correspondiente.

Una función de membresía define un mapeo entre el dominio de valores que puede
tomar una variable difusa y el rango de sus grados de pertenencia. En nuestro
caso, el término lingüístico es *muy buena*, y su dominio puede definirse, por
ejemplo, en el intervalo de 0\% a 40\%. Aunque matemáticamente sería posible no
establecer un límite superior, en la práctica es importante definir un dominio
adecuado de acuerdo con el problema que se desea modelar.

La función de membresía mapea entonces el dominio de los porcentajes de propina
al intervalo de grados de pertenencia comprendido entre 0 y 1.

Veamos la definición formal de conjunto difuso propuesta por zadeh :cite:`zadeh1965fuzzy`:

Conjunto Difuso
---------------

Un **conjunto difuso** se define como un par :math:`(U, m)` 
donde:

- :math:`U` es un conjunto (usualmente no vacío), llamado **universo de
  discurso**, (en nuestro ejemplo es el conjuntp de porcentajes de propine que
  podemos dar).

- :math:`m` es una función de membresía :math:`m : U \rightarrow [0,1]` que asigna a cada elemento 
  :math:`x \in U`,un grado de membresía.

Así decimos que la función :math:`m = \mu_A` se denomina **función de membresía** del conjunto
difuso :math:`A = (U, m)`.

Dado un elemento :math:`x \in U`, se dice que:

- :math:`x` **no pertenece** al conjunto difuso si :math:`m(x) = 0`,
- :math:`x` **pertenece completamente** al conjunto difuso si :math:`m(x) = 1`,
- :math:`x` **pertenece parcialmente** al conjunto difuso si :math:`0 < m(x) < 1`.

Resulta útil visualizar este concepto de manera gráfica así que entraremos en 
materia utilizando la librería de `scikit fuzzy` para definir el término 
difuso *propina muy buena*. 

Visualización de funciones de membresía con scikit-fuzzy
--------------------------------------------------------

Una ventaja práctica de utilizar la librería ``scikit-fuzzy`` es que permite definir
funciones de membresía con formas estándar (triangulares, trapezoidales, gaussianas,
etc.) y visualizarlas de manera directa. Esto es útil para validar rápidamente si
la interpretación de un término lingüístico (por ejemplo, *muy buena*) coincide con
lo que esperamos en el problema.

En el ejemplo siguiente modelamos el término *propina muy buena* sobre el dominio
de 0\% a 100\% utilizando una función trapezoidal.

.. code-block:: python

   import numpy as np
   import skfuzzy as fuzz
   import matplotlib.pyplot as plt

   # Dominio (universo) de la variable: porcentaje de propina
   x_propina = np.linspace(0, 40, 501)

   # Función de membresía trapezoidal para el término lingüístico "muy buena"
   # [a, b, c, d] define el inicio, subida, meseta y bajada (en porcentaje).
   mx_muy_buena = fuzz.trapmf(x_propina, [10, 15, 20, 30])

   # Gráfica
   plt.figure(figsize=(8, 5))  # <- tamaño físico de la figura
   plt.plot(x_propina, mx_muy_buena, linewidth=2)
   plt.title("Función de membresía: propina 'muy buena'", fontsize=14)
   plt.xlabel("Propina (%)", fontsize=12)
   plt.ylabel("Grado de membresía μ", fontsize=12)

   plt.xticks(fontsize=10)
   plt.yticks(fontsize=10)
   
   plt.ylim(-0.05, 1.05)
   plt.grid(True)
   plt.tight_layout()
   plt.show()

.. note::

   Los parámetros ``[10, 15, 20, 30]`` son una elección de modelado. En
   problemas reales estos valores se ajustan con conocimiento experto, datos
   históricos o técnicas de optimización (esto se conecta con la siguiente
   capítulo de cómputo evolutivo).

El código anterior nos genera la siguiente gráfica:

.. figure:: ./images/fm.png
   :align: center
   :alt: Función de membresía (pertenencia) en scikit fuzzy.

   Función de membresía para el término lingüístico *Muy buena* (propina).

La función define un incremento en el grado de membresía a partir del 10\%,
hasta alcanzar el valor máximo de 1.0 en el intervalo comprendido entre 15\%
y 20\%. A partir de ese punto, el grado de membresía comienza a decrecer.

La razón de esta disminución es que también consideraremos el término
lingüístico *Excelente* (propina). En este esquema, porcentajes mayores al
20\% y más cercanos a 40\% tendrían un grado de pertenencia más alto al
término *Excelente* que al término *Muy buena*.

Variables lingüísticas
---------------------

En el contexto de nuestro ejemplo, la **propina** puede considerarse una
**variable lingüística** definida sobre el universo de discurso de los
porcentajes de propina. Esta variable puede tomar **valores lingüísticos** como
*poca*, *normal*, *buena*, *muy buena* y *excelente*, los cuales representan
conceptos cualitativos que usamos en el lenguaje natural.  

Matemáticamente modelamos cada uno de los **valores lingüísticos** usando
el **término difuso** correspondiente, es decir, un conjunto difuso definido sobre el universo
de discurso y caracterizado por su función de membresía.

Por ejemplo, el valor lingüístico *muy buena* se representa mediante el término
difuso asociado a la función de membresía
:math:`\mu_{\text{muy\_buena}}(x)`, que asigna a cada porcentaje de propina un
grado de pertenencia entre 0 y 1.

Reglas de inferencia difusas
---------------------------- 

Una de las manera de representar el conocimiento computacionalmente es mediante reglas IF-THEN, 
las cuales especifican que acciones se realizarán cuando ciertas condiciones se cumplan. 
Las reglas IF-THEN (también llamadas reglas de producción) tienen una dos partes; 
el antecedente, conformado por un conjunto de condiciones y el consecuente constituido por un
conjunto de conclusiones:

   .. code::

   SI (condición) ENTONCES (conclusión).

Utilizando lógica difusa podemos definir reglas de inferencia que busquen
capturar la forma en que un humano razona en situaciones donde los límites
no son completamente nítidos. Por ejemplo, al decidir una propina, 
usamos razonamientos como:

- “Si el servicio fue *excelente*, entonces la propina debe ser *excelente*”.
- “Si el servicio fue *bueno* y la comida fue *buena*, entonces la propina es
  *muy buena*”.
- “Si el servicio fue *malo*, entonces la propina es *poca*”.

En un sistema difuso, las condiciones (proposiciones difusas) se construyen combinando términos
lingüísticos con conectores lógicos como **AND** y **OR**. Por ejemplo:

- SI servicio es *bueno* AND comida es *buena* ENTONCES propina es *muy buena*.
- SI servicio es *malo* OR comida es *mala* ENTONCES propina es *poca*.

Estas reglas no producen una decisión *binaria*. En su lugar, cada regla puede
tener cierto **grado** de activación, dependiendo de qué tan bien se cumplan sus
condiciones.

Sistemas de Inferencia Difusos
******************************

Los sistemas de inferencia difusos (FISs) se basan en las reglas de inferencia
difusas que vimos anteriormente. Los FIS definen relaciones entre variables de
entrada y de salida. Las variables de entrada se incluyen en los antecedentes
de la reglas y las variables de salida en los consecuentes. Dependiendo del
tipo de consecuente, se pueden distinguir dos tipos de sistemas de inferencia
difusos:

- Modelo difuso lingüístico: donde ambos el antecedente y consecuentes son proposiciones difusas.
- Modelo difuso Takagi-Sugeno* el antecedente es una preposición difusa; el consecuente es una función nítida (crisp).

Los sistemas de inferencia difusos típicamente tienen estos cuatro comonentes:

- Base de Reglas. El conjunto de reglas difusas.
- Máquina de Inferencia Difusa. Este modulo ejecuta las operaciones de inferencia difusa.
- Fusificador. Este modulo transforma las entradas del sistema (valores numéricos) en valores lingüísticos.
- Defusificador. Transforma los resultados difusas a valores numéricos.

Tipos de sistemas de inferencia difusa
--------------------------------------

A continuación se describen los tres tipos más utilizados de FIS.
La diferencia entre ellos es principalmente la forma en
que producen la salida.

**Tsukamoto**
   En el método de inferenca Tsukamoto, la salida de cada regla es un valor nítido
   obtenido a partir del grado de activación de la regla. La salida global del
   sistema se calcula como un promedio ponderado de las salidas individuales
   de las reglas.

**Mamdani**
   En el método de Mamdani, cada regla produce una **salida difusa**.

   Para obtener una salida nítida a partir del conjunto difuso resultante, se
   utilizan distintos métodos de **defuzzificación**, entre los más comunes se
   encuentran:
   - el método del **centroide**,
   - la **bisección del área**,
   - el **promedio de los máximos**,
   - el **criterio del máximo**.

   Este es uno de los métodos más utilizados debido a su interpretación
   intuitiva y a su cercanía con el razonamiento humano.

**Sugeno**
   En el método de Sugeno, el consecuente de cada regla no es un conjunto
   difuso, sino una **función matemática** de las variables de entrada, típicamente
   una combinación lineal de estas más un término constante.
   Este enfoque es especialmente adecuado para sistemas
   de control y optimización, ya que facilita el análisis matemático y la
   implementación computacional.

En este capítulo no entraremos en detalle sobre como se hace implementan
internamente este tipo de sistemas. Lo que nos interesa es la implementación en
Python. Implementemos un FIS que tome de entrada las variables difusas *comida*
y *servicio* y nos de como salida la *propina* que vamos a dejar.

Implementación de un sistema de inferencia difusa en Python
-----------------------------------------------------------

El primer paso es definir las variables lingüisticas y asignarlas a su posición ya sea en  
el *antedecente* o el *consecuente*. Lo importante para definir estas variables el dominio 
o universo de discurso. En el caso de las variables de entrada que miden la calidad de la comida 
y el servicio, estas irán de cero a diez. Como ya lo decidimos la propina va de 0 a 40 porciento.

.. code-block:: python

   import numpy as np
   import skfuzzy as fuzz
   from skfuzzy import control as ctrl
   import matplotlib.pyplot as plt

   # Variables de entrada (antecedentes)
   comida = ctrl.Antecedent(np.arange(0, 11, 1), 'comida')     # 0..10
   servicio = ctrl.Antecedent(np.arange(0, 11, 1), 'servicio') # 0..10

   # Variable de salida (consecuente)
   propina = ctrl.Consequent(np.arange(0, 41, 1), 'propina')   # 0..40 (%)

Una vez definidas las variables agregamos las funciones de membresía de para los términos difusos de cada una.
Utilizamos funciones triangulares y trapezoidales:

.. code-block:: python

   # Funciones de membresía: comida
   comida['mala'] = fuzz.trapmf(comida.universe, [0, 0, 2, 4])
   comida['regular'] = fuzz.trimf(comida.universe, [3, 5, 7])
   comida['buena'] = fuzz.trapmf(comida.universe, [6, 8, 10, 10])

   # Funciones de membresía: servicio
   servicio['malo'] = fuzz.trapmf(servicio.universe, [0, 0, 2, 4])
   servicio['regular'] = fuzz.trimf(servicio.universe, [3, 5, 7])
   servicio['excelente'] = fuzz.trapmf(servicio.universe, [6, 8, 10, 10])

   # Funciones de membresía: propina
   propina['poca'] = fuzz.trapmf(propina.universe, [0, 0, 5, 10])
   propina['normal'] = fuzz.trimf(propina.universe, [8, 12, 16])
   propina['muy_buena'] = fuzz.trapmf(propina.universe, [14, 18, 22, 26])
   propina['excelente'] = fuzz.trapmf(propina.universe, [22, 28, 40, 40])

Podemos ver las variables gráficamente utilizando el metodo ``view()``:

.. code-block:: python

   # (Opcional) Visualizar funciones
   comida.view(); servicio.view(); propina.view()
   plt.show()

Ejemplo:

.. figure:: ./images/propina.png
   :align: center
   :alt: Variable lingüística ``propina`` en scikit fuzzy.

   Gráfica de las funciones de membresía para la variable lingüística *propina*.

Base de reglas difusas
----------------------

Creamos las reglas utilizando los operadores lógicos, antecedente y consecuente 
según la variable lingüística y función de membresía:

.. code-block:: python

   regla1 = ctrl.Rule(servicio['malo'] | comida['mala'], propina['poca'])
   regla2 = ctrl.Rule(servicio['regular'] & comida['regular'], propina['normal'])
   regla3 = ctrl.Rule(servicio['excelente'] & comida['buena'], propina['excelente'])

   # Reglas intermedias para dar suavidad al sistema
   regla4 = ctrl.Rule(servicio['regular'] & comida['buena'], propina['muy_buena'])
   regla5 = ctrl.Rule(servicio['excelente'] & comida['regular'], propina['muy_buena'])


Construcción y simulación del sistema
-------------------------------------

Vamos a construir un FIS tipo Mamdani y probaremos el caso de una *comida* de 7.0 
con un buen servicio 9.0. Recordemos que en el caso de Mamdani las entradas y salidas
son datos nítidos.

.. code-block:: python

   sistema = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5])
   simulacion = ctrl.ControlSystemSimulation(sistema)

   # Entradas nítidas (crisp) del usuario
   simulacion.input['comida'] = 7.0
   simulacion.input['servicio'] = 9.0

   # Ejecutar inferencia
   simulacion.compute()

   # Salida nítida
   print("Propina sugerida (%):", simulacion.output['propina'])

   # Visualizar el resultado sobre la membresía de salida
   propina.view(sim=simulacion)
   plt.tight_layout()
   plt.show()

Podemos ver gráficamente el resultado de la inferencia con una defuzzificación por centroide:

.. figure:: ./images/salida.png
   :align: center
   :alt: Salida de nuestro FIS para ``propina`` en scikit fuzzy.

   Gráfica de las funciones de membresía para la variable lingüística *propina*.



