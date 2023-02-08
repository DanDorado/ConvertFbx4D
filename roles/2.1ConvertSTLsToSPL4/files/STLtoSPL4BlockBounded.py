
## Command to make the file run ##
#
# python3 convertStlsToSpl4.py -- Hollow                         (or other)
#
## ARGV ##
#ARGV[0] - TYPE Hollow / Bounded / Hyperloop / Klein
#

# Example of installing modules in correct place
# pip install --target=../packages/vtk vtk
import sys
sys.path.append("/home/dandorado/blender/ansible/packages/pyvista")
sys.path.append("/home/dandorado/blender/ansible/packages/appdirs")
sys.path.append("/home/dandorado/blender/ansible/packages/vtk")
sys.path.append("/home/dandorado/blender/ansible/packages/scooby")
# Import prerequesites for the Moeller-Trumbore Algorithm
import pyvista as pv

#Import regular modules needed
import math
import os
import re
import sys
from math import sin, cos

# Importing prerequisites for Delaney cellization
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt



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
spl4 = open(spl4Directory+'/'+subdir+'/'+subdir+'_BBP_w-'+str(argv[1])+'.spl4', 'w+')
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
    if (i==0) or (i==(len(stlFrames)-2)):
        # If the first frame cap the first frame being linked by prisms.
        if (i==0):
            stlToCheck=stl1
            depthAmount=depth
        # If the second frame cap the second frame being linked.
        if (i==(len(stlFrames)-2)):
            stlToCheck=stl2
            depthAmount=depth+1
        #print("I'm'a start "+str(i))
        # For this frame set the points and triangles array to zero.
        points=[]
        triangles=[]
        for k in range(len(stlToCheck)):
            # Grab the points in one array ( to be used by Delaney into tetrahedrons)
            # Grab the triangles into another to be used by the raycasting algorythm to check if the Delaney tetrahedrons are isndie/outside
            if re.search("outer loop", stlToCheck[k]):
                individualTriangle=[]
                line=(stlToCheck[k+1][:-1].split())
                del line[0]
                ##print(line)
                points.append(line)
                individualTriangle.append(line)
                line=(stlToCheck[k+2][:-1].split())
                del line[0]
                ##print(line)
                points.append(line)
                individualTriangle.append(line)
                line=(stlToCheck[k+3][:-1].split())
                del line[0]
                points.append(line)
                individualTriangle.append(line)
                triangles.append(individualTriangle)
                points.append(line)
        # Get Delaney tetrahedrons, they will already be good for convex shapes, but need to be culled if convex (cost intensive)
        # TODO allow convex shapes to not call the rest
        tetras = Delaunay(points)
        ##print(points)
        numberOfTetras=len(tetras.simplices)
        #print("Length "+str(numberOfTetras))
        numberOfTetrasProcessed=0
        # For each tetrahedron check it for inside or outside, you'll need to check each triangle:
        for tetra in tetras.simplices:
                spl4.write("tetrahedron start\n")
                for vertex in range(len(tetra)):
                    spl4.write("vertex  "+str(points[tetra[vertex]][0])+" "+str(points[tetra[vertex]][1])+" "+str(points[tetra[vertex]][2])+" "+str((depthAmount)*wAxisInc)+'\n')
            #print("\n")
    depth = (depth+1)
