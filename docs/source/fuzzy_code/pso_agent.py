import random

import ray
from dataclasses import dataclass, field
from typing import List, Tuple, Dict
from evaluate_controller import evaluate_controller


@ray.remote
def remote_ev_controller(x: List[float]) -> float:
    fitness = evaluate_controller(x)
    # Normaliza a float aunque venga como (val,)
    if isinstance(fitness, tuple):
        return float(fitness[0])
    return float(fitness)

def clip(value: float, vmin: float, vmax: float) -> float:
    return max(vmin, min(vmax, value))

@dataclass
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
    x: List[float] = field(default_factory=list)
    speed: List[float] = field(default_factory=list)
    fitness: float = float('inf')
    best_x: List[float] = field(default_factory=list)
    best_f: float = float("inf")
    
    def __repr__(self) -> str:
        return f"Particle(f={self.fitness:.4f}, x={[round(v, 3) for v in self.x]})"

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
    def __init__(self, config: Dict) -> None:
        self.config = config
        self.swarm_size = int(config["swarm_size"])
        self.size = int(config['dim'])

        self.smin = float(config['smin'])
        self.smax = float(config['smax'])
        self.pmax = float(config['pmax'])
        self.pmin = float(config['pmin'])
        self.weight = float(config.get("w", 0.7))
        self.phi1 = float(config['phi1'])
        self.phi2 = float(config['phi2'])
        self.pop: List[Particle] = [self.generate() for _ in range(self.swarm_size)]
        self.gbest = Particle(
            x=self.pop[0].x.copy(),
            speed=[0.0] * self.size,
            fitness=float("inf"),
            best_x=self.pop[0].x.copy(),
            best_f=float("inf"),
        )

    def generate(self) -> Particle:
        x = [random.uniform(self.pmin, self.pmax) for _ in range(self.size)]
        speed = [random.uniform(self.smin, self.smax) for _ in range(self.size)]
        return Particle(x=x, speed=speed, fitness=float("inf"), best_x=x.copy(), best_f=float("inf"))

    def _update_particle(self, p: Particle) -> None:
        for d in range(self.size):
            r1 = random.random()
            r2 = random.random()

            cognitive = self.phi1 * r1 * (p.best_x[d] - p.x[d])
            social = self.phi2 * r2 * (self.gbest.x[d] - p.x[d])

            p.speed[d] = self.weight * p.speed[d] + cognitive + social
            p.speed[d] = clip(p.speed[d], self.smin, self.smax)

            p.x[d] = p.x[d] + p.speed[d]
            p.x[d] = clip(p.x[d], self.pmin, self.pmax)


    def evaluate_population_ray(self):
        futures_fitness_values = [remote_ev_controller.remote(list(particle.x)) for particle in self.pop] 
        results = ray.get(futures_fitness_values)
        assert len(self.pop) == len(results)
        
        for p, f in zip(self.pop, results):
            p.fitness = f

            if f < p.best_f:
                p.best_f = f
                p.best_x = p.x.copy()

            if f < self.gbest.fitness:
                self.gbest.fitness = f
                self.gbest.x = p.x.copy()
                self.gbest.best_f = f
                self.gbest.best_x = p.x.copy()

 
    def migrate(self, candidates: List[Tuple[float, List[float]]]) -> None:
        """
        candidates: lista de (fitness, x) (tipos planos).
        Reemplaza las peores partículas por estos candidatos.
        """
        # Asegurar fitness actualizado para identificar peores
        self.evaluate_population_ray()

        # Peores primero
        worst_idx = sorted(range(self.swarm_size), key=lambda i: self.pop[i].fitness, reverse=True)
        k = min(len(candidates), self.swarm_size)

        for j in range(k):
            f_cand, x_cand = candidates[j]
            i = worst_idx[j]
            # Insertar candidato con velocidad nueva (para no heredar dinámica ajena)
            self.pop[i] = Particle(
                x=list(x_cand),
                speed=[random.uniform(self.smin, self.smax) for _ in range(self.size)],
                fitness=float(f_cand),
                best_x=list(x_cand),
                best_f=float(f_cand),
            )

            if f_cand < self.gbest.fitness:
                self.gbest.fitness = float(f_cand)
                self.gbest.x = list(x_cand)


    def step(self, n_iters: int) -> Particle:
        for _ in range(n_iters):
            self.evaluate_population_ray()
            for part in self.pop:
                self._update_particle(part)
            # Gather all the fitnesses in one list and print the stats
            # print(logbook.stream)
        return self.gbest


config = {
    "smin": -0.2,
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
       futures = [a.step.remote(config['ngen']) for a in agents]
       bests = [best for best in ray.get(futures)]  # [(f, x), ...]
       bests.sort(key=lambda best: best.fitness) 

       # 2) Actualizar mejor global
       best = bests[0]
       if best_global.fitness > best.fitness:
           best_global.x = best.x[:] 
           best_global.fitness  = best.fitness
       print(f"Ronda {r:02d} | Mejor: {best_global.fitness:.6f}")
       
       # 3) Migración: intercambio de candidatos entre agentes
       if (r + 1) % int(config["migrate_interval"]) == 0:
           print("Migrando")
           migration_futures = []
           migration_particles = [(particle.fitness, particle.x)  for particle in bests[:config['migrate_k']]]
           for a in agents:
               # Candidatos: enviamos los k mejores a los otros agentes 
               migration_futures.append(a.migrate.remote(migration_particles))
           ray.get(migration_futures)
    print(f"Mejor global: {best_global.fitness:.6f} | {best_global.x}")
finally:
    ray.shutdown()

