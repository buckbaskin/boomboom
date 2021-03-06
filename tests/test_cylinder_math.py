from engine_parameters import *
from boomboom.cylinder import KinematicCylinderModel

if __name__ == '__main__' or True:
    kcm = KinematicCylinderModel([0.0])

    total_revs = 1
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

    print('check math')

    for i in range(0, num_steps):
        kcm.step(step_angle, step_time)

        angle.append(angle[-1] + step_angle)
        time.append(time[-1] + step_time)

        S.append(kcm.lin_s[0])
        Si.append(kcm.lin_position(angle[-1]))
        V.append(kcm.lin_v[0])
        Vi.append(kcm.lin_velocity(angle[-1], rad_per_sec))
        A.append(kcm.lin_a[0])
        Ai.append(kcm.lin_accel(angle[-1], rad_per_sec))
        
        # assert increasing time, angle
        assert angle[-2] < angle[-1]
        assert time[-2] < time[-1]

        # assert cycling position, velocity, angle
        # rev 1, downward swing
        if (1 < i < num_steps / 2):
            assert S[-2] < S[-1] # decreasing position
            assert Si[-2] < Si[-1]
            assert V[-1] < 0.0 # negative velocity
            assert Vi[-1] < 0.0
            if (1 < i < num_steps / 4):
                assert A[-1] < 0.0 # accel aligned with velocity
                assert Ai[-1] < 0.0
            else:
                assert A[-1] >= 0.0 # accel against with velocity
                assert Ai[-1] >= 0.0

        elif (1 * num_steps / 2 < i < 2 * num_steps / 2):
            assert S[-2] > S[-1]
            assert Si[-2] > Si[-1]
            assert V[-1] > 0.0
            assert Vi[-1] > 0.0
            if (num_steps / 4 < i < 2 * num_steps / 4):
                assert A[-1] > 0.0 # accel aligned with velocity
                assert Ai[-1] > 0.0
            else:
                assert A[-1] <= 0.0 # accel against with velocity
                assert Ai[-1] <= 0.0

        else:
            break

    print('done checking math')