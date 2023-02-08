# python3 convertStlsToSpl4.py -- Hollow                         (or other)

import os
import re
import sys

stlDirectory = '../processFiles/3-OBJintoSTL'
spl4Directory = '../processFiles/4-STLintoSPL4'

argv = sys.argv[sys.argv.index("--") + 1:]
wAxisInc = float(argv[1])

subdir = argv[0]
spl4_file = os.path.join(spl4Directory, subdir, f"{subdir}_HP_w-{argv[1]}.spl4")
stlFrames = sorted(os.listdir(os.path.join(stlDirectory, subdir)))
stl2 = open(os.path.join(stlDirectory, subdir, stlFrames[0]), 'r').readlines()

with open(spl4_file, 'w+') as spl4:
    depth = 0
    for i in range(len(stlFrames) - 1):
        stl1 = stl2
        stl2 = open(os.path.join(stlDirectory, subdir, stlFrames[i+1]), 'r').readlines()
        for j in range(len(stl1)):
            if re.search("outer loop", stl1[j]):
                spl4.write("prism start\n")
                spl4.write(f"{stl1[j+1][:-1]} {depth * wAxisInc}\n")
                spl4.write(f"{stl1[j+2][:-1]} {depth * wAxisInc}\n")
                spl4.write(f"{stl1[j+3][:-1]} {depth * wAxisInc}\n")
                spl4.write(f"{stl2[j+1][:-1]} {(depth+1) * wAxisInc}\n")
                spl4.write(f"{stl2[j+2][:-1]} {(depth+1) * wAxisInc}\n")
                spl4.write(f"{stl2[j+3][:-1]} {(depth+1) * wAxisInc}\n")
        depth += 1