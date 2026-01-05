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
        self.size = config['dim']
        self.smin = config['smin']
        self.smax = config['smax']
        self.pmax = config['pmax']
        self.pmin = config['pmin']
        self.phi1 = config['phi1']
        self.phi2 = config['phi2']

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Particle", list, fitness=creator.FitnessMin, speed=list, smin=None, smax=None, best=None)

    def generate(self):
        part = creator.Particle(random.uniform(self.pmin, self.pmax) for _ in range(self.size))
        part.speed = [random.uniform(self.smin, self.smax) for _ in range(self.size)]
        part.smin = self.smin
        part.smax = self.smax
        return part

    def update_particle(self, part, best):
        u1 = (random.uniform(0, self.phi1) for _ in range(len(part)))
        u2 = (random.uniform(0, self.phi2) for _ in range(len(part)))
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
    
    def migrate(self, migration_particles):
        self.pop.sort(key=lambda p: p.fitness.values)
        particles = [] 
        for x, f in migration_particles:
            part = self.generate()
            part[:] = x 
            part.fitness.values = f 
            particles.append(part)
        
        self.pop = self.pop[:-len(particles)] + particles


    def main(self, config):
        toolbox = base.Toolbox()
        toolbox.register("particle", self.generate)
        toolbox.register("population", tools.initRepeat, list, toolbox.particle)
        toolbox.register("update", self.update_particle)
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
            # print(logbook.stream)
        
    
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
    "num_rounds": 8,
}

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Particle", list, fitness=creator.FitnessMin, speed=list, smin=None, smax=None, best=None)

ray.init(ignore_reinit_error=True, include_dashboard=False)
try:
   agents = [SwarmAgent.remote(config) for i in range(config['num_swarms'])
   ]
   
   best_global = None
   for r in range(config["num_rounds"]):
       # 1) Cada agente ejecuta varias iteraciones locales en paralelo
       futures = [a.main.remote(config) for a in agents]
       bests = [best for best, _ in ray.get(futures)]  # [(f, x), ...]
       bests.sort(key=lambda best: best.fitness.values) 


       # 2) Actualizar mejor global
       best = bests[0]
       if best_global is None or best_global.fitness < best.fitness:
           best_global = creator.Particle(best)
           best_global.fitness.values = best.fitness.values
       print(f"Ronda {r:02d} | mejor global = {best_global.fitness.values[0]:.6f} | {best_global}")
       
       # 3) Migración: intercambio de candidatos entre agentes
       migration_futures = []
       migration_particles = [(list(p), p.fitness.values) for p in bests[:config['migrate_k']]]
       for a in agents:
           # Candidatos: enviamos los k mejores a los otros agentes 
           migration_futures.append(a.migrate.remote(migration_particles))
       ray.get(migration_futures)

finally:
   ray.shutdown()






