from math import pi

from numpy import sin, cos

# Params from a Huyabusa

total_displacement = 1340 # cc
num_cylinders = 4
disp_per_cylinder = total_displacement / num_cylinders # cubic centimeters

piston_orientation = [0, 2 * pi / 3, 4 * pi / 3]

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