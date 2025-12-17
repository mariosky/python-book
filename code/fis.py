import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

def get_fuzzy_controller():
    # Entradas (universos normalizados)

    e_th = ctrl.Antecedent(np.linspace(-1.2, 1.2, 201), 'e_th')  # ~±69°
    #e_th = ctrl.Antecedent(np.linspace(-8.0, 8.0, 201), 'e_th') # Error the heading
    e   = ctrl.Antecedent(np.linspace(-8.0, 8.0, 201), 'e') # Error tracking



    # Términos lingüísticos (3 niveles: NS, Z, PS)
    #e_th['NS'] = fuzz.trapmf(e_th.universe, [-5, -5, -0.1, 0.0])
    #e_th['Z']  = fuzz.trimf(e_th.universe,  [-1, 0.0, 1])
    #e_th['PS'] = fuzz.trapmf(e_th.universe, [0.0, 0.1, 5, 5])

    e_th['NS'] = fuzz.trapmf(e_th.universe, [-1.2, -1.2, -0.3, 0.0])
    e_th['Z'] = fuzz.trimf(e_th.universe, [-0.15, 0.0, 0.15])
    e_th['PS'] = fuzz.trapmf(e_th.universe, [0.0, 0.3, 1.2, 1.2])

    e['NS'] = fuzz.trapmf(e.universe, [-10, -10, -0.2, 0.0])
    e['Z']  = fuzz.trimf(e.universe,  [-0.5, 0.0, 0.5])
    e['PS'] = fuzz.trapmf(e.universe, [0.0, 0.2 , 10, 10])

    #omega = ctrl.Consequent(np.linspace(-2.0, 2.0, 201), 'omega')
    #omega['NS'] = fuzz.trapmf(omega.universe, [-2, -2, -0.8, -0.1])
    #omega['Z'] = fuzz.trimf(omega.universe, [-0.2, 0.0, 0.2])
    #omega['PS'] = fuzz.trapmf(omega.universe, [0.1, 0.8, 2, 2])

    # Salida (velocidad angular)
    omega = ctrl.Consequent(np.linspace(-8.0, 8, 201), 'omega')
    # Ajuste: MFs consistentes con universo [-5,5]
    omega['NS'] = fuzz.trapmf(omega.universe, [-8, -8, -2, -0.5])
    omega['Z']  = fuzz.trimf(omega.universe,  [-1, 0, 1])
    omega['PS'] = fuzz.trapmf(omega.universe, [0.5, 2, 8, 8])

    e_th.view()
    omega.view()
    e.view() 

    r1 = ctrl.Rule(e_th['NS'] & e['NS'], omega['PS'])
    r2 = ctrl.Rule(e_th['NS'] & e['Z'],  omega['PS'])
    r3 = ctrl.Rule(e_th['NS'] & e['PS'], omega['Z'])
    r4 = ctrl.Rule(e_th['Z']  & e['NS'], omega['PS'])
    r5 = ctrl.Rule(e_th['Z']  & e['Z'],  omega['Z'])
    r6 = ctrl.Rule(e_th['Z']  & e['PS'], omega['NS'])
    r7 = ctrl.Rule(e_th['PS'] & e['NS'], omega['Z'])
    r8 = ctrl.Rule(e_th['PS'] & e['Z'],  omega['NS'])
    r9 = ctrl.Rule(e_th['PS'] & e['PS'], omega['NS'])
    rules = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
    fis = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(fis)

    return sim

if __name__ == '__main__':
    controller = get_fuzzy_controller()
    try:
        controller.input['e_th'] = -3.0273813880653915
        controller.input['e'] = 0.0
        controller.compute()
        omega = controller.output['omega']
    except Exception as e:
        print(e)
    print(controller.output['omega'])

