import os
import sys
import json

START_FRAME = 116
END_FRAME = 220
NEUTRAL_FRAME = 1
FRAME_STEP = 5

# INPUT_WRAP_FILE = 'F:\CatherineShoot\catherineMeshes\wrapMultiFrame\sequential\coarse_noBlink\seqDenseMarkers.wrap'
# OUTPUT_WRAP_FILE = 'F:\CatherineShoot\catherineMeshes\wrapMultiFrame\sequential\coarse_noBlink\seqDenseMarkersTemp.wrap'
# NEUTRAL = 'F:\CatherineShoot\catherineMeshes\wrapNeutral\catherineNeutralRescaled.obj'
# MESH_TARGET = 'F:\CatherineShoot\catherineMeshes\high400k_165frames_Rescaled\\frame.%i.obj'
# IN_MESH = 'F:\CatherineShoot/catherineMeshes/wrapMultiFrame/sequential/coarse_noBlink/frame.%d.obj'
# OUT_MESH = 'F:\CatherineShoot/catherineMeshes/wrapMultiFrame/sequential/coarse_noBlink/frame.%d.obj'
#
# POLYGON_FILE = 'F:/CatherineShoot/catherineMeshes/wrapNeutral/catMask_withEyes.txt'
#
# TEMPLATE_MARKERS = 'F:\CatherineShoot\catherineShort\WrapMarkers\dense_noBlink\NeutralMarkers\\frameNewHigh%d.txt'
# AGISOFT_MESH_MARKERS = 'F:\CatherineShoot\catherineShort\WrapMarkers\dense_noBlink\\frameNewHigh%d.txt'

INPUT_WRAP_FILE = 'G:\\results\markerTracking\wrapFiles\seqMarkers_twoWraps.wrap'
OUTPUT_WRAP_FILE = 'G:\\results\markerTracking\wrapFiles\seqMarkers_twoWraps_Temp.wrap'
NEUTRAL = 'G:/results/markerTracking/cache/frame_4k_groups.0001.obj'
MESH_TARGET = 'G:\\20181113-CubicMotion-Meshes-Textures-240frames\meshes-scaled-240framesCopy\Frame.%06i.obj'
IN_MESH = 'G:\\results\markerTracking\\seqLips_4k_twoWraps/frame.%04i.obj'
OUT_MESH = 'G:\\results\markerTracking\\seqLips_4k_twoWraps/frame.%04i.obj'

POLYGON_FILE = 'G:/results/markerTracking/cache/mask_5k_lips.txt'

TEMPLATE_MARKERS = 'G:/results/markerTracking/cache/frameBary_corrected_0001.txt'
AGISOFT_MESH_MARKERS = 'G:\\results\\agisoftToWrap\outWrapMarkers\\frameBary_%04i.txt'


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
for i in range(START_FRAME, END_FRAME+1,FRAME_STEP):
    # Load example JSON wrap file saved from first frame
    with open(INPUT_WRAP_FILE) as json_data:
        d = json.load(json_data)

    # Set paths for Input and Output meshes
    if i == NEUTRAL_FRAME:
        d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(NEUTRAL)]
        d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(MESH_TARGET % i)]
        d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH % i)
    else:
        d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(IN_MESH % (i-FRAME_STEP))]
        d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(MESH_TARGET % i)]
        d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH % i)

    # Set paths for Select Points and Polygons
    d['nodes']['SelectPolygons01']['params']['fileName']['value'] = unicode(POLYGON_FILE)
    d['nodes']['SelectPoints01']['params']['fileNameLeft']['value'] = unicode(TEMPLATE_MARKERS)
    d['nodes']['SelectPoints01']['params']['fileNameRight']['value'] = unicode(AGISOFT_MESH_MARKERS % i)


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
    cmd = "wrap3cmd compute %s" % OUTPUT_WRAP_FILE
    os.system(cmd)

    d = None # Delete all node data
