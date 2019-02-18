import os
import glob
import numpy as np
import numpy.matlib
import objloader
import loadAgisoftOut3D
import json

def checkBarycentric(P, A, B, C):
    inTriangle = False

    v0 = C - A
    v1 = B - A
    v2 = P - A

    dot00 = np.dot(v0, v0)
    dot01 = np.dot(v0, v1)
    dot02 = np.dot(v0, v2)
    dot11 = np.dot(v1, v1)
    dot12 = np.dot(v1, v2)

    invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
    u = (dot11 * dot02 - dot01 * dot12) * invDenom
    v = (dot00 * dot12 - dot01 * dot02) * invDenom

    if (1 >= u >= 0) and (1 >= v >= 0):
        inTriangle = True

    if not np.isfinite(u):
        u = 0.0
        v = 0.0

    if u > 0.9999:
        u = 1.0

    if v > 0.9999:
        v = 1.0

    if u < 0.0001:
        u = 0.0

    if v > 0.0001:
        v = 0.0

    return(inTriangle ,u ,v)


def checkBarycentric2(P, v0, v1, v2):

    v0v1 = v1 - v0
    v0v2 = v2 - v0
    N = np.cross(v0v1,v0v2)
    area = np.linalg.norm(N) / 2

    edge1 = v2 - v1
    vp1 = P - v1
    C = np.cross(edge1, vp1)
    u = (np.linalg.norm(C) / 2 ) / area
    if (np.dot(N,C) < 0):
        return (False,0,0)

    edge2 = v0 - v2
    vp2 = P - v2
    C = np.cross(edge2, vp2)
    v = (np.linalg.norm(C) / 2) / area
    if (np.dot(N, C) < 0):
        return (False,0,0)

    if( u <= 0.0 or u >= 1.0):
        return (False, 0, 0)

    if (v <= 0.0 or v >= 1.0):
        return (False, 0, 0)

    if (u + v >= 1.0):
        return (False, 0, 0)

    return (True, u , v)


def checkBarycentric3(P, v0, v1, v2):
    v0v1 = v1 - v0
    v0v2 = v2 - v0
    N = np.cross(v0v1, v0v2)
    denom = np.dot(N,N)
    #
    # NdotRayDirection = np.dot(N,P)
    # if np.abs(NdotRayDirection < 0.00000001):
    #     return (False, 0, 0)
    #
    # d = np.dot(N,v0)
    #
    # t = (np.dot(N,[0,0,0]) + d) / NdotRayDirection
    #
    # if (t <0):
    #     return False

    edge0 = v1 - v0
    vp0 = P - v0
    C = np.cross(edge0, vp0)
    if (np.dot(N, C) < 0):
        return (False, 0, 0)

    edge1 = v2 - v1
    vp1 = P - v1
    C = np.cross(edge1, vp1)
    u = np.dot(N, C)
    if ( u < 0 ):
        return (False, 0, 0)

    edge2 = v0 - v2
    vp2 = P - v2
    C = np.cross(edge2, vp2)
    v = np.dot(N, C)
    if ( v < 0 ):
        return (False, 0, 0)

    u = u / denom
    v = v / denom

    if (not np.isfinite(u) or not np.isfinite(v)):
        return (False, 0, 0)


    return (True, u, v)

def checkBarycentric4(orig, dir, v0, v1, v2):
    v0v1 = v1 - v0
    v0v2 = v2 - v0
    pvec = np.cross(dir, v0v2)
    det = np.dot(v0v1, pvec)

    if np.abs(det) < 0.00000001:
        return (False, 0, 0, 0)

    invDet = 1/det

    tvec = orig - v0
    u = np.dot(tvec,pvec) * invDet
    if (u < 0 or u > 1):
        return (False, 0, 0, 0)

    qvec = np.cross(tvec,v0v1)
    v = np.dot(dir, qvec) * invDet
    if (v < 0 or u + v > 1):
        return (False, 0, 0, 0)

    if (not np.isfinite(u) or not np.isfinite(v)):
        return (False, 0, 0, 0)

    t = np.dot(v0v2, qvec) * invDet

    return (True,u, v, t)






