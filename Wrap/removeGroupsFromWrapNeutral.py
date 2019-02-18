
IN_PATH = 'G:\\results\\fullSequence\\fullWithGroups\\optiWrapped_20k_groups.%04i.obj'
OUT_PATH = 'G:\\results\\fullSequence\\full_niceQuads\\optiWrapped_20k.%04i.obj'

START_FRAME = 626
END_FRAME = 900

linesToRemove = ["g Face", "g HeadBack", "g Nostrils", "g Eyes", "g EarsBack", "g EyelidsUpper", "g EyelidsLower",
                 "g NasolabialArea", "g Jaw", "g MouthSocketUpper","g MouthSocketLower","g MouthSocket"]

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


