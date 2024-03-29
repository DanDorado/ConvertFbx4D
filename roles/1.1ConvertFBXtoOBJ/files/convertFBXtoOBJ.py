
## Command to make the file run ##
#
# sudo '../../../mnt/c/Program Files/Blender Foundation/Blender 3.2/blender.exe'  -b -P importscript.py -- 1 1
#
## ARGV ##
#ARGV[0] - The file passed in to convert into obj files
#

# Import yhe needed modules (bpy is Blender)
import bpy
import math
import os
import re
import sys


#
## Values that could change ##
# save/load .obj files to/from
objDirectory = '../processFiles/2-FBXintoOBJ'


# Get the arguments and save as strings
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
#print(argv)


# delete starting objects generated by Blender by Default
#print("Deleting Starting Objects")
#print("")
startingObjects = ["Light", "Camera"]
for obj in startingObjects:
    bpy.data.objects[obj].select_set(True)    
    bpy.context.view_layer.objects.active = bpy.data.objects[obj]
bpy.ops.object.delete()

print("PRINT")
print(argv[0])

######## Convert fbx to Obj ##########

#print("beginning to convert fbx files to obj frames.")
# For each fbx animation.
fbxFile = argv[0]
# checking if it is a file
if os.path.isfile(fbxFile):
    print("Beginning import of "+fbxFile)
    # Import FBX into the scene
    bpy.ops.import_scene.fbx(filepath=fbxFile)

# Make sure nothing selected
bpy.ops.object.select_all(action='DESELECT')

# Make sure that the scene only contains frames of actual animation for your fbx
if bpy.data.actions:
    #print("Trimming Frames")
    # get all actions
    action_list = [action.frame_range for action in bpy.data.actions]
    # sort, remove doubles and create a set
    keys = (sorted(set([item for sublist in action_list for item in sublist])))
    # #print first and last keyframe
    print ("{} {}".format("first keyframe:", keys[0]))
    print ("{} {}".format("last keyframe:", keys[-1]))
    # set the frames to fit
    bpy.data.scenes[0].frame_start = int(keys[0])
    bpy.data.scenes[0].frame_end = int(keys[-1])
else:
    print ("no actions for frames")

# Get everything imported
objects = bpy.context.scene.objects
#print("Now exporting frames as obj")
for obj in objects:
    # Make sure nothing else selected
    bpy.ops.object.select_all(action='DESELECT')
    objectToSelect = obj
    print("Considering "+obj.name)
    objectToSelect.select_set(True)
    # Check if the frame contains the Armature name using regex
    if re.search("Armature", obj.name):
        print(obj.name+" is going to be used.")
        # If so create a directory for the animation and export it
        bpy.context.view_layer.objects.active = obj
        newpath = objDirectory+"/"+obj.name 
        if not os.path.exists(newpath):
            os.makedirs(newpath)   
        bpy.context.view_layer.objects.active = objectToSelect
        bpy.ops.export_scene.obj(filepath=newpath+"/"+obj.name+".obj",use_animation=True)