import tunable_fuzzy as fc
import rear_wheel_sim as rw_sim
import path
import numpy as np

def compute_rmse(traces):
    errors = np.array([tr.error for tr in traces])
    return np.sqrt(np.mean(errors**2))


def evaluate_controller(params): 

    paths = [
        ([0.0, 6.0, 12.5, 5.0, 7.5, 3.0, -1.0], [0.0, 0.0, 5.0, 6.5, 3.0, 5.0, -2.0]),
        ([0.0, 1.0, 2.5, 5.0, 7.5, 3.0, -1.0], [0.0, -4.0, 6.0, 6.5, 3.0, 5.0, -2.0]),
        ([0.0, 2.0, 2.5, 5.0, 7.5, -3.0, -1.0], [0.0, 3.0, 6.0, 6.5, 5.0, 5.0, -2.0]),
    ]

    #controller = None
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

        traces = result["traces"]
        rmse = compute_rmse(traces)
        rmses.append(rmse)

        # Visualización (opcional): se ejecuta después de la simulación
        #rw_sim.animate(result, pause=0.001)
        #rw_sim.plot(result)
    
    return float(np.mean(rmses)), # Return Tuple for DEAP

if __name__ == "__main__":
    print("rear wheel feedback tracking start!!")
    print(evaluate_controller(params=[0.2,0.4,0.3,0.6,0.2,0.3]))
    print(evaluate_controller(params=[0.9,0.9,0.2,0.8,0.1,0.03]))

