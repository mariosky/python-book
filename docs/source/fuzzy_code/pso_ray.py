import operator
import random

import numpy
import math

from deap import base
from deap import creator
from deap import tools

import ray
from evaluate_controller import evaluate_controller

@ray.remote
def remote_ev_controller(particle):
    return evaluate_controller(particle)


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Particle", list, fitness=creator.FitnessMin, speed=list,
    smin=None, smax=None, best=None)



def generate(size, pmin, pmax, smin, smax):
    part = creator.Particle(random.uniform(pmin, pmax) for _ in range(size))
    part.speed = [random.uniform(smin, smax) for _ in range(size)]
    part.smin = smin
    part.smax = smax
    return part

def updateParticle(part, best, phi1, phi2):
    u1 = (random.uniform(0, phi1) for _ in range(len(part)))
    u2 = (random.uniform(0, phi2) for _ in range(len(part)))
    v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
    v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
    part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
    for i, speed in enumerate(part.speed):
        if abs(speed) < part.smin:
            part.speed[i] = math.copysign(part.smin, speed)
        elif abs(speed) > part.smax:
            part.speed[i] = math.copysign(part.smax, speed)
    part[:] = list(map(operator.add, part, part.speed))

toolbox = base.Toolbox()
toolbox.register("particle", generate, size=6, pmin=-0.05, pmax=1.5, smin=-0.1, smax=0.1)
toolbox.register("population", tools.initRepeat, list, toolbox.particle)
toolbox.register("update", updateParticle, phi1=2.0, phi2=2.0)
#toolbox.register("evaluate", ev_controller)


def evaluate_population_ray(pop):
    futures_fitness_values = [remote_ev_controller.remote(list(particle)) for particle in pop] 
    results = ray.get(futures_fitness_values)
    assert len(pop) == len(results)
    
    for i, part in enumerate(pop):
        part.fitness.values = results[i]
    return pop

def main():
    pop = toolbox.population(n=50)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    logbook = tools.Logbook()
    logbook.header = ["gen", "evals"] + stats.fields

    GEN = 20
    best = None
    

    for g in range(GEN):
        evaluate_population_ray(pop)
        for part in pop:
            # No calculamos el fitnes utilizando el toolbox
            # lo hacemos con la función evaluate_population_ray(pop)

            # part.fitness.values = toolbox.evaluate(part)
        
            # Se compara el fitness no el valor del RMSE
            # en este caso los controladores con menor RMSE
            # tienen un mayor fitness. DEAP internamente 
            # hace la multiplicación por -1 ya que estamos minimizando. 
            if not part.best or part.best.fitness < part.fitness:
                part.best = creator.Particle(part)
                part.best.fitness.values = part.fitness.values
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values

        for part in pop:
            toolbox.update(part, best)
        # Gather all the fitnesses in one list and print the stats
        logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
        print(logbook.stream)
        
    print(best.fitness.values, best)
    return pop, logbook, best

if __name__ == "__main__":
    ray.init()
    main()
    ray.shutdown()





