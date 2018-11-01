import PhotoScan
import loadQPTmono

QPT_PATH = 'F:\CatherineShoot\catherineShort_Calib\catherine_cam5_eyes.qpt'
OUT3D_PATH = 'F:\CatherineShoot\catherineShort_Calib\catherine_eyes_agisoftOut3D.txt'
markersPerFrame = loadQPTmono.loadQPTmono(QPT_PATH)
#
doc = PhotoScan.app.document
chunk = doc.chunk
cameraExp = chunk.cameras[0]
CHOSEN_CAM = 5
NUM_CAMS = len(chunk.cameras)
NUM_FRAMES = len(markersPerFrame)
NUM_MARKERS = len(markersPerFrame[0])

f_out = open(OUT3D_PATH,'w')

START_FRAME = 65
fid = 0

for frameId in range(START_FRAME, START_FRAME + NUM_FRAMES):
    chunk.frame = frameId - 1
    cam = chunk.frame.cameras[CHOSEN_CAM-1]
    markersMat = markersPerFrame[fid]

    for mId, marker in enumerate(markersMat):
        imgX = marker[1]
        imgY = marker[2]
        point2D = PhotoScan.Vector([imgX, imgY])  # coordinates of the point on the given photo
        sensor = cam.sensor
        calibration = sensor.calibration
        x = PhotoScan.app.document.chunk.model.pickPoint(cam.center, cam.transform.mulp(sensor.calibration.unproject(point2D)))

        PhotoScan.app.document.chunk.frame.addMarker(point=x)
        lastMarker = PhotoScan.app.document.chunk.frame.markers[-1]
        lastMarker.label = 'point %i' % marker[0]

        markerPosition = chunk.transform.matrix.mulp(x)

        # if(frameId == 0):
        #     chunk.frame.addMarker(point=x)
        #     lastMarker = chunk.frame.markers[-1]
        #     lastMarker.label = 'point %i' % marker[0]
        # else:
        #     marker = chunk.frame.markers[mId]
        #     marker.projections[cam] = (imgX, imgY)
        #     chunk.frame.markers[-1].projections[chunk.cameras[4]].coord =

        outStr = "%i %f %f %f\n" % (marker[0],markerPosition[0],markerPosition[1],markerPosition[2])
        f_out.write(outStr)

    print("\nProcessing frame #" + str(frameId) + ": ")

    fid = fid + 1

f_out.close()

