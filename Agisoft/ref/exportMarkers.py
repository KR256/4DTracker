import PhotoScan

doc = PhotoScan.app.document
chunk = doc.chunk
PATH = "C:/kyleBathStuff/Agisoft/outMarkersDense300k"
cameraExp = chunk.cameras[0]
NUM_FRAMES = len(cameraExp.frames)

for frameId in range(NUM_FRAMES):

    chunk.frame = frameId
    print("\nProcessing frame #" + str(frameId + 1) + ": ")

    framePath = PATH + ('/frame%03d' % (frameId+1)) + '.txt'
    chunk.saveReference(framePath, items=PhotoScan.ReferenceItemsMarkers)