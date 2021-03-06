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
        self.lin_s = self.lin_position(self.piston_orientation)
        self.lin_v = 0.0
        self.lin_a = 0.0

        # crank orientation in radians, with 0.0 = TDC for front piston
        self.allocate_intakev = np.vectorize(self.__allocate_intake, otypes=[np.float])
        self.allocate_exhaustv = np.vectorize(self.__allocate_exhaust, otypes=[np.float])

    def lin_position(self, crank_orientation):
        val = (crank_radius * (1 - cos(crank_orientation)) + 
            crank_ratio / 2 * crank_radius * sin(crank_orientation)**2)
        val += combustion_chamber_height
        return val

    def lin_velocity(self, crank_orientation, crank_vel):
        return (crank_vel*crank_radius*sin(crank_orientation) * 
            (1 + crank_ratio * cos(crank_orientation)))

    def lin_accel(self, crank_orientation, crank_vel):
        i = crank_vel**2 * crank_radius
        j = cos(crank_orientation)
        k = crank_ratio * cos(2 * crank_orientation)
        return i * (j + k)

    def step(self, crank_step, time_step, intake_airflow, exhaust_airflow):
        pass

    def request_airflow(self, crank_step, time_step):
        # TODO(buckbaskin): incorporate 4-stroke timing here
        # I could do:
        #  - given a cam timing, intake starts at the beginning of the rise on
        #    the intake cam (overlaps exhaust)
        #  - compression is the close of the intake cam to spark
        #  - burn is the spark until exhaust valve opens (overlaps exhaust)
        #  - exhaust is the exhaust value until it closes (overlaps intake)
        # But I don't have a cam yet. So, define each cycle and when it starts/
        #   stops. Then only send to intake/exhaust requests when in those cycles
        #   Track pressures and things.

        # Ideal filling and cylinder rotation
        rad_per_sec = crank_step / time_step
        old_orientation = self.piston_orientation
        new_orientation = self.piston_orientation + crank_step

        avg_vel = (self.lin_position(new_orientation) - self.lin_position(old_orientation)) / time_step
        lv1 = self.lin_velocity(new_orientation, rad_per_sec)
        lv2 = self.lin_velocity(old_orientation, rad_per_sec)
        avg_accel = (lv1 - lv2) / time_step
        i_accel = self.lin_accel(new_orientation, rad_per_sec)

        self.lin_s = (self.lin_position(new_orientation) + self.lin_position(old_orientation)) / 2
        self.lin_v = avg_vel
        self.lin_a = avg_accel
        self.piston_orientation = new_orientation

        dist_swept = self.lin_v * time_step
        vol_swept = (bore/2)**2 * pi * dist_swept

        # print(cycle_intake, cycle_exhaust)

        for index, oriented in enumerate(np.mod(new_orientation, (4*pi))):
            if not (cycle_intake[0] < oriented < cycle_intake[1]):
                # print('new orient %s' % (new_orientation,))
                # print('old val swept %s' % vol_swept)
                vol_swept[index] = min(0.0, vol_swept[index])
                # print('new vol swept %s' % vol_swept)
            if not (cycle_exhaust[0] < oriented < cycle_exhaust[1]):
                vol_swept[index] = max(0.0, vol_swept[index])

        return (self.allocate_intakev(vol_swept), self.allocate_exhaustv(vol_swept))

    def __allocate_intake(self, vol_swept):
        return max(0.0, vol_swept)

    def __allocate_exhaust(self, vol_swept):
        return -min(0.0, vol_swept)


