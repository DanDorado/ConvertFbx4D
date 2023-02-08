
import math
import os
import sys

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

hyperplaneFile = str(argv[0])
nFile = open(hyperplaneFile, 'r').readlines()[0].split()


a = float(nFile[0])
b = float(nFile[1])
c = float(nFile[2])
d = float(nFile[3])

Ay=(-a*b)
By=(a**2+c**2+d**2)
Cy=(-c*b)
Dy=(-d*b)


Ax=1
Bx=0
Cx=((-a-d)/c)
Dx=1


Az=1
Bz=0
Cz=(c*(d-a))/(d*(a+d)+c**2)
Dz=(-(a*d)-(a**2)-(c**2))/((d*(a+d))+(c**2))



oLength=(math.sqrt((a**2)+(b**2)+(c**2)+(d**2)))
a=a/oLength
b=b/oLength
c=c/oLength
d=d/oLength

xLength=(math.sqrt((Ax**2)+(Bx**2)+(Cx**2)+(Dx**2)))
Ax=Ax/xLength
Bx=Bx/xLength
Cx=Cx/xLength
Dx=Dx/xLength

yLength=(math.sqrt((Ay**2)+(By**2)+(Cy**2)+(Dy**2)))
Ay=Ay/yLength
By=By/yLength
Cy=Cy/yLength
Dy=Dy/yLength

zLength=(math.sqrt((Az**2)+(Bz**2)+(Cz**2)+(Dz**2)))
Az=Az/zLength
Bz=Bz/zLength
Cz=Cz/zLength
Dz=Dz/zLength

oPlane=[a,b,c,d]
xAxis=[Ax,Bx,Cx,Dx]
yAxis=[Ay,By,Cy,Dy]
zAxis=[Az,Bz,Cz,Dz]

writeThings=[oPlane,xAxis,yAxis,zAxis]

nFile = open(hyperplaneFile, 'w+')

for parts in writeThings:
    for part in parts:
        nFile.write(str(f'{part:f}')+' ')
    nFile.write("\n")

nFile.close()