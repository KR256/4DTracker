import os
import sys
import json
from math import pi, sqrt, exp
# from scipy import scipy.ndimage.filters.gaussian_filter
# import numpy as np

def gauss(n=11,sigma=1):
    r = range(-int(n/2),int(n/2)+1)
    return [1 / (sigma * sqrt(2*pi)) * exp(-float(x)**2/(2*sigma**2)) for x in r]

START_FRAME = 1
END_FRAME = 100

KERNEL_SIZE = 1
SIGMA = 2

#KERNEL = [0.03125,0.0625,0.125,0.5,0.125,0.0625,0.03125]
KERNEL = [0.25,0.5,0.25]
#KERNEL = gauss(KERNEL_SIZE*2 + 1 ,SIGMA)

if KERNEL_SIZE == 1:

    INPUT_WRAP_FILE = 'G:\\results\meshProcessing\wrapTemporalSmoothing_kernel1.wrap'
    OUTPUT_WRAP_FILE = 'G:\\results\meshProcessing\wrapTemporalSmoothing_kernel1_temp.wrap'

elif KERNEL_SIZE == 2:

    INPUT_WRAP_FILE = 'G:\\results\meshProcessing\wrapTemporalSmoothing_kernel2.wrap'
    OUTPUT_WRAP_FILE = 'G:\\results\meshProcessing\wrapTemporalSmoothing_kernel2_temp.wrap'

elif KERNEL_SIZE == 3:

    INPUT_WRAP_FILE = 'G:\\results\meshProcessing\wrapTemporalSmoothing_kernel3.wrap'
    OUTPUT_WRAP_FILE = 'G:\\results\meshProcessing\wrapTemporalSmoothing_kernel3_temp.wrap'

IN_MESH = 'G:\\results\\fullSequence\\fullWithGroups/frame_20k_groups.%04i.obj'
OUT_MESH = 'G:\\results\meshProcessing\\temporalSmoothing/kernel1_sigma2/frame_smoothed.%04i.obj'


# Creates meshes from frame2:NUM_FRAMES. Assumes first frame is manual.
for i in range(START_FRAME, END_FRAME+1):

    if i <= KERNEL_SIZE:
        continue

    with open(INPUT_WRAP_FILE) as json_data:
        d = json.load(json_data)

    # Set paths for Input and Output meshes

    d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(IN_MESH % (i))]
    d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(IN_MESH % (i - 1))]
    d['nodes']['LoadGeom03']['params']['fileNames']['value'] = [unicode(IN_MESH % (i + 1))]
    d['nodes']['Blendshapes01']['params']['weights']['value'][0]['value'] = 0.5

    if KERNEL_SIZE > 1:

        d['nodes']['LoadGeom04']['params']['fileNames']['value'] = [unicode(IN_MESH % (i - 2))]
        d['nodes']['LoadGeom05']['params']['fileNames']['value'] = [unicode(IN_MESH % (i + 2))]
        d['nodes']['Blendshapes03']['params']['weights']['value'][0]['value'] = 0.5
        d['nodes']['Blendshapes04']['params']['weights']['value'][0]['value'] = KERNEL[KERNEL_SIZE-1] * 2

    if KERNEL_SIZE > 2:

        d['nodes']['LoadGeom06']['params']['fileNames']['value'] = [unicode(IN_MESH % (i - 3))]
        d['nodes']['LoadGeom07']['params']['fileNames']['value'] = [unicode(IN_MESH % (i + 3))]
        d['nodes']['Blendshapes05']['params']['weights']['value'][0]['value'] = 0.5
        d['nodes']['Blendshapes06']['params']['weights']['value'][0]['value'] = KERNEL[KERNEL_SIZE - 2] * 2


    d['nodes']['Blendshapes02']['params']['weights']['value'][0]['value'] = KERNEL[KERNEL_SIZE]

    d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH % (i))





    # Save JSON file
    with open(OUTPUT_WRAP_FILE, 'w') as outfile:
        json.dump(d, outfile)

    # Run Wrap node script for frame
    print("Reconstructing Frame %d: %s" % (i, OUT_MESH % (i)))
    # os.chdir("C:\kyleBathStuff\Wrap3.4.2_Portable\Wrap3.4.2")
    cmd = "wrap3cmd compute %s" % OUTPUT_WRAP_FILE
    os.system(cmd)

    d = None # Delete all node data




