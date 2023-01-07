
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

    #print("Starting with "+hyperPlaneFile)

# Get the hyperplane and create a folder for the frames if needs be
hyperplaneFile = str(argv[0])
print(hyperplaneFile)
hyperplanes = open(hyperplaneFile, 'r').readlines()
hyperplaneName = os.path.basename(hyperplaneFile)
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

spl4Path=str(argv[1])

# Creates a list of the needed spl4 data of the form:
# prisms[i][0-5][0-4]
#        ^    ^   ^
#        |    |   x,y,z,w
#        |    vertex
#        prism

#print("Starting with "+spl4Path)

spl4 = open(spl4Directory+'/'+spl4Path, 'r').readlines()

#print(len(spl4))
#Starting at zero, with the prisms and tetrahedron lists empty
i=0
prisms=[]
tetrahedrons=[]
#print(str(len(spl4))+" lines to consider.")
# Look at each line of the file
while(i<len(spl4)):
    #print(spl4[i])
    # If it contains "prism"
    if re.search("prism", spl4[i]):
        #print("Prism "+str(i)+" beginning with comment line "+str(spl4[i]+str(i))+"\n")
        # initiate a list of 6 nones which will be overwritten by the six vertices of the prism
        prism=[None]*6
        # For each vertex create an array of coordinates x, y, z, w for that vertex and set it as the vertex of the prism.
        j=1
        while(j<7):
            vertex=[float(spl4[j+(i)].split()[1]),float(spl4[j+(i)].split()[2]),float(spl4[j+(i)].split()[3]),float(spl4[j+(i)].split()[4])]
            #print(vertex)
            prism[j-1]=vertex
            j=j+1
        #print("\nPrism")
        #print(prism)
        # Add the fully formed prism to prisms
        prisms.append(prism)
    # If it is a tetrahedron then do the same but with the four vertices of the tetrahedron
    if re.search("tetrahedron", spl4[i]):
        #print("Tetrahedron "+str(i)+" beginning with comment line "+str(spl4[i]+str(i))+"\n")
        tetrahedron=[None]*4
        j=1
        while(j<5):
            vertex=[float(spl4[j+(i)].split()[1]),float(spl4[j+(i)].split()[2]),float(spl4[j+(i)].split()[3]),float(spl4[j+(i)].split()[4])]
            #print(vertex)
            tetrahedron[j-1]=vertex
            j=j+1
        #print("\Tetrahedron")
        #print(tetrahedron)
        tetrahedrons.append(tetrahedron)
    i=i+1

##########CONFIRMED WORKING###########

# Set the order of vertices
prismVertices=[0,1,2,3,4,5]
tetrahedronVertices=[0,1,2,3]
constants=[]

## Dealing with PRISMS ##
i=0
#normalizer=(math.sqrt((a**2)+(b**2)+(c**2)+(d**2)))
# furthPos/Neg are going to record the furthest e or "time constant i.e. seconds"  (unit of original hyperplane (orthagonal to the "x" "y" and "z" hyperplanes) constant )
# Is used to slice the shape into segemnts of time constants between the furthest and closest points in spacetime along the time axis
furthPosAny=None
furthNegAny=None
# Create an empty list to record handy infromation on all prisms as we go
allPrismsDistanceInfo=[]
# For each prism:
while(i<len(prisms)):
    #print("Prism "+str(i))
    storePrism=[]
    furthPosPrism=None
    furthNegPrism=None
    # For each vertex
    for vertex in prismVertices:
        #print("Checking the value of e required from the hyperplane to intersect vertex "+str(vertex))
        #print(str(prisms[i][vertex]))
        # Get the x,y,z,w coordinates of that vertex
        pX=prisms[i][vertex][0]
        pY=prisms[i][vertex][1]
        pZ=prisms[i][vertex][2]
        pW=prisms[i][vertex][3]
        #print("Sanity Check")
        #print(a)
        #print(b)
        #print(c)
        #print(d)
        #print(pX)
        #print(pY)
        #print(pZ)
        #print(pW)
        eRequiredToHit=((a*pX)+(b*pY)+(c*pZ)+(d*pW))*(-1)
        # e required to reach this distance is dis*normalizer, so we can remove this part
        #print(eRequiredToHit)
        # If the "number of seconds" to hit this vertex is greated or lesser than any seen for this prism then record it.
        storePrism.append(eRequiredToHit)
        if (furthPosPrism==None):
            #print("First furthest pos e")
            furthPosPrism=eRequiredToHit
        elif (eRequiredToHit>furthPosPrism):
            #print("New furthest pos e")
            furthPosPrism=eRequiredToHit
        if (furthNegPrism==None):
            #print("First furthest neg e")
            furthNegPrism=eRequiredToHit
        elif (eRequiredToHit<furthNegPrism):
            #print("New furthest neg e")
            furthNegPrism=eRequiredToHit
    #print("Appending this prism to the list")
    # Append to the list
    allPrismsDistanceInfo.append([furthPosPrism,furthNegPrism,[storePrism]])
    # Then check if the furthest of this prism is the new furthest in total or not
    #print("\nFinal Checks\n")
    if (furthPosAny==None):
        #print("First abs furthest pos e")
        furthPosAny=furthPosPrism
    elif (furthPosPrism>furthPosAny):
        #print("New abs furthest pos e")
        furthPosAny=furthPosPrism
    if (furthNegAny==None):
        #print("First abs furthest neg e")
        furthNegAny=furthNegPrism
    elif (furthNegPrism<furthNegAny):
        #print("New abs furthest neg e")
        furthNegAny=furthNegPrism
    i+=1


