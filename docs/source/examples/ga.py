import random


def create_individual(size):
   return [random.randint(0, 1) for _ in range(size)]

def get_population(n, size):
   return [create_individual(size) for _ in range(n)]

def one_max(solution):
   return sum(solution)


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


def tournament_selection(population, fitness, k=3):
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

def bit_flip_mutation(individual, pb_flip=0.05):
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

    
import random
# Probabilidades y número de generaciones
PB_CRUCE, PB_MUT, NGEN = 0.5, 0.1, 40

# Población inicial (300 individuos, cromosomas de longitud 100)
population = get_population(300, 100)

# Desempeño de los individuos de la población
fitness = [one_max(i) for i in population]
print(f'Gen:{NGEN} Mejor:{max(fitness)}´')

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
           
    # 4) Mutación (in place) con probabilidad MUTPB por individuo
    for individual in selected:
        if random.random() < PB_MUT:
            # Mutación Bit Flip con probabilidad pb_flip de 0.05   
            bit_flip_mutation(individual, pb_flip=0.05)

    # Reemplazamos la población anterior con la nueva
    population[:] = selected
    # Calculamos el fitness de la nueva generación 
    fitness = [one_max(i) for i in population]
    print(f'Gen:{NGEN} Mejor:{max(fitness)}´')
