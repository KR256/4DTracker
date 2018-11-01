import PhotoScan

doc = PhotoScan.app.document
chunk = doc.chunk
PATH = "F:\CatherineShoot\catherineShort\AgisoftOutMarkers\dense_noBlink"
#neutralPath = 'F:\CatherineShoot\catherineMeshes\wrapNeutral\catherineNeutral_Mask_20k_tris_notWrapped.obj'
#neutralPath = 'F:\CatherineShoot\catherineMeshes\wrapNeutral\catMaskAgisoftCoordRescaledHighWrap.obj'
neutralPath ='F:/CatherineShoot/catherineMeshes/wrapNeutral/catMask_withEyes_tris.obj'
markersOverTimeFile = PATH + "\\temporalMarkersHigh_noBlink.txt"
cameraExp = chunk.cameras[0]
NUM_FRAMES = len(cameraExp.frames)

START_FRAME = 65
END_FRAME = 165

with open(markersOverTimeFile, 'w') as markersOverTime:

    for frameId in range(START_FRAME-1, END_FRAME):
    #for frameId in range(START_FRAME, END_FRAME):

        chunk.frame = frameId
        print("\nProcessing frame #" + str(frameId + 1) + ": ")

        framePath = PATH + ('\\frameMesh.%i' % (frameId + 1)) + '.obj'
        #chunk.saveReference(framePath, items=PhotoScan.ReferenceItemsMarkers)

        markers = PhotoScan.app.document.chunk.markers
        # print(PhotoScan.app.document.chunk.markers[1606].position)
        neutralOpen = open(neutralPath, 'r')
        with open(framePath, 'w') as fileF:
            with open(neutralPath, 'r') as neutralOpen:
                markerId = 0
                for l, line in enumerate(neutralOpen):
                    if line[:2] == "v ":
                        position = chunk.transform.matrix.mulp(markers[markerId].position)
                        fileF.write("v %.9f %.9f %.9f\n" % (position[0], position[1], position[2]))
                        markersOverTime.write("%i %.9f %.9f %.9f\n" % (l, position[0], position[1], position[2]))
                        markerId = markerId + 1
                    else:
                        fileF.write(line)
