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
AGISOFT_DIR = 'F:\CatherineShoot\catherineShort_Calib\catherine_eyes_agisoftOut3D.txt'
#MARKERS_3D_FILE = 'C:/kyleBathStuff/PaddyTracking/out3D.txt'

#markersAtFrame = loadAgisoftOut3D.loadAgisoftOut3DFromQPT(MARKERS_3D_FILE)
markersAtFrame = loadAgisoftOut3D.loadAgisoftOut3DFromAgisoftMarkers(AGISOFT_DIR)
NUM_FRAMES = len(markersAtFrame)
NUM_MARKERS = len(markersAtFrame[0])

# 3D POINTS to FACES for Wrap.
#MESH_DIR = 'F:\CatherineShoot\catherineShort\Agisoft\\10frames_rescaledAndHigherPrecision'
MESH_DIR = 'F:\CatherineShoot\catherineShort\Agisoft\\180_frames_withTexture'


# maskOrOriginal = 'original'
# wholeHeadFaces = True
# #refineAlongNormals = True
#
# #if maskOrOriginal == 'mask':
# maskToWholeHeadDictPath = 'F:\CatherineShoot\catherineMeshes\wrapNeutral\maskDicts\.catMask_withEyes.json'
# with open(maskToWholeHeadDictPath) as fileContents:
#     maskToWholeHeadDict = json.load(fileContents)




agisoftMeshFileNames = glob.glob(os.path.join(MESH_DIR, '*.obj'))
#NUM_FRAMES = 1

START_FRAME = 64
END_FRAME = 164
NEUTRAL_FRAME = 64
#allMarkerFaces = [[]] * (END_FRAME - START_FRAME)
f = START_FRAME

for f in range(START_FRAME, END_FRAME + 1):

    NAUGHTY_MARKERS_PATH = 'F:\CatherineShoot\catherineShort_Calib\\naughtyMarkers\\naughtyMarkers.%i.txt' % (f + 1)

    # if maskOrOriginal == 'mask':
    #     meshNameStr = 'frameMesh.%d.obj'
    #     meshName = os.path.join('F:\CatherineShoot\catherineShort\AgisoftOutMarkers\dense_noBlink\\', meshNameStr % (f + 1))
    #     with open(NAUGHTY_MARKERS_PATH) as naughtyfile:
    #         naughtyMarkers = np.array(naughtyfile.read().strip('[').strip(']').split(',')).astype(int)
    # else:

    meshNameStr = 'frame.%i.obj'
    meshName = os.path.join(MESH_DIR, meshNameStr % (f + 1))
    naughtyMarkers = []



    #frameMarkers = markersAtFrame[f]
    frameMarkers = markersAtFrame[f - NEUTRAL_FRAME]
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

    for m in range(NUM_MARKERS):
        marker = frameMarkers[m]
        #marker = frameMarkers[7463]
        diffVec = np.sum(np.abs(vertsArray - numpy.matlib.repmat(marker, vertsArray.shape[0], 1)), axis=1)
        markerVtx = np.argmin(diffVec)
        closestVrts = np.argsort(diffVec) #[:10]
        bestTriangle3 = 0
        id = 0
        recVal = 2


        while (id < 3 and recVal < 4):
            # print facesArray[:, id]
            FaceIds = np.argwhere(facesArray[:, id] == (markerVtx+1))
            #FaceIds = np.array([174580, 173594 , 174576  ])
            # if len(FaceIds) == 1:
            #     FaceIds = [FaceIds]
            for fids in range(len(FaceIds)):
                # print FaceIds[0][0]
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
            markerFaces[m] = None
        else:
            markerFaces[m] = None

    #allMarkerFaces[abs(f - END_FRAME) - 1] = markerFaces

    # if maskOrOriginal == 'original':
    with open(NAUGHTY_MARKERS_PATH, 'w') as naughtyfile:
        naughtyfile.write(str(naughtyMarkers))

    OUT_WRAP_PATH = 'F:\CatherineShoot\catherineShort_Calib\outWrap\\'
    # if maskOrOriginal == 'mask':
    #     OUT_WRAP_PATH = 'F:\CatherineShoot\catherineShort\WrapMarkers\dense_noBlink\\NeutralMarkers\\'
    # print allMarkerFaces[0]
    outfileName = OUT_WRAP_PATH + 'frameNewHigh' + str(f + 1) + '.txt'
    with open(outfileName, 'w') as outfile:
        # frameArray = allMarkerFaces[abs(f - END_FRAME) - 1]
        #frameArray = allMarkerFaces[f - START_FRAME]

        arrayOut = [x for x in markerFaces if x is not None]
        # for marker in frameArray:
        #     if not marker:
        outfile.write(str(arrayOut))

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