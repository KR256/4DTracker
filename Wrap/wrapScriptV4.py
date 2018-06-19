import os
import sys
import json

NUM_FRAMES = 40
START_FRAME = 80
INPUT_WRAP_FILE = 'C:\kyleBathStuff\Wrap\meshPropagationAlignmentBefore.wrap'
OUTPUT_WRAP_FILE = 'C:\kyleBathStuff\Wrap\meshPropagationAlignmentBeforeTemp.wrap'
MESH_SOURCE = 'C:/kyleBathStuff/Wrap/paddyHD1DivTrisRA/frame.%03d.obj'
MESH_TARGET = 'C:\kyleBathStuff\PaddyTracking\meshes\paddyFrame%d.obj'
OUT_MESH = 'C:/kyleBathStuff/Wrap/paddyHD1DivTrisRA/frame.%03d.obj'

MARKERS_TARGET = 'C:/kyleBathStuff/Wrap/WrapMarkersSparse300k/WrapMarkersSparse300kframeNew%d.txt'
MARKERS_SOURCE = 'C:/kyleBathStuff/Wrap/templateMarkers/paddyHD1DivTemplateTris.txt'
POLYGON_FILE = 'C:/kyleBathStuff/Wrap/baseMeshSelection1SubDivTris.txt'

FOURD_OUTFILE = 'C:/kyleBathStuff/Wrap/out4D/frame4d.%03d.obj'
OUT_SHIFT = 'C:/kyleBathStuff/Wrap/meshPropagationShift/frameShift.%03d.obj'

# Create Wrap parameter settings
SUBDIVISIONS = 3 #default 3
ICP_ITERATIONS = 5 #default 5
OPT_ITERATIONS = 20 #default 20
SAMP_INIT = 5 #default 5
SAMP_FINAL = 0.2 #default 0.2
SMOOTH_INIT = 1 #default 1
SMOOTH_FINAL = 0.1 #default 0.1
CTL_POINTS_WEIGHT_INIT = 3 #default 10
CTL_POINTS_WEIGHT_FINAL = 3 #default 10
MAX_OPT_ITERATIONS = 100 #default 100
NORM_THRESHOLD = 0.65 #default 0.65
DP_INIT = 0.01 #default 0.01
DP_FINAL = 0.002 #default 0.002

# Creates meshes from frame2:NUM_FRAMES. Assumes first frame is manual.
for i in range(START_FRAME, START_FRAME + NUM_FRAMES):
    # Load example JSON wrap file saved from first frame
    with open(INPUT_WRAP_FILE) as json_data:
        d = json.load(json_data)

    # Set paths for Input and Output meshes
    d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(MESH_TARGET % i)]
    d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(MESH_SOURCE % (i-1))]
    d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH % i)

    # Set paths for Select Points and Polygons
    d['nodes']['SelectPoints01']['params']['fileNameLeft']['value'] = unicode(MARKERS_SOURCE )
    d['nodes']['SelectPoints01']['params']['fileNameRight']['value'] = unicode(MARKERS_TARGET % i)
    d['nodes']['SelectPolygons01']['params']['fileName']['value'] = unicode(POLYGON_FILE)

    # Remove previous marker coords
    d['nodes']['SelectPoints01']['params']['pointsLeft']['value'] = []
    d['nodes']['SelectPoints01']['params']['pointsRight']['value'] = []

    #Set chosen Wrap parameters
    d['nodes']['Wrapping01']['params']['nSubdivisions']['value'] = SUBDIVISIONS
    d['nodes']['Wrapping01']['params']['nICPIterations']['value'] = ICP_ITERATIONS
    d['nodes']['Wrapping01']['params']['nOptimizationIterations']['value'] = OPT_ITERATIONS
    d['nodes']['Wrapping01']['params']['samplingMaxMultiplier']['value'] = SAMP_INIT
    d['nodes']['Wrapping01']['params']['samplingMinMultiplier']['value'] = SAMP_FINAL
    d['nodes']['Wrapping01']['params']['globalSmoothWeightMax']['value'] = SMOOTH_INIT
    d['nodes']['Wrapping01']['params']['globalSmoothWeightMin']['value'] = SMOOTH_FINAL
    d['nodes']['Wrapping01']['params']['globalControlPointsWeightInitial']['value'] = CTL_POINTS_WEIGHT_INIT
    d['nodes']['Wrapping01']['params']['globalControlPointsWeightFinal']['value'] = CTL_POINTS_WEIGHT_FINAL
    d['nodes']['Wrapping01']['params']['maxOptimizationIterations']['value'] = MAX_OPT_ITERATIONS
    d['nodes']['Wrapping01']['params']['minCosBetweenNormals']['value'] = NORM_THRESHOLD
    d['nodes']['Wrapping01']['params']['maxDp']['value'] = DP_INIT
    d['nodes']['Wrapping01']['params']['minDp']['value'] = DP_FINAL

    d['nodes']['SaveGeom02']['params']['fileName']['value'] = unicode(FOURD_OUTFILE % i)
    d['nodes']['SaveGeom03']['params']['fileName']['value'] = unicode(OUT_SHIFT % i)


    # Save JSON file
    with open(OUTPUT_WRAP_FILE, 'w') as outfile:
        json.dump(d, outfile)

    # Run Wrap node script for frame
    print("Reconstructing Frame %d: %s\n as %s" % (i, (MESH_TARGET % i), (OUT_MESH % i)))
    cmd = "wrap3cmd compute %s" % OUTPUT_WRAP_FILE
    os.system(cmd)
    d = None # Delete all node data
