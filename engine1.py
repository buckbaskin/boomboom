from engine_parameters import *
from boomboom.cylinder import *
from boomboom.intake import *
from boomboom.exhaust import *

print('load pyplot')

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

print('done loading dependencies')

class Engine(AbstractModel):
    def __init__(self, intake, cylinder, exhaust):
        self._intake = intake
        self._cylinder = cylinder
        self._exhuast = exhaust

    def step(self, crank_degree, time_step):
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

    S = [0.0]
    V = [0.0]
    A = [0.0]
    angle = [0.0]
    time = [0.0]

    print('simulate steps')

    for _ in range(0, num_steps):
        e.step(step_angle, step_time)

        S.append(e._cylinder.lin_s[0])
        V.append(e._cylinder.lin_v[0])
        A.append(e._cylinder.lin_a[0])
        angle.append(angle[-1] + step_angle)
        time.append(time[-1] + step_time)

    print('render steps')

    # fig = plt.figure()
    # ax = plt.axes()

    plt.plot(np.array(angle), np.array(S))
    # plt.plot(angle, V)
    # plt.plot(angle, A)
    plt.show()