# AGISOFT MARKER TXT FILE TO 3D MARKER POINTS per frame
AGISOFT_DIR_CAM1 = 'T:\Seb\\4D_Project\Shots\kyle4d_cam01_4k_uncompressed_part003\Dynamics\kyle4d_cam01_2k_part003_3DpointsFromAgisoft_1200to1595.txt'
AGISOFT_DIR_CAM2 = 'T:\Seb\\4D_Project\Shots\kyle4d_cam02_4k_uncompressed_part003\Dynamics\kyle4d_cam02_2k_part003_3DpointsFromAgisoft_1200to1595.txt'
#MARKERS_3D_FILE = 'C:/kyleBathStuff/PaddyTracking/out3D.txt'

#markersAtFrame = loadAgisoftOut3D.loadAgisoftOut3DFromQPT(MARKERS_3D_FILE)
markersAtFrame = loadAgisoftOut3D.loadAgisoftOut3DFromAgisoftMarkers_withKnownFrames(AGISOFT_DIR_CAM1)
markersAtFrame_cam2 = loadAgisoftOut3D.loadAgisoftOut3DFromAgisoftMarkers_withKnownFrames(AGISOFT_DIR_CAM2)
NUM_FRAMES = len(markersAtFrame)
NUM_MARKERS = len(markersAtFrame[0])

# 3D POINTS to FACES for Wrap.
#MESH_DIR = 'F:\CatherineShoot\catherineShort\Agisoft\\10frames_rescaledAndHigherPrecision'
MESH_DIR = 'G:\\20181113-CubicMotion-RC-Meshes-PNG\meshes'


# maskOrOriginal = 'original'
# wholeHeadFaces = True
# #refineAlongNormals = True
#
# #if maskOrOriginal == 'mask':
# maskToWholeHeadDictPath = 'F:\CatherineShoot\catherineMeshes\wrapNeutral\maskDicts\.catMask_withEyes.json'
# with open(maskToWholeHeadDictPath) as fileContents:
#     maskToWholeHeadDict = json.load(fileContents)


agisoftToRcTransform = np.array([[7.820529460906982,-0.38326722383499146,4.0604567527771,46.313907623291016],
                        [0.04927149415016174,8.789347648620605,0.7347301840782166,19.39959144592285],
                        [-4.078207015991211,-0.6287783980369568,7.7953667640686035,66.12821960449219],
                        [0,0,0,1]])

meshFileNames = glob.glob(os.path.join(MESH_DIR, '*.obj'))
#NUM_FRAMES = 1

START_FRAME = 1200
END_FRAME = 1595
NEUTRAL_FRAME = 1200
#allMarkerFaces = [[]] * (END_FRAME - START_FRAME)
f = START_FRAME
DROP_MARKERS = False

