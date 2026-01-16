.. role:: python(code)
   :language: python

Servicios Web con FastAPI
=========================

En este capítulo final presentamos de manera **introductoria** el concepto de
**servicios web**, utilizando un ejemplo sencillo implementado con el framework 
``FastAPI``. El objetivo no es profundizar en el desarrollo de APIs ni en los
detalles del protocolo HTTP, sino **mostrar cómo un modelo computacional puede
exponerse como un servicio accesible a través de la red**.

Entre otras ventajas, este enfoque nos permite **compartir funcionalidad** desarrollada
en un lenguaje o tecnología particular con otros componentes escritos en
lenguajes distintos, o incluso con aplicaciones desarrolladas por terceros.
Asimismo, facilita la **escalabilidad de los algoritmos**, al permitir su
ejecución de manera distribuida mediante servicios independientes que se
comunican a través de **protocolos estándar**.

Este enfoque es especialmente relevante en el contexto de este libro, ya que
permite integrar técnicas como **control difuso**, **metaheurísticas** o
**aprendizaje automático** dentro de arquitecturas modernas de software, 
por ejemplo, micro-servicios o funciones serverless.


¿Qué es un servicio web?
------------------------

Un **servicio web** es una aplicación que expone funcionalidad a través de una
interfaz accesible mediante la red, típicamente utilizando el protocolo
**HTTP**. Estos servicios pueden intercambiar información también utilizando formatos 
web com JSON o XML. Aunque inicialmente los servicios web se basaban en 
protocolos complejos como SOAP o arquitecturas orientadas a brokers, en la actualidad suelen
implementarse utilizando mecanismos más simples y familiares para los
desarrolladores web.

En este capítulo utilizaremos el patrón **REST (Representational State
Transfer)**, en el cual:

- Cada operación se asocia a una **URL** (endpoint).
- Los parámetros se envían como parte de la ruta o de la consulta.
- Las respuestas se devuelven típicamente en formato **JSON**.
- Las operaciones se invocan utilizando métodos HTTP como ``GET`` o ``POST``,
  donde el **verbo HTTP** indica el tipo de acción que se realiza
  (consulta, creación, actualización, etc.).

FastAPI
-------

Para ilustrar estos conceptos utilizaremos la librería **FastAPI**, un
framework moderno para Python que permite construir servicios web de forma
rápida, clara y eficiente. FastAPI se apoya en **anotaciones de tipos** para
definir los parámetros de entrada y generar automáticamente documentación
interactiva, lo que lo hace especialmente adecuado para exponer modelos
computacionales y prototipos académicos como servicios accesibles desde la
red.

En este ejemplo vamos a implementar un **controlador difuso** encapsulado dentro de un
servicio REST. De esta forma, la lógica de inferencia se mantiene separada de
la interfaz de acceso, y puede ser utilizada por aplicaciones externas,
independientemente del lenguaje o plataforma en la que estén implementadas.

Un servicio difuso para el cálculo de propinas
-----------------------------------------------

Como ejemplo, implementamos un servicio web que calcula una **propina**
utilizando un **sistema de control difuso**, similar a los ejemplos clásicos
presentados en capítulos anteriores.

El servicio recibe dos valores numéricos (``float``):

- ``comida_val``: calidad de la comida (0–10),
- ``servicio_val``: calidad del servicio (0–10),

y devuelve un valor numérico correspondiente a la propina recomendada.

Implementación del servicio
~~~~~~~~~~~~~~~~~~~~~~~~~~~

El código completo del servicio es el siguiente:

.. code-block:: python
   :linenos:

   from fastapi import FastAPI
   import numpy as np
   import skfuzzy as fuzz
   from skfuzzy import control as ctrl

   app = FastAPI()

   @app.get("/")
   def read_root():
       return {"Hola": "Mundo"}

   @app.get("/propina/{comida_val}/{servicio_val}")
   def calc_propina(comida_val: float, servicio_val: float):
       # Variables difusas de entrada y salida
       comida = ctrl.Antecedent(np.arange(0, 11, 1), 'comida')
       servicio = ctrl.Antecedent(np.arange(0, 11, 1), 'servicio')
       propina = ctrl.Consequent(np.arange(0, 26, 1), 'propina')

       # Funciones de membresía automáticas
       comida.automf(3)
       servicio.automf(3)
       
       # Dominio de las funciones
       propina['low'] = fuzz.trimf(propina.universe, [0, 0, 13])
       propina['medium'] = fuzz.trimf(propina.universe, [0, 13, 25])
       propina['high'] = fuzz.trimf(propina.universe, [13, 25, 25])

       # Reglas difusas
       rule1 = ctrl.Rule(comida['poor'] | servicio['poor'], propina['low'])
       rule2 = ctrl.Rule(servicio['average'], propina['medium'])
       rule3 = ctrl.Rule(servicio['good'] | comida['good'], propina['high'])

       # Controlador difuso
       propina_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
       calcula_propina = ctrl.ControlSystemSimulation(propina_ctrl)
       
       # Entradas
       calcula_propina.input['comida'] = comida_val
       calcula_propina.input['servicio'] = servicio_val
       calcula_propina.compute()

       # Salida
       return {"propina": calcula_propina.output['propina']}

