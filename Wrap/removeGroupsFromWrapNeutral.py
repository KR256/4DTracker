
IN_PATH = 'F:\CatherineShoot\catherineMeshes\wrapMultiFrame\sequential\coarse_noBlink\\frame.%d.obj'
OUT_PATH = 'F:\CatherineShoot\catherineMeshes\wrapMultiFrame\perFrame\coarse_noBlink_niceQuads\\frame.%d.obj'

START_FRAME = 65
END_FRAME = 165

linesToRemove = ["g Face", "g HeadBack", "g Nostrils", "g Eyes", "g EarsBack"]

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


