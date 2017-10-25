import numpy as np
import scipy.signal as signal
import tables

from engine_parameters import *

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

def smooth_lift(ideal_cam_lift, limit=100):
    win = signal.hann(100)
    filtered = signal.convolve(
            ideal_cam_lift,
            win,
            mode='same',
        ) / np.sum(win)
    return filtered

def fft_lift(ideal_cam_lift, limit=200):
    fft_ = np.fft.fft(ideal_cam_lift)
    fft_[int(limit):] = 0.0
    return np.fft.ifft(fft_)

def plot_S(angle, lift, projection='polar'):
    ax = plt.subplot(111, projection=projection)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.plot(angle, lift + cam_base_radius, 'r')
    ax.plot(angle, fft_lift(lift, 200) + cam_base_radius, 'g')
    ax.plot(angle, smooth_lift(lift, 100) + cam_base_radius, 'b')

    ax.set_rmax(max_valve_lift + cam_base_radius)
    ax.set_rmin(0.0)

    ax.set_rticks([0.5 * max_valve_lift, max_valve_lift])  # less radial ticks
    ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
    ax.grid(True)

    plt.show()

def plot_FFT(angle, lift, projection='polar'):
    ax = plt.subplot(111, projection=projection)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.plot(angle, lift + cam_base_radius, 'r')

    offset = 1

    ax.plot(angle, fft_lift(lift, 16+offset) + cam_base_radius, 'g')
    ax.plot(angle, fft_lift(lift, 8+offset) + cam_base_radius, 'b')
    ax.plot(angle, fft_lift(lift, 4+offset) + cam_base_radius, 'xkcd:sky blue')
    ax.plot(angle, fft_lift(lift, 2+offset) + cam_base_radius, 'xkcd:beige')

    ax.set_rmax(max_valve_lift + cam_base_radius)
    ax.set_rmin(0.0)

    ax.set_rticks([0.5 * max_valve_lift, max_valve_lift])  # less radial ticks
    ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
    ax.grid(True)

    plt.show()

def numerical_vel(angle, lift):
    x = angle
    y = lift
    dy = np.zeros(y.shape,np.float)
    dy[0:-1] = np.diff(y)/np.diff(x)
    dy[-1] = (y[-1] - y[-2])/(x[-1] - x[-2])
    return dy

def plot_V(angle, lift, projection='polar'):
    ax = plt.subplot(111, projection=projection)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.plot(angle, numerical_vel(angle, lift), 'r')
    ax.plot(angle, numerical_vel(fft_lift(lift)), 'g')
    ax.plot(angle, numerical_vel(smooth_lift(lift)), 'b')

    # ax.set_rmax(max_valve_lift)
    ax.set_rmin(min_valve_lift)

    ax.set_rticks([0.5 * max_valve_lift, max_valve_lift])  # less radial ticks
    ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
    ax.grid(True)

    plt.show()

def numerical_accel(angle, lift):
    x = angle
    y = numerical_vel(angle, lift)
    dy = np.zeros(y.shape,np.float)
    dy[0:-1] = np.diff(y)/np.diff(x)
    dy[-1] = (y[-1] - y[-2])/(x[-1] - x[-2])
    return dy

def plot_A(angle, lift, projection='polar'):
    ax = plt.subplot(111, projection=projection)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.plot(angle, numerical_accel(angle, lift), 'r')
    ax.plot(angle, numerical_accel(fft_lift(lift)), 'g')
    ax.plot(angle, numerical_accel(smooth_lift(lift)), 'b')

    # ax.set_rmax(max_valve_lift)
    ax.set_rmin(0.0)

    ax.set_rticks([0.5 * max_valve_lift, max_valve_lift])  # less radial ticks
    ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
    ax.grid(True)

    plt.show()

def numerical_jerk(angle, lift):
    x = angle
    y = numerical_accel(angle, lift)
    
    dy = np.zeros(y.shape,np.float)
    dy[0:-1] = np.diff(y)/np.diff(x)
    dy[-1] = (y[-1] - y[-2])/(x[-1] - x[-2])

    return dy

def plot_SVA(angle, lift, projection='polar'):
    ax = plt.subplot(111, projection=projection)
    ax.plot(angle, lift, 'r')
    ax.plot(angle, numerical_vel(angle, lift), 'g')
    ax.plot(angle, numerical_accel(angle, lift), 'b')
    # ax.plot(angle, numerical_jerk(angle, lift), 'xkcd:sky blue')
    
    if projection == 'polar':
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
    
        ax.set_rmax(cam_base_radius + max_valve_lift * 2)
        ax.set_rmin(min_valve_lift)

        ax.set_rticks([
            cam_base_radius,
            0.5 * max_valve_lift + cam_base_radius,
            max_valve_lift + cam_base_radius])  # less radial ticks
        ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
        ax.grid(True)

    else:
        ax.set_xlabel('Cam rotation (radians)')
        ax.set_ylim([-20, 20])
        ax.set_ylabel('SVA (cm, cm/sec, cm/sec**2)')
    ax.set_title('SVA Diagram')

    plt.show()

def plot_SVAJ(angle, lift, projection='polar'):
    ax = plt.subplot(111, projection=projection)
    ax.plot(angle, lift, 'r')
    ax.plot(angle, numerical_vel(angle, lift), 'g')
    ax.plot(angle, numerical_accel(angle, lift), 'b')
    ax.plot(angle, numerical_jerk(angle, lift), 'xkcd:sky blue')
    
    if projection == 'polar':
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
    
        ax.set_rmax(max_valve_lift * 1.2)
        ax.set_rmin(min_valve_lift)

        ax.set_rticks([0.5 * max_valve_lift, max_valve_lift])  # less radial ticks
        ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
        ax.grid(True)

    else:
        ax.set_xlabel('Cam rotation (radians)')
        ax.set_ylim([-20, 20])
        ax.set_ylabel('SVAJ (cm, cm/sec, cm/sec**2, cm/sec**3)')
    ax.set_title('SVAJ Diagram')

    plt.show()

def fit_dwell_curve(angle, lift):
    # TODO(buckbaskin):
    return lift

if __name__ == '__main__':
    # note: working on this for one cam lobe at a time
    cam_angle = load('cam.tbl', 'cam_angle')[:,1]
    ideal_cam_lift = load('cam.tbl', 'cam_lift')[:,1]

    # plot_FFT(cam_angle, ideal_cam_lift)
    plot_SVA(
        cam_angle,
        smooth_lift(ideal_cam_lift + cam_base_radius, 400),
        None)