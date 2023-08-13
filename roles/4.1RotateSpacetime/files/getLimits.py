
## Command to make the file run ##
#
# python3 rotatespacetime.py -- 1
#
## ARGV ##
#ARGV[0] - Generate a single frame or a sequence of frames:
# 0=SINGLE FRAME with 'constant' being taken as e
# 1=FULL FRAMES outputting n frames where n is 'frames' constant. This splits the spl4 shape into n segments out outputs frames from the centre of each.
# 2=FULL FPS outputting a number of frames where the constant is set to the lowest possible (rounded up slightly) and then incremented by 'increment'

import math
import os
import re
import sys

## Values that could change ##
# Directory that raw and normalized hyperplanes are stored inside
spl4Directory = '../processFiles/4-STLintoSPL4'
RotatedSTLPath = '../processFiles/6-RotatedSTLFrames'




# Get the arguments and save as strings
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
#print(argv)

#Render various shapes (normally should all be set to true unless debugging)
renderPrisms=True
renderTetrahedrons=True


#########Gets all the necessary details for rotating different parts of the spl4
#print("Begin the conversion")
# These tables return lists of triangles depending on 0/1 inputs they are given denoting vertexes of a prism or tetrahedron above/below the current timelike hyperplane.
# N.B since each intersection is effectively an inversion of itself as far as the intersecting slice is concerned, we only need to pass n-1 above/below values, where n is the number of vertices of the shape.
# Each entry (except the entry set where all vertices are above/below, which in theory we should never call anyway) returns a list of one or more triangles
# The "triangles" are really just a list of three lines each between two vertices e.g. [3,5], which means a vertex of that triangle is sitting on the line between vertex 3 and vertex 5 of the prism.
intersectTriangleTable=[[[[[[[[[3,5],[4,5],[2,5]]]],[[[[1,4],[2,5],[3,5]],[[3,4],[2,5],[3,5]],[[3,4],[1,4],[3,5]],[[3,4],[1,4],[2,5]]]]],[[[[[0,3],[2,5],[4,5]],[[3,4],[2,5],[4,5]],[[3,4],[0,3],[4,5]],[[3,4],[0,3],[2,5]]]],[[[[0,3],[1,4],[2,5]]]]]],[[[[[[1,2],[4,5],[3,5]],[[0,2],[4,5],[3,5]],[[0,2],[1,2],[3,5]],[[0,2],[1,2],[4,5]]]],[[[[1,4],[3,4],[3,5]],[[1,2],[3,4],[3,5]],[[1,2],[1,4],[3,5]],[[1,2],[1,4],[3,4]],[[0,2],[3,4],[3,5]],[[0,2],[1,4],[3,5]],[[0,2],[1,4],[3,4]],[[0,2],[1,2],[3,5]],[[0,2],[1,2],[3,4]],[[0,2],[1,2],[1,4]]]]],[[[[[0,3],[3,4],[4,5]],[[0,2],[3,4],[4,5]],[[0,2],[0,3],[4,5]],[[0,2],[0,3],[3,4]],[[1,2],[3,4],[4,5]],[[1,2],[0,3],[4,5]],[[1,2],[0,3],[3,4]],[[1,2],[0,2],[4,5]],[[1,2],[0,2],[3,4]],[[1,2],[0,2],[0,3]]]],[[[[0,3],[1,4],[1,2]],[[0,2],[1,4],[1,2]],[[0,2],[0,3],[1,2]],[[0,2],[0,3],[1,4]]]]]]],[[[[[[[1,2],[0,1],[1,4]],[[3,5],[4,5],[2,5]]]],[[[[2,5],[3,5],[3,4]],[[1,2],[3,5],[3,4]],[[1,2],[2,5],[3,4]],[[1,2],[2,5],[3,5]],[[0,1],[3,5],[3,4]],[[0,1],[2,5],[3,4]],[[0,1],[2,5],[3,5]],[[0,1],[1,2],[3,4]],[[0,1],[1,2],[3,5]],[[0,1],[1,2],[2,5]]]]],[[[[[1,2],[0,1],[1,4]],[[0,3],[2,5],[1,2]],[[0,1],[2,5],[1,2]],[[0,1],[0,3],[1,2]],[[0,1],[0,3],[2,5]],[[3,4],[4,5],[1,4]],[[0,3],[2,5],[4,5]],[[3,4],[2,5],[4,5]],[[3,4],[0,3],[4,5]],[[3,4],[0,3],[2,5]]]],[[[[0,3],[2,5],[1,2]],[[0,1],[2,5],[1,2]],[[0,1],[0,3],[1,2]],[[0,1],[0,3],[2,5]]]]]],[[[[[[1,4],[4,5],[3,5]],[[0,1],[4,5],[3,5]],[[0,1],[1,4],[3,5]],[[0,1],[1,4],[4,5]],[[0,2],[4,5],[3,5]],[[0,2],[1,4],[3,5]],[[0,2],[1,4],[4,5]],[[0,2],[0,1],[3,5]],[[0,2],[0,1],[4,5]],[[0,2],[0,1],[1,4]]]],[[[[0,2],[3,5],[3,4]],[[0,1],[3,5],[3,4]],[[0,1],[0,2],[3,4]],[[0,1],[0,2],[3,5]]]]],[[[[[0,1],[0,2],[0,3]],[[3,4],[4,5],[1,4]]]],[[[[0,1],[0,2],[0,3]]]]]]]],[[[[[[[[0,1],[0,2],[0,3]],[[3,5],[4,5],[2,5]]]],[[[[0,1],[0,2],[0,3]],[[1,4],[2,5],[0,2]],[[0,1],[2,5],[0,2]],[[0,1],[1,4],[0,2]],[[0,1],[1,4],[2,5]],[[3,4],[3,5],[0,3]],[[1,4],[2,5],[3,5]],[[3,4],[2,5],[3,5]],[[3,4],[1,4],[3,5]],[[3,4],[1,4],[2,5]]]]],[[[[[2,5],[4,5],[3,4]],[[0,2],[4,5],[3,4]],[[0,2],[2,5],[3,4]],[[0,2],[2,5],[4,5]],[[0,1],[4,5],[3,4]],[[0,1],[2,5],[3,4]],[[0,1],[2,5],[4,5]],[[0,1],[0,2],[3,4]],[[0,1],[0,2],[4,5]],[[0,1],[0,2],[2,5]]]],[[[[1,4],[2,5],[0,2]],[[0,1],[2,5],[0,2]],[[0,1],[1,4],[0,2]],[[0,1],[1,4],[2,5]]]]]],[[[[[[0,3],[3,5],[4,5]],[[0,1],[3,5],[4,5]],[[0,1],[0,3],[4,5]],[[0,1],[0,3],[3,5]],[[1,2],[3,5],[4,5]],[[1,2],[0,3],[4,5]],[[1,2],[0,3],[3,5]],[[1,2],[0,1],[4,5]],[[1,2],[0,1],[3,5]],[[1,2],[0,1],[0,3]]]],[[[[1,2],[0,1],[1,4]],[[3,4],[3,5],[0,3]]]]],[[[[[0,1],[3,4],[4,5]],[[1,2],[3,4],[4,5]],[[1,2],[0,1],[4,5]],[[1,2],[0,1],[3,4]]]],[[[[1,2],[0,1],[1,4]]]]]]],[[[[[[[0,2],[1,2],[2,5]],[[0,3],[1,4],[1,2]],[[0,2],[1,4],[1,2]],[[0,2],[0,3],[1,2]],[[0,2],[0,3],[1,4]],[[3,5],[4,5],[2,5]],[[4,5],[0,3],[1,4]],[[3,5],[0,3],[1,4]],[[3,5],[4,5],[1,4]],[[3,5],[4,5],[0,3]]]],[[[[0,2],[1,2],[2,5]],[[3,4],[3,5],[0,3]]]]],[[[[[0,2],[1,2],[2,5]],[[3,4],[4,5],[1,4]]]],[[[[0,2],[1,2],[2,5]]]]]],[[[[[[4,5],[0,3],[1,4]],[[3,5],[0,3],[1,4]],[[3,5],[4,5],[1,4]],[[3,5],[4,5],[0,3]]]],[[[[3,4],[3,5],[0,3]]]]],[[[[[3,4],[4,5],[1,4]]]],[[]]]]]]]
intersectTetrahedronTable=[[[[[[[0,3],[1,3],[2,3]]]],[[[[0,2],[0,3],[1,3]],[[0,2],[1,3],[1,2]]]]],[[[[[0,1],[0,3],[2,3]],[[0,1],[1,2],[2,3]]]],[[[[0,1],[0,2],[0,3]]]]]],[[[[[[0,1],[0,2],[1,3]],[[0,2],[1,3],[2,3]]]],[[[[0,1],[1,2],[1,3]]]]],[[[[[0,2],[1,2],[2,3]]]],[[]]]]]


