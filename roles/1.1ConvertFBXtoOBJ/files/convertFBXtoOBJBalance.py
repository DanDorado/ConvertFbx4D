
## Command to make the file run ##
#
# sudo '../../../mnt/c/Program Files/Blender Foundation/Blender 3.2/blender.exe'  -b -P importscript.py -- 1 1
#
## ARGV ##
#ARGV[0] - The file passed in to convert into obj files
#

# Import yhe needed modules (bpy is Blender)
import bpy
import os
import re
import sys

# Values that could change
# save/load .obj files to/from
obj_directory = '../processFiles/2-FBXintoOBJ'

# Get the arguments and save as strings
argv = sys.argv[sys.argv.index("--") + 1:]
fbx_file = argv[0]

# Delete starting objects generated by Blender by default
starting_objects = ["Light", "Camera"]
for obj in starting_objects:
    bpy.data.objects[obj].select_set(True)
    bpy.ops.object.delete()

# Check if fbx file is valid
if not os.path.isfile(fbx_file):
    print("Invalid file")
    sys.exit()

# Import FBX into the scene
bpy.ops.import_scene.fbx(filepath=fbx_file)

# Get the range of frames of animation
if bpy.data.actions:
    action_list = [action.frame_range for action in bpy.data.actions]
    keys = sorted(set([item for sublist in action_list for item in sublist]))
    bpy.data.scenes[0].frame_start = int(keys[0])
    bpy.data.scenes[0].frame_end = int(keys[-1])
else:
    print("No actions for frames")
    sys.exit()

# Get all objects in the scene
objects = bpy.context.scene.objects

# Export frames as obj
for obj in objects:
    # Check if the frame contains the Armature name using regex
    if re.search("Armature", obj.name):
        # Remove underscores from the object name
        new_name = obj.name.replace("_", "")
        
        # If so, create a directory for the animation and export it
        newpath = obj_directory + "/" + new_name
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        bpy.context.view_layer.objects.active = obj
        bpy.ops.export_scene.obj(filepath=newpath + "/" + new_name + ".obj", use_animation=True)