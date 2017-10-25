import numpy as np

print('load pyplot')

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt



class AbstractSensor(object):
    pass

class SVASensor(object):
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

    def register(self, engine):
        self._engine = engine

    def step(self, crank_step, time_step):
        rad_per_sec = crank_step / time_step

        self.angle.append(self.angle[-1] + crank_step)
        self.time.append(self.time[-1] + time_step)

        self.S.append(self._engine._cylinder.lin_s[0])
        self.Si.append(self._engine._cylinder.lin_position(self.angle[-1]))
        self.V.append(self._engine._cylinder.lin_v[0])
        self.Vi.append(self._engine._cylinder.lin_velocity(self.angle[-1], rad_per_sec))
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
