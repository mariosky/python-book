class Persona:
   def __init__(self, nombre, apellido, **kwargs):
      self.nombre = nombre
      self.apellido = apellido
      super().__init__(**kwargs)

   def saluda(self):
      print(f"Hola, soy {self.nombre} {self.apellido}")

class Estudiante(Persona):
   def __init__(self, especialidad, **kwargs):
      self.especialidad = especialidad
      super().__init__(**kwargs)

   def saluda(self):
      super().saluda()
      print(f"Estudio {self.especialidad}")

class Empleado(Persona):
   def __init__(self, empleo, **kwargs):
      self.empleo = empleo
      super().__init__(**kwargs)

   def saluda(self):
      super().saluda()
      print(f"Trabajo como {self.empleo}")

class Estudiante_Empleado(Estudiante, Empleado):
   def __init__(self, nombre, apellido, especialidad, empleo):
      super().__init__(
            nombre=nombre,
            apellido=apellido,
            especialidad=especialidad,
            empleo=empleo
      )

   def saluda(self):
      super().saluda()

ana = Estudiante_Empleado('Ana', 'Lee', 'Arquitectura', 'Asistente')
ana.saluda()
