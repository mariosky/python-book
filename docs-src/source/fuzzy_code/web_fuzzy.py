from fastapi import FastAPI

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hola": "Mundo"}


@app.get("/propina/{comida_val}/{servicio_val}")
def calc_propina(comida_val: float, servicio_val: float):

    comida = ctrl.Antecedent(np.arange(0, 11, 1), 'comida')
    servicio = ctrl.Antecedent(np.arange(0, 11, 1), 'servicio')
    propina = ctrl.Consequent(np.arange(0, 26, 1), 'propina')

    comida.automf(3)
    servicio.automf(3)

    propina['low'] = fuzz.trimf(propina.universe, [0, 0, 13])
    propina['medium'] = fuzz.trimf(propina.universe, [0, 13, 25])
    propina['high'] = fuzz.trimf(propina.universe, [13, 25, 25])
    rule1 = ctrl.Rule(comida['poor'] | servicio['poor'], propina['low'])
    rule2 = ctrl.Rule(servicio['average'], propina['medium'])
    rule3 = ctrl.Rule(servicio['good'] | comida['good'], propina['high'])
    propina_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    calcula_propina = ctrl.ControlSystemSimulation(propina_ctrl)

    calcula_propina.input['comida'] = comida_val
    calcula_propina.input['servicio'] = servicio_val



    calcula_propina.compute()
    return {"propina": calcula_propina.output['propina']}

