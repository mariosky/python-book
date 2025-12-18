
# Based on PythonRobotics (Atsushi Sakai et al.).
# Licensed under the MIT License. See LICENSE file for details.
# Modified substantially for this book: ODE simulation + fuzzy control, refactoring of animation, plots.

from scipy.integrate import odeint
import matplotlib.pyplot as plt
import math
import numpy as np
from angle import Pi_2_pi
import warnings
import path
from dataclasses import dataclass

# Parámetros iniciales
L= 2.9      # longitud del vehiculo en mts
ERROR_MAX = 10 # En metros


@dataclass
class SimulationTrace:
    """
    Registro temporal de la simulación.
    """
    t: int          # tiempo (s)
    x: float        # posición x (m)
    y: float        # posición y (m)
    yaw: float      # orientación (rad)
    v: float        # velocidad lineal (m/s)
    error_theta: float  # error de orientación (rad)
    error: float    # error lateral (m)
    path_s: float   # parámetro de progreso sobre la ruta




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

def paden_control(error, error_theta, v, k):
    """
    Controlador de referencia basado en Paden et al.
    """

    # Constantes del controlador (baseline)
    KTH = 1.0
    KE = 0.5

    omega = (
        v * k * math.cos(error_theta) / (1.0 - k * error)
        - KTH * abs(v) * error_theta
        - KE * v * math.sin(error_theta) / error_theta * error
    )

    return omega

# Control rueda trasera
def control_rueda_trasera(v, yaw0, e, k, yaw_ref, controller, params):
    # calcular el error
    error_theta = Pi_2_pi(yaw0 - yaw_ref)
    omega = 0.0
    if not controller:
        omega = paden_control(e, error_theta, v, k)
    else:
        omega = controller(error_theta, e)
    if error_theta == 0.0 or omega == 0.0 or v == 0.0:
        return 0.0

    delta = math.atan2(L * omega / v, 1.0)
    return delta

def pid_control(velocidad_objetivo, v):
    Kp = 1.0
    a = Kp * (velocidad_objetivo - v)
    return a

def simulacion(ruta, meta_objetivo, controller=None, params=None):
    # posiciones iniciales
    x0 = 0.0
    y0 = 0.0
    yaw0 = 0.0
    v0 = 0.0
    s0 = 0
    direction = 1
    z0 = x0, y0, yaw0, v0

    traces = [SimulationTrace(t=0, x=x0, y=y0, yaw=yaw0, v=v0, error_theta=0, error=0, path_s=s0)]

    # defines un arreglo de los tiempos que vas a medir de 0-10 seg, y los partes en 100 pedazos
    # lo pones en 101 para que haga 100 pedazos
    t = np.linspace(1, 50, 501)

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

        error_t = Pi_2_pi(yaw0 - yaw_ref)

        try:
            di = control_rueda_trasera(v0, yaw0, e, k, yaw_ref, controller, params)
        except Exception as ex:
            error_flag = True
            break

        speed_ref, direction = path.calc_target_speed(yaw0, yaw_ref, direction)
        aceleracion = pid_control(speed_ref, v0)

        inputs = (di, aceleracion)

        z = None
        # integración
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            z = odeint(modelo, z0, [0, 0.1], args=inputs)

        z0 = z[-1]
        x0, y0, yaw0, v0 = z0  # le asignas el ultimo valor de z que es donde estan los valores

        traces.append(SimulationTrace(t=i, x=x0, y=y0, yaw=yaw0, v=v0, error_theta=error_t, error=e, path_s=s0))

        dx = x0 - meta_objetivo[0]
        dy = y0 - meta_objetivo[1]

        if math.hypot(dx, dy) <= 0.3:
            # print("META")
            goal_flag = True
            break

    result = {
        'traces':traces,
        'error_flag': error_flag,
        'goal_flag': goal_flag,
        'ruta': ruta,
    }

    return result


def animate(sim_trace, pause=0.0001):
    ruta = sim_trace['ruta']
    traces= sim_trace['traces']
    for trace in traces:
        #trace= traces[i]
        plt.cla()
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect('key_release_event',
                                     lambda event: [exit(0) if event.key == 'escape' else None])
        spline = np.arange(0, ruta.length + 0.09, 0.1)
        plt.plot(ruta.X(spline), ruta.Y(spline), "-r", label="course")
        plt.plot(trace.x, trace.y, "ob", label="trajectory")
        plt.plot(ruta.X(trace.path_s), ruta.Y(trace.path_s), "xg", label="target")
        plt.axis("equal")
        plt.grid(True)
        plt.title(f"speed[km/h]:{round(trace.v * 3.6, 2):.2f}, target s-param:{trace.path_s:.2f}")
        plt.pause(pause)

def plot(sim_trace):
    plt.close()
    plt.subplots(1)
    ruta = sim_trace['ruta']
    traces= sim_trace['traces']
    #plt.plot(ax, ay, "xb", label="input")
    spline = np.arange(0, ruta.length + 0.09, 0.1)
    plt.plot(ruta.X(spline), ruta.Y(spline), "-r", label="spline")
    plt.plot(np.array([t.x for t in traces]), np.array([t.y for t in traces]), "-g", label="tracking")
    plt.grid(True)
    plt.axis("equal")
    plt.xlabel("x[m]")
    plt.ylabel("y[m]")
    plt.legend()

    plt.subplots(1)
    plt.plot(spline, np.rad2deg(ruta.calc_yaw(spline)), "-r", label="yaw")
    plt.grid(True)
    plt.legend()
    plt.xlabel("line length[m]")
    plt.ylabel("yaw angle[deg]")

    plt.subplots(1)
    plt.plot(spline, ruta.calc_curvature(spline), "-r", label="curvature")
    plt.grid(True)
    plt.legend()
    plt.xlabel("line length[m]")
    plt.ylabel("curvature [1/m]")

    plt.show()

