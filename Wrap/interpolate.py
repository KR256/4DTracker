import os
import sys
import json
from shutil import copyfile

START_FRAME = 5
END_FRAME = 150
NEUTRAL_FRAME = 1
FRAME_STEP = 5

INPUT_WRAP_FILE = 'G:\\results\perFrame\\interpolate_5k.wrap'
OUTPUT_WRAP_FILE = 'G:\\results\perFrame\\interpolate_5k_Temp.wrap'
NEUTRAL = 'G:/results/wrapTests/wrapped_5K_manual.obj'
# NEUTRAL_TEXTURE = 'G:\\results\wrapTests\optiWrapped_80K.jpg'
MESH_TARGET = 'G:/results/perFrame/blendWrapped_5k/Frame.%06i.obj'
# TARGET_TEXTURE = 'G:\\20181113-CubicMotion-Meshes-Textures-240frames\\textures-png-240frames\\Frame%06i_u1_v1.png'
IN_MESH = 'G:/results/perFrame/blendWrapped_5k/Frame.%06i.obj'
# IN_MESH_TEXTURE = 'G:\\results\meshPropagation\opticalFlow_super\Frame.%06i.jpg'
OUT_MESH = 'G:/results/perFrame/blendWrapped_5k/Frame.%06i.obj'
# OUT_MESH_TEXTURE = 'G:\\results\meshPropagation\opticalFlow_super\Frame.%06i.jpg'

# OUT_POLY_UP = 'G:\\results\meshPropagation\opticalFlow_super_projectedUp\Frame200k.%06i.obj'

# POLYGON_FILE = 'G:/results/wrapTests/mask_5k.txt'

# TEMPLATE_MARKERS = 'F:\CatherineShoot\catherineShort\WrapMarkers\dense_noBlink\NeutralMarkers\\frameNewHigh%d.txt'
# AGISOFT_MESH_MARKERS = 'F:\CatherineShoot\catherineShort\WrapMarkers\dense_noBlink\\frameNewHigh%d.txt'


# Create Wrap parameter settings
# SUBDIVISIONS = 3 #default 3
# ICP_ITERATIONS = 5 #default 5
# OPT_ITERATIONS = 20 #default 20
# SAMP_INIT = 5 #default 5
# SAMP_FINAL = 0.2 #default 0.2
# SMOOTH_INIT = 1 #default 1
# SMOOTH_FINAL = 0.1 #default 0.1
# CTL_POINTS_WEIGHT_INITIAL = 10 #default 3
# CTL_POINTS_WEIGHT_FINAL = 10 #default 3
# MAX_OPT_ITERATIONS = 100 #default 100
# NORM_THRESHOLD = 0.65 #default 0.65
# DP_INIT = 0.01 #default 0.01
# DP_FINAL = 0.002 #default 0.002

# Creates meshes from frame2:NUM_FRAMES. Assumes first frame is manual.
for i in range(START_FRAME, END_FRAME+1, FRAME_STEP):
    # Load example JSON wrap file saved from first frame
    with open(INPUT_WRAP_FILE) as json_data:
        d = json.load(json_data)

    # Set paths for Input and Output meshes

    d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(IN_MESH % i)]
    # d['nodes']['LoadImage01']['params']['fileNames']['value'] = [unicode(OUT_MESH_TEXTURE % (i - 1))]
    d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(MESH_TARGET % (i+FRAME_STEP))]
    # d['nodes']['LoadImage02']['params']['fileNames']['value'] = [unicode(TARGET_TEXTURE % i)]
    d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH % (i+1))
    d['nodes']['SaveGeom02']['params']['fileName']['value'] = unicode(OUT_MESH % (i + 2))
    d['nodes']['SaveGeom03']['params']['fileName']['value'] = unicode(OUT_MESH % (i + 3))
    d['nodes']['SaveGeom04']['params']['fileName']['value'] = unicode(OUT_MESH % (i + 4))
        # d['nodes']['SaveImage01']['params']['fileName']['value'] = unicode(OUT_MESH_TEXTURE % i)
        # d['nodes']['SaveGeom02']['params']['fileName']['value'] = unicode(OUT_POLY_UP % i)

    # Set paths for Select Points and Polygons
    #d['nodes']['SelectPolygons01']['params']['fileName']['value'] = unicode(POLYGON_FILE)
    # d['nodes']['SelectPoints01']['params']['fileNameLeft']['value'] = unicode(TEMPLATE_MARKERS % i)
    # d['nodes']['SelectPoints01']['params']['fileNameRight']['value'] = unicode(AGISOFT_MESH_MARKERS % i)


    #Set chosen Wrap parameters
    # d['nodes']['Wrapping01']['params']['nSubdivisions']['value'] = SUBDIVISIONS
    # d['nodes']['Wrapping01']['params']['nICPIterations']['value'] = ICP_ITERATIONS
    # d['nodes']['Wrapping01']['params']['nOptimizationIterations']['value'] = OPT_ITERATIONS
    # d['nodes']['Wrapping01']['params']['samplingMaxMultiplier']['value'] = SAMP_INIT
    # d['nodes']['Wrapping01']['params']['samplingMinMultiplier']['value'] = SAMP_FINAL
    # d['nodes']['Wrapping01']['params']['globalSmoothWeightMax']['value'] = SMOOTH_INIT
    # d['nodes']['Wrapping01']['params']['globalSmoothWeightMin']['value'] = SMOOTH_FINAL
    # d['nodes']['Wrapping01']['params']['globalControlPointsWeightInitial']['value'] = CTL_POINTS_WEIGHT_INITIAL
    # d['nodes']['Wrapping01']['params']['globalControlPointsWeightFinal']['value'] = CTL_POINTS_WEIGHT_FINAL
    # d['nodes']['Wrapping01']['params']['maxOptimizationIterations']['value'] = MAX_OPT_ITERATIONS
    # d['nodes']['Wrapping01']['params']['minCosBetweenNormals']['value'] = NORM_THRESHOLD
    # d['nodes']['Wrapping01']['params']['maxDp']['value'] = DP_INIT
    # d['nodes']['Wrapping01']['params']['minDp']['value'] = DP_FINAL


    # Save JSON file
    with open(OUTPUT_WRAP_FILE, 'w') as outfile:
        json.dump(d, outfile)

    # Run Wrap node script for frame
    print("Reconstructing Frame %d: %s" % (i, (MESH_TARGET % i)))
    # os.chdir("C:\kyleBathStuff\Wrap3.4.2_Portable\Wrap3.4.2")
    cmd = "wrap3cmd compute %s" % OUTPUT_WRAP_FILE
    os.system(cmd)

    d = None # Delete all node data
