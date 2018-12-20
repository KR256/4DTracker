
IN_PATH = 'G:\\results\perFrame\\blendWrapped_5k_iFrames\Frame.%06i.obj'
OUT_PATH = 'G:\\results\perFrame\\blendWrapped_5k_iFrames_niceQuads\Frame.%06i.obj'

START_FRAME = 30
END_FRAME = 30

linesToRemove = ["g Face", "g HeadBack", "g Nostrils", "g Eyes", "g EarsBack", "g EyelidsUpper", "g EyelidsLower",
                 "g NasolabialArea", "g Jaw", "g MouthSocketUpper","g MouthSocketLower"]

for f in range(START_FRAME, END_FRAME + 1):

    fileNameIn = IN_PATH % f
    fileNameOut = OUT_PATH % f
    with open(fileNameIn) as fileContentsIn:
        fileContentsOut = open(fileNameOut, 'w')

        for line in fileContentsIn:

            writeTrue = True

            for l in linesToRemove:

                if l in line:

                    writeTrue = False

            if writeTrue:

                fileContentsOut.write(line)

        fileContentsOut.close()


