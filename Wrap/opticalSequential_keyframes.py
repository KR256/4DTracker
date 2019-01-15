import os
import sys
import json

#KEYFRAMES = [1,25,27,29,31,33,35,37,39,45,60,70,73,76,80,82,84,86,88]
KEYFRAMES = [88,94,96,98,100,102,104,106,108,110,112,115,120,130,150,153,155,157,159,161,165,170]
#KEYFRAMES.reverse()

INPUT_WRAP_FILE = 'G:\\results\\fullSequence\optiwrapKeyframes_legacy.wrap'
OUTPUT_WRAP_FILE = 'G:\\results\\fullSequence\optiwrapKeyframes_legacy_temp.wrap'


MESH_TARGET = 'G:/20181113-CubicMotion-RC-Meshes-PNG/meshes/Frame%06i.obj'
TARGET_TEXTURE = 'G:/20181113-CubicMotion-RC-Meshes-PNG/textures-png/Frame%06i_u1_v1.png'

IN_MESH = 'G:\\results\\fullSequence\sneer_0170\opti_interpolation/frame.%04i.obj'
IN_MESH_TEXTURE = 'G:\\results\\fullSequence\sneer_0170\opti_interpolation/frame.%04i.jpg'

OUT_MESH = 'G:\\results\\fullSequence\sneer_0170\opti_interpolation/frame.%04i.obj'
OUT_MESH_TEXTURE = 'G:\\results\\fullSequence\sneer_0170\opti_interpolation/frame.%04i.jpg'

POLYGON_FILE = 'G:/results/wrapTests/mask_5k_optical.txt'


for i,k in enumerate(KEYFRAMES):

    if i == 0:
        continue

    with open(INPUT_WRAP_FILE) as json_data:
        d = json.load(json_data)

    targetFrame = k
    lastFrame = KEYFRAMES[i-1]

    # Set paths for Input and Output meshes

    d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(IN_MESH % lastFrame)]
    d['nodes']['LoadImage01']['params']['fileNames']['value'] = [unicode(OUT_MESH_TEXTURE % lastFrame)]
    d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(MESH_TARGET % targetFrame)]
    d['nodes']['LoadImage02']['params']['fileNames']['value'] = [unicode(TARGET_TEXTURE % targetFrame)]
    d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH % targetFrame)
    d['nodes']['SaveImage01']['params']['fileName']['value'] = unicode(OUT_MESH_TEXTURE % targetFrame)

    d['nodes']['SelectPolygons01']['params']['fileName']['value'] = unicode(POLYGON_FILE)

    # Save JSON file
    with open(OUTPUT_WRAP_FILE, 'w') as outfile:
        json.dump(d, outfile)

    # Run Wrap node script for frame
    print("Reconstructing Frame %d: %s" % (targetFrame, (MESH_TARGET % targetFrame)))
    cmd = "wrap3cmd compute %s" % OUTPUT_WRAP_FILE
    os.system(cmd)

    d = None # Delete all node data
