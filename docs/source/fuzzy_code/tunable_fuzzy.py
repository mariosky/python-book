
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def clamp(x, lo, hi):
   return max(lo, min(hi, x))

def decode_params(x):
   """
   Convierte un vector (lista de floats) en un diccionario de parámetros.

   x : list[float]
       Vector que produce PSO. En este ejemplo se asume longitud 6.
   """
   assert len(x) == 6

   # Interpretación: parámetros simétricos por variable en universo [-1, 1]
   e_z, e_a, eth_z, eth_a, w_z, w_a = x

   # Límites básicos para mantener MFs válidas y estables
   # - z controla el ancho de la zona "cero" (debe ser pequeño)
   # - a controla dónde empieza la saturación de NS/PS (debe ser mayor que z)
   e_z   = clamp(e_z,   0.05, 0.60)
   e_a   = clamp(e_a,   0.10, 1.00)
   eth_z = clamp(eth_z, 0.05, 0.60)
   eth_a = clamp(eth_a, 0.10, 1.00)
   w_z   = clamp(w_z,   0.05, 0.80)
   w_a   = clamp(w_a,   0.10, 1.00)

   # Asegurar orden: a >= z + margen
   margin = 0.05
   e_a   = max(e_a,   e_z   + margin)
   eth_a = max(eth_a, eth_z + margin)
   w_a   = max(w_a,   w_z   + margin)

   params = {
       "e_z": e_z, "e_a": e_a,
       "eth_z": eth_z, "eth_a": eth_a,
       "w_z": w_z, "w_a": w_a,
   }

   return params

def build_fis(params=None):
    """
    Construye el sistema de inferencia difusa (FIS).

    params: dict | None
        Parámetros opcionales para modificar las funciones de membresía.
        En esta versión base, se ignoran o se usan valores por defecto.
    """
    p = decode_params(params)
    eth_z = p["eth_z"]
    eth_a = p["eth_a"]
    e_z   = p["e_z"]
    e_a   = p["e_a"]
    w_z   = p["w_z"]
    w_a   = p["w_a"]

    # Universos (normalizados)
    e_th = ctrl.Antecedent(np.linspace(-1.0, 1.0, 201), "e_th")   # adimensional
    e    = ctrl.Antecedent(np.linspace(-1.0, 1.0, 201), "e")      # adimensional
    omega = ctrl.Consequent(np.linspace(-1.0, 1.0, 201), "omega") # adimensional

    e_th["NS"] = fuzz.trapmf(e_th.universe, [-1.0, -1.0, -eth_a, 0.0])
    e_th["Z"]  = fuzz.trimf(e_th.universe,  [-eth_z,  0.0,  eth_z])
    e_th["PS"] = fuzz.trapmf(e_th.universe, [ 0.0,  eth_a,  1.0, 1.0])

    e["NS"] = fuzz.trapmf(e.universe, [-1.0, -1.0, -e_a, 0.0])
    e["Z"]  = fuzz.trimf(e.universe,  [-e_z,  0.0,  e_z])
    e["PS"] = fuzz.trapmf(e.universe, [ 0.0,  e_a,  1.0, 1.0])

    omega["NS"] = fuzz.trapmf(omega.universe, [-1.0, -1.0, -w_a, 0.0])
    omega["Z"]  = fuzz.trimf(omega.universe,  [-w_z,  0.0,  w_z])
    omega["PS"] = fuzz.trapmf(omega.universe, [ 0.0,  w_a,  1.0, 1.0])


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
    fis = build_fis(params)
    sim = ctrl.ControlSystemSimulation(fis)

    # Escalas físicas (baseline)
    ETH_MAX = 1.5   # rad
    E_MAX = 3.0     # m
    OMEGA_MAX = 8.0 # rad/s

    def controller(e_th, e):
        # 1) Normalizar entradas
        e_th_n = clamp(float(e_th) / ETH_MAX,-1.0,1.0)
        e_n = clamp(float(e) / E_MAX,-1.0,1.0)

        # 2) Evaluar FIS
        sim.reset()
        sim.input["e_th"] = e_th_n
        sim.input["e"] = e_n
        sim.compute()

        # 3) Desnormalizar salida
        omega_n = float(sim.output["omega"])
        omega = OMEGA_MAX * omega_n
        return omega

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

