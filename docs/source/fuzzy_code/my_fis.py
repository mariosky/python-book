import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def build_fis(params=None):
    """
   Construye el sistema de inferencia difusa (FIS).

   params: dict | None
       Parámetros opcionales para modificar las funciones de membresía.
       En esta versión base, se ignoran o se usan valores por defecto.
   """

    # Universos (sin normalizar todavía)
    e_th = ctrl.Antecedent(np.linspace(-1.5, 1.5, 201), 'e_th')  # rad aprox.
    e = ctrl.Antecedent(np.linspace(-3.0, 3.0, 201), 'e')  # m
    omega = ctrl.Consequent(np.linspace(-8.0, 8.0, 201), 'omega')  # rad/s

    # e_th: NS, Z, PS
    e_th['NS'] = fuzz.trapmf(e_th.universe, [-1.5, -1.5, -0.4, 0.0])
    e_th['Z'] = fuzz.trimf(e_th.universe, [-0.15, 0.0, 0.15])
    e_th['PS'] = fuzz.trapmf(e_th.universe, [0.0, 0.4, 1.5, 1.5])

    # e: NS, Z, PS
    e['NS'] = fuzz.trapmf(e.universe, [-3.0, -3.0, -0.8, 0.0])
    e['Z'] = fuzz.trimf(e.universe, [-0.30, 0.0, 0.30])
    e['PS'] = fuzz.trapmf(e.universe, [0.0, 0.8, 3.0, 3.0])

    # omega: NS, Z, PS
    omega['NS'] = fuzz.trapmf(omega.universe, [-8.0, -8.0, -2.5, 0.0])
    omega['Z'] = fuzz.trimf(omega.universe, [-0.80, 0.0, 0.80])
    omega['PS'] = fuzz.trapmf(omega.universe, [0.0, 2.5, 8.0, 8.0])

    # Reglas explícitas (3x3)
    rules = [
        ctrl.Rule(e_th['NS'] & e['NS'], omega['PS']),
        ctrl.Rule(e_th['NS'] & e['Z'], omega['PS']),
        ctrl.Rule(e_th['NS'] & e['PS'], omega['Z']),

        ctrl.Rule(e_th['Z'] & e['NS'], omega['PS']),
        ctrl.Rule(e_th['Z'] & e['Z'], omega['Z']),
        ctrl.Rule(e_th['Z'] & e['PS'], omega['NS']),

        ctrl.Rule(e_th['PS'] & e['NS'], omega['Z']),
        ctrl.Rule(e_th['PS'] & e['Z'], omega['NS']),
        ctrl.Rule(e_th['PS'] & e['PS'], omega['NS']),
    ]

    fis = ctrl.ControlSystem(rules)
    return fis


def get_controller(params=None):
    """
   Devuelve un controlador callable: (e_th, e) -> omega.
   """

    fis = build_fis(params)
    sim = ctrl.ControlSystemSimulation(fis)

    def controller(e_th, e):
        # scikit-fuzzy acumula estado interno; para simulación en lazo cerrado
        # suele ser más robusto reiniciar en cada evaluación.
        sim.reset()
        sim.input['e_th'] = float(e_th)
        sim.input['e'] = float(e)
        sim.compute()
        return float(sim.output['omega'])

    return controller


def plot_mfs(params=None):
    """
   Visualiza las funciones de membresía (modo exploración).
   """
    fis = build_fis(params)
    for variable in fis.fuzzy_variables:
        variable.view()
    

if __name__ == "__main__":
    # Ejecuta: python my_fis.py
    # para inspeccionar las funciones de membresía.
    plot_mfs()
