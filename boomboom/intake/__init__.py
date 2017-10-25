import numpy as np

from engine_parameters import *
from boomboom import AbstractModel

print('load pyplot')

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

class IntakeValveRecorderModel(AbstractModel):
    def __init__(self, cam_orientation):
        self.cam_orientation = np.array(cam_orientation)
        self.cam_profile = {
            'cam_position': [self.cam_orientation],
            'cam_lift': [np.zeros(self.cam_orientation.shape)],
        }
        self.intake_pressure = input_pressure
        self.intake_temp = input_temp

    def request_airflow(self, requested_kg, time_step):
        max_airflow_area = max_valve_lift * pi * intake_valve_diameter * num_intake_valves
        max_airflow_volume_cm = max_airflow_area * speed_of_sound
        density = self.intake_pressure / (R * self.intake_temp)
        max_airflow_volume_m = max_airflow_volume_cm / (100**3)
        max_airflow_mass = max_airflow_volume_m * density

        last_af_area = self.cam_profile['cam_lift'][-1] * pi * intake_valve_diameter * num_intake_valves
        last_af_volume_cm = last_af_area * speed_of_sound
        density = self.intake_pressure / (R * self.intake_temp)
        last_af_volume_m = last_af_volume_cm / (100**3)
        last_af_mass = last_af_volume_m * density

        trap_max_mass = (max_airflow_mass + last_af_mass) / 2

        print('requested kg %s vs max_mass %s' % (requested_kg, trap_max_mass,))

        return np.minimum(requested_kg, trap_max_mass)

    def step(self, crank_step, time_step, airflow_mass):
        cam_step = crank_step / 2.0
        old_orientation = self.cam_orientation
        new_orientation = self.cam_orientation + cam_step

        density = self.intake_pressure / (R * self.intake_temp)
        airflow_volume_m = airflow_mass / density
        airflow_volume_cm = airflow_volume_m * (100**3)
        curtain_area = airflow_volume_cm / (speed_of_sound * num_intake_valves)

        simulated_avg_lift = curtain_area / (pi * intake_valve_diameter)

        last_lift = self.cam_profile['cam_lift'][-1]
        next_lift = 2 * simulated_avg_lift - last_lift
        next_lift = np.maximum(next_lift, np.zeros(next_lift.shape))

        print('last %.2f > sim %.2f > next %.2f' % (last_lift[1], simulated_avg_lift[1], next_lift[1],))

        self.cam_orientation = new_orientation
        self.cam_profile['cam_position'].append(new_orientation)
        self.cam_profile['cam_lift'].append(next_lift)

    def plot(self):
        angle = np.array(self.cam_profile['cam_position'][1:])[:,1]
        lift = np.array(self.cam_profile['cam_lift'][1:])[:,1]
        print(angle)

        plt.xlabel('Camshaft angle, first piston (radians)')
        plt.ylabel('Camshaft lift (cm)')
        # plt.plot(lift)
        plt.plot(angle, lift)
        print('Plot Intake Cam Lift')
        plt.show()
