.. role:: python(code)
   :language: python

Bases de Datos
==============

En esta sección nos centraremos en el amacenamiento de
datos utilizando servicios de sistemas de bases de datos relacionales y
no relacionales. Estos sistemas son de vital importancia para
el desarrollo de aplicaciones, ya que la mayoría de ellas requiere una gestión
de datos escalable, eficiente y segura.

Elegir entre una base de datos relacional o no relacional depende del tipo de
aplicación que estemos desarrollando: Los sistemas relacionales como *PostgreSQL*, *MySQL* o *Oracle*, ofrecen un
esquema estructurado y formal que ofrece integridad y consistencia de los datos,
además de contar con un lenguaje estándar como SQL que nos permite hacer
consultas complejas de manera eficiente. Por otro lado, los sistemas no
relacionaes como *MongoDB* o *Redis*, aportan flexibilidad en el manejo de estructuras de datos
heterogéneas y una escalabilidad superior, lo que los hace especialmente
adecuados para aplicaciones distribuidas con una gran demanda.

.. list-table:: Comparación entre bases de datos relacionales y no relacionales
   :widths: 25 35 40
   :header-rows: 1

   * - Característica
     - Relacional (SQL)
     - No Relacional (NoSQL)
   * - Ejemplos
     - PostgreSQL, MySQL, Oracle
     - MongoDB, Redis
   * - Modelo de datos
     - Tablas con esquemas rígidos
     - Documentos, clave-valor, documentos, gráfos, etc.
   * - Lenguaje de consulta
     - SQL
     - Específico de cada sistema
   * - Consistencia
     - Alta (ACID)
     - Eventual o configurable (BASE)
   * - Escalabilidad
     - Vertical
     - Horizontal
   * - Adecuado para
     - Transacciones, reportes, ERP
     - Big Data, IoT, aplicaciones web modernas
   * - Flexibilidad del esquema
     - Baja
     - Alta

Python cuenta con un ecosistema maduro de bibliotecas que permiten la
comunicación con diversos sistemas gestores de bases de datos.  En las
siguientes secciones, se presentarán ejemplos prácticos de uso para diferentes
tipos de gestores, tanto relacionales como no relacionales

Bases de Datos relacionales
***************************

Al igual que otros lenguajes, Python cuenta con una especificación estándar que
deben seguir los desarrolladores de APIs para que los desarrolladores puedan
interactuar con bases de datos sin preocuparse de los detalles específicos del
sistema de base de datos.  Si ya haz desarrollado aplicaciones de datos en otros
lenguajes probablemente haz utilizado librerías que siguen un estándar como ODBC
(Open Database Connectivity), JDBC (Java Database Connectivity) o ADO.NET.
Python por su parte cuenta con el Python Database API Specification v2.0 (PEP
249), dónde se especifica una interfaz estándar para conectar aplicaciones
Python con sistemas de bases de datos relacionales.  Antes de ver detalles
especificos veamos los componentes principales del estándar:

1. Conectar
Antes de empezar a interactuar con un servidor de base de datos, debemos
establecer una conexión, normalmente utilizamon una cadena dónde enviamos
los datos específicos de la conexión y una vez establecida la conexión nos
regresa un objecto que representa una conexión específica.

2. Conexión
Una conexión es un objeto de la clase :python:`Connection` la cual
contiene métodos para interactuar a nivel alto con el servidor:

:python:`cursor()` Crea un cursor con el cual podemos hacer consultas o enviar comandos de SQL al servidor.

:python:`commit()` Compromete los cambios hechos por la transacción actual.

:python:`rollback()` Deshace los cambios hechos por la transacción actual.

:python:`close()` Cierra la conexión.

3. Cursor
Un cursor incluye los siguientes métodos:

:python:`execute(sql, params)` ejecuta una consulta, envía los parámetros de la consulta por separado.

:python:`executemany(sql, seq_of_params)` ejecuta varias consultas.

:python:`fetchone()` devuelve un registro solamente.

:python:`fetchall()` devuelve todos los registros.

:python:`fetchmany(size)` devuelve un número específico de registros.

Atributos:

:python:`description` información de los campos del resultado.

:python:`rowcount` número de registros afectados por la última operación