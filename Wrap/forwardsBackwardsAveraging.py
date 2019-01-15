import os
import sys
import json
from shutil import copyfile


START_FRAME = 1
END_FRAME = 88

INPUT_WRAP_FILE = 'G:\\results\\fullSequence\\forwardBackwardsAveraging.wrap'
OUTPUT_WRAP_FILE = 'G:\\results\\fullSequence\\forwardBackwardsAveraging_Temp.wrap'

IN_MESH = 'G:\\results\\fullSequence\smile_0088\\opti_interpolation\\frame.%04i.obj'
TARGET_MESH_FORWARDS = 'G:\\results\\fullSequence\smile_0088\\opti_interpolation\\frame.%04i.obj'
TARGET_MESH_BACKWARDS = 'G:\\results\\fullSequence\smile_0088\\opti_interpolation\\frame_backwards.%04i.obj'

OUT_MESH = 'G:\\results\\fullSequence\smile_0088\\opti_interpolation\\frame_averaged.%04i.obj'

FRAME_WEIGHT = 1 / float(END_FRAME - START_FRAME - 1)

upWeight = 0.0
downWeight = 1.0

for i in range(START_FRAME, END_FRAME):


    with open(INPUT_WRAP_FILE) as json_data:
        d = json.load(json_data)

    upWeight = upWeight + FRAME_WEIGHT
    downWeight = downWeight - FRAME_WEIGHT

    d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(IN_MESH % i)]
    d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(TARGET_MESH_FORWARDS % (i+1))]
    d['nodes']['LoadGeom03']['params']['fileNames']['value'] = [unicode(TARGET_MESH_BACKWARDS % (i + 1))]

    d['nodes']['Blendshapes01']['params']['weights']['value'][0]['value'] = downWeight
    d['nodes']['Blendshapes01']['params']['weights']['value'][1]['value'] = upWeight
    d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH % (i+1))





    # Save JSON file
    with open(OUTPUT_WRAP_FILE, 'w') as outfile:
        json.dump(d, outfile)

    # Run Wrap node script for frame
    print("Reconstructing Frame %d: %s" % (i+1, OUT_MESH % (i+1)))
    # os.chdir("C:\kyleBathStuff\Wrap3.4.2_Portable\Wrap3.4.2")
    cmd = "wrap3cmd compute %s" % OUTPUT_WRAP_FILE
    os.system(cmd)

    d = None # Delete all node data