for f in range(START_FRAME, END_FRAME + 1):

    NAUGHTY_MARKERS_PATH = 'G:\\results\\agisoftToWrap\\naughtyMarkers\\naughtyMarkers.%i.txt' % (f)

    # if maskOrOriginal == 'mask':
    #     meshNameStr = 'frameMesh.%d.obj'
    #     meshName = os.path.join('F:\CatherineShoot\catherineShort\AgisoftOutMarkers\dense_noBlink\\', meshNameStr % (f + 1))
    #     with open(NAUGHTY_MARKERS_PATH) as naughtyfile:
    #         naughtyMarkers = np.array(naughtyfile.read().strip('[').strip(']').split(',')).astype(int)
    # else:

    meshNameStr = 'Frame%06i.obj'
    meshName = os.path.join(MESH_DIR, meshNameStr % (f))
    naughtyMarkers = []



    #frameMarkers = markersAtFrame[f]
    frameMarkers = markersAtFrame[f - NEUTRAL_FRAME]
    frameMarkers_cam2 = markersAtFrame_cam2[f - NEUTRAL_FRAME]
    #meshName = agisoftPointsFileNames[f]
    #meshName = os.path.join(MESH_DIR, meshNameStr % (f+1))
    print("Reading in %s\n" % meshName)
    # frameMesh = pymesh.load_mesh(meshName)
    frameMesh = objloader.ObjLoader(meshName)
    vertsArray = np.array(frameMesh.v)
    facesArray = np.array(frameMesh.f)
    #normsArray = np.array(frameMesh.vn)
    # frameMesh3 = pywavefront.Wavefront(meshName)
    markerFaces = [[]] * NUM_MARKERS
    points3DMarkers = [[]] * NUM_MARKERS

    for m in range(NUM_MARKERS):

        if m in [0,6,14,15,16,26,30,31]: # Skip marker on eyeball
            markerFaces[m] = None
            continue

        marker_cam1 = frameMarkers[m]
        marker_cam2 = frameMarkers_cam2[m]
        marker = np.divide(np.add(marker_cam1,marker_cam2),2)
        #marker = frameMarkers[7463]

        markerTemp = np.append(marker,1)
        marker2 = np.dot(agisoftToRcTransform,np.transpose(markerTemp))
        marker = marker2[0:3]
        points3DMarkers[m] = {"x": marker[0], "y": marker[1], "z": marker[2]}

        diffVec = np.sum(np.abs(vertsArray - numpy.matlib.repmat(marker, vertsArray.shape[0], 1)), axis=1)
        markerVtx = np.argmin(diffVec)
        closestVrts = np.argsort(diffVec) #[:10]
        bestTriangle3 = 0
        id = 0
        recVal = 2
        firstFace = None


        while (id < 3 and recVal < 4):
            # print facesArray[:, id]
            FaceIds = np.argwhere(facesArray[:, id] == (markerVtx+1))
            #FaceIds = np.array([174580, 173594 , 174576  ])
            # if len(FaceIds) == 1:
            #     FaceIds = [FaceIds]
            for fids in range(len(FaceIds)):
                # print FaceIds[0][0]
                if not firstFace:
                    firstFace = FaceIds[fids]
                outVerts = facesArray[FaceIds[fids]] - [1, 1, 1]
                A = vertsArray[outVerts[0][0]]
                B = vertsArray[outVerts[0][1]]
                C = vertsArray[outVerts[0][2]]
                #(bestTriangle, u1, v1) = checkBarycentric(marker, A, B, C)
                #(bestTriangle2, u2, v2) = checkBarycentric2(marker, A, B, C)
                (bestTriangle3, u3, v3) = checkBarycentric3(marker, A, B, C)
                #(bestTriangle4, u4, v4) = checkBarycentric4(marker, A, B, C)
                #(bestTriangle, u, v) = checkBarycentricV2(marker, A, B, C)
                if (bestTriangle3):
                    # Wrap is annoying and takes 3rd Vertex as A
                    FaceId = FaceIds[fids]
                    outVerts2 = facesArray[FaceId[0]] - [1,1,1]
                    A2 = vertsArray[outVerts2[0]]
                    B2 = vertsArray[outVerts2[1]]
                    C2 = vertsArray[outVerts2[2]]
                    (bT, u, v) = checkBarycentric3(marker, A2, B2, C2)
                    print "Marker %i: [%i, %f, %f]" % (m, FaceId, u , v)
                    # if maskOrOriginal == 'mask' and wholeHeadFaces:
                    #     FaceId = [int(maskToWholeHeadDict[str(FaceId[0])])]
                    break
            if (bestTriangle3):
                # print "Best Triangle at %f %f %f" % (A2,B2,C2)
                # print "recVal = %i" % recVal
                break

            id = id + 1

            # If can't find triangle choose second nearest triangle
            if (not bestTriangle3 and id == 3):
                print 'Couldn\'t find barycentric for Frame: %d, Marker %d on First Attempt\n' % (f, m)
                #idx = np.argpartition(diffVec, recVal)
                #markerVtx = idx[recVal-1]

                markerVtx = closestVrts[recVal-1]
                id = 0
                recVal = recVal + 1
            #
                # if(recVal > 5):
                #     break
            #         print 'Couldn\'t find barycentric for Frame: %d, Marker %d at all\n' % (f, m)
            #         # try:
            #         #     FaceId = np.argwhere(facesArray[:, 2] == (idx[0] + 1))[0]
            #         # except:
            #         #     try:
            #         #         FaceId = np.argwhere(facesArray[:, 0] == (idx[0] + 1))[0]
            #         #     except:
            #         #         FaceId = np.argwhere(facesArray[:, 1] == (idx[0] + 1))[0]
            #
            #         u,v = 0.00,0.00
            #         break

        # if maskOrOriginal == 'mask' and (m in naughtyMarkers):
        #     markerFaces[m] = None
        if(bestTriangle3):
            markerFaces[m] = [FaceId[0], float(u), float(v)]
        elif(not bestTriangle3):
            naughtyMarkers.append(m)
            if DROP_MARKERS:
                markerFaces[m] = None
            else:
                markerFaces[m] = [firstFace[0], float(0.5), float(0.5)]
        else:
            if DROP_MARKERS:
                markerFaces[m] = None
            else:
                markerFaces[m] = [firstFace[0], float(0.5), float(0.5)]

    #allMarkerFaces[abs(f - END_FRAME) - 1] = markerFaces

    # if maskOrOriginal == 'original':
    with open(NAUGHTY_MARKERS_PATH, 'w') as naughtyfile:
        naughtyfile.write(str(naughtyMarkers))

    OUT_WRAP_PATH = 'G:\\results\\agisoftToWrap\outWrapMarkers\\'
    # if maskOrOriginal == 'mask':
    #     OUT_WRAP_PATH = 'F:\CatherineShoot\catherineShort\WrapMarkers\dense_noBlink\\NeutralMarkers\\'
    # print allMarkerFaces[0]
    outfileName = OUT_WRAP_PATH + 'frameBary_%04i.txt' % f
    with open(outfileName, 'w') as outfile:
        # frameArray = allMarkerFaces[abs(f - END_FRAME) - 1]
        #frameArray = allMarkerFaces[f - START_FRAME]

        arrayOut = [x for x in markerFaces if x is not None]
        # for marker in frameArray:
        #     if not marker:
        outfile.write(str(arrayOut))

    outfileName3D = OUT_WRAP_PATH + 'frame3D_%04i.txt' % f
    with open(outfileName3D, 'w') as outfile3D:
        # frameArray = allMarkerFaces[abs(f - END_FRAME) - 1]
        #frameArray = allMarkerFaces[f - START_FRAME]
        # for marker in frameArray:
        #     if not marker:
        str3dmarker = str(points3DMarkers)
        str3dmarker = str3dmarker.replace("'", '"')
        outfile3D.write(str3dmarker)

    # if maskOrOriginal == 'original':
    #     maskOrOriginal = 'mask'
    # else:
    #     maskOrOriginal = 'original'
    #     f = f + 1

# Write to txt file compatable with Wrap.
# OUT_WRAP_PATH = 'F:\CatherineShoot\catherineShort\WrapMarkers\dense_noBlank\\'
# if maskOrOriginal == 'mask':
#     OUT_WRAP_PATH = 'F:\CatherineShoot\catherineShort\WrapMarkers\dense_noBlank\\NeutralMarkers\\'
# # print allMarkerFaces[0]
# for f in range(START_FRAME,END_FRAME):
#     outfileName = OUT_WRAP_PATH + 'frameNewHigh' + str(f+1) + '.txt'
#     with open(outfileName, 'w') as outfile:
#             #frameArray = allMarkerFaces[abs(f - END_FRAME) - 1]
#             frameArray = allMarkerFaces[f - START_FRAME]
#             arrayOut = [x for x in frameArray if x is not None]
#             # for marker in frameArray:
#             #     if not marker:
#             outfile.write(str(arrayOut))

print naughtyMarkers