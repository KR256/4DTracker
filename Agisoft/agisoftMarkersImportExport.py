import PhotoScan
import loadQPTmono

QPT_PATH = 'C:/kyleBathStuff/PaddyTracking/cam5-Configs.qpt'
OUT3D_PATH = 'C:/kyleBathStuff/PaddyTracking/out3D.txt'
markersPerFrame = loadQPTmono.loadQPTmono(QPT_PATH)
#
doc = PhotoScan.app.document
chunk = doc.chunk
cameraExp = chunk.cameras[0]
CHOSEN_CAM = 4
NUM_CAMS = len(chunk.cameras)
NUM_FRAMES = len(markersPerFrame)
NUM_MARKERS = len(markersPerFrame[0])

f_out = open(OUT3D_PATH,'w')


for frameId in range(NUM_FRAMES):
    chunk.frame = frameId
    cam = chunk.frame.cameras[CHOSEN_CAM]
    markersMat = markersPerFrame[frameId]

    for mId, marker in enumerate(markersMat):
        imgX = marker[1]
        imgY = marker[2]
        point2D = PhotoScan.Vector([imgX, imgY])  # coordinates of the point on the given photo
        sensor = cam.sensor
        calibration = sensor.calibration
        x = chunk.point_cloud.pickPoint(cam.center, cam.transform.mulp(sensor.calibration.unproject(point2D)))

        chunk.frame.addMarker(point=x)
        lastMarker = chunk.frame.markers[-1]
        lastMarker.label = 'point %i' % marker[0]

        # if(frameId == 0):
        #     chunk.frame.addMarker(point=x)
        #     lastMarker = chunk.frame.markers[-1]
        #     lastMarker.label = 'point %i' % marker[0]
        # else:
        #     marker = chunk.frame.markers[mId]
        #     marker.projections[cam] = (imgX, imgY)
        #     chunk.frame.markers[-1].projections[chunk.cameras[4]].coord =

        outStr = "%i %f %f %f\n" % (marker[0],x[0],x[1],x[2])
        f_out.write(outStr)

    print("\nProcessing frame #" + str(frameId + 1) + ": ")

f_out.close()

