import numpy as np

from engine_parameters import *

print('load pyplot')

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

class AbstractSensor(object):
    pass

class SVASensor(AbstractSensor):
    def __init__(self, visual=False):
        self.visual = visual
        self._engine = None
        self.S = [0.0]
        self.Si = [0.0]
        self.V = [0.0]
        self.Vi = [0.0]
        self.A = [0.0]
        self.Ai = [0.0]
        self.angle = [0.0]
        self.time = [0.0]

        self.mean_piston_speed = 0.0
        self.max_piston_speed = 0.0
        self.rpm = [0.0]

    def register(self, engine):
        self._engine = engine

    def step(self, crank_step, time_step):
        rad_per_sec = crank_step / time_step
        rpm = rad_per_sec * 60 / (2 * pi)
        self.rpm.append(rpm)

        self.angle.append(self.angle[-1] + crank_step)
        self.time.append(self.time[-1] + time_step)

        self.S.append(self._engine._cylinder.lin_s[0])
        self.Si.append(self._engine._cylinder.lin_position(self.angle[-1]))
        self.V.append(self._engine._cylinder.lin_v[0])
        self.Vi.append(self._engine._cylinder.lin_velocity(self.angle[-1], rad_per_sec))

        np_vel = np.array(self.Vi[1:])
        self.mean_piston_speed = np.mean(np.abs(np_vel))
        self.max_piston_speed = np.amax(np_vel)

        self.A.append(self._engine._cylinder.lin_a[0])
        self.Ai.append(self._engine._cylinder.lin_accel(self.angle[-1], rad_per_sec))

    def plot(self, values=None):
        if values is None:
            values = ['S', 'V']
        S = np.array(self.S[1:]) / 100
        V = np.array(self.V[1:]) / 100
        A = np.array(self.A[1:]) / 100
        Si = np.array(self.Si[1:]) / 100
        Vi = np.array(self.Vi[1:]) / 100
        Ai = np.array(self.Ai[1:]) / 100
        angle = np.array(self.angle[1:])
        time = np.array(self.time[1:])

        plt.xlabel('Crankshaft angle, first piston (radians)')
        if ('S' in values):
            plt.plot(angle, S)
        if ('V' in values):
            plt.plot(angle, V)
        if ('A' in values):
            plt.plot(angle, A)
        plt.show()

    def summary(self):
        avg_rpm = np.mean(np.array(self.rpm[1:]))
        print('Avg RPM           %5d' % (avg_rpm,))
        print('Mean Piston Speed %2.2f m/s' % (self.mean_piston_speed / 100,))
        print('Max Piston Speed  %2.2f m/s' % (self.max_piston_speed / 100,))
