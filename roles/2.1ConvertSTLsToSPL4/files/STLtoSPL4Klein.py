## Command to make the file run ##
#
# python3 convertStlsToSpl4.py -- Hollow                         (or other)
#
## ARGV ##
#ARGV[0] - TYPE Hollow / Bounded / Hyperloop / Klein
#

#Import regular modules needed
import math
import os
import re
import sys
from math import sin, cos

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

# Axis that will be rotated into w - 0=x, 1=y, 2=z
substituteAxis = int(argv[1])

# If the origin is within the shapes own range will probably cause the shape to clip circling within its own range
originDistance = float(argv[2])

######## Convert STL to SPL4 ##########

#For a STL animation of N frames with M triangles, the SPL4 will contain M(N-1) prisms
#The first frame will start with a waxis value of 0, then each frame will be incremented by wAxisInc
# The Prisms are of the form:
#Triangle1 Vertex1, Triangle1 Vertex2, Triangle1 Vertex3, Triangle2 Vertex1, Triangle2 Vertex2, Triangle2 Vertex3, 

######## CURRENTLY WORKING - Klein converts into a hyperloop as above, but also twists the two remaining dimensions by 180 degrees.
# For each subdirectory with stl frames, then for each frame create a new .spl4 object
subdir=argv[0]
vertexCount=0
kleinFlip=float(argv[3])
# Get the remaining axes which are not rotated into a hyperloop in order to rotate into a Klein bottle
allSpatialAxes=[0,1,2]
allSpatialAxes.remove(substituteAxis)


centreTorusCalculationTotal=0
centreKleinTotal1=0
centreKleinTotal2=0
upperLimit=None
lowerLimit=None
frameArray=[]
spl4 = open(spl4Directory+'/'+subdir+'_KL_sAxis-'+str(substituteAxis)+'_oDis-'+str(originDistance)+'_rota-'+str(kleinFlip)+'.spl4', 'w+')
stlFrames = sorted(os.listdir(os.path.join(stlDirectory, subdir)))
#Get the coords of each triangle in each frame and put it into an array
for i in range(len(stlFrames)):
    ##print(i)
    currentSTL=[]
    stl = open(stlDirectory+'/'+subdir+'/'+stlFrames[i], 'r').readlines()
    for j in range(len(stl)):
        #For each line in the stl, it finds a triangle by searching for "outer loop" and puts it into the array
        if re.search("outer loop", stl[j]):
            currentTriangle=[]
            k=0
            while (k<3):
                currentVertex=[]
                #print(k)
                k=k+1
                vertexInfo=(stl[j+k]).split()
                l=0
                while (l<3):
                    l=l+1
                    #print(vertexInfo[l])
                    currentVertex.append(float(vertexInfo[l]))
                #print(currentVertex[substituteAxis])
                vertexCount=vertexCount+1
                if(upperLimit==None):
                    upperLimit=currentVertex[substituteAxis]
                    lowerLimit=currentVertex[substituteAxis]
                if(upperLimit<currentVertex[substituteAxis]):
                    upperLimit=currentVertex[substituteAxis]
                if(lowerLimit>currentVertex[substituteAxis]):
                    lowerLimit=currentVertex[substituteAxis]
                centreTorusCalculationTotal=centreTorusCalculationTotal+currentVertex[substituteAxis]
                centreKleinTotal1=centreKleinTotal1+currentVertex[allSpatialAxes[0]]
                centreKleinTotal2=centreKleinTotal2+currentVertex[allSpatialAxes[1]]
                #print("New Total")
                #print(centreTorusCalculationTotal)
                currentTriangle.append(currentVertex)
            currentSTL.append(currentTriangle)
    frameArray.append(currentSTL)
