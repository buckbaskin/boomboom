from math import pi

from numpy import sin, cos

total_displacement = 1600 # cc
num_cylinders = 3
disp_per_cylinder = total_displacement / num_cylinders

piston_orientation = [0, 2 * pi / 3, 4 * pi / 3]

bore_to_stroke = 1.2

bore = (4 * bore_to_stroke * disp_per_cylinder / pi)**(1/3)
stroke = (4 * disp_per_cylinder / (pi * bore_to_stroke**2))**(1/3)

cylinder_radius = bore / 2

crank_radius = stroke / 2

crank_ratio = 0.25

connecting_rod_len = crank_radius / crank_ratio 

compression_ratio = 10

combustion_chamber_volume = disp_per_cylinder / (compression_ratio - 1)