## Dealing with TETRAHEDRONS ##
# Do the same with tetrahedron N.B. the furthest/closest distance is shared across all shapes for the total.
i=0
#normalizer=(math.sqrt((a**2)+(b**2)+(c**2)+(d**2)))
allTetrahedronsDistanceInfo=[]
while(i<len(tetrahedrons)):
    #print("Tetrahedron "+str(i))
    #print(tetrahedrons[i])
    storeTet=[]
    furthPosTet=None
    furthNegTet=None
    for vertex in tetrahedronVertices:
        #print("Checking the value of e required from the hyperplane to intersect vertex "+str(vertex))
        #print(str(tetrahedrons[i][vertex]))
        pX=tetrahedrons[i][vertex][0]
        pY=tetrahedrons[i][vertex][1]
        pZ=tetrahedrons[i][vertex][2]
        pW=tetrahedrons[i][vertex][3]
        #print("Sanity Check")
        #print(a)
        #print(b)
        #print(c)
        #print(d)
        #print(pX)
        #print(pY)
        #print(pZ)
        #print(pW)
        eRequiredToHit=((a*pX)+(b*pY)+(c*pZ)+(d*pW))*(-1)
        # e required to reach this distance is dis*normalizer, so we can remove this part
        #print(eRequiredToHit)
        storeTet.append(eRequiredToHit)
        if (furthPosTet==None):
            #print("First furthest pos e")
            furthPosTet=eRequiredToHit
        elif (eRequiredToHit>furthPosTet):
            #print("New furthest pos e")
            furthPosTet=eRequiredToHit
        if (furthNegTet==None):
            #print("First furthest neg e")
            furthNegTet=eRequiredToHit
        elif (eRequiredToHit<furthNegTet):
            #print("New furthest neg e")
            furthNegTet=eRequiredToHit
    #print("Appending this Tetrahedron to the list")
    allTetrahedronsDistanceInfo.append([furthPosTet,furthNegTet,[storeTet]])
    #print("\nFinal Checks\n")
    if (furthPosAny==None):
        #print("First abs furthest pos e")
        furthPosAny=furthPosTet
    elif (furthPosTet>furthPosAny):
        #print("New abs furthest pos e")
        furthPosAny=furthPosTet
    if (furthNegAny==None):
        #print("First abs furthest neg e")
        furthNegAny=furthNegTet
    elif (furthNegTet<furthNegAny):
        #print("New abs furthest neg e")
        furthNegAny=furthNegTet
    i+=1

# Write the distance and note the furthest/closest of any vertex
allPrismsDistanceInfo=[allPrismsDistanceInfo]
allPrismsDistanceInfo.insert(0,(furthNegAny))
allPrismsDistanceInfo.insert(0,(furthPosAny))
#print("everything here "+str(allPrismsDistanceInfo))

allTetrahedronsDistanceInfo=[allTetrahedronsDistanceInfo]
allTetrahedronsDistanceInfo.insert(0,(furthNegAny))
allTetrahedronsDistanceInfo.insert(0,(furthPosAny))
#print("everything here "+str(allTetrahedronsDistanceInfo))

#print("COMPARE")
#print(allPrismsDistanceInfo[0])
#print(furthPosAny)

# NOTE Check what the hell I am doing here. In theory it should be fine in shapes of my own construction, but we should be prepared for shapes with further tetrahedons than prisms.
# Set the starting and ending distance to the ones noted in the shapes
startingDistance=allPrismsDistanceInfo[0]
endingDistance=allPrismsDistanceInfo[1]

