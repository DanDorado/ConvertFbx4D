import math
import sys

argv = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"
hyperplane_file = str(argv[0])

# Read the hyperplane from the input file
with open(hyperplane_file, 'r') as f:
    a, b, c, d = map(float, f.readline().split())

# Calculate the values for normalizing the original hyperplane and each axis
o_plane = [a/math.sqrt(a**2 + b**2 + c**2 + d**2), b/math.sqrt(a**2 + b**2 + c**2 + d**2), c/math.sqrt(a**2 + b**2 + c**2 + d**2), d/math.sqrt(a**2 + b**2 + c**2 + d**2)]
x_axis = [1/math.sqrt(1 + (Cx**2) + (Dx**2)), 0, (-a-d)/(c * math.sqrt(1 + (Cx**2) + (Dx**2))), 1/math.sqrt(1 + (Cx**2) + (Dx**2))]
y_axis = [(-a*b)/math.sqrt((a**2)+(b**2)+(c**2)+(d**2)), math.sqrt((a**2)+(b**2)+(c**2)+(d**2)), (-c*b)/math.sqrt((a**2)+(b**2)+(c**2)+(d**2)), (-d*b)/math.sqrt((a**2)+(b**2)+(c**2)+(d**2))]
z_axis = [1/math.sqrt(1 + (Cz**2) + (Dz**2)), 0, c*(d-a)/((d*(a+d))+(c**2) * math.sqrt(1 + (Cz**2) + (Dz**2))), -(a*d)-(a**2)-(c**2)/((d*(a+d))+(c**2) * math.sqrt(1 + (Cz**2) + (Dz**2)))]

# Write the calculated values to the input file
with open(hyperplane_file, 'w') as f:
    for plane in [o_plane, x_axis, y_axis, z_axis]:
        f.write(' '.join(str(f'{part:f}') for part in plane))
        f.write("\n")