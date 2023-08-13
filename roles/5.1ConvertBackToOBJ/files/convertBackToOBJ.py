
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
# Set directory to save/load .stl files to/from
stlDirectory = '../processFiles/6-RotatedSTLFiles'
finalPath = '../processFiles/7-rotatedOBJ'

# Get command line arguments
argv = sys.argv[sys.argv.index("--") + 1:]

# Delete default objects in Blender scene
bpy.data.objects["Light"].select_set(True)
bpy.data.objects["Camera"].select_set(True)
bpy.ops.object.delete()

######## Convert obj to stl ##########

# Import OBJ file
stlFile = argv[0]
if os.path.isfile(stlFile):
    print("FOUND STL\n\n\n")
    print(stlFile)
    bpy.ops.import_mesh.stl(filepath=stlFile)
    objects = bpy.context.scene.objects
    scene = bpy.context.scene
    selected = bpy.context.selected_objects
    meshes = [o for o in selected if o.type == 'MESH']
    for obj in meshes:
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.flip_normals()

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.import_mesh.stl(filepath=stlFile)
    objects = bpy.context.scene.objects
    bpy.ops.object.select_all(action='SELECT')

    scene = bpy.context.scene

    bpy.ops.object.select_all(action='SELECT')
    # print(endPath+"/DS"+os.path.basename(filename)[:-3]+"obj")

    if (argv[1] == "True"):
        directory_path = os.path.dirname(stlFile)
        final_subdir = os.path.basename(directory_path)
        if not os.path.exists(finalPath+"/"+final_subdir):
            os.makedirs(finalPath+"/"+final_subdir)
        bpy.ops.export_scene.obj(filepath=finalPath+"/"+final_subdir+"/"+os.path.basename(stlFile)[:-3]+"obj",use_selection=True)
    else:
        bpy.ops.export_scene.obj(filepath=finalPath+"/"+os.path.basename(stlFile)[:-3]+"obj",use_selection=True)
    bpy.ops.object.delete()
