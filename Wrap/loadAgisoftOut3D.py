def loadAgisoftOut3D(QPT_PATH):

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