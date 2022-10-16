# Import basic modules
import math
import os
import sys

# Get the arguments and save as strings
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
print(argv)


######## Generate full axes for each hyperplane ##########

hyperplaneFile = str(argv[0])
print(hyperplaneFile)
nFile = open(hyperplaneFile, 'r').readlines()[0].split()

print()
print("Generating for  "+hyperplaneFile)
print()

a = float(nFile[0])
b = float(nFile[1])
c = float(nFile[2])
d = float(nFile[3])

# Get the vector perpendicular to the y axis

Ay=(-a*b)
By=(a**2+c**2+d**2)
Cy=(-c*b)
Dy=(-d*b)


print("Vector perpendicular to the y axis")

print(str(Ay))
print(str(By))
print(str(Cy))
print(str(Dy))
print()

# Get the vector perpendicular to the x axis

Ax=1
Bx=0
Cx=((-a-d)/c)
Dx=1

print("Vector perpendicular to the x axis")

print(str(Ax))
print(str(Bx))
print(str(Cx))
print(str(Dx))
print()

# Get the vector perpendicular to the z axis

print("Vector perpendicular to the z axis")

Az=1
Bz=0
Cz=(c*(d-a))/(d*(a+d)+c**2)
Dz=(-(a*d)-(a**2)-(c**2))/((d*(a+d))+(c**2))

print(str(Az))
print(str(Bz))
print(str(Cz))
print(str(Dz))
print()



# These checks are disabled since I believe everything is working.
# We know that two lines/planes/hyperplanes are orthagonal if the sum of the products of their axis-vectors is 0
# I run 6 checks, for each axes (which corresponds to a rotation)
#
#print("Checking XY / XZ / YZ orthanoganality")
#print()
#
#
#print("Checking XY")
#print(str(f'{Ax*Ay:f}'))
#print(str(f'{Bx*By:f}'))
#print(str(f'{Cx*Cy:f}'))
#print(str(f'{Dx*Dy:f}'))
#print("Checking")
#print(str(f'{Ax*Ay+Bx*By+Cx*Cy+Dx*Dy:f}'))
#print()
#
#print("Checking XZ")
#print(str(f'{Ax*Az:f}'))
#print(str(f'{Bx*Bz:f}'))
#print(str(f'{Cx*Cz:f}'))
#print(str(f'{Dx*Dz:f}'))
#print("Checking")
#print(str(f'{Ax*Az+Bx*Bz+Cx*Cz+Dx*Dz:f}'))
#print()
#
#print("Checking YZ")
#print(str(f'{Az*Ay:f}'))
#print(str(f'{Bz*By:f}'))
#print(str(f'{Cz*Cy:f}'))
#print(str(f'{Dz*Dy:f}'))
#print("Checking")
#print(str(f'{Az*Ay+Bz*By+Cz*Cy+Dz*Dy:f}'))
#print()        
#
#
#print("Checking XO")
#print(str(f'{Ax*a:f}'))
#print(str(f'{Bx*b:f}'))
#print(str(f'{Cx*c:f}'))
#print(str(f'{Dx*d:f}'))
#print("Checking")
#print(str(f'{Ax*a+Bx*b+Cx*c+Dx*d:f}'))
#print()
#
#print("Checking YO")
#print(str(f'{Ay*a:f}'))
#print(str(f'{By*b:f}'))
#print(str(f'{Cy*c:f}'))
#print(str(f'{Dy*d:f}'))
#print("Checking")
#print(str(f'{Ay*a+By*b+Cy*c+Dy*d:f}'))
#print()
#
#print("Checking ZO")
#print(str(f'{Az*a:f}'))
#print(str(f'{Bz*b:f}'))
#print(str(f'{Cz*c:f}'))
#print(str(f'{Dz*d:f}'))
#print("Checking")
#print(str(f'{Az*a+Bz*b+Cz*c+Dz*d:f}'))
#print()

#Normalize each set of axes
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



# Set the axes we need to save
oPlane=[a,b,c,d]
xAxis=[Ax,Bx,Cx,Dx]
yAxis=[Ay,By,Cy,Dy]
zAxis=[Az,Bz,Cz,Dz]

writeThings=[oPlane,xAxis,yAxis,zAxis]

#Save as the final file, which adds the axes to the hyperplane file
nFile = open(hyperplaneFile, 'w+')

for parts in writeThings:
    for part in parts:
        print(f'{part:f}')
        nFile.write(str(f'{part:f}')+' ')
    nFile.write("\n")

nFile.close()