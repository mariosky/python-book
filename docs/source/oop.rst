.. role:: python(code)
   :language: python

Programación Orientada a Objetos en Python
==========================================

Como ya hemos visto, Python *no* es un lenguaje orientado a objetos (OO) puro.
Podemos programar scripts en los cuales  no es necesario utilizar el paradigma
explicitamente.  Aunque los tipos de datos, estructuras e incluso las funciones
son objetos, no es necesario implementar una clase principal o métodos miembro
para poder escribir un programa. Incluso parecería que la implementación del 
paradigma es un agregado de último momento. Un parche. Esta impresión radica (en 
mi opinión) en la sintáxis para expresar algunos elementos,
como los constructores, el páso de una referencia (:python:`self`) en la 
definición métodos miembro, entre otras. 

Un aspecto crucial de la Programción Orientada a Objetos es el tipado estrícto. 
Esto ocasiona que tengamos que utilizar mecanismos elaborados para hacer 
cosas que en un lenguaje dinámico se hacen muy fácilmente. Por ejemplo, 
el polimorfismo, plantillas o el uso de interfaces. Un programador
experimentado sabe que todas estas 'libertades' pueden traer problemas, pero al 
mismo tiempo nos permiten el desarrollo de programas *sin tanto verbo* (del inglés verbose).

Por esta razón, creo que Python puede no ser el mejor lenguaje para aprender
Programación Orientada a Objetos (POO), ya que muchos de los temas o elementos de 
programación no tienen una aplicación directa.  Por otro lado, el hecho de que
el paradigma sea *opcional* evita que se establezcan reglas de acción para
solucionar problemas de una manera más o menos estándar, ya que hay varias
formas de hacer todo. Entonces, creo que est sección no debería ser 
tan extensa como en los libros de otros lenguajes ya que los elemento de POO 
en Python son los más básicos.

.. note::
    A lo largo del libro veremos que si hay un estilo de programación en Python, 
    pero al igual que el lenguaje es algo libre e híbrido.  

