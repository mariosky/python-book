
# Based on PythonRobotics (Atsushi Sakai et al.).
# Licensed under the MIT License. See LICENSE file for details.
# Modified substantially for this book: ODE simulation + fuzzy control.

from scipy.integrate import odeint
import matplotlib.pyplot as plt
import math
import numpy as np
import sys
import pathlib
from angle import Pi_2_pi
import warnings
import path


# Parámetros iniciales
L= 2.9      # longitud del vehiculo en mts
KTH = 1.0   # constante de ajuste k2
KE = 0.3    # constanste k
Kp = 1      # Kp

ERROR_MAX = 10 # En metros

show_animation = True

# Modelo del robot estilo bicicleta
#
# Paden, Brian, et al.
# "A survey of motion planning and control techniques for self-driving urban vehicles."
# IEEE Transactions on intelligent vehicles 1.1(2016): 33 - 55.
# https://arxiv.org/abs/1604.07446

def modelo(z, t, delta, aceleracion):
    x, y, teta, v = z
    dx_dt    = v * np.cos(teta)
    dy_dt    = v * np.sin(teta)
    dteta_dt = v / L * np.tan(delta)
    dv_dt    = aceleracion

    return [dx_dt, dy_dt,dteta_dt,dv_dt]


# Control rueda trasera
def control_rueda_trasera(v, yaw0, e, k, yaw_ref, controller, params):
    # calcular el error
    error_teta = Pi_2_pi(yaw0 - yaw_ref)
    
    print(error_teta,e)
    omega = 0.0
    if not controller:
        omega = v * k * math.cos(error_teta) / (1.0 - k * e) - KTH * abs(v) * error_teta - KE * v * math.sin(
            error_teta) / error_teta * e
        print(error_teta,e, omega)
    else:
        try:
            controller.input['e_th'] = error_teta
            controller.input['e'] = e
            controller.compute()
            omega = controller.output['omega']
        except  Exception as e:
            print('Exception', e)

    if error_teta == 0.0 or omega == 0.0 or v == 0.0:
        return 0.0

    delta = math.atan2(L * omega / v, 1.0)
    return delta

def pid_control(velocidad_objetivo, v):
    a = Kp * (velocidad_objetivo - v)
    return a

def simulacion(ruta, meta_objetivo, show_animation=False, controller=None, params=None):
    # posiciones iniciales
    x0 = 0.0
    y0 = 0.0
    yaw0 = 0.0
    v0 = 0.0
    s0 = 0

    x = [x0]
    y = [y0]
    yaw = [yaw0]
    error_teta = []
    v = [v0]
    direction = 1
    z0 = x0, y0, yaw0, v0
    error = []

    # defines un arreglo de los tiempos que vas a medir de 0-10 seg, y los partes en 100 pedazos
    # lo pones en 101 para que haga 100 pedazos
    t = np.linspace(1, 50, 501)

    di = 0
    aceleracion = 0

    for i in range(len(t) - 1):

        goal_flag = False
        error_flag = False

        # di = metodo de control
        # aceleracion
        # control_rueda_trasera = feedback por la retroaliemntacion que da
        e, k, yaw_ref, s0 = ruta.calc_track_error(x0, y0, s0)
        # estaba en 100, vamos a ver que pasa si lo reducimos a 10
        if abs(e) > ERROR_MAX:
            # pass
            error_flag = True
            break

        error.append(e)
        error_t = Pi_2_pi(yaw0 - yaw_ref)
        error_teta.append(error_t)

        try:
            di = control_rueda_trasera(v0, yaw0, e, k, yaw_ref, controller, params)
        except Exception as ex:
            # print(ex, controller, params)
            error_flag = True
            break

        speed_ref, direction = path.calc_target_speed(yaw0, yaw_ref, direction)
        aceleracion = pid_control(speed_ref, v0)

        inputs = (di, aceleracion)

        z = None
        # correr el modelo
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            z = odeint(modelo, z0, [0, 0.1], args=inputs)

        z0 = z[-1]
        x0, y0, yaw0, v0 = z0  # le asignas el ultimo valor de z que es donde estan los valores

        x.append(x0)
        y.append(y0)
        yaw.append(yaw0)
        v.append(v0)

        if show_animation:
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect('key_release_event',
                                         lambda event: [exit(0) if event.key == 'escape' else None])
            spline = np.arange(0, ruta.length + 0.09, 0.1)
            plt.plot(ruta.X(spline), ruta.Y(spline), "-r", label="course")
            plt.plot(x, y, "ob", label="trajectory")
            plt.plot(ruta.X(s0), ruta.Y(s0), "xg", label="target")
            plt.axis("equal")
            plt.grid(True)
            plt.title(f"speed[km/h]:{round(v0 * 3.6, 2):.2f}, target s-param:{s0:.2f}")
            plt.pause(0.0001)
        dx = x0 - meta_objetivo[0]
        dy = y0 - meta_objetivo[1]

        if math.hypot(dx, dy) <= 0.3:
            # print("META")
            goal_flag = True
            break

    sim_trace = {
        't': i,  # tiempo
        'x': x,
        'y': y,
        'yaw': yaw,
        'v': v,
        'error': error,
        'error_flag': error_flag,
        'goal_flag': goal_flag,
    }

    return sim_trace


def main(controller=None, params=None):
    print("rear wheel feedback tracking start!!")
    ax = [0.0, 6.0, 12.5, 5.0, 7.5, 3.0, -1.0]
    ay = [0.0, 0.0, 5.0, 6.5, 3.0, 5.0, -2.0]
    goal = [ax[-1], ay[-1]]

    reference_path = path.CubicSplinePath(ax, ay)
    s = np.arange(0, reference_path.length, 0.1)

    sim_trace = simulacion(reference_path, goal, controller=controller, params=params )

    # Test
    assert sim_trace['goal_flag'], "Cannot goal"

    if show_animation:  # pragma: no cover
        plt.close()
        plt.subplots(1)
        plt.plot(ax, ay, "xb", label="input")
        plt.plot(reference_path.X(s), reference_path.Y(s), "-r", label="spline")
        plt.plot(sim_trace['x'], sim_trace['y'], "-g", label="tracking")
        plt.grid(True)
        plt.axis("equal")
        plt.xlabel("x[m]")
        plt.ylabel("y[m]")
        plt.legend()

        plt.subplots(1)
        plt.plot(s, np.rad2deg(reference_path.calc_yaw(s)), "-r", label="yaw")
        plt.grid(True)
        plt.legend()
        plt.xlabel("line length[m]")
        plt.ylabel("yaw angle[deg]")

        plt.subplots(1)
        plt.plot(s, reference_path.calc_curvature(s), "-r", label="curvature")
        plt.grid(True)
        plt.legend()
        plt.xlabel("line length[m]")
        plt.ylabel("curvature [1/m]")

        plt.show()

if __name__ == '__main__':
    from fis import get_fuzzy_controller 
    fis = get_fuzzy_controller()
    main(controller=fis, params=None)
    #main(controller=None, params=None)
