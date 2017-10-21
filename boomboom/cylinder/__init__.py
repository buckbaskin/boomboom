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
        self.lin_p = self.lin_position(self.piston_orientation)
        self.lin_v = 0.0
        self.lin_a = 0.0

        # crank orientation in radians, with 0.0 = TDC for front piston

    def lin_position(crank_orientation):
        return crank_radius * (1 - cos(crank_orientation))

    def lin_velocity(crank_orientation):
        pass

    def lin_accel(crank_orientation):
        pass

    def step(crank_step, time_step):
        deg_per_sec = crank_degree / time_step
        rad_per_sec = deg_per_sec / 180 * pi
        old_orientation = self.piston_orientation
        new_orientation = self.piston_orientation + crank_degree

        avg_vel = self.lin_position(new_orientation) - self.lin_position(old_orientation) / time_step
        avg_accel = self.lin_velocity(new_orientation) - self.lin_velocity(old_orientation) / time_step

        self.lin_p = (self.lin_position(new_orientation) + self.lin_position(old_orientation)) / 2 + self.clearance
        self.lin_v = avg_vel
        self.lin_a = avg_accel
        print(lin_a)
        self.crank_orientation = new_orientation


