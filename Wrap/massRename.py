import os
import sys

IN_PATH = 'G:\\results\\fullSequence\\fullWithGroups\\Frame.%06i.jpg'
OUT_PATH = 'G:\\results\\fullSequence\\full_niceQuads\\optiWrapped_20k.%04i.jpg'

START_FRAME = 626
END_FRAME = 900

os.system("cd %s" % IN_PATH)
# cmd = "ffmpeg -start_number 65 -i frame.%d.png -c:v ffv1 out.avi"
# os.system(cmd)

#os.system("copy F:\CatherineShoot\catherineMeshes\wrapMultiFrame\opticalWrapping\high\\frame.65.png F:\CatherineShoot\catherineMeshes\wrapMultiFrame\opticalWrapping\high_03\\frame.065.png")

for f in range(START_FRAME, END_FRAME + 1):
    inStr = str(IN_PATH % f)
    outStr = str(OUT_PATH % f)
    cmd = "copy %s %s" % (inStr,outStr)
    os.system(cmd)