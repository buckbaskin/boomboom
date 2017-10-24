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
    Si = [0.0]
    V = [0.0]
    Vi = [0.0]
    A = [0.0]
    Ai = [0.0]
    angle = [0.0]
    time = [0.0]

    print('simulate steps')

    for i in range(0, num_steps):
        e._cylinder.step(step_angle, step_time)

        angle.append(angle[-1] + step_angle)
        time.append(time[-1] + step_time)

        S.append(e._cylinder.lin_s[0])
        Si.append(e._cylinder.lin_position(angle[-1]))
        V.append(e._cylinder.lin_v[0])
        Vi.append(e._cylinder.lin_velocity(angle[-1], rad_per_sec))
        A.append(e._cylinder.lin_a[0])
        Ai.append(e._cylinder.lin_accel(angle[-1], rad_per_sec))


    S = np.array(S)
    V = np.array(V)
    A = np.array(A)
    angle = np.array(angle)
    time = np.array(time)
    
    print('render steps')

    # fig = plt.figure()
    # ax = plt.axes()

    # plt.plot(angle, S)
    # plt.plot(angle, Si)
    # plt.xlabel('Crankshaft angle, first piston (radians)')
    # plt.ylabel('Distance from cylinder roof (cm)')
    
    plt.plot(angle, V)
    plt.plot(angle, Vi)
    plt.xlabel('Crankshaft angle, first piston (radians)')
    plt.ylabel('Velocity (cm / sec)')
    
    # plt.plot(angle, A)
    # plt.plot(angle, Vi)
    # plt.xlabel('Crankshaft angle, first piston (radians)')
    # plt.ylabel('Distance from cylinder roof (cm)')
    plt.show()
