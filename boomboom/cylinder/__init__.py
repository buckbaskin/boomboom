import numpy as np

from engine_parameters import *
from boomboom import AbstractModel

class AbstractCylinderModel(AbstractModel):
    pass

class KinematicCylinderModel(AbstractCylinderModel):
    def __init__(self, piston_orientation):
        # ex [0, 90, 180, 270]
        self.piston_orientation = np.array(piston_orientation)

        # flat roof assumption
        self.clearance = combustion_chamber_volume / (cylinder_radius**2 * pi)
        self.lin_s = self.lin_position(self.piston_orientation)
        self.lin_v = 0.0
        self.lin_a = 0.0

        # crank orientation in radians, with 0.0 = TDC for front piston

    def lin_position(self, crank_orientation):
        return (crank_radius * (1 - cos(crank_orientation)) + 
            crank_ratio / 2 * crank_radius * sin(crank_orientation)**2)

    def lin_velocity(self, crank_orientation, crank_vel):
        return (crank_vel*crank_radius*sin(crank_orientation) * 
            (1 + crank_ratio * cos(crank_orientation)))

    def lin_accel(self, crank_orientation, crank_vel):
        return (crank_vel**2 * crank_ratio *
            (cos(crank_orientation) + crank_ratio* cos(2 * crank_orientation)))

    def step(self, crank_step, time_step):
        deg_per_sec = crank_step / time_step
        rad_per_sec = deg_per_sec / 180 * pi
        old_orientation = self.piston_orientation
        new_orientation = self.piston_orientation + crank_step

        avg_vel = self.lin_position(new_orientation) - self.lin_position(old_orientation) / time_step
        avg_accel = (self.lin_velocity(new_orientation, rad_per_sec) -
            self.lin_velocity(old_orientation, rad_per_sec) / time_step)

        self.lin_s = (self.lin_position(new_orientation) + self.lin_position(old_orientation)) / 2 + self.clearance
        self.lin_v = avg_vel
        self.lin_a = avg_accel
        # print(self.lin_a)
        self.crank_orientation = new_orientation


