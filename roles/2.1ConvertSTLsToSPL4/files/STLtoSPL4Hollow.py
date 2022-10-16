
## Command to make the file run ##
#
# python3 convertStlsToSpl4.py -- Hollow                         (or other)
#
## ARGV ##
#ARGV[0] - TYPE Hollow / Bounded / Hyperloop / Klein
#

#Import regular modules needed
#import math
import os
import re
import sys
#from math import sin, cos

#
## Values that could change ##
# save/load .stl files to/from
stlDirectory = '../processFiles/3-OBJintoSTL'
# save/load custom .spl4 files to/from
spl4Directory = '../processFiles/4-STLintoSPL4'


# Get the arguments and save as strings
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
##print(argv)

# default w-axis increment by frame
wAxisInc = float(argv[1])

######## Convert STL to SPL4 ##########

#For a STL animation of N frames with M triangles, the SPL4 will contain M(N-1) prisms
#The first frame will start with a waxis value of 0, then each frame will be incremented by wAxisInc
# The Prisms are of the form:
#Triangle1 Vertex1, Triangle1 Vertex2, Triangle1 Vertex3, Triangle2 Vertex1, Triangle2 Vertex2, Triangle2 Vertex3, 

######## CURRENTLY WORKING - HOLLOW just converts each STL into prisms between them.
# For each subdirectory with stl frames, then for each frame create a new .spl4 object
subdir=argv[0]
spl4 = open(spl4Directory+'/'+subdir+'_HP_w-'+str(argv[1])+'.spl4', 'w+')
depth=0
stlFrames = sorted(os.listdir(os.path.join(stlDirectory, subdir)))
#Gets the first frame to pass to stl1 to start the process
stl2 = open(stlDirectory+'/'+subdir+'/'+stlFrames[0], 'r').readlines()
for i in range(len(stlFrames)-1):
    ##print(i)
    #Set the "front" stl to be the "end" stl of the last time, and moves the "end" one frame forwards
    stl1 = stl2
    stl2 = open(stlDirectory+'/'+subdir+'/'+stlFrames[i+1], 'r').readlines()
    for j in range(len(stl1)):
        #For each line in the "front" stl, it finds a triangle by searching for "outer loop" and transforms it into a prism.
        # This is a prism (3d shape) which is rotated into 4D (same as a triangle (2D) shape in an STL (3d format))
        # Even so, technically this can create a poorly defined shape, specificaly when one of the points of a triangle moves directly through the line between the two remaining points between frames.
        if re.search("outer loop", stl1[j]):
            spl4.write("prism start\n")
            # w-dimensional "depth" is calculated by the wAxisInc var
            spl4.write(stl1[j+1][:-1]+' '+str(depth*wAxisInc)+'\n')
            spl4.write(stl1[j+2][:-1]+' '+str(depth*wAxisInc)+'\n')
            spl4.write(stl1[j+3][:-1]+' '+str(depth*wAxisInc)+'\n')
            spl4.write(stl2[j+1][:-1]+' '+str((depth+1)*wAxisInc)+'\n')
            spl4.write(stl2[j+2][:-1]+' '+str((depth+1)*wAxisInc)+'\n')
            spl4.write(stl2[j+3][:-1]+' '+str((depth+1)*wAxisInc)+'\n')
    depth = (depth+1)

