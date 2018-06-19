import os
import glob
import numpy as np
import numpy.matlib
import objloader
import loadAgisoftOut3D

def checkBarycentric(P, A, B, C):
    inTriangle = 0

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
        inTriangle = 1

    return(inTriangle,u,v)




# AGISOFT MARKER TXT FILE TO 3D MARKER POINTS per frame
AGISOFT_DIR = 'C:\\kyleBathStuff\\Agisoft\\outMarkersSparse300k'
MARKERS_3D_FILE = 'C:/kyleBathStuff/PaddyTracking/out3D.txt'

markersAtFrame = loadAgisoftOut3D.loadAgisoftOut3D(MARKERS_3D_FILE)
NUM_FRAMES = len(markersAtFrame)
NUM_MARKERS = len(markersAtFrame[0])

# 3D POINTS to FACES for Wrap.
MESH_DIR = 'C:\\kyleBathStuff\\PaddyTracking\\meshes'
agisoftMeshFileNames = glob.glob(os.path.join(MESH_DIR, '*.obj'))
NUM_FRAMES = len(agisoftMeshFileNames)
# NUM_FRAMES = 3;
allMarkerFaces = [[]] * NUM_FRAMES
for f in range(NUM_FRAMES):
    frameMarkers = markersAtFrame[f]
    #meshName = agisoftPointsFileNames[f]
    meshName = os.path.join(MESH_DIR,'paddyFrame%d.obj' % (f+1))
    print("Reading in %s\n" % meshName)
    # frameMesh = pymesh.load_mesh(meshName)
    frameMesh = objloader.ObjLoader(meshName)
    vertsArray = np.array(frameMesh.v)
    facesArray = np.array(frameMesh.f)
    # frameMesh3 = pywavefront.Wavefront(meshName)
    markerFaces = [[]] * NUM_MARKERS
    for m in range(NUM_MARKERS):
        marker = frameMarkers[m]
        diffVec = np.sum(np.abs(vertsArray - numpy.matlib.repmat(marker, vertsArray.shape[0], 1)), axis=1)
        markerVtx = np.argmin(diffVec)
        bestTriangle = 0
        id = 0
        recVal = 2
        while (id < 3):
            # print facesArray[:, id]
            FaceIds = np.argwhere(facesArray[:, id] == (markerVtx+1))
            # if len(FaceIds) == 1:
            #     FaceIds = [FaceIds]
            for fids in range(len(FaceIds)):
                # print FaceIds[0][0]
                outVerts = facesArray[FaceIds[fids]] - [1, 1, 1]
                A = vertsArray[outVerts[0][0]]
                B = vertsArray[outVerts[0][1]]
                C = vertsArray[outVerts[0][2]]
                (bestTriangle, _, _) = checkBarycentric(marker, A, B, C)
                # (bestTriangle, u, v) = checkBarycentricV2(marker, A, B, C)
                if (bestTriangle):
                    # Wrap is annoying and takes 3rd Vertex as A
                    FaceId = FaceIds[fids]
                    outVerts2 = facesArray[FaceId[0]] - [1,1,1]
                    A2 = vertsArray[outVerts2[2]]
                    B2 = vertsArray[outVerts2[0]]
                    C2 = vertsArray[outVerts2[1]]
                    (_, v, u) = checkBarycentric(marker, A2, B2, C2)
                    break
            if (bestTriangle):
                break

            id = id + 1

            # If can't find triangle choose second nearest triangle
            if (not bestTriangle and id == 3):
                print 'Couldn\'t find barycentric for Frame: %d, Marker %d on First Attempt\n' % (f, m)
                idx = np.argpartition(diffVec, recVal)
                markerVtx = idx[recVal-1]
                id = 0
                recVal = recVal + 1
                if(recVal > 5):
                    print 'Couldn\'t find barycentric for Frame: %d, Marker %d at all\n' % (f, m)
                    try:
                        FaceId = np.argwhere(facesArray[:, 2] == (idx[0] + 1))[0]
                    except:
                        try:
                            FaceId = np.argwhere(facesArray[:, 0] == (idx[0] + 1))[0]
                        except:
                            FaceId = np.argwhere(facesArray[:, 1] == (idx[0] + 1))[0]

                    u,v = 0.00,0.00
                    break

        markerFaces[m] = [FaceId[0], float(u), float(v)]
    allMarkerFaces[f] = markerFaces

# Write to txt file compatable with Wrap.
OUT_WRAP_PATH = 'C:\\kyleBathStuff\\Wrap\\WrapMarkersSparse300k'
# print allMarkerFaces[0]
for f in range(NUM_FRAMES):
    outfileName = OUT_WRAP_PATH + 'frameNew' + str(f+1) + '.txt'
    with open(outfileName, 'w') as outfile:
        outfile.write(str(allMarkerFaces[f]))