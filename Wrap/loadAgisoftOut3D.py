import glob
import os

def loadAgisoftOut3DFromQPT(QPT_PATH):

    f = open(QPT_PATH)
    data = f.readlines()

    tempList = []
    markersPerFrame = []
    firstMarker = int(data[0].strip().split()[0])

    for i,line in enumerate(data):
        splitLine = line.strip().split()
        markerId = int(splitLine[0])

        if markerId == firstMarker and i != 0:
            markersPerFrame.append(tempList)
            tempList = [(float(splitLine[1]), float(splitLine[2]), float(splitLine[3]))]
        else:
            tempList.append((float(splitLine[1]), float(splitLine[2]), float(splitLine[3])))

    markersPerFrame.append(tempList)

    f.close()
    return markersPerFrame

def loadAgisoftOut3DFromAgisoftMarkers(AgisoftMarkersPath):

    f = open(AgisoftMarkersPath)
    data = f.readlines()

    tempList = []
    markersPerFrame = []
    firstMarker = int(data[0].strip().split()[0])

    for i, line in enumerate(data):
        splitLine = line.strip().split()
        markerId = int(splitLine[0])

        if markerId == firstMarker and i != 0:
            markersPerFrame.append(tempList)
            tempList = [(float(splitLine[1]), float(splitLine[2]), float(splitLine[3]))]
        else:
            tempList.append((float(splitLine[1]), float(splitLine[2]), float(splitLine[3])))

    markersPerFrame.append(tempList)

    f.close()
    return markersPerFrame

def loadAgisoftOut3DFromAgisoftMarkers_withKnownFrames(AgisoftMarkersPath):

    f = open(AgisoftMarkersPath)
    data = f.readlines()

    tempList = []
    markersPerFrame = []
    firstMarker = int(data[0].strip().split()[1])

    for i, line in enumerate(data):
        splitLine = line.strip().split()
        if not splitLine:
            continue
        try:
            markerId = int(splitLine[1])
        except:
            pass

        if markerId == firstMarker and i != 0:
            markersPerFrame.append(tempList)
            tempList = [(float(splitLine[2]), float(splitLine[3]), float(splitLine[4]))]
        else:
            try:
                tempList.append((float(splitLine[2]), float(splitLine[3]), float(splitLine[4])))
            except:
                pass

    markersPerFrame.append(tempList)

    f.close()
    return markersPerFrame