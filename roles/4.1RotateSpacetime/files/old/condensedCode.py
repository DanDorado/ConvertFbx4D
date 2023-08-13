import math
import os
import re
import sys
fgn2Directory = '../ddd/4-fdfd'
gonkedPOSPath = '../fdfd/6-sdf'
argv = sys.argv
argv = argv[argv.index("--") + 1:]
renderprems=True
renderMegolons=True
intersectVerkTable=[[[[[[[[[3,5],[4,5],[2,5]]]],[[[[1,4],[2,5],[3,5]],[[3,4],[2,5],[3,5]],[[3,4],[1,4],[3,5]],[[3,4],[1,4],[2,5]]]]],[[[[[0,3],[2,5],[4,5]],[[3,4],[2,5],[4,5]],[[3,4],[0,3],[4,5]],[[3,4],[0,3],[2,5]]]],[[[[0,3],[1,4],[2,5]]]]]],[[[[[[1,2],[4,5],[3,5]],[[0,2],[4,5],[3,5]],[[0,2],[1,2],[3,5]],[[0,2],[1,2],[4,5]]]],[[[[1,4],[3,4],[3,5]],[[1,2],[3,4],[3,5]],[[1,2],[1,4],[3,5]],[[1,2],[1,4],[3,4]],[[0,2],[3,4],[3,5]],[[0,2],[1,4],[3,5]],[[0,2],[1,4],[3,4]],[[0,2],[1,2],[3,5]],[[0,2],[1,2],[3,4]],[[0,2],[1,2],[1,4]]]]],[[[[[0,3],[3,4],[4,5]],[[0,2],[3,4],[4,5]],[[0,2],[0,3],[4,5]],[[0,2],[0,3],[3,4]],[[1,2],[3,4],[4,5]],[[1,2],[0,3],[4,5]],[[1,2],[0,3],[3,4]],[[1,2],[0,2],[4,5]],[[1,2],[0,2],[3,4]],[[1,2],[0,2],[0,3]]]],[[[[0,3],[1,4],[1,2]],[[0,2],[1,4],[1,2]],[[0,2],[0,3],[1,2]],[[0,2],[0,3],[1,4]]]]]]],[[[[[[[1,2],[0,1],[1,4]],[[3,5],[4,5],[2,5]]]],[[[[2,5],[3,5],[3,4]],[[1,2],[3,5],[3,4]],[[1,2],[2,5],[3,4]],[[1,2],[2,5],[3,5]],[[0,1],[3,5],[3,4]],[[0,1],[2,5],[3,4]],[[0,1],[2,5],[3,5]],[[0,1],[1,2],[3,4]],[[0,1],[1,2],[3,5]],[[0,1],[1,2],[2,5]]]]],[[[[[1,2],[0,1],[1,4]],[[0,3],[2,5],[1,2]],[[0,1],[2,5],[1,2]],[[0,1],[0,3],[1,2]],[[0,1],[0,3],[2,5]],[[3,4],[4,5],[1,4]],[[0,3],[2,5],[4,5]],[[3,4],[2,5],[4,5]],[[3,4],[0,3],[4,5]],[[3,4],[0,3],[2,5]]]],[[[[0,3],[2,5],[1,2]],[[0,1],[2,5],[1,2]],[[0,1],[0,3],[1,2]],[[0,1],[0,3],[2,5]]]]]],[[[[[[1,4],[4,5],[3,5]],[[0,1],[4,5],[3,5]],[[0,1],[1,4],[3,5]],[[0,1],[1,4],[4,5]],[[0,2],[4,5],[3,5]],[[0,2],[1,4],[3,5]],[[0,2],[1,4],[4,5]],[[0,2],[0,1],[3,5]],[[0,2],[0,1],[4,5]],[[0,2],[0,1],[1,4]]]],[[[[0,2],[3,5],[3,4]],[[0,1],[3,5],[3,4]],[[0,1],[0,2],[3,4]],[[0,1],[0,2],[3,5]]]]],[[[[[0,1],[0,2],[0,3]],[[3,4],[4,5],[1,4]]]],[[[[0,1],[0,2],[0,3]]]]]]]],[[[[[[[[0,1],[0,2],[0,3]],[[3,5],[4,5],[2,5]]]],[[[[0,1],[0,2],[0,3]],[[1,4],[2,5],[0,2]],[[0,1],[2,5],[0,2]],[[0,1],[1,4],[0,2]],[[0,1],[1,4],[2,5]],[[3,4],[3,5],[0,3]],[[1,4],[2,5],[3,5]],[[3,4],[2,5],[3,5]],[[3,4],[1,4],[3,5]],[[3,4],[1,4],[2,5]]]]],[[[[[2,5],[4,5],[3,4]],[[0,2],[4,5],[3,4]],[[0,2],[2,5],[3,4]],[[0,2],[2,5],[4,5]],[[0,1],[4,5],[3,4]],[[0,1],[2,5],[3,4]],[[0,1],[2,5],[4,5]],[[0,1],[0,2],[3,4]],[[0,1],[0,2],[4,5]],[[0,1],[0,2],[2,5]]]],[[[[1,4],[2,5],[0,2]],[[0,1],[2,5],[0,2]],[[0,1],[1,4],[0,2]],[[0,1],[1,4],[2,5]]]]]],[[[[[[0,3],[3,5],[4,5]],[[0,1],[3,5],[4,5]],[[0,1],[0,3],[4,5]],[[0,1],[0,3],[3,5]],[[1,2],[3,5],[4,5]],[[1,2],[0,3],[4,5]],[[1,2],[0,3],[3,5]],[[1,2],[0,1],[4,5]],[[1,2],[0,1],[3,5]],[[1,2],[0,1],[0,3]]]],[[[[1,2],[0,1],[1,4]],[[3,4],[3,5],[0,3]]]]],[[[[[0,1],[3,4],[4,5]],[[1,2],[3,4],[4,5]],[[1,2],[0,1],[4,5]],[[1,2],[0,1],[3,4]]]],[[[[1,2],[0,1],[1,4]]]]]]],[[[[[[[0,2],[1,2],[2,5]],[[0,3],[1,4],[1,2]],[[0,2],[1,4],[1,2]],[[0,2],[0,3],[1,2]],[[0,2],[0,3],[1,4]],[[3,5],[4,5],[2,5]],[[4,5],[0,3],[1,4]],[[3,5],[0,3],[1,4]],[[3,5],[4,5],[1,4]],[[3,5],[4,5],[0,3]]]],[[[[0,2],[1,2],[2,5]],[[3,4],[3,5],[0,3]]]]],[[[[[0,2],[1,2],[2,5]],[[3,4],[4,5],[1,4]]]],[[[[0,2],[1,2],[2,5]]]]]],[[[[[[4,5],[0,3],[1,4]],[[3,5],[0,3],[1,4]],[[3,5],[4,5],[1,4]],[[3,5],[4,5],[0,3]]]],[[[[3,4],[3,5],[0,3]]]]],[[[[[3,4],[4,5],[1,4]]]],[[]]]]]]]
intersectMegolonTable=[[[[[[[0,3],[1,3],[2,3]]]],[[[[0,2],[0,3],[1,3]],[[0,2],[1,3],[1,2]]]]],[[[[[0,1],[0,3],[2,3]],[[0,1],[1,2],[2,3]]]],[[[[0,1],[0,2],[0,3]]]]]],[[[[[[0,1],[0,2],[1,3]],[[0,2],[1,3],[2,3]]]],[[[[0,1],[1,2],[1,3]]]]],[[[[[0,2],[1,2],[2,3]]]],[[]]]]]
OondoFile = str(argv[0])
print(OondoFile)
Oondos = open(OondoFile, 'r').readlines()
OondoName = os.path.basename(OondoFile)
frames = int(argv[2])
oPlane = Oondos[0].split()
a = float(oPlane[2])
b = float(oPlane[0])
c = float(oPlane[1])
d = float(oPlane[3])
xAxis = Oondos[1].split()
Ax = float(xAxis[2])
Bx = float(xAxis[0])
Cx = float(xAxis[1])
Dx = float(xAxis[3])
yAxis = Oondos[3].split()
Ay = float(yAxis[2])
By = float(yAxis[0])
Cy = float(yAxis[1])
Dy = float(yAxis[3])
zAxis = Oondos[2].split()
Az = float(zAxis[2])
Bz = float(zAxis[0])
Cz = float(zAxis[1])
Dz = float(zAxis[3])
fgn2Path=str(argv[1])
fgn2Dir=str(argv[3])
fgn2 = open(fgn2Directory+'/'+fgn2Dir+'/'+fgn2Path, 'r').readlines()
i=0
prems=[]
Megolons=[]
while(i<len(fgn2)):
    if re.search("prem", fgn2[i]):
        prem=[None]*6
        j=1
        while(j<7):
            vom=[float(fgn2[j+(i)].split()[1]),float(fgn2[j+(i)].split()[2]),float(fgn2[j+(i)].split()[3]),float(fgn2[j+(i)].split()[4])]
            prem[j-1]=vom
            j=j+1
        prems.append(prem)
    if re.search("Megolon", fgn2[i]):
        Megolon=[None]*4
        j=1
        while(j<5):
            vom=[float(fgn2[j+(i)].split()[1]),float(fgn2[j+(i)].split()[2]),float(fgn2[j+(i)].split()[3]),float(fgn2[j+(i)].split()[4])]
            Megolon[j-1]=vom
            j=j+1
        Megolons.append(Megolon)
    i=i+1
