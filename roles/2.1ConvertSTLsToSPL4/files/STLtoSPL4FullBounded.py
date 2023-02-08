
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
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import the delaney module
from scipy.spatial import Delaunay



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

# Define the Moeller-Trumbore Algorithm

def ray_triangle_intersection(ray_start, ray_vec, triangle):
    """Moeller–Trumbore intersection algorithm.

    Parameters
    ----------
    ray_start : np.ndarray
        Length three numpy array representing start of point.

    ray_vec : np.ndarray
        Direction of the ray.

    triangle : np.ndarray
        ``3 x 3`` numpy array containing the three vertices of a
        triangle.

    Returns
    -------
    bool
        ``True`` when there is an intersection.

    tuple
        Length three tuple containing the distance ``t``, and the
        intersection in unit triangle ``u``, ``v`` coordinates.  When
        there is no intersection, these values will be:
        ``[np.nan, np.nan, np.nan]``

    """
    # define a null intersection
    null_inter = np.array([np.nan, np.nan, np.nan])

    # break down triangle into the individual points
    v1, v2, v3 = triangle
    eps = 0.000001

    # compute edges
    edge1 = v2 - v1
    edge2 = v3 - v1
    pvec = np.cross(ray_vec, edge2)
    det = edge1.dot(pvec)

    if abs(det) < eps:  # no intersection
        return False, null_inter
    inv_det = 1.0 / det
    tvec = ray_start - v1
    u = tvec.dot(pvec) * inv_det

    if u < 0.0 or u > 1.0:  # if not intersection
        return False, null_inter

    qvec = np.cross(tvec, edge1)
    v = ray_vec.dot(qvec) * inv_det
    if v < 0.0 or u + v > 1.0:  # if not intersection
        return False, null_inter

    t = edge2.dot(qvec) * inv_det
    if t < eps:
        return False, null_inter

    return True, np.array([t, u, v])


######## Convert STL to SPL4 ##########

#For a STL animation of N frames with M triangles, the SPL4 will contain M(N-1) prisms
#The first frame will start with a waxis value of 0, then each frame will be incremented by wAxisInc
# The Prisms are of the form:
#Triangle1 Vertex1, Triangle1 Vertex2, Triangle1 Vertex3, Triangle2 Vertex1, Triangle2 Vertex2, Triangle2 Vertex3, 

######## CURRENTLY WORKING - HOLLOW just converts each STL into prisms between them.
# For each subdirectory with stl frames, then for each frame create a new .spl4 object
subdir=argv[0]
spl4 = open(spl4Directory+'/'+subdir+'/'+subdir+'_FBP_w-'+str(argv[1])+'.spl4', 'w+')
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
            numberOfTetrasProcessed = numberOfTetrasProcessed+1
            print(str(numberOfTetrasProcessed)+"/"+str(numberOfTetras)+"  ("+str(i)+")")
            #print("Tetrahedron by number")
            #print(tetra)
            #print("coords of each four vertex as x,y,z")
            #print(str(points[tetra[0]])+str(points[tetra[1]])+str(points[tetra[2]])+str(points[tetra[3]]))
            #print(str("coords of the centralpoint"))
            pX=((float(points[tetra[0]][0])+float(points[tetra[1]][0])+float(points[tetra[2]][0])+float(points[tetra[3]][0]))/4)
            #print(pX)
            pY=((float(points[tetra[0]][1])+float(points[tetra[1]][1])+float(points[tetra[2]][1])+float(points[tetra[3]][1]))/4)
            #print(pY)
            pZ=((float(points[tetra[0]][2])+float(points[tetra[1]][2])+float(points[tetra[2]][2])+float(points[tetra[3]][2]))/4)
            #print(pZ)
            # If numberOfCollisions ends as odd then tetrahedron was inside
            numberOfCollisions = 0
            # numberOfTriangles just used for display
            numberOfTriangles = 0
            # For each tetrahdron, for each triangle
            for triangleToConsider in triangles:
                numberOfTriangles = numberOfTriangles+1
                # Grab the points of the triangle
                #print(triangleToConsider)
                tAx=float(triangleToConsider[0][0])
                tAy=float(triangleToConsider[0][1])
                tAz=float(triangleToConsider[0][2])
                tBx=float(triangleToConsider[1][0])
                tBy=float(triangleToConsider[1][1])
                tBz=float(triangleToConsider[1][2])
                tCx=float(triangleToConsider[2][0])
                tCy=float(triangleToConsider[2][1])
                tCz=float(triangleToConsider[2][2])
                #print(tAx)
                #print(tAy)
                #print(tAz)
                #print(tBx)
                #print(tBy)
                #print(tBz)
                #print(tCx)
                #print(tCy)
                #print(tCz)
                #print("Against the points:")
                #print(pX)
                #print(pY)
                #print(pZ)

                # Create a basic triangle within pyvista
                triPoints = np.array([[tAx, tAy, tAz], [tBx, tBy, tBz], [tCx, tCy, tCz]])
                faces = np.array([3, 0, 1, 2])
                tri = pv.PolyData(triPoints, faces)

                # cast a ray in an arbitrary direction (1, 2, 3)
                start = np.array([pX, pY, pZ])
                direction = np.array([1, 2, 3])

                # compute if the intersection exists
                inter, tuv = ray_triangle_intersection(start, direction, triPoints)
                t, u, v = tuv

                if (inter):
                #    print('Intersected', inter)
                #    print('t:', t)
                #    print('u:', u)
                #    print('v:', v)
                    numberOfCollisions = numberOfCollisions + 1

            #print("Total Number of Triangles")
            #print(numberOfTriangles)
            #print("Total Number of Collisions")
            #print(numberOfCollisions)
            # If odd (remainder after divide by two) then write the tetrahedron, otherwise don't
            if ( numberOfCollisions % 2):
                print ("It was inside the shape because there were an odd number of collisions")
                spl4.write("tetrahedron start\n")
                print(tetra)
                for vertex in range(len(tetra)):
                    spl4.write("vertex  "+str(points[tetra[vertex]][0])+" "+str(points[tetra[vertex]][1])+" "+str(points[tetra[vertex]][2])+" "+str((depthAmount)*wAxisInc)+'\n')
            #print("\n")
    depth = (depth+1)
