import os
import sys
import json

NUM_FRAMES = 119
START_FRAME = 1
INPUT_WRAP_FILE = 'C:\kyleBathStuff\Wrap\postAlignment.wrap'
OUTPUT_WRAP_FILE = 'C:\kyleBathStuff\Wrap\postAlignmentTemp.wrap'
MESH_SOURCE = 'C:/kyleBathStuff/Wrap/paddyHD1DivTrisRA/frame.%03d.obj'
MESH_TARGET_STATIC = 'C:/kyleBathStuff/Wrap/paddyHD1DivTrisRA/frame.001.obj'
OUT_MESH = 'C:/kyleBathStuff/Wrap/afterAlignment/paddyHD1DivTrisRA/frameRA.%03d.obj'

RIGID_ALIGNMENT_MARKERS = 'C:/kyleBathStuff/Wrap/templateMarkers/rigidAlignmentEarsTris'

# Creates meshes from frame2:NUM_FRAMES. Assumes first frame is manual.
for i in range(START_FRAME, START_FRAME + NUM_FRAMES):
    # Load example JSON wrap file saved from first frame
    with open(INPUT_WRAP_FILE) as json_data:
        d = json.load(json_data)

    # Set paths for Input and Output meshes
    d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(MESH_SOURCE % i)]
    d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(MESH_TARGET_STATIC)]
    d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH % i)

    # Set paths for Select Points and Polygons
    d['nodes']['SelectPoints01']['params']['fileNameLeft']['value'] = unicode(RIGID_ALIGNMENT_MARKERS)
    d['nodes']['SelectPoints01']['params']['fileNameRight']['value'] = unicode(RIGID_ALIGNMENT_MARKERS)

    # Remove previous marker coords
    d['nodes']['SelectPoints01']['params']['pointsLeft']['value'] = []
    d['nodes']['SelectPoints01']['params']['pointsRight']['value'] = []

    # Save JSON file
    with open(OUTPUT_WRAP_FILE, 'w') as outfile:
        json.dump(d, outfile)

    # Run Wrap node script for frame
    print("Aligning Frame %d\n" % i)
    cmd = "wrap3cmd compute %s" % OUTPUT_WRAP_FILE
    os.system(cmd)
    d = None # Delete all node data
