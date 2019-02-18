
import sys

def wrap_removeGroupsFunc(IN_PATH,OUT_PATH):


    linesToRemove = ["g Face", "g HeadBack", "g Nostrils", "g Eyes", "g EarsBack", "g EyelidsUpper", "g EyelidsLower",
                     "g NasolabialArea", "g Jaw", "g MouthSocketUpper","g MouthSocketLower"]

    fileNameIn = IN_PATH
    fileNameOut = OUT_PATH
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

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    wrap_removeGroupsFunc(*sys.argv[1:])


