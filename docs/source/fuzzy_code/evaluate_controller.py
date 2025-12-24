import tunable_fuzzy as fc
import rear_wheel_sim as rw_sim
import path
import numpy as np
import json

def compute_rmse(traces):
    errors = np.array([tr.error for tr in traces])
    return np.sqrt(np.mean(errors**2))

def load_best(path_cfg):
    with open(path_cfg, "r") as f:
        cfg = json.load(f)
    params = cfg["params"]
    paths = [(p["ax"], p["ay"]) for p in cfg["paths"]]
    return params, paths, cfg

def show_controlller(params, p):
    controller = fc.get_controller(params)
    goal = [p[0][-1], p[1][-1]]

    reference_path = path.CubicSplinePath(p[0], p[1])

    result = rw_sim.simulacion(
        reference_path,
        goal,
        controller=controller,
    )
    if not result['goal_flag']:
        print('No goal')
    if result['error_flag']:
        print('Error')

    traces = result["traces"]
    rmse = compute_rmse(traces)
    print(result['goal_flag'], result['error_flag'], rmse)
    # Visualización (opcional): se ejecuta después de la simulación
    rw_sim.animate(result, pause=0.001)
    rw_sim.plot(result)
    fc.plot_mfs(params=params)

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
            print('No goal')
            return float(10.0), # Return Tuple for DEAP
        if result['error_flag']:
            print('Error')
            return float(10.0), # Return Tuple for DEAP

        traces = result["traces"]
        rmse = compute_rmse(traces)
        rmses.append(rmse)
        #print(result['goal_flag'], result['error_flag'], rmse)
        # Visualización (opcional): se ejecuta después de la simulación
        #rw_sim.animate(result, pause=0.001)
        #rw_sim.plot(result)
        #fc.plot_mfs(params=params)
    print(np.mean(rmses))
    return float(np.mean(rmses)), # Return Tuple for DEAP

if __name__ == "__main__":
    print("loading best..")
    params, paths, cfg = load_best("best_controller.json")
    show_controlller(params, paths[2])



    show_controlller(params, paths[2])
