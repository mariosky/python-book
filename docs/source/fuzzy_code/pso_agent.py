import math
import operator
import random

import numpy
import ray
from typing import List, Tuple, Dict
from deap import base, creator, tools
from evaluate_controller import evaluate_controller


@ray.remote
def remote_ev_controller(particle):
    return evaluate_controller(particle)

class Particle:
    """
    Partícula para PSO.

    Attributes
    ----------
    x : list[float]
        Posición (solución candidata).
    v : list[float]
        Velocidad.
    best_x : list[float]
        Mejor posición personal encontrada hasta el momento.
    best_f : float
        Mejor valor de fitness (a minimizar) asociado a best_x.
    """
    x: List[float] = []
    speed: List[float] = []
    fitness: float = float('inf')
    smin: float
    smax: float
    best_x: List[float]
    best_f: float
    
    def __repr__(self) -> str:
        return (
            f"Particle(f={self.fitness:.4f}, "
            f"x={[round(v, 3) for v in self.x]})"
            f"speed    = {[round(v, 4) for v in self.speed]}"
            f"best_f   = {self.best_f:.6f}\n"
            f"best_x   = {[round(v, 4) for v in self.best_x]}"
        )

    def __str__(self) -> str:
        return (
            "Particle(\n"
            f"  fitness = {self.fitness:.6f}\n"
            f"  x        = {[round(v, 4) for v in self.x]}\n"
            f"  speed    = {[round(v, 4) for v in self.speed]}\n"
            f"  best_f   = {self.best_f:.6f}\n"
            f"  best_x   = {[round(v, 4) for v in self.best_x]}\n"
            ")"
        )

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

    def generate(self):
        part = Particle()
        part.x = [random.uniform(self.pmin, self.pmax) for _ in range(self.size)]
        part.speed = [random.uniform(self.smin, self.smax) for _ in range(self.size)]
        part.fitness = float('inf')
        part.smin = self.smin
        part.smax = self.smax
        part.best_x = []
        part.best_f = float('inf')
        return part

    def update_particle(self, part, best):
        u1 = (random.uniform(0, self.phi1) for _ in range(len(part.x)))
        u2 = (random.uniform(0, self.phi2) for _ in range(len(part.x)))
        v_u1 = map(operator.mul, u1, map(operator.sub, part.best_x, part.x))
        v_u2 = map(operator.mul, u2, map(operator.sub, best.x, part.x))
        part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
        for i, speed in enumerate(part.speed):
            if abs(speed) < part.smin:
                part.speed[i] = math.copysign(part.smin, speed)
            elif abs(speed) > part.smax:
                part.speed[i] = math.copysign(part.smax, speed)
        part.x = list(map(operator.add, part.x, part.speed))



    def evaluate_population_ray(self):
        futures_fitness_values = [remote_ev_controller.remote(list(particle.x)) for particle in self.pop] 
        results = ray.get(futures_fitness_values)
        assert len(self.pop) == len(results)
        
        for i, part in enumerate(self.pop):
            part.fitness = results[i][0] # remote_ev_controller returns a Tuple 
        return self.pop
    
    def migrate(self, migration_particles):
        self.pop.sort(key=lambda p: p.fitness)
        self.pop = self.pop[:-len(migration_particles)] + migration_particles


    def main(self, config):
        self.pop = [self.generate() for _ in range(config['swarm_size'])]

        GEN = config['ngen']
        best = self.generate()
        for g in range(GEN):
            self.evaluate_population_ray()
            for part in self.pop:
                if  part.best_f > part.fitness:
                    part.best_x = part.x[:]
                    part.best_f = part.fitness
                if  best.fitness > part.fitness:
                    best.x =  part.x[:]
                    best.fitness = part.fitness
             
            for part in self.pop:
                self.update_particle(part, best)
            # Gather all the fitnesses in one list and print the stats
            # print(logbook.stream)
        
    
        #print(best.fitness.values, best)
        #return self.pop, logbook, best
        return best


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


import os
os.environ["RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO"] = "0"
os.environ["RAY_DISABLE_DASHBOARD"] = "1"
os.environ["RAY_USAGE_STATS_ENABLED"] = "0"

ray.init(ignore_reinit_error=True, include_dashboard=False)

try:
    agents = [SwarmAgent.remote(config) for i in range(config['num_swarms'])
    ]
   
    best_global = Particle()

    for r in range(config["num_rounds"]):
       # 1) Cada agente ejecuta varias iteraciones locales en paralelo
       futures = [a.main.remote(config) for a in agents]
       bests = [best for best in ray.get(futures)]  # [(f, x), ...]
       bests.sort(key=lambda best: best.fitness) 

       # 2) Actualizar mejor global
       best = bests[0]
       if best_global is None or best_global.fitness > best.fitness:
           best_global.x = best.x[:] 
           best_global.fitness  = best.fitness
       print(f"Ronda {r:02d} | Mejor: {best_global.fitness:.6f}")
       
       # 3) Migración: intercambio de candidatos entre agentes
       if (r + 1) % int(config["migrate_interval"]) == 0:
           print("Migrando")
           migration_futures = []
           migration_particles = bests[:config['migrate_k']]
           for a in agents:
               # Candidatos: enviamos los k mejores a los otros agentes 
               migration_futures.append(a.migrate.remote(migration_particles))
           ray.get(migration_futures)
    
    print(f"Mejor global: {best_global.fitness:.6f} | {best_global.x}")
finally:
    ray.shutdown()






