import os
import sys
import json
import numpy as np

from functools import partial
from multiprocessing.dummy import Pool
from subprocess import call

START_FRAME = 107
END_FRAME = 114

NUM_THREADS = 4

INPUT_WRAP_FILE = 'F:\CatherineShoot\catherineMeshes\wrapMultiFrame\perFrame\concurrent\seqNoMarkers.wrap'
OUTPUT_WRAP_FILE = 'F:\CatherineShoot\catherineMeshes\wrapMultiFrame\perFrame\concurrent\seqNoMarkersTemp%d.wrap'

NEUTRAL = 'F:/CatherineShoot/catherineMeshes/wrapNeutral/catherineNeutralAgisoftCoordRescaledHighWrap.obj'
MESH_TARGET = 'F:\CatherineShoot\catherineMeshes\high400k_165frames_Rescaled\\frame.%i.obj'
IN_MESH = 'F:\CatherineShoot\catherineMeshes\wrapMultiFrame\perFrame\concurrent2/frame.%d.obj'
OUT_MESH = 'F:\CatherineShoot/catherineMeshes/wrapMultiFrame/perFrame/super_noMarkers/frame.%d.obj'

POLYGON_FILE = 'F:/CatherineShoot/catherineMeshes/wrapNeutral/catMask_super_2.txt'


# Create Wrap parameter settings
SUBDIVISIONS = 1 #default 3
ICP_ITERATIONS = 2 #default 5
OPT_ITERATIONS = 5 #default 20
SAMP_INIT = 5 #default 5
SAMP_FINAL = 0.2 #default 0.2
SMOOTH_INIT = 1 #default 1
SMOOTH_FINAL = 0.1 #default 0.1
CTL_POINTS_WEIGHT_INITIAL = 10 #default 3
CTL_POINTS_WEIGHT_FINAL = 10 #default 3
MAX_OPT_ITERATIONS = 100 #default 100
NORM_THRESHOLD = 0.65 #default 0.65
DP_INIT = 0.01 #default 0.01
DP_FINAL = 0.002 #default 0.002

commands = []

threadId = 1
batchStart = START_FRAME

# Creates meshes from frame2:NUM_FRAMES. Assumes first frame is manual.
i = START_FRAME
while i <= END_FRAME:
    # Load example JSON wrap file saved from first frame


    with open(INPUT_WRAP_FILE) as json_data:
        d = json.load(json_data)

    # Set paths for Input and Output meshes
    d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(IN_MESH % i )]
    d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(MESH_TARGET % i)]
    d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH % i)

    # Set paths for Select Points and Polygons
    d['nodes']['SelectPolygons01']['params']['fileName']['value'] = unicode(POLYGON_FILE)

    # Set paths for Select Points and Polygons
    d['nodes']['SelectPolygons01']['params']['fileName']['value'] = unicode(POLYGON_FILE)


    #Set chosen Wrap parameters
    d['nodes']['Wrapping01']['params']['nSubdivisions']['value'] = SUBDIVISIONS
    d['nodes']['Wrapping01']['params']['nICPIterations']['value'] = ICP_ITERATIONS
    d['nodes']['Wrapping01']['params']['nOptimizationIterations']['value'] = OPT_ITERATIONS
    d['nodes']['Wrapping01']['params']['samplingMaxMultiplier']['value'] = SAMP_INIT
    d['nodes']['Wrapping01']['params']['samplingMinMultiplier']['value'] = SAMP_FINAL
    d['nodes']['Wrapping01']['params']['globalSmoothWeightMax']['value'] = SMOOTH_INIT
    d['nodes']['Wrapping01']['params']['globalSmoothWeightMin']['value'] = SMOOTH_FINAL
    d['nodes']['Wrapping01']['params']['globalControlPointsWeightInitial']['value'] = CTL_POINTS_WEIGHT_INITIAL
    d['nodes']['Wrapping01']['params']['globalControlPointsWeightFinal']['value'] = CTL_POINTS_WEIGHT_FINAL
    d['nodes']['Wrapping01']['params']['maxOptimizationIterations']['value'] = MAX_OPT_ITERATIONS
    d['nodes']['Wrapping01']['params']['minCosBetweenNormals']['value'] = NORM_THRESHOLD
    d['nodes']['Wrapping01']['params']['maxDp']['value'] = DP_INIT
    d['nodes']['Wrapping01']['params']['minDp']['value'] = DP_FINAL


    left = np.min([END_FRAME - batchStart + 1, NUM_THREADS])
    if threadId <= left:
    # Save JSON file
        outWrapFile = OUTPUT_WRAP_FILE % threadId

        with open(outWrapFile, 'w') as outfile:
            json.dump(d, outfile)


        commands.append("wrap3cmd compute %s" % outWrapFile)

        d = None  # Delete all node data

        threadId = threadId + 1


    if threadId == (NUM_THREADS + 1):

        pool = Pool(NUM_THREADS)  # two concurrent commands at a time
        for j, returncode in enumerate(pool.imap(partial(call, shell=True), commands)):
            if returncode != 0:
                print("%d command failed: %d" % (i, returncode))

        threadId = 1

        batchStart = batchStart + NUM_THREADS
        #i = batchStart - 1
        print "Starting Batch: %i to %i" % (batchStart , np.min([END_FRAME, batchStart + NUM_THREADS]) )

    i = i + 1

    # Run Wrap node script for frame
    # print("Reconstructing Frame %d: %s" % (i, (MESH_TARGET % i)))
    # cmd = "wrap3cmd compute %s" % OUTPUT_WRAP_FILE
    # os.system(cmd)


