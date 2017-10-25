from math import pi

from numpy import sin, cos

### Cylinder ###

# Params from a Huyabusa

total_displacement = 1340 # cc
num_cylinders = 2
disp_per_cylinder = total_displacement / num_cylinders # cubic centimeters

piston_orientation = [0, 0, 0, 0]

cam_orientation = piston_orientation

bore_to_stroke = 81.0 / 65.0

bore = (4 * bore_to_stroke * disp_per_cylinder / pi)**(1/3) # centimeters
bore_mm = bore * 10
bore_in = bore_mm / 25.4
stroke = (4 * disp_per_cylinder / (pi * bore_to_stroke**2))**(1/3) # centimeters
stroke_mm = stroke * 10
stroke_in = stroke_mm / 25.4

print('Engine bore %.1f mm (%.2f in)\nEngine stroke %.1f mm (%.2f in)' % (bore_mm, bore_in, stroke_mm, stroke_in,))

cylinder_radius = bore / 2 # centimeters

crank_radius = stroke / 2 # centimeters

crank_ratio = 0.25

connecting_rod_len = crank_radius / crank_ratio # centimeters

compression_ratio = 12.5

combustion_chamber_volume = disp_per_cylinder / (compression_ratio - 1)

combustion_chamber_height = combustion_chamber_volume / (pi * (bore / 2)**2)

### Valves ###

cam_base_diameter = 2.54 # cm
cam_base_radius = cam_base_diameter / 2
max_valve_lift = 2.0 # cm
min_valve_lift = 0.0 # cm
max_valve_vel = None
min_valve_vel = None
max_valve_accel =  99000 # cm / sec**2
min_valve_accel = -90001 # cm / sec**2

intake_valve_diameter = 2.54 # cm
num_intake_valves = 2
exhaust_valve_diameter = 2.54 * 0.8 # cm
num_exhaust_valves = 2

### Intake ###

specific_gas_constant_for_dry_air = 287.05 # J / (kg K)
R = specific_gas_constant_for_dry_air

speed_of_sound = 34300 # cm/sec

kpa_per_atm = 101.325024
input_pressure = 101.325024 # kilopascals

input_temp = 290 # Kelvin, about 60 F