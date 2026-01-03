import tunable_fuzzy as fc
import rear_wheel_sim as rw_sim
import path
import numpy as np
import ray

def compute_rmse(traces):
    errors = np.array([tr.error for tr in traces])
    return np.sqrt(np.mean(errors**2))

def evaluate_controller(params):

    paths = [
        ([0.0, 6.0, 12.5, 5.0, 7.5, 3.0, -1.0], [0.0, 0.0, 5.0, 6.5, 3.0, 5.0, -2.0]),
        ([0.0, 1.0, 2.5, 5.0, 7.5, 3.0, -1.0], [0.0, -4.0, 6.0, 6.5, 3.0, 5.0, -2.0]),
        ([0.0, 2.0, 2.5, 5.0, 7.5, -3.0, -1.0], [0.0, 3.0, 6.0, 6.5, 5.0, 5.0, -2.0]),
    ]
    
    controller = None
    
    if params:
        controller = fc.get_controller(params)
    
    rmses = []
    for ax, ay in paths:
        goal = [ax[-1], ay[-1]]
        reference_path = path.CubicSplinePath(ax, ay)

        result = rw_sim.simulacion(
            reference_path,
            goal,
            controller=controller,
        )
        if not result['goal_flag']:
            return float(10.0), # Return Tuple for DEAP
        if result['error_flag']:
            return float(10.0), # Return Tuple for DEAP

        traces = result["traces"]
        rmse = compute_rmse(traces)
        rmses.append(rmse)
        #print(result['goal_flag'], result['error_flag'], rmse)
        # Visualización (opcional): se ejecuta después de la simulación
        #rw_sim.animate(result, pause=0.001)
        #rw_sim.plot(result)
        #fc.plot_mfs(params=params)
    #print(np.mean(rmses))
    return float(np.mean(rmses)), # Return Tuple for DEAP


def evaluate_controller_ray(params):
    remote_sim = ray.remote(rw_sim.simulacion)
    paths = [
        ([0.0, 6.0, 12.5, 5.0, 7.5, 3.0, -1.0], [0.0, 0.0, 5.0, 6.5, 3.0, 5.0, -2.0]),
        ([0.0, 1.0, 2.5, 5.0, 7.5, 3.0, -1.0], [0.0, -4.0, 6.0, 6.5, 3.0, 5.0, -2.0]),
        ([0.0, 2.0, 2.5, 5.0, 7.5, -3.0, -1.0], [0.0, 3.0, 6.0, 6.5, 5.0, 5.0, -2.0]),
    ]
    
    controller = None
    
    if params:
        controller = fc.get_controller(params)
      
    rmses = []
    futures = []
    for ax, ay in paths:
        goal = [ax[-1], ay[-1]]
        reference_path = path.CubicSplinePath(ax, ay)

        future = remote_sim.remote(
            reference_path,
            goal,
            controller=controller,
        )
        futures.append(future)
    results = ray.get(futures)

    for result in results:
        if not result['goal_flag']:
            return float(10.0), # Return Tuple for DEAP
        if result['error_flag']:
            return float(10.0), # Return Tuple for DEAP

        traces = result["traces"]
        rmse = compute_rmse(traces)
        rmses.append(rmse)
        #print(result['goal_flag'], result['error_flag'], rmse)
        # Visualización (opcional): se ejecuta después de la simulación
        #rw_sim.animate(result, pause=0.001)
        #rw_sim.plot(result)
        #fc.plot_mfs(params=params)
    #print(np.mean(rmses))
    return float(np.mean(rmses)), # Return Tuple for DEAP



