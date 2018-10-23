
import objloader
import numpy as np
import numpy.matlib
import json

WRAP_WHOLEHEAD_TRI_PATH = 'F:/CatherineShoot/catherineMeshes/wrapNeutral/catherine_super_notwrapped_tris.obj'

MASK_TRI_PATH = 'F:/CatherineShoot/catherineMeshes/wrapNeutral/mask_super_notwrapped_tris.obj'

DICT_PATH = 'F:\CatherineShoot\catherineMeshes\wrapNeutral\maskDicts\\faces_catMask_super.json'
DICT_PATH_VERTS = 'F:\CatherineShoot\catherineMeshes\wrapNeutral\maskDicts\\verts_catMask_super.json'

maskMesh = objloader.ObjLoader(MASK_TRI_PATH)
mask_vertsArray = np.array(maskMesh.v)
mask_facesArray = np.array(maskMesh.f)

headMesh = objloader.ObjLoader(WRAP_WHOLEHEAD_TRI_PATH)
head_vertsArray = np.array(headMesh.v)
head_facesArray = np.array(headMesh.f)

face_dictionary = {}
verts_dictionary = {}

for f, face in enumerate(mask_facesArray):
    print "Processing %f ....  Face %i out of %i" % (f/len(mask_facesArray),f, len(mask_facesArray))
    (verts1, verts2, verts3) = face - [1,1,1]
    diffVec = np.sum(np.abs(head_vertsArray - numpy.matlib.repmat(mask_vertsArray[verts1], head_vertsArray.shape[0], 1)), axis=1)
    markerVtx1 = np.argmin(diffVec)
    diffVec2 = np.sum(np.abs(head_vertsArray - numpy.matlib.repmat(mask_vertsArray[verts2], head_vertsArray.shape[0], 1)), axis=1)
    markerVtx2 = np.argmin(diffVec2)
    diffVec3 = np.sum(np.abs(head_vertsArray - numpy.matlib.repmat(mask_vertsArray[verts3], head_vertsArray.shape[0], 1)), axis=1)
    markerVtx3 = np.argmin(diffVec3)

    faceVerts = np.array([markerVtx1,markerVtx2,markerVtx3]) + [1,1,1]
    diffVec = np.sum(np.abs(head_facesArray - numpy.matlib.repmat(faceVerts, head_facesArray.shape[0], 1)), axis=1)
    wholeHeadFaceId = np.argmin(diffVec)
    #wholeHeadFaceId2 = numpy.where( Set(head_facesArray) == faceVerts )
    face_dictionary[f] = int(wholeHeadFaceId)
    verts_dictionary[verts1] = int(markerVtx1)
    verts_dictionary[verts2] = int(markerVtx2)
    verts_dictionary[verts3] = int(markerVtx3)

with open(DICT_PATH, "w") as write_file:
    json.dump(face_dictionary, write_file)

with open(DICT_PATH_VERTS, "w") as write_file_verts:
    json.dump(verts_dictionary, write_file_verts)