#For each hyperplane work out the frames when approaching from that direction
#[0,2],[1,3],[1,2]

# Get the hyperplane and create a folder for the frames if needs be
hyperplaneFilePath = str(argv[0])
print(hyperplaneFilePath)
with open(hyperplaneFilePath, 'r') as hyperplaneFile:
    hyperplanes = hyperplaneFile.readlines()
hyperplaneName = os.path.basename(hyperplaneFilePath)
frames = int(argv[2])

#print("Getting hypervectors")
#Get the original hyperplane  and "x", "y", and "z" hyperplane components of the of the hyperplane-axis construct

oPlane = hyperplanes[0].split()

a = float(oPlane[2])
b = float(oPlane[0])
c = float(oPlane[1])
d = float(oPlane[3])

xAxis = hyperplanes[1].split()

Ax = float(xAxis[2])
Bx = float(xAxis[0])
Cx = float(xAxis[1])
Dx = float(xAxis[3])
    
yAxis = hyperplanes[3].split()

Ay = float(yAxis[2])
By = float(yAxis[0])
Cy = float(yAxis[1])
Dy = float(yAxis[3])

zAxis = hyperplanes[2].split()

Az = float(zAxis[2])
Bz = float(zAxis[0])
Cz = float(zAxis[1])
Dz = float(zAxis[3])