Estructura del servicio
***********************

El servicio define dos *endpoints* principales:

- ``/``  
  Devuelve un mensaje simple, útil para verificar que el servicio está activo.

- ``/propina/{comida_val}/{servicio_val}``  
  Ejecuta el sistema difuso y devuelve la propina calculada.

Cada vez que se llama al *endpoint* de propina:

1. Se construye el sistema difuso.
2. Se asignan los valores de entrada.
3. Se ejecuta la inferencia.
4. Se devuelve el resultado como un objeto JSON.

Desde el punto de vista del cliente, el sistema difuso se comporta como una
**caja negra**, accesible mediante una llamada HTTP.

Ejecución del servicio
***********************

El servicio puede ejecutarse con:

.. code-block:: bash

   uvicorn main:app --reload

Una vez en ejecución, es posible acceder a:

- ``http://localhost:8000/``  
- ``http://localhost:8000/propina/7.2/8.3``  

FastAPI genera automáticamente una interfaz de documentación interactiva en:

.. code-block:: text

   http://localhost:8000/docs


Consumo del servicio desde Python
---------------------------------

Una de las principales ventajas de exponer funcionalidad mediante un servicio
web es que **puede ser utilizada desde múltiples interfaces**, no únicamente
desde un navegador web. Cualquier cliente capaz de realizar solicitudes HTTP
puede interactuar con el servicio, independientemente del lenguaje o plataforma
en la que esté escrito.

En esta sección mostramos cómo consumir el servicio de cálculo de propina
implementado con ``FastAPI`` desde un **script de Python**, utilizando la
biblioteca ``requests``.

La librería ``requests`` es el cliente HTTP de facto en Python y permite enviar
peticiones de manera simple y legible.

Supongamos que el servicio se está ejecutando localmente en la dirección:

::

   http://127.0.0.1:8000

y que queremos invocar el endpoint:

::

   /propina/{comida_val}/{servicio_val}

donde ``comida_val`` y ``servicio_val`` son valores numéricos en el rango
``[0, 10]``.

Ejemplo básico con ``requests``
*******************************

El siguiente script realiza una petición HTTP ``GET`` al servicio y procesa la
respuesta en formato **JSON**:

.. code-block:: python
   :linenos:

   import requests

   # URL base del servicio
   base_url = "http://127.0.0.1:8000"

   # Parámetros de entrada
   comida_val = 8.0
   servicio_val = 9.0

   # Construcción de la URL del endpoint
   url = f"{base_url}/propina/{comida_val}/{servicio_val}"

   # Envío de la petición GET
   response = requests.get(url)

   # Verificamos que la respuesta sea correcta
   if response.status_code == 200:
       data = response.json()
       print("Propina calculada:", data["propina"])
   else:
       print("Error en la solicitud:", response.status_code)

En este ejemplo:

- Se construye la URL del endpoint incorporando los parámetros en la ruta.
- Se envía una petición HTTP ``GET`` utilizando ``requests.get``.
- La respuesta se interpreta como un objeto JSON mediante ``response.json()``.
- El valor de la propina se extrae directamente del diccionario resultante.

Separación entre cliente y servidor
***********************************

Es importante notar que este script **no depende en absoluto** de FastAPI ni de
la implementación interna del controlador difuso. Desde el punto de vista del
cliente:

- El servicio es una *caja negra*.
- La comunicación se realiza exclusivamente mediante HTTP.
- Los datos se intercambian en un formato estándar (JSON).

Este mismo servicio podría ser consumido:

- desde otro lenguaje de programación (por ejemplo JavaScript, Java o C++),
- desde una aplicación móvil,
- desde un sistema embebido,
- o como parte de una arquitectura distribuida basada en microservicios.

Este ejemplo ilustra cómo los modelos desarrollados a lo largo del libro pueden
**integrarse fácilmente en sistemas más grandes**, sin necesidad de reescribir
la lógica principal ni acoplarla a una interfaz específica.

Resumén del capítulo
--------------------

En este capítulo se presentó un ejemplo ilustrativo de cómo podemos
**desacoplar** nuestros algoritmos de un lenguaje de programación o
arquitectura específica y exponerlos como un servicios independientes
utilizando el protocolo HTTP.

Más que profundizar en los detalles de FastAPI, el objetivo de este capítulo es
mostrar cómo las técnicas vistas a lo largo del libro pueden integrarse de
forma natural en **sistemas distribuidos y orientados a servicios**.

