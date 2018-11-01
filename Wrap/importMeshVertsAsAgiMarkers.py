import PhotoScan
# import objloader
# import numpy as np


#pointsPath = 'F:\CatherineShoot\catherineMeshes\wrapNeutral\catherineNeutral_Mask_20k_tris_notWrapped.obj'
pointsPath = 'F:/CatherineShoot/catherineMeshes/wrapNeutral/catMask_withEyes.obj'
#pointsPath = 'F:\CatherineShoot\catherineMeshes\wrapNeutral\catMaskAgisoftCoordRescaledHighWrap.obj'
#pointsPath = 'F:\CatherineShoot\catherineShort\AgisoftOutMarkers\\frameMesh_TwoStep.008.obj'
NORMAL_PROJECT = False


class ObjLoader(object):

    def __init__(self, fileName):
        self.v = []
        self.vn = []
        self.f = []
        ##
        try:
            f = open(fileName)
            for line in f:
                if line[:2] == "v ":
                    # index1 = line.find(" ") + 1
                    # index2 = line.find(" ", index1 + 1)
                    # index3 = line.find(" ", index2 + 1)
                    #
                    # print float(line[index1:index2])
                    # print float(line[index2:index3])
                    # print float(line[:-1])
                    splitLine = line.split()
                    vertex = (float(splitLine[1]), float(
                        splitLine[2]), float(splitLine[3]))
                    # vertex = (round(vertex[0], 2), round(vertex[1], 2),
                    # round(vertex[2], 2))
                    self.v.append(vertex)

                elif line[0] == "f":
                    string = line.replace("//", "/")
                    # print(string)
                    ##
                    splitLineFace = line.split()
                    face = (int(splitLineFace[1].split('/')[0]), int(splitLineFace[2].split('/')[0]),
                            int(splitLineFace[3].split('/')[0]))  # WILL ONLY WORK FOR TRIS
                    # for item in range(string.count(" ")):
                    #     if string.find(" ", i) == -1:
                    #         face.append(string[i:-1])
                    #         break
                    #     face.append(string[i:string.find(" ", i)])
                    #     i = string.find(" ", i) + 1
                    ##
                    self.f.append(face)

                elif line[:3] == "vn ":
                    splitLine = line.split()
                    vertexNorm = (float(splitLine[1]), float(
                        splitLine[2]), float(splitLine[3]))
                    # vertex = (round(vertex[0], 2), round(vertex[1], 2),
                    # round(vertex[2], 2))
                    self.vn.append(vertexNorm)

            f.close()
        except IOError:
            print(".obj file not found.")

doc = PhotoScan.app.document
chunk = doc.chunk

frameMesh = ObjLoader(pointsPath)
# vertsArray = np.array(frameMesh.v)
# facesArray = np.array(frameMesh.f)
vertsArray = frameMesh.v
#facesArray = frameMesh.f
normsArray = frameMesh.vn

print(vertsArray[0])

for fid, feature in enumerate(vertsArray):
    vec3Feature = PhotoScan.Vector([feature[0], feature[1], feature[2]])

    T = chunk.transform.matrix
    Tb = T.inv()
    position = Tb.mulp(vec3Feature)

    print(position)

    if NORMAL_PROJECT:
        norm = normsArray[fid]
        vec3Norm = PhotoScan.Vector([norm[0], norm[1], norm[2]])

        normOffset = vec3Feature + (0.1 * vec3Norm)
        normInset = vec3Feature - (0.1 * vec3Norm)
        projectedOffsetPosition = Tb.mulp(normOffset)
        projectedInsetPosition = Tb.mulp(normInset)

        print(projectedOffsetPosition)
        print(projectedInsetPosition)

        # normalProjected = Tb.mulv(vec3Norm)
        # normalProjected2 = Tb.mulv(vec3Norm)
        # print(norm)
        # print(normalProjected)
        # print(normalProjected2)

        positionT = chunk.model.pickPoint(position, projectedOffsetPosition)
        #position = chunk.model.pickPoint(vec3Feature, vec3Norm)
        if positionT:
            print("%i corrected" % fid)
            position = positionT
        # else:
        #     positionT = chunk.model.pickPoint(position, projectedInsetPosition)

        # if positionT:
        #     position = positionT
        
        print(position)

    chunk.addMarker(position,True)

