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
   mu_muy_buena = fuzz.trapmf(x_propina, [10, 15, 20, 30])

   # Gráfica
   plt.figure(figsize=(8, 5))  # <- tamaño físico de la figura
   plt.plot(x_propina, mu_muy_buena, linewidth=2)
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

Variables difusas
------------------