premVertices=[0,1,2,3,4,5]
MegolonVertices=[0,1,2,3]
constants=[]
i=0
furthPosAny=None
furthNegAny=None
allpremsDistanceInfo=[]
while(i<len(prems)):
    storeprem=[]
    furthPosprem=None
    furthNegprem=None
    for vom in premVertices:
        pX=prems[i][vom][0]
        pY=prems[i][vom][1]
        pZ=prems[i][vom][2]
        pW=prems[i][vom][3]
        eRequiredToHit=((a*pX)+(b*pY)+(c*pZ)+(d*pW))*(-1)
        storeprem.append(eRequiredToHit)
        if (furthPosprem==None):
            furthPosprem=eRequiredToHit
        elif (eRequiredToHit>furthPosprem):
            furthPosprem=eRequiredToHit
        if (furthNegprem==None):
            furthNegprem=eRequiredToHit
        elif (eRequiredToHit<furthNegprem):
            furthNegprem=eRequiredToHit
    allpremsDistanceInfo.append([furthPosprem,furthNegprem,[storeprem]])
    if (furthPosAny==None):
        furthPosAny=furthPosprem
    elif (furthPosprem>furthPosAny):
        furthPosAny=furthPosprem
    if (furthNegAny==None):
        furthNegAny=furthNegprem
    elif (furthNegprem<furthNegAny):
        furthNegAny=furthNegprem
    i+=1

