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

def bit_flip_mutation(individual, p=0.05):
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

CXPB, MUTPB, NGEN = 0.5, 0.1, 40

population = get_population(300, 100)
fitness = [one_max(i) for i in population]
print(max(fitness))

for n in range(NGEN):

    selected = [tournament_selection(population, fitness)[:] for _ in range(len(population))]
    random.shuffle(selected)
    pairs = list(zip(selected[::2], selected[1::2]))

    for child1, child2 in pairs:
       if random.random() < CXPB:
           one_point_crossover(child1, child2)

    for individual in selected:
        if random.random() < MUTPB:
            bit_flip_mutation(individual)
    
    population[:] = selected
    fitness = [one_max(i) for i in population]
    print(max(fitness))