# Get the path of the spl4 and the directory above it
spl4Path=str(argv[1])
spl4Dir=str(argv[3])

spl4 = open(spl4Directory+'/'+spl4Dir+'/'+spl4Path, 'r').readlines()

#print(len(spl4))
#Starting at zero, with the prisms and tetrahedron lists empty
i=0
prisms=[]
tetrahedrons=[]
# Look at each line of the file
while(i<len(spl4)):
    # If it contains "prism"
    if re.search("prism", spl4[i]):
        # initiate a list of 6 nones which will be overwritten by the six vertices of the prism
        prism=[None]*6
        # For each vertex create an array of coordinates x, y, z, w for that vertex and set it as the vertex of the prism.
        j=1
        while(j<7):
            vertex=[float(spl4[j+(i)].split()[1]),float(spl4[j+(i)].split()[2]),float(spl4[j+(i)].split()[3]),float(spl4[j+(i)].split()[4])]
            prism[j-1]=vertex
            j=j+1
        # Add the fully formed prism to prisms
        prisms.append(prism)
    # If it is a tetrahedron then do the same but with the four vertices of the tetrahedron
    if re.search("tetrahedron", spl4[i]):
        tetrahedron=[None]*4
        j=1
        while(j<5):
            vertex=[float(spl4[j+(i)].split()[1]),float(spl4[j+(i)].split()[2]),float(spl4[j+(i)].split()[3]),float(spl4[j+(i)].split()[4])]
            tetrahedron[j-1]=vertex
            j=j+1
        tetrahedrons.append(tetrahedron)
    i=i+1

##########CONFIRMED WORKING###########

