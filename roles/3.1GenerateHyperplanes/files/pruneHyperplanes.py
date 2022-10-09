
# ~~~~~~~~~~~~~~~~~~~~~~~USAGE~~~~~~~~~~~~~~~~~~~~~~~~
# Be passed a list of four floats
# These floats correspond to the components of a hyperplane.
# Hyperplanes are of the form ax+by+cz+dw+e=0
# e is set in the rotatespacetime.py part of the script since it corresponds to time in our current hyperplane
# The values correspond to a, b, c, d
# So the normal hyperplane which humans use would be 0, 0, 0, 1     (when stationary)

# Import basic modules
import math
import os
import sys

## Values that could change ##
# Directory that raw and normalized hyperplanes are stored inside
hyperplaneDirectory = '../processFiles/5-Hyperplanes'

# Get the arguments and save as strings
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
print(argv)

######### Correct any hyperplanes which become singularities in my method (could also be done by using a seperate set of equations in those cases, but think its no big deal)
print("Correct Hyperplanes")
# For each hyperplane

a = float(argv[1])
b = float(argv[2])
c = float(argv[3])
d = float(argv[4])

#To prevent division by zero in my technique some things must be true
# We could instead of this do 'If this case use alternate method' but instead I fudge the numbers to get a non-exception
if(c==0):
    c=0.0001
if(((a**2)+2*(b**2)+(d**2))==0):
    a=a*1.0001
if((d*(a+d)+c**2)==0):
    c=c*1.0001


#This part just saves the fudged numbers for the future
parts=[a,b,c,d]

nFile = open(hyperplaneDirectory+'/'+argv[0], 'w+')

for part in parts:
    print(f'{part:f}')
    nFile.write(str(f'{part:f}')+' ')

nFile.close()

