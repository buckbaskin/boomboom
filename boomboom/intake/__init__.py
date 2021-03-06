import numpy as np

from engine_parameters import *
from boomboom import AbstractModel

print('load pyplot')

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

print('done loading pyplot')
print('loading pytables')

import tables


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
        # TODO(buckbaskin): redo max as compressible air calculations
        max_airflow_area = max_valve_lift * pi * intake_valve_diameter * num_intake_valves
        max_airflow_volume_cm = max_airflow_area * speed_of_sound
        density = self.intake_pressure / (R * self.intake_temp)
        max_airflow_volume_m = max_airflow_volume_cm / (100**3)
        max_airflow_mass = max_airflow_volume_m * density

        # TODO(buckbaskin): redo max as compressible air calculations
        last_af_area = self.cam_profile['cam_lift'][-1] * pi * intake_valve_diameter * num_intake_valves
        last_af_volume_cm = last_af_area * speed_of_sound
        density = self.intake_pressure / (R * self.intake_temp)
        last_af_volume_m = last_af_volume_cm / (100**3)
        last_af_mass = last_af_volume_m * density

        trap_max_mass = (max_airflow_mass + last_af_mass) / 2

        return np.minimum(requested_kg, trap_max_mass)

    def step(self, crank_step, time_step, airflow_mass):
        cam_step = crank_step / 2.0
        old_orientation = self.cam_orientation
        new_orientation = self.cam_orientation + cam_step

        # TODO(buckbaskin): redo max as compressible air calculations
        density = self.intake_pressure / (R * self.intake_temp)
        airflow_volume_m = airflow_mass / density
        airflow_volume_cm = airflow_volume_m * (100**3)
        curtain_area = airflow_volume_cm / (speed_of_sound * num_intake_valves)

        simulated_avg_lift = curtain_area / (pi * intake_valve_diameter)

        last_lift = self.cam_profile['cam_lift'][-1]
        next_lift = 2 * simulated_avg_lift - last_lift

        # Acceleration limits
        use_acceleration_limits = False

        if len(self.cam_profile['cam_lift']) >= 2:
            early_lift = self.cam_profile['cam_lift'][-2]
        else:
            early_lift = 0.0
        incoming_cam_vel = (last_lift - early_lift) / time_step
        next_cam_vel = (next_lift - last_lift) / time_step
        accel = (next_cam_vel - incoming_cam_vel) / time_step
        # positive acceleration (force/pressure angle) limits
        accel = np.minimum(accel, np.ones(accel.shape) * max_valve_accel)    
        # negative acceleration (spring/force/pressure angle) limits
        accel = np.maximum(accel, np.ones(accel.shape) * min_valve_accel)
        
        if use_acceleration_limits:
            # rewrite cam velocity and new positions
            next_cam_vel = (accel * time_step) + incoming_cam_vel
            next_lift = (next_cam_vel * time_step) + last_lift
        
        # Valve limits based on maximum/minimum position limits
        next_lift = np.maximum(next_lift, np.ones(next_lift.shape) * min_valve_lift)
        next_lift = np.minimum(next_lift, np.ones(next_lift.shape) * max_valve_lift)
        
        # TODO(buckbaskin): limit maximum required torque from lift pressure angle

        self.cam_orientation = new_orientation
        self.cam_profile['cam_position'].append(new_orientation)
        self.cam_profile['cam_lift'].append(next_lift)

    def plot(self):
        angle = np.array(self.cam_profile['cam_position'][1:])[:,1]
        lift = np.array(self.cam_profile['cam_lift'][1:])[:,1]
        
        plt.xlabel('Camshaft angle, first piston (radians)')
        plt.ylabel('Camshaft lift (cm)')
        # plt.plot(lift)
        plt.plot(angle, lift)
        print('Plot Intake Cam Lift')
        plt.show()

    def save(self):
        angle = np.array(self.cam_profile['cam_position'])
        lift = np.array(self.cam_profile['cam_lift'])
        with tables.open_file('cam.tbl', 'w') as h5_file:
            h5_file.create_array('/', 'cam_angle', angle)
            h5_file.create_array('/', 'cam_lift', lift)
