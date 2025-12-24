import json
import tunable_fuzzy as fc
from evaluate_controller import compute_rmse
import rear_wheel_sim as rw_sim
import path
import argparse

def load_config(path_cfg):
    with open(path_cfg, "r") as f:
        cfg = json.load(f)
    params = cfg["params"]
    paths = [(p["ax"], p["ay"]) for p in cfg["paths"]]
    return params, paths, cfg

def show_controller(params, paths, path_id):

    controller = fc.get_controller(params)

    ax, ay = paths[path_id]
    goal = [ax[-1], ay[-1]]
    reference_path = path.CubicSplinePath(ax, ay)
    result = rw_sim.simulacion(
        reference_path,
        goal,
        controller=controller,
    )
    if not result['goal_flag']:
        print("⚠️  No se alcanzó la meta")
    if result['error_flag']:
        print("⚠️  Error en la simulación")

    traces = result["traces"]
    rmse = compute_rmse(traces)
    print('rmse: {rmse}')

    rw_sim.animate(result, pause=0.001)
    rw_sim.plot(result)
    fc.plot_mfs(params=params)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualiza el controlador difuso para una ruta específica"
    )
    parser.add_argument(
        "path_id",
        type=int,
        nargs="?",
        default=0,
        help="Índice de la ruta a mostrar (default: 0)",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="best_controller.json",
        help="Archivo de configuración del controlador",
    )

    args = parser.parse_args()

    params, paths, cfg = load_config(args.config)

    if args.path_id < 0 or args.path_id >= len(paths):
        raise ValueError(f"path_id debe estar entre 0 y {len(paths)-1}")

    show_controller(params, paths, path_id=args.path_id)

