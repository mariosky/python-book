import math
import operator
import random

import numpy
import ray
from deap import base, creator, tools
from evaluate_controller import evaluate_controller


@ray.remote
def remote_ev_controller(particle):
    return evaluate_controller(particle)



@ray.remote
class SwarmAgent:
    def __init__(self, config) -> None:
        self.config = config
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Particle", list, fitness=creator.FitnessMin, speed=list, smin=None, smax=None, best=None)

    def generate(self, size, pmin, pmax, smin, smax):
        part = creator.Particle(random.uniform(pmin, pmax) for _ in range(size))
        part.speed = [random.uniform(smin, smax) for _ in range(size)]
        part.smin = smin
        part.smax = smax
        return part

    def update_particle(self, part, best, phi1, phi2):
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



    def evaluate_population_ray(self,pop):
        futures_fitness_values = [remote_ev_controller.remote(list(particle)) for particle in self.pop] 
        results = ray.get(futures_fitness_values)
        assert len(self.pop) == len(results)
        
        for i, part in enumerate(self.pop):
            part.fitness.values = results[i]
        return self.pop

    def main(self, config):
        toolbox = base.Toolbox()
        toolbox.register("particle", self.generate, size=config['dim'], pmin=-0.05, pmax=1.5, smin=-0.1, smax=0.1)
        toolbox.register("population", tools.initRepeat, list, toolbox.particle)
        toolbox.register("update", self.update_particle, phi1=2.0, phi2=2.0)
        self.pop = toolbox.population(n=config['swarm_size'])

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        logbook = tools.Logbook()
        logbook.header = ["gen", "evals"] + stats.fields

        GEN = config['ngen']
        best = None
        for g in range(GEN):
            self.evaluate_population_ray(self.pop)
            for part in self.pop:
                if part.best is None or part.best.fitness < part.fitness:
                    part.best = creator.Particle(part)
                    part.best.fitness.values = part.fitness.values
                if best is None or best.fitness < part.fitness:
                    best = creator.Particle(part)
                    best.fitness.values = part.fitness.values

            for part in self.pop:
                toolbox.update(part, best)
            # Gather all the fitnesses in one list and print the stats
            logbook.record(gen=g, evals=len(self.pop), **stats.compile(self.pop))
            print(logbook.stream)
            
        #print(best.fitness.values, best)
        #return self.pop, logbook, best
        return best, logbook


config = {
    "smin": -0.20,
    "smax":  0.20,
    "pmin": 0.0,
    "pmax": 1.0,
    "phi1": 2.0,
    "phi2": 2.0,

    "dim": 6,
    "swarm_size": 10,

    "ngen": 4,
    "migrate_interval":2,
    "migrate_k":2,
    "num_swarms": 6,
    "num_rounds": 4,
}

ray.init(ignore_reinit_error=True)
try:
   agents = [SwarmAgent.remote(config) for i in range(config['num_swarms'])
   ]

   for r in range(config["num_rounds"]):
       # 1) Cada agente ejecuta varias iteraciones locales en paralelo
       futures = [a.main.remote(config) for a in agents]
       bests = ray.get(futures)  # [(f, x), ...]

       # 2) Actualizar mejor global
       for best, log in bests:
           print(best.fitness.values, best)

       #print(f"Ronda {r:02d} | mejor global = {best_global_f:.6f}")

       # 3) Migración: intercambio de candidatos entre agentes
       #if (r + 1) % migrate_every == 0:
           # Tomar los mejores de cada agente
       #    elites = [x for (f, x) in bests]
           # Enviar a cada agente candidatos de otros agentes
       #    mig_futures = []
       #    for i, a in enumerate(agents):
               # Candidatos: mejores de los otros (rotación simple)
       #        others = [elites[(i + j) % n_agents] for j in range(1, n_agents)]
        #       mig_futures.append(a.inject_candidates.remote(others[:migrate_k]))
        #   ray.get(mig_futures)

finally:
   ray.shutdown()