# Set the order of vertices
prismVertices=[0,1,2,3,4,5]
tetrahedronVertices=[0,1,2,3]
constants=[]

## Dealing with PRISMS ##
i=0
furthPosAny=None
furthNegAny=None
# For each prism:
while(i<len(prisms)):
    storePrism=[]
    furthPosPrism=None
    furthNegPrism=None
    # For each vertex
    for vertex in prismVertices:
        # Get the x,y,z,w coordinates of that vertex
        pX=prisms[i][vertex][0]
        pY=prisms[i][vertex][1]
        pZ=prisms[i][vertex][2]
        pW=prisms[i][vertex][3]
        eRequiredToHit=((a*pX)+(b*pY)+(c*pZ)+(d*pW))*(-1)
        if (furthPosPrism==None):
            furthPosPrism=eRequiredToHit
        elif (eRequiredToHit>furthPosPrism):
            furthPosPrism=eRequiredToHit
        if (furthNegPrism==None):
            furthNegPrism=eRequiredToHit
        elif (eRequiredToHit<furthNegPrism):
            furthNegPrism=eRequiredToHit
    # Then check if the furthest of this prism is the new furthest in total or not
    if (furthPosAny==None):
        furthPosAny=furthPosPrism
    elif (furthPosPrism>furthPosAny):
        furthPosAny=furthPosPrism
    if (furthNegAny==None):
        furthNegAny=furthNegPrism
    elif (furthNegPrism<furthNegAny):
        furthNegAny=furthNegPrism
    i+=1


## Dealing with TETRAHEDRONS ##
# Do the same with tetrahedron N.B. the furthest/closest distance is shared across all shapes for the total.
i=0
#normalizer=(math.sqrt((a**2)+(b**2)+(c**2)+(d**2)))
while(i<len(tetrahedrons)):
    furthPosTet=None
    furthNegTet=None
    for vertex in tetrahedronVertices:
        pX=tetrahedrons[i][vertex][0]
        pY=tetrahedrons[i][vertex][1]
        pZ=tetrahedrons[i][vertex][2]
        pW=tetrahedrons[i][vertex][3]
        eRequiredToHit=((a*pX)+(b*pY)+(c*pZ)+(d*pW))*(-1)
        # e required to reach this distance is dis*normalizer, so we can remove this part
        if (furthPosTet==None):
            furthPosTet=eRequiredToHit
        elif (eRequiredToHit>furthPosTet):
            furthPosTet=eRequiredToHit
        if (furthNegTet==None):
            furthNegTet=eRequiredToHit
        elif (eRequiredToHit<furthNegTet):
            furthNegTet=eRequiredToHit
    #print("\nFinal Checks\n")
    if (furthPosAny==None):
        furthPosAny=furthPosTet
    elif (furthPosTet>furthPosAny):
        furthPosAny=furthPosTet
    if (furthNegAny==None):
        furthNegAny=furthNegTet
    elif (furthNegTet<furthNegAny):
        furthNegAny=furthNegTet
    i+=1

# Try to update the fifth and sixth lines
try:
    # Check if the fifth and sixth lines exist
    if len(hyperplanes) >= 6:
        # Try to convert them to floats
        fifth_line_float = float(hyperplanes[4].strip())
        sixth_line_float = float(hyperplanes[5].strip())
        hyperplanes[4] = str(min(fifth_line_float, furthNegAny)) + "\n"
        hyperplanes[5] = str(max(sixth_line_float, furthPosAny)) + "\n"
    else:
        # If the lines do not exist, append them
        hyperplanes.append(str(furthNegAny) + "\n")
        hyperplanes.append(str(furthPosAny) + "\n")
except (IndexError, ValueError):
    hyperplanes.append(str(furthNegAny) + "\n")
    hyperplanes.append(str(furthPosAny) + "\n")

# Overwrite the file with the updated lines
with open(hyperplaneFilePath, 'w') as hyperplaneFile:
    hyperplaneFile.writelines(hyperplanes)