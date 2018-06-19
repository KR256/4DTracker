
def loadQPTmono(QPT_PATH):

    f = open(QPT_PATH)
    data = f.readlines()[1:]
    NUM_FRAMES = int(data[-1].split(',')[0]) + 1

    frame = 0
    tempList = []
    markersPerFrame = []
    for line in data:
        if frame > NUM_FRAMES:
            break
        splitLine = line.strip().split(',')
        frameId = int(splitLine[0])

        if frameId == frame:
            tempList.append((int(splitLine[1]), float(splitLine[2]), float(splitLine[3])))
        else:
            markersPerFrame.append(tempList)
            tempList = [(int(splitLine[1]), float(splitLine[2]), float(splitLine[3]))]
            frame = frame + 1
    f.close()
    return markersPerFrame



# QPT_PATH = 'C:/kyleBathStuff/PaddyTracking/cam5-Configs.qpt'
# OUT_XML = 'C:/kyleBathStuff/PaddyTracking/cubicMarkers.xml'
# CAM_ID = 4
# WIDTH = 3840
# HEIGHT = 2160
#
# markersPerFrame = loadQPTmono(QPT_PATH)
#
# NUM_FRAMES = len(markersPerFrame)
# NUM_MARKERS = len(markersPerFrame[0])
#
# str0 = '\n\t\t\t<camera id="%i" sensor_id="0" label="frame%i" enabled="1" />' % (CAM_ID, 0)
#
# str1 = '<?xml version="1.0" encoding="UTF-8"?>\n<document version="1.4.0">' \
#        '\n\t<chunk label="Chunk 1" enabled="1">' \
#        '\n\t\t<sensors next_id="1">' \
#        '\n\t\t\t<sensor id="0" label="unknown" type="frame">' \
#        '\n\t\t\t\t<resolution width="%i" height="%i" />' \
#        '\n\t\t\t\t<property name="fixed" value="0"/>' \
#        '\n\t\t\t\t<property name="layer_index" value="0"\>' \
#        '\n\t\t\t</sensor>' \
#        '\n\t\t</sensors>' \
#        '\n\t\t<cameras next_id="%i" next_group_id="0">' \
#         '%s' \
#        '\n\t\t</cameras>' \
#        '\n\t\t<markers next_id="%i" next_group_id="0">' % (WIDTH,HEIGHT,10,str0, 999)
#
# str2 = '\n\t\t</markers>\n\t\t<frames next_id="%i">' % (NUM_FRAMES+1)
# str3 = '\n\t\t\t\t</markers>\n\t\t\t</frame>'
# str4 = '\n\t\t</frames>\n\t</chunk>\n</document>'
#
#
# for i,markers in enumerate(markersPerFrame):
#     strTemp = '\n\t\t\t<frame id="%i">\n\t\t\t\t<markers>' % i
#     str2 = str2 + strTemp
#     for j,marker in enumerate(markers):
#         markerId = marker[0]
#         X_coord = marker[1]
#         Y_coord = marker[2]
#
#         if i == 0:
#             str1 = '%s\n\t\t\t<marker id="%i" label="point %i" />' % (str1,markerId,markerId)
#         str2 = '%s\n\t\t\t\t\t<marker marker_id="%i" >' % (str2, markerId)
#         str2 = '%s\n\t\t\t\t\t\t<location camera_id="%i" pinned="%i" x="%d" y="%d" />' % (str2, CAM_ID, markerId, X_coord, Y_coord)
#         str2 = '%s\n\t\t\t\t\t</marker>' % str2
#
#     str2 = str2 + str3
#
# outString = str1 + str2 + str4
# f_out = open(OUT_XML,'w')
# f_out.write(outString)
# f_out.close()
# print("Stump")
