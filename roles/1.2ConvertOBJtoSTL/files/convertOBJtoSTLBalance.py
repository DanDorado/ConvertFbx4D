
## Command to make the file run ##
#
# sudo '../../../mnt/c/Program Files/Blender Foundation/Blender 3.2/blender.exe'  -b -P importscript.py -- 1 1
#
## ARGV ##
#ARGV[0] - The file passed in to convert into obj files
#

# Import the needed modules (bpy is Blender)
import bpy
import os
import sys


#
## Values that could change ##
# Set directory to save/load .obj files to/from
stlDirectory = '../processFiles/3-OBJintoSTL'

# Get command line arguments
argv = sys.argv[sys.argv.index("--") + 1:]
timesToRepeat = int(argv[2])

# Delete default objects in Blender scene
bpy.data.objects["Light"].select_set(True)
bpy.data.objects["Camera"].select_set(True)
bpy.ops.object.delete()


######## Convert obj to stl ##########

# Import OBJ file
objFile = argv[0]
if os.path.isfile(objFile):
    bpy.ops.import_scene.obj(filepath=objFile)

# Deselect all objects
bpy.ops.object.select_all(action='DESELECT')

# Get imported objects
objects = bpy.context.scene.objects

# Export each object as STL multiple times
for obj in objects:
    # Remove underscores from the object name
    new_name = obj.name.replace("_", "")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    newpath = stlDirectory+"/"+new_name+"_"+str(timesToRepeat)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    while (timesToRepeat>0):
        bpy.ops.export_mesh.stl(filepath = newpath + "/" + str(timesToRepeat) + "_" + argv[1][:-4] + ".stl", ascii=True, use_selection=True)
        timesToRepeat -= 1