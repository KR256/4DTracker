import PhotoScan
import loadQPTmono

QPT_PATH = 'T:\Seb\\4D_Project\Shots\kyle4d_cam02_4k_uncompressed_part003\Dynamics\kyle4d_cam02_2k_part003.qpt'
OUT3D_PATH = 'T:\Seb\\4D_Project\Shots\kyle4d_cam02_4k_uncompressed_part003\Dynamics\kyle4d_cam02_2k_part003_3DpointsFromAgisoft_1549to1595.txt'
markersPerFrame = loadQPTmono.loadQPTmono(QPT_PATH)
#
doc = PhotoScan.app.document
chunk = doc.chunk
cameraExp = chunk.cameras[0]
CHOSEN_CAM = 2
NUM_CAMS = len(chunk.cameras)
NUM_FRAMES = len(markersPerFrame)
NUM_FRAMES = 400
#NUM_MARKERS = len(markersPerFrame[0])

f_out = open(OUT3D_PATH,'w')

START_FRAME = 1549
fid = 348
UPRES = 2

for frameId in range(START_FRAME, START_FRAME + NUM_FRAMES):
    chunk.frame = frameId - 1
    cam = chunk.frame.cameras[CHOSEN_CAM-1]
    markersMat = markersPerFrame[fid]

    for mId, marker in enumerate(markersMat):

        imgX = marker[1]
        imgY = marker[2]
        if (UPRES > 1):
            imgX = imgX * UPRES
            imgY = imgY * UPRES
        point2D = PhotoScan.Vector([imgX, imgY])  # coordinates of the point on the given photo
        sensor = cam.sensor
        calibration = sensor.calibration

        T = chunk.transform.matrix
        #ptDstT = T.inv().mulp(chunk.crs.unproject(point2D))
        #x = chunk.model.pickPoint(cam.center, ptDstT)

        #x = PhotoScan.app.document.chunk.model.pickPoint(cam.center, cam.transform.mulp(sensor.calibration.unproject(point2D)))


        projectedPoint = cam.sensor.calibration.unproject(point2D)

        withCameraTransform = cam.transform.mulp(projectedPoint)

        pointOnMesh = chunk.crs.project(withCameraTransform)

        print(pointOnMesh)

        x = PhotoScan.app.document.chunk.model.pickPoint(cam.center,
                                                         pointOnMesh)


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

        outStr = "%i %i %f %f %f\n" % (frameId, marker[0],markerPosition[0],markerPosition[1],markerPosition[2])
        f_out.write(outStr)

    print("\nProcessing frame #" + str(frameId) + ": ")

    fid = fid + 1

f_out.close()