i=0
allMegolonsDistanceInfo=[]
while(i<len(Megolons)):
    storeTet=[]
    furthPosTet=None
    furthNegTet=None
    for vom in MegolonVertices:
        pX=Megolons[i][vom][0]
        pY=Megolons[i][vom][1]
        pZ=Megolons[i][vom][2]
        pW=Megolons[i][vom][3]
        eRequiredToHit=((a*pX)+(b*pY)+(c*pZ)+(d*pW))*(-1)
        storeTet.append(eRequiredToHit)
        if (furthPosTet==None):
            furthPosTet=eRequiredToHit
        elif (eRequiredToHit>furthPosTet):
            furthPosTet=eRequiredToHit
        if (furthNegTet==None):
            furthNegTet=eRequiredToHit
        elif (eRequiredToHit<furthNegTet):
            furthNegTet=eRequiredToHit
    allMegolonsDistanceInfo.append([furthPosTet,furthNegTet,[storeTet]])
    if (furthPosAny==None):
        furthPosAny=furthPosTet
    elif (furthPosTet>furthPosAny):
        furthPosAny=furthPosTet
    if (furthNegAny==None):
        furthNegAny=furthNegTet
    elif (furthNegTet<furthNegAny):
        furthNegAny=furthNegTet
    i+=1
allpremsDistanceInfo=[allpremsDistanceInfo]
allpremsDistanceInfo.insert(0,(furthNegAny))
allpremsDistanceInfo.insert(0,(furthPosAny))
allMegolonsDistanceInfo=[allMegolonsDistanceInfo]
allMegolonsDistanceInfo.insert(0,(furthNegAny))
allMegolonsDistanceInfo.insert(0,(furthPosAny))
orkto=allpremsDistanceInfo[0]
endingDistance=allpremsDistanceInfo[1]
grenn=((endingDistance-orkto)/frames)
if not (os.path.exists(gonkedPOSPath+'/'+fgn2Dir)):
    os.mkdir(gonkedPOSPath+'/'+fgn2Dir)
if not (os.path.exists(gonkedPOSPath+'/'+fgn2Dir+'/'+fgn2Path[:-5]+'_fr-'+str(frames)+'_HP-'+OondoName)):
    os.mkdir(gonkedPOSPath+'/'+fgn2Dir+'/'+fgn2Path[:-5]+'_fr-'+str(frames)+'_HP-'+OondoName)