finalTorusCentre=(centreTorusCalculationTotal/vertexCount)
centreKleinTotal1=(centreKleinTotal1/vertexCount)
centreKleinTotal2=(centreKleinTotal2/vertexCount)
#print("Final Total is "+str(centreTorusCalculationTotal)+" / "+str(vertexCount)+" = "+str(finalTorusCentre))
#print("Outer bounds are: lower - "+str(lowerLimit)+" upper - "+str(upperLimit))
upperDisFromCentre=upperLimit-finalTorusCentre
lowerDisFromCentre=finalTorusCentre-lowerLimit
#print(upperDisFromCentre)
#print(lowerDisFromCentre)
originDistanceStandard=max(upperDisFromCentre,lowerDisFromCentre)
originCoord=finalTorusCentre+(max(upperDisFromCentre,lowerDisFromCentre)*originDistance)
#print("Final coords of origin (rotateAxis, w) are ("+str(originCoord)+", 0)")
frameCount=0
#print(len(frameArray))
degreesPerFrame=360/(len(frameArray)-1)
#print(degreesPerFrame)
for frame in frameArray:
    #print(frameCount)
    degreesThisFrame=frameCount*degreesPerFrame
    radiansThisFrame=(degreesThisFrame*(math.pi))/180
    #print(degreesThisFrame)
    for triangle in frame:
        for vertex in triangle:
            #print("START VERTEX")
            #print(vertex)
            #print(frameCount)
            swapValue=vertex[substituteAxis]
            #print("DEGREES ARE "+(str(degreesThisFrame)))
            #print("Radians "+str(radiansThisFrame))
            origin=[originCoord,0]
            point=[swapValue,0]
            swapCoord = origin[0] + cos(radiansThisFrame) * (point[0] - origin[0]) - sin(radiansThisFrame) * (point[1] - origin[1])
            wCoord = origin[1] + sin(radiansThisFrame) * (point[0] - origin[0]) + cos(radiansThisFrame) * (point[1] - origin[1])

            origin=[centreKleinTotal1,centreKleinTotal2]
            point=[vertex[allSpatialAxes[0]],vertex[allSpatialAxes[1]]]

            remainingSpatialCoord1 = origin[0] + cos(radiansThisFrame*kleinFlip) * (point[0] - origin[0]) - sin(radiansThisFrame*kleinFlip) * (point[1] - origin[1])
            remainingSpatialCoord2 = origin[1] + sin(radiansThisFrame*kleinFlip) * (point[0] - origin[0]) + cos(radiansThisFrame*kleinFlip) * (point[1] - origin[1])

            #print("Swap - W")
            #print(f'{swapCoord:.7f}')
            #print(f'{wCoord:.7f}')
            vertex[substituteAxis]=swapCoord
            vertex.append(wCoord)
            vertex[allSpatialAxes[0]]=remainingSpatialCoord1
            vertex[allSpatialAxes[1]]=remainingSpatialCoord2
            #print("NOW SWAPPED FULL VERTEX")
            #print(vertex)
    frameCount=frameCount+1

currentFrameInt=0
for frame in frameArray:
    if (currentFrameInt!=0):
        triangleInt=0
        for triangle in frame:
            spl4.write("prism start\n")
            spl4.write("vertex "+str([ '%.7f' % elem for elem in frameArray[currentFrameInt-1][triangleInt][0] ])[1:-1].replace("'","").replace(",","")+"\n")
            spl4.write("vertex "+str([ '%.7f' % elem for elem in frameArray[currentFrameInt-1][triangleInt][1] ])[1:-1].replace("'","").replace(",","")+"\n")
            spl4.write("vertex "+str([ '%.7f' % elem for elem in frameArray[currentFrameInt-1][triangleInt][2] ])[1:-1].replace("'","").replace(",","")+"\n")
            spl4.write("vertex "+str([ '%.7f' % elem for elem in frameArray[currentFrameInt][triangleInt][0] ])[1:-1].replace("'","").replace(",","")+"\n")
            spl4.write("vertex "+str([ '%.7f' % elem for elem in frameArray[currentFrameInt][triangleInt][1] ])[1:-1].replace("'","").replace(",","")+"\n")
            spl4.write("vertex "+str([ '%.7f' % elem for elem in frameArray[currentFrameInt][triangleInt][2] ])[1:-1].replace("'","").replace(",","")+"\n")
            triangleInt=triangleInt+1
    currentFrameInt=currentFrameInt+1