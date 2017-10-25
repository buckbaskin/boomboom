from engine_parameters import *
from boomboom.cylinder import *
from boomboom.intake import *
from boomboom.exhaust import *
from boomboom.sensor import SVASensor

print('load pyplot')

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

print('done loading dependencies')

class Engine(AbstractModel):
    def __init__(self, intake, cylinder, exhaust, sensor):
        self._intake = intake
        self._cylinder = cylinder
        self._exhuast = exhaust
        self._sensor = sensor
        self._sensor.register(self)

    def step(self, crank_degree, time_step):
        self._cylinder.step(crank_degree, time_step)
        self._sensor.step(crank_degree, time_step)

if __name__ == '__main__':
    e = Engine(None, KinematicCylinderModel(piston_orientation), None, SVASensor())

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
        e.step(step_angle, step_time)

    e._sensor.plot()
