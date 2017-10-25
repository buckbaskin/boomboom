import numpy as np
import scipy.signal as signal
import tables

print('load pyplot')

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

print('done loading pyplot')

# from intake
# def save(self):
#     angle = np.array(self.cam_profile['cam_position'][1:])[:,1]
#     lift = np.array(self.cam_profile['cam_lift'][1:])[:,1]
#     with tables.open_file('cam.tbl', 'w') as h5_file:
#         h5_file.create_array('/', 'cam_angle', angle)
#         h5_file.create_array('/', 'cam_lift', lift)

def save(file_, name, data):
    with tables.open_file(file_, 'w') as h5_file:
        h5_file.create_array('/', 'cam_recording', data)

def load(file_, name):
    with tables.open_file(file_, 'r') as h5_file:
        data = getattr(h5_file.root, name).read()
        return data

def smooth_lift(ideal_cam_lift):
    win = signal.hann(50)
    filtered = signal.convolve(
            ideal_cam_lift,
            win,
            mode='same',
        ) / np.sum(win)
    return filtered

def fft_lift(ideal_cam_lift):
    return ideal_cam_lift

def plot_S(angle, lift):
    plt.xlabel('Camshaft angle, first piston (radians)')
    plt.ylabel('Camshaft lift (cm)')
    
    plt.plot(angle, lift)
    plt.plot(cam_angle, fft_lift(lift))
    plt.plot(angle, smooth_lift(lift))
    
    plt.show()

def numerical_vel(lift):
    # TODO(buckbaskin)
    return lift

def plot_V(angle, lift):
    plt.xlabel('Camshaft angle, first piston (radians)')
    plt.ylabel('Camshaft vel (cm / sec)')
    
    plt.plot(angle, numerical_vel(lift))
    plt.plot(cam_angle, numerical_vel(fft_lift(lift)))
    plt.plot(angle, numerical_vel(smooth_lift(lift)))
    
    plt.show()

def numerical_accel(lift):
    # TODO(buckbaskin)
    return lift

def plot_A(angle, lift):
    plt.xlabel('Camshaft angle, first piston (radians)')
    plt.ylabel('Camshaft accel (cm / sec**2)')
    
    plt.plot(angle, numerical_accel(lift))
    plt.plot(cam_angle, numerical_accel(fft_lift(lift)))
    plt.plot(angle, numerical_accel(smooth_lift(lift)))
    
    plt.show()

if __name__ == '__main__':
    # note: working on this for one cam lobe at a time
    cam_angle = load('cam.tbl', 'cam_angle')[:,1]
    ideal_cam_lift = load('cam.tbl', 'cam_lift')[:,1]

    