# Set the increment to be equidistant slices of that length
increment=((endingDistance-startingDistance)/frames)
#print("\n increment to seperate frames "+str(increment)+"\n")

if not (os.path.exists(RotatedSTLPath+'/'+spl4Path[:-5]+'_fr-'+str(frames))):
    os.mkdir(RotatedSTLPath+'/'+spl4Path[:-5]+'_fr-'+str(frames)+'_HP-'+hyperplaneName)

# For each frame
# NOTE It is going to be possible (but unlikely in most animations) that there will be legitimate "blank frames", how should we deal?
i=0
while (i<frames):
    # Set the time-like value to be a slice of the 4d shape corresponding to that frame
    constantValue=((i*increment)+0.5*increment)+startingDistance
    #print("\nConstant to take cross-section "+str(constantValue)+" for frame "+str(i))
    # Create a new STL file where we'll write a cross section.
    frameAsSTL = open(RotatedSTLPath+'/'+spl4Path[:-5]+'_fr-'+str(frames)+'_HP-'+hyperplaneName+'/'+spl4Path[:-5]+'_HP-'+hyperplaneName+"_"+str(("%04d" % (i,)))+'.stl', 'w+')
    frameAsSTL.write("solid Created by spacetimerotatepython\n")
    frameAsSTL.write("\n")  
    # If we are going to write the prism component
    if (renderPrisms):
        j=0
        # For each prism
        while(j<len(prisms)):
            # Get that prism
            prism=allPrismsDistanceInfo[2][j]
            # If the "slice" lands between the furthest and closest vertex in time, we need to generate triangles.
            if (prism[0]>constantValue):
                if (prism[1]<constantValue):
                    #print("YES")
                    #frameAsSTL.write("Starting Prism Notes\n")
                    # Get True/False values for whether each vertex of the prism is above/below the timelike hyperplane. 
                    aAbove=((prism[2][0][0]-constantValue)>0)
                    bAbove=((prism[2][0][1]-constantValue)>0)
                    cAbove=((prism[2][0][2]-constantValue)>0)
                    dAbove=((prism[2][0][3]-constantValue)>0)
                    eAbove=((prism[2][0][4]-constantValue)>0)
                    fAbove=((prism[2][0][5]-constantValue)>0)

                    #frameAsSTL.write(str(aAbove)+"\n")
                    #frameAsSTL.write(str(bAbove)+"\n")
                    #frameAsSTL.write(str(cAbove)+"\n")
                    #frameAsSTL.write(str(dAbove)+"\n")
                    #frameAsSTL.write(str(eAbove)+"\n")
                    #frameAsSTL.write(str(fAbove)+"\n")

                    # If f is not above the hyperplane, flip the truthy values of each vertex, then ignore f in the table
                    # This works because the intersection of a shape with an n-plane is unchanged if you invert that shape about its n-plane
                    if(not fAbove):
                        aAbove=not aAbove
                        bAbove=not bAbove
                        cAbove=not cAbove
                        dAbove=not dAbove
                        eAbove=not eAbove

                    frameAsSTL.write("\n") 


                    #frameAsSTL.write(str(intersectTriangleTable[aAbove][bAbove][cAbove][dAbove][eAbove])+"\n")
                    # Pass the truthy values of the f-stabilized a-e vertices into the table and get the returned triangles which will need to be drawn.
                    trianglesToRender=intersectTriangleTable[aAbove][bAbove][cAbove][dAbove][eAbove]

                    # For each triangle we need to render
                    for polygon in trianglesToRender:
                        frameAsSTL.write("PrismPolygon ")
                        for triangle in polygon:
                            frameAsSTL.write("facet normal\n")
                            frameAsSTL.write("outer loop\n")
                            #print(str(triangle))
                            #print(str(prism))
                            #print("\n")
                            #print(str(constantValue))
                            #print("\n")
                            #print(str(prism[2][0][triangle[0][0]]))
                            #print(str(prism[2][0][triangle[0][1]]))
                            #print(str(prisms[j]))
                            # For each vertex
                            for vertex in triangle:
                                #print("\nVertex of triangle sits between")
                                #print(str(vertex))
                                #print("Point 1 coords and distance to hyperplane")
                                #print(str(prisms[j][vertex[0]]))
                                #print(str(prism[2][0][triangle[0][0]]-constantValue))
                                #print("Point 2 coords and distance to hyperplane")
                                #print(str(prisms[j][vertex[1]]))
                                #print(str(prism[2][0][triangle[0][1]]-constantValue))
                                #print("Point that intersect hyperplane")

                                # Grab the x,y,z,w coordinates of each vertex of the line that triangle's vertex sites between.
                                #print("Coords for the first point")
                                point1x = prisms[j][vertex[0]][0]
                                #print(str(point1x))
                                point1y = prisms[j][vertex[0]][1]
                                #print(str(point1y))
                                point1z = prisms[j][vertex[0]][2]
                                #print(str(point1z))
                                point1w = prisms[j][vertex[0]][3]
                                #print(str(point1w))
                                #print("Coords for the second point")
                                point2x = prisms[j][vertex[1]][0]
                                #print(str(point2x))
                                point2y = prisms[j][vertex[1]][1]
                                #print(str(point2y))
                                point2z = prisms[j][vertex[1]][2]
                                #print(str(point2z))
                                point2w = prisms[j][vertex[1]][3]
                                #print(str(point2w))


                                #print("Constant (e)")
                                #print(str(constantValue))

                                # Get the coordinates of the intersection between the two lines.
                                # If these points actually sit on each other (likely if some part of an animation doesn't move between two frames) then set it to one of the points.
                                # Otherwise, set it by algorithm. We can do this since we can compare the coordinates of each line vertex with the distance of that vertex from the timelike hyperplane
                                if(point2x==point1x):
                                    Colx=point1x
                                else:
                                    Colx=(((d*((point1x*(point2w-point1w))/(point2x-point1x)))-(d*point1w)+(b*((point1x*(point2y-point1y))/(point2x-point1x)))-(b*point1y)+(c*((point1x*(point2z-point1z))/(point2x-point1x)))-(c*point1z)-constantValue)/((a)+(b*((point2y-point1y)/(point2x-point1x)))+(c*((point2z-point1z)/(point2x-point1x)))+(d*((point2w-point1w)/(point2x-point1x)))))
                                if(point2y==point1y):
                                    Coly=point1y
                                else:
                                    Coly=(((a*((point1y*(point2x-point1x))/(point2y-point1y)))-(a*point1x)+(c*((point1y*(point2z-point1z))/(point2y-point1y)))-(c*point1z)+(d*((point1y*(point2w-point1w))/(point2y-point1y)))-(d*point1w)-constantValue)/((b)+(c*((point2z-point1z)/(point2y-point1y)))+(d*((point2w-point1w)/(point2y-point1y)))+(a*((point2x-point1x)/(point2y-point1y)))))
                                if(point2z==point1z):
                                    Colz=point1z
                                else:
                                    Colz=(((b*((point1z*(point2y-point1y))/(point2z-point1z)))-(b*point1y)+(d*((point1z*(point2w-point1w))/(point2z-point1z)))-(d*point1w)+(a*((point1z*(point2x-point1x))/(point2z-point1z)))-(a*point1x)-constantValue)/((c)+(d*((point2w-point1w)/(point2z-point1z)))+(a*((point2x-point1x)/(point2z-point1z)))+(b*((point2y-point1y)/(point2z-point1z)))))
                                if(point2w==point1w):
                                    Colw=point1w
                                else:
                                    Colw=(((c*((point1w*(point2z-point1z))/(point2w-point1w)))-(c*point1z)+(a*((point1w*(point2x-point1x))/(point2w-point1w)))-(a*point1x)+(b*((point1w*(point2y-point1y))/(point2w-point1w)))-(b*point1y)-constantValue)/((d)+(a*((point2x-point1x)/(point2w-point1w)))+(b*((point2y-point1y)/(point2w-point1w)))+(c*((point2z-point1z)/(point2w-point1w)))))

                                #print("Final coords of collision point")
                                #print(str(Colx))
                                #print(str(Coly))
                                #print(str(Colz))
                                #print(str(Colw))

                                #print("Checking the split")
                                #if(point2x==point1x):
                                #    #print("Perfect match")
                                #else:
                                #    #print((point2x-Colx)/(Colx-point1x))
                                #if(point2y==point1y):
                                #    #print("Perfect match")
                                #else:
                                #    #print((point2y-Coly)/(Coly-point1y))
                                #if(point2z==point1z):
                                #    #print("Perfect match")
                                #else:
                                #    #print((point2z-Colz)/(Colz-point1z))
                                #if(point2w==point1w):
                                #    #print("Perfect match")
                                #else:
                                #    #print((point2w-Colw)/(Colw-point1w))


                                #print("Converting the 4 dimensional coords of Cx,Cy,Cz,Cw into 3 dimensional fX,fY,fZ")
                                # For each x,y,z hyperplane we are going to find the shortest distance from that hyperplane to the triangle's vertex. This is the definition of the coordinate in the total coordinate system

                                fX=((Ax*Colx)+(Bx*Coly)+(Cx*Colz)+(Dx*Colw)/(math.sqrt((Ax**2)+(Bx**2)+(Cx**2)+(Dx**2))))
                                fY=((Ay*Colx)+(By*Coly)+(Cy*Colz)+(Dy*Colw)/(math.sqrt((Ay**2)+(By**2)+(Cy**2)+(Dy**2))))
                                fZ=((Az*Colx)+(Bz*Coly)+(Cz*Colz)+(Dz*Colw)/(math.sqrt((Az**2)+(Bz**2)+(Cz**2)+(Dz**2))))

                                #print(str(fX)+str(fY)+str(fZ))
                                #print(fX)
                                #print(fY)
                                #print(fZ)
                                # Write down these coordinates as x,y,z coords
                                frameAsSTL.write("vertex "+str(fX)+" "+str(fY)+" "+str(fZ)+"\n")





                                #CHECK THE RESPONSE TIMES FOR THE BELOW TWO METHODS
                                #For each point which intersects the plane Xn,Yn,Zn,Wn, get the final coordinates for it compared to the plane itself. xf.yf,zf
                                #
                                #xf=AxXn+BxYn+CxZn+DxWn/(sqrt(AxAx+BxBx+CxCx+DxDx))
                                #
                                #xf=Xn+Zn((-a-d)/c)+Wn/(sqrt(2+((-a-d)(-a-d)/cc)))
                                #
                                #yf=AyXn+ByYn+CyZn+DyWn/(sqrt(AyAy+ByBy+CyCy+DyDy))
                                #
                                #yf=-abXn+Yn(aa+cc+dd)-cbZn-dbWn/((-ab)(-ab)+(aa+cc+dd)(aa+bb+cc)+(-cb)(-cb)+(-db)(-db))
                                #
                                #zf=AzXn+BzYn+CzZn+DzWn/(sqrt(AzAz+BzBz+CzCz+DzDz))
                                #
                                #zf=Xn+Zn((c(d-a))/(d(a+d)+cc))+Wn((ad-aa+cc)/(d(a+d)+cc))
                            frameAsSTL.write("endloop\n")
                            frameAsSTL.write("endfacet\n") 
            j=j+1



        #####Handling Tetrahedrons########
    # Do the same thing with tetrahedrons
    # NOTE Work out why you often needed the isclose code here, and if it is still needed.
    if (renderTetrahedrons):
        j=0
        while(j<len(tetrahedrons)):
            #print("\nNumber of Tetrahedron to check is "+str(j))
            #frameAsSTL.write("vertex "+str(tetrahedrons[j][3][0])+" "+str(tetrahedrons[j][3][1])+" "+str(tetrahedrons[j][3][2])+"\n")
            #print("--")
            tetrahedron=allTetrahedronsDistanceInfo[2][j]
            #print("Let's check this tetrahedron: "+str(tetrahedron))
            if (tetrahedron[0]>constantValue):
                if (tetrahedron[1]<constantValue):
                    #print(constantValue)
                    #print("I need to render the intersection of this one")
                    #frameAsSTL.write("Starting Tetrahedron Notes\n")
                    aAbove=((tetrahedron[2][0][0]-constantValue)>0)
                    bAbove=((tetrahedron[2][0][1]-constantValue)>0)
                    cAbove=((tetrahedron[2][0][2]-constantValue)>0)
                    dAbove=((tetrahedron[2][0][3]-constantValue)>0)
                    #eAbove=((tetrahedron[2][0][4]-constantValue)>0)
                    #fAbove=((tetrahedron[2][0][5]-constantValue)>0)
                    #frameAsSTL.write(str(aAbove)+"\n")
                    #frameAsSTL.write(str(bAbove)+"\n")
                    #frameAsSTL.write(str(cAbove)+"\n")
                    #frameAsSTL.write(str(dAbove)+"\n")
                    #frameAsSTL.write(str(eAbove)+"\n")
                    #frameAsSTL.write(str(fAbove)+"\n")
                    if(not dAbove):
                        aAbove=not aAbove
                        bAbove=not bAbove
                        cAbove=not cAbove
                        #dAbove=not dAbove
                        #eAbove=not eAbove
                    #frameAsSTL.write(("\n"))
                    #frameAsSTL.write(str(intersectTriangleTable[aAbove][bAbove][cAbove][dAbove][eAbove])+"\n")
                    trianglesToRender=intersectTetrahedronTable[aAbove][bAbove][cAbove]#[dAbove][eAbove]
                    #print("The Triangles I need to render are: "+str(trianglesToRender))
                    for polygon in trianglesToRender:
                        frameAsSTL.write("TetrahedronPolygon")
                        for triangle in polygon:
                            frameAsSTL.write("facet normal\n")
                            frameAsSTL.write("outer loop\n")
                            #print("Triangle calculating now "+str(triangle))
                            #print(str(tetrahedron))
                            #print(str(constantValue))
                            #print(str(triangle[0][0]))
                            #print(str(tetrahedron[2][0][triangle[0][0]]))
                            #print(str(tetrahedron[2][0][triangle[0][1]]))
                            #print(str(tetrahedrons[j]))
                            for vertex in triangle:
                                #print("\nVertex of triangle sits between")
                                #print(str(vertex))
                                #print("Point 1 coords and distance to hyperplane")
                                #print(str(tetrahedrons[j][vertex[0]]))
                                #print(str(tetrahedron[2][0][triangle[0][0]]-constantValue))
                                #print("Point 2 coords and distance to hyperplane")
                                #print(str(tetrahedrons[j][vertex[1]]))
                                #print(str(tetrahedron[2][0][triangle[0][1]]-constantValue))
                                #print("Point that intersect hyperplane")
                                #print("Coords for the first point")
                                point1x = tetrahedrons[j][vertex[0]][0]
                                #print(str(point1x))
                                point1y = tetrahedrons[j][vertex[0]][1]
                                #print(str(point1y))
                                point1z = tetrahedrons[j][vertex[0]][2]
                                #print(str(point1z))
                                point1w = tetrahedrons[j][vertex[0]][3]
                                #print(str(point1w))
                                #print("Coords for the second point")
                                point2x = tetrahedrons[j][vertex[1]][0]
                                #print(str(point2x))
                                point2y = tetrahedrons[j][vertex[1]][1]
                                #print(str(point2y))
                                point2z = tetrahedrons[j][vertex[1]][2]
                                #print(str(point2z))
                                point2w = tetrahedrons[j][vertex[1]][3]
                                #print(str(point2w))
                                #print("Constant (e)")
                                #print(str(constantValue))
                                if(math.isclose(point1x, point2x, rel_tol=1e-05)):
                                    Colx=point1x
                                elif (((a)+(b*((point2y-point1y)/(point2x-point1x)))+(c*((point2z-point1z)/(point2x-point1x)))+(d*((point2w-point1w)/(point2x-point1x))))==0):
                                    #print("\n\nNumber of Tetrahedron to check is "+str(j))
                                    #print("TRAP TRAP TRAP TRAP TRAPPPPPPED \n by X")
                                    #print("\nVertex of triangle sits between")
                                    #print(str(vertex))
                                    #print("Point 1 coords and distance to hyperplane")
                                    #print(str(tetrahedrons[j][vertex[0]]))
                                    #print(str(tetrahedron[2][0][triangle[0][0]]-constantValue))
                                    #print("Point 2 coords and distance to hyperplane")
                                    #print(str(tetrahedrons[j][vertex[1]]))
                                    #print(str(tetrahedron[2][0][triangle[0][1]]-constantValue))
                                    #print("Point that intersect hyperplane")
                                    #print("Coords for the first point")
                                    #print(str(point1x))
                                    #print(str(point1y))
                                    #print(str(point1z))
                                    #print(str(point1w))
                                    #print("Coords for the second point")
                                    #print(str(point2x))
                                    #print(str(point2y))
                                    #print(str(point2z))
                                    #print(str(point2w))
                                    Colx=(0)
                                else:
                                    Colx=(((d*((point1x*(point2w-point1w))/(point2x-point1x)))-(d*point1w)+(b*((point1x*(point2y-point1y))/(point2x-point1x)))-(b*point1y)+(c*((point1x*(point2z-point1z))/(point2x-point1x)))-(c*point1z)-constantValue)/((a)+(b*((point2y-point1y)/(point2x-point1x)))+(c*((point2z-point1z)/(point2x-point1x)))+(d*((point2w-point1w)/(point2x-point1x)))))
                                if(math.isclose(point1y, point2y, rel_tol=1e-05)):
                                    Coly=point1y
                                elif (((b)+(c*((point2z-point1z)/(point2y-point1y)))+(d*((point2w-point1w)/(point2y-point1y)))+(a*((point2x-point1x)/(point2y-point1y))))==0):
                                    #print("\n\nNumber of Tetrahedron to check is "+str(j))
                                    #print("TRAP TRAP TRAP TRAP TRAPPPPPPED \n by Y")
                                    #print("\nVertex of triangle sits between")
                                    #print(str(vertex))
                                    #print("Point 1 coords and distance to hyperplane")
                                    #print(str(tetrahedrons[j][vertex[0]]))
                                    #print(str(tetrahedron[2][0][triangle[0][0]]-constantValue))
                                    #print("Point 2 coords and distance to hyperplane")
                                    #print(str(tetrahedrons[j][vertex[1]]))
                                    #print(str(tetrahedron[2][0][triangle[0][1]]-constantValue))
                                    #print("Point that intersect hyperplane")
                                    #print("Coords for the first point")
                                    #print(str(point1x))
                                    #print(str(point1y))
                                    #print(str(point1z))
                                    #print(str(point1w))
                                    #print("Coords for the second point")
                                    #print(str(point2x))
                                    #print(str(point2y))
                                    #print(str(point2z))
                                    #print(str(point2w))
                                    Coly=(0)
                                else:
                                    Coly=(((a*((point1y*(point2x-point1x))/(point2y-point1y)))-(a*point1x)+(c*((point1y*(point2z-point1z))/(point2y-point1y)))-(c*point1z)+(d*((point1y*(point2w-point1w))/(point2y-point1y)))-(d*point1w)-constantValue)/((b)+(c*((point2z-point1z)/(point2y-point1y)))+(d*((point2w-point1w)/(point2y-point1y)))+(a*((point2x-point1x)/(point2y-point1y)))))
                                if(math.isclose(point1z, point2z, rel_tol=1e-05)):
                                    Colz=point1z
                                elif (((c)+(d*((point2w-point1w)/(point2z-point1z)))+(a*((point2x-point1x)/(point2z-point1z)))+(b*((point2y-point1y)/(point2z-point1z))))==0):
                                    #print("\n\nNumber of Tetrahedron to check is "+str(j))
                                    #print("TRAP TRAP TRAP TRAP TRAPPPPPPED \n by Z")
                                    #print("\nVertex of triangle sits between")
                                    #print(str(vertex))
                                    #print("Point 1 coords and distance to hyperplane")
                                    #print(str(tetrahedrons[j][vertex[0]]))
                                    #print(str(tetrahedron[2][0][triangle[0][0]]-constantValue))
                                    #print("Point 2 coords and distance to hyperplane")
                                    #print(str(tetrahedrons[j][vertex[1]]))
                                    #print(str(tetrahedron[2][0][triangle[0][1]]-constantValue))
                                    #print("Point that intersect hyperplane")
                                    #print("Coords for the first point")
                                    #print(str(point1x))
                                    #print(str(point1y))
                                    #print(str(point1z))
                                    #print(str(point1w))
                                    #print("Coords for the second point")
                                    #print(str(point2x))
                                    #print(str(point2y))
                                    #print(str(point2z))
                                    #print(str(point2w))
                                    Colz=(0)
                                else:
                                    #print("Checking weird z")
                                    #print(((b*((point1z*(point2y-point1y))/(point2z-point1z)))-(b*point1y)+(d*((point1z*(point2w-point1w))/(point2z-point1z)))-(d*point1w)+(a*((point1z*(point2x-point1x))/(point2z-point1z)))-(a*point1x)-constantValue))
                                    #print("Divided by")
                                    #print(((c)+(d*((point2w-point1w)/(point2z-point1z)))+(a*((point2x-point1x)/(point2z-point1z)))+(b*((point2y-point1y)/(point2z-point1z)))))
                                    Colz=(((b*((point1z*(point2y-point1y))/(point2z-point1z)))-(b*point1y)+(d*((point1z*(point2w-point1w))/(point2z-point1z)))-(d*point1w)+(a*((point1z*(point2x-point1x))/(point2z-point1z)))-(a*point1x)-constantValue)/((c)+(d*((point2w-point1w)/(point2z-point1z)))+(a*((point2x-point1x)/(point2z-point1z)))+(b*((point2y-point1y)/(point2z-point1z)))))
                                if(math.isclose(point1w, point2w, rel_tol=1e-05)):
                                    Colw=point1w
                                elif (((d)+(a*((point2x-point1x)/(point2w-point1w)))+(b*((point2y-point1y)/(point2w-point1w)))+(c*((point2z-point1z)/(point2w-point1w))))==0):
                                    #print("\n\nNumber of Tetrahedron to check is "+str(j))
                                    #print("TRAP TRAP TRAP TRAP TRAPPPPPPED \n by W")
                                    #print("\nVertex of triangle sits between")
                                    #print(str(vertex))
                                    #print("Point 1 coords and distance to hyperplane")
                                    #print(str(tetrahedrons[j][vertex[0]]))
                                    #print(str(tetrahedron[2][0][triangle[0][0]]-constantValue))
                                    #print("Point 2 coords and distance to hyperplane")
                                    #print(str(tetrahedrons[j][vertex[1]]))
                                    #print(str(tetrahedron[2][0][triangle[0][1]]-constantValue))
                                    #print("Point that intersect hyperplane")
                                    #print("Coords for the first point")
                                    #print(str(point1x))
                                    #print(str(point1y))
                                    #print(str(point1z))
                                    #print(str(point1w))
                                    #print("Coords for the second point")
                                    #print(str(point2x))
                                    #print(str(point2y))
                                    #print(str(point2z))
                                    #print(str(point2w))
                                    Colw=(0)
                                else:
                                    Colw=(((c*((point1w*(point2z-point1z))/(point2w-point1w)))-(c*point1z)+(a*((point1w*(point2x-point1x))/(point2w-point1w)))-(a*point1x)+(b*((point1w*(point2y-point1y))/(point2w-point1w)))-(b*point1y)-constantValue)/((d)+(a*((point2x-point1x)/(point2w-point1w)))+(b*((point2y-point1y)/(point2w-point1w)))+(c*((point2z-point1z)/(point2w-point1w)))))
                                #print("Final coords of collision point")
                                #print(str(Colx))
                                #print(str(Coly))
                                #print(str(Colz))
                                #print(str(Colw))
                                #print("Checking the split")
                                #if(point2x==point1x):
                                #    #print("Perfect match")
                                #else:
                                #    #print((point2x-Colx)/(Colx-point1x))
                                #if(point2y==point1y):
                                #    #print("Perfect match")
                                #else:
                                #    #print((point2y-Coly)/(Coly-point1y))
                                #if(point2z==point1z):
                                #    #print("Perfect match")
                                #else:
                                #    #print((point2z-Colz)/(Colz-point1z))
                                #if(point2w==point1w):
                                #    #print("Perfect match")
                                #else:
                                #    #print((point2w-Colw)/(Colw-point1w))
                                #print("Converting the 4 dimensional coords of Cx,Cy,Cz,Cw into 3 dimensional fX,fY,fZ")
                                fX=((Ax*Colx)+(Bx*Coly)+(Cx*Colz)+(Dx*Colw)/(math.sqrt((Ax**2)+(Bx**2)+(Cx**2)+(Dx**2))))
                                fY=((Ay*Colx)+(By*Coly)+(Cy*Colz)+(Dy*Colw)/(math.sqrt((Ay**2)+(By**2)+(Cy**2)+(Dy**2))))
                                fZ=((Az*Colx)+(Bz*Coly)+(Cz*Colz)+(Dz*Colw)/(math.sqrt((Az**2)+(Bz**2)+(Cz**2)+(Dz**2))))
                                #print(str(fX)+str(fY)+str(fZ))
                                #print(fX)
                                #print(fY)
                                #print(fZ)
                                frameAsSTL.write("vertex "+str(fX)+" "+str(fY)+" "+str(fZ)+"\n")
                                #CHECK THE RESPONSE TIMES FOR THE BELOW TWO METHODS
                                #For each point which intersects the plane Xn,Yn,Zn,Wn, get the final coordinates for it compared to the plane itself. xf.yf,zf
                                #
                                #xf=AxXn+BxYn+CxZn+DxWn/(sqrt(AxAx+BxBx+CxCx+DxDx))
                                #
                                #xf=Xn+Zn((-a-d)/c)+Wn/(sqrt(2+((-a-d)(-a-d)/cc)))
                                #
                                #yf=AyXn+ByYn+CyZn+DyWn/(sqrt(AyAy+ByBy+CyCy+DyDy))
                                #
                                #yf=-abXn+Yn(aa+cc+dd)-cbZn-dbWn/((-ab)(-ab)+(aa+cc+dd)(aa+bb+cc)+(-cb)(-cb)+(-db)(-db))
                                #
                                #zf=AzXn+BzYn+CzZn+DzWn/(sqrt(AzAz+BzBz+CzCz+DzDz))
                                #
                                #zf=Xn+Zn((c(d-a))/(d(a+d)+cc))+Wn((ad-aa+cc)/(d(a+d)+cc))
                            frameAsSTL.write("endloop\n")
                            frameAsSTL.write("endfacet\n")  
            j=j+1
    i+=1