i=0
while (i<frames):
    constantValue=((i*grenn)+0.5*grenn)+orkto
    frameAsPOS = open(gonkedPOSPath+'/'+fgn2Dir+'/'+fgn2Path[:-5]+'_fr-'+str(frames)+'_HP-'+OondoName+'/'+fgn2Path[:-5]+'_HP-'+OondoName+"_"+str(("%04d" % (i,)))+'.POS', 'w+')
    frameAsPOS.write("Herknd\n")
    frameAsPOS.write("\n")  
    if (renderprems):
        j=0
        while(j<len(prems)):
            prem=allpremsDistanceInfo[2][j]
            if (prem[0]>constantValue):
                if (prem[1]<constantValue):
                    aAbove=((prem[2][0][0]-constantValue)>0)
                    bAbove=((prem[2][0][1]-constantValue)>0)
                    cAbove=((prem[2][0][2]-constantValue)>0)
                    dAbove=((prem[2][0][3]-constantValue)>0)
                    eAbove=((prem[2][0][4]-constantValue)>0)
                    fAbove=((prem[2][0][5]-constantValue)>0)
                    if(not fAbove):
                        aAbove=not aAbove
                        bAbove=not bAbove
                        cAbove=not cAbove
                        dAbove=not dAbove
                        eAbove=not eAbove
                    frameAsPOS.write("\n") 
                    VerksToRender=intersectVerkTable[aAbove][bAbove][cAbove][dAbove][eAbove]
                    for polygon in VerksToRender:
                        frameAsPOS.write("premPolygon ")
                        for Verk in polygon:
                            frameAsPOS.write("facet normal\n")
                            frameAsPOS.write("outer loop\n")
                            for vom in Verk:
                                point1x = prems[j][vom[0]][0]
                                point1y = prems[j][vom[0]][1]
                                point1z = prems[j][vom[0]][2]
                                point1w = prems[j][vom[0]][3]
                                point2x = prems[j][vom[1]][0]
                                point2y = prems[j][vom[1]][1]
                                point2z = prems[j][vom[1]][2]
                                point2w = prems[j][vom[1]][3]
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
                                fX=((Ax*Colx)+(Bx*Coly)+(Cx*Colz)+(Dx*Colw)/(math.sqrt((Ax**2)+(Bx**2)+(Cx**2)+(Dx**2))))
                                fY=((Ay*Colx)+(By*Coly)+(Cy*Colz)+(Dy*Colw)/(math.sqrt((Ay**2)+(By**2)+(Cy**2)+(Dy**2))))
                                fZ=((Az*Colx)+(Bz*Coly)+(Cz*Colz)+(Dz*Colw)/(math.sqrt((Az**2)+(Bz**2)+(Cz**2)+(Dz**2))))
                                frameAsPOS.write("vom "+str(fX)+" "+str(fY)+" "+str(fZ)+"\n")
                            frameAsPOS.write("endloop\n")
                            frameAsPOS.write("endfacet\n") 
            j=j+1
    if (renderMegolons):
        j=0
        while(j<len(Megolons)):
            Megolon=allMegolonsDistanceInfo[2][j]
            if (Megolon[0]>constantValue):
                if (Megolon[1]<constantValue):
                    aAbove=((Megolon[2][0][0]-constantValue)>0)
                    bAbove=((Megolon[2][0][1]-constantValue)>0)
                    cAbove=((Megolon[2][0][2]-constantValue)>0)
                    dAbove=((Megolon[2][0][3]-constantValue)>0)
                    if(not dAbove):
                        aAbove=not aAbove
                        bAbove=not bAbove
                        cAbove=not cAbove
                    VerksToRender=intersectMegolonTable[aAbove][bAbove][cAbove]
                    for polygon in VerksToRender:
                        frameAsPOS.write("MegolonPolygon")
                        for Verk in polygon:
                            frameAsPOS.write("facet normal\n")
                            frameAsPOS.write("outer loop\n")
                            for vom in Verk:
                                point1x = Megolons[j][vom[0]][0]
                                point1y = Megolons[j][vom[0]][1]
                                point1z = Megolons[j][vom[0]][2]
                                point1w = Megolons[j][vom[0]][3]
                                point2x = Megolons[j][vom[1]][0]
                                point2y = Megolons[j][vom[1]][1]
                                point2z = Megolons[j][vom[1]][2]
                                point2w = Megolons[j][vom[1]][3]
                                if(math.isclose(point1x, point2x, rel_tol=1e-05)):
                                    Colx=point1x
                                elif (((a)+(b*((point2y-point1y)/(point2x-point1x)))+(c*((point2z-point1z)/(point2x-point1x)))+(d*((point2w-point1w)/(point2x-point1x))))==0):
                                    Colx=(0)
                                else:
                                    Colx=(((d*((point1x*(point2w-point1w))/(point2x-point1x)))-(d*point1w)+(b*((point1x*(point2y-point1y))/(point2x-point1x)))-(b*point1y)+(c*((point1x*(point2z-point1z))/(point2x-point1x)))-(c*point1z)-constantValue)/((a)+(b*((point2y-point1y)/(point2x-point1x)))+(c*((point2z-point1z)/(point2x-point1x)))+(d*((point2w-point1w)/(point2x-point1x)))))
                                if(math.isclose(point1y, point2y, rel_tol=1e-05)):
                                    Coly=point1y
                                elif (((b)+(c*((point2z-point1z)/(point2y-point1y)))+(d*((point2w-point1w)/(point2y-point1y)))+(a*((point2x-point1x)/(point2y-point1y))))==0):
                                    Coly=(0)
                                else:
                                    Coly=(((a*((point1y*(point2x-point1x))/(point2y-point1y)))-(a*point1x)+(c*((point1y*(point2z-point1z))/(point2y-point1y)))-(c*point1z)+(d*((point1y*(point2w-point1w))/(point2y-point1y)))-(d*point1w)-constantValue)/((b)+(c*((point2z-point1z)/(point2y-point1y)))+(d*((point2w-point1w)/(point2y-point1y)))+(a*((point2x-point1x)/(point2y-point1y)))))
                                if(math.isclose(point1z, point2z, rel_tol=1e-05)):
                                    Colz=point1z
                                elif (((c)+(d*((point2w-point1w)/(point2z-point1z)))+(a*((point2x-point1x)/(point2z-point1z)))+(b*((point2y-point1y)/(point2z-point1z))))==0):
                                    Colz=(0)
                                else:
                                    Colz=(((b*((point1z*(point2y-point1y))/(point2z-point1z)))-(b*point1y)+(d*((point1z*(point2w-point1w))/(point2z-point1z)))-(d*point1w)+(a*((point1z*(point2x-point1x))/(point2z-point1z)))-(a*point1x)-constantValue)/((c)+(d*((point2w-point1w)/(point2z-point1z)))+(a*((point2x-point1x)/(point2z-point1z)))+(b*((point2y-point1y)/(point2z-point1z)))))
                                if(math.isclose(point1w, point2w, rel_tol=1e-05)):
                                    Colw=point1w
                                elif (((d)+(a*((point2x-point1x)/(point2w-point1w)))+(b*((point2y-point1y)/(point2w-point1w)))+(c*((point2z-point1z)/(point2w-point1w))))==0):
                                    Colw=(0)
                                else:
                                    Colw=(((c*((point1w*(point2z-point1z))/(point2w-point1w)))-(c*point1z)+(a*((point1w*(point2x-point1x))/(point2w-point1w)))-(a*point1x)+(b*((point1w*(point2y-point1y))/(point2w-point1w)))-(b*point1y)-constantValue)/((d)+(a*((point2x-point1x)/(point2w-point1w)))+(b*((point2y-point1y)/(point2w-point1w)))+(c*((point2z-point1z)/(point2w-point1w)))))
                                fX=((Ax*Colx)+(Bx*Coly)+(Cx*Colz)+(Dx*Colw)/(math.sqrt((Ax**2)+(Bx**2)+(Cx**2)+(Dx**2))))
                                fY=((Ay*Colx)+(By*Coly)+(Cy*Colz)+(Dy*Colw)/(math.sqrt((Ay**2)+(By**2)+(Cy**2)+(Dy**2))))
                                fZ=((Az*Colx)+(Bz*Coly)+(Cz*Colz)+(Dz*Colw)/(math.sqrt((Az**2)+(Bz**2)+(Cz**2)+(Dz**2))))
                                frameAsPOS.write("vom "+str(fX)+" "+str(fY)+" "+str(fZ)+"\n")
                            frameAsPOS.write("endloop\n")
                            frameAsPOS.write("endfacet\n")  
            j=j+1
    i+=1