from engine_parameters import *
from boomboom.cylinder import *
from boomboom.intake import *
from boomboom.exhaust import *

import matplotlib.pyplot as plt

class Engine(AbstractModel):
    def __init__(self, intake, cylinder, exhaust):
        self._intake = intake
        self._cylinder = cylinder
        self._exhuast = exhaust

    def step(crank_degree, time_step):
        self._cylinder.step(crank_degree, time_step)

if __name__ == '__main__':
    e = Engine(None, KinematicCylinderModel(piston_orientation), None)

    total_revs = 2
    total_rad = total_revs * 2 * pi
    num_steps = 1000

    rpm = 1000
    rad_per_sec = rpm / 60 * 2 * pi

    step_angle = total_rad / num_steps
    step_time = step_angle / rad_per_sec

    S = []
    V = []
    A = []
    angle = []
    time = []

    for _ in range(0, num_steps):
        e.step(step_angle, step_time)

        S.append(e.lin_p)
        V.append(e.lin_v)
        A.append(e.lin_a)
        angle.append(angle[-1] + step_angle)
        time.append(time[-1] + step_time)


    fig = plt.figure()
    ax = plt.axes()

    plt.plot(angle, S)
    plt.plot(angle, V)
    plt.plot(angle, A)