from OpenGL.GL import *


class ObjLoader(object):
    def __init__(self, fileName):
        self.v = []
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
                    vertex = (float(splitLine[1]), float(splitLine[2]), float(splitLine[3]))
                    # vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))
                    self.v.append(vertex)

                elif line[0] == "f":
                    string = line.replace("//", "/")
                    ##
                    splitLineFace = line.split()
                    face = (int(splitLineFace[1].split('//')[0]),int(splitLineFace[2].split('//')[0]),
                            int(splitLineFace[3].split('//')[0]))
                    # for item in range(string.count(" ")):
                    #     if string.find(" ", i) == -1:
                    #         face.append(string[i:-1])
                    #         break
                    #     face.append(string[i:string.find(" ", i)])
                    #     i = string.find(" ", i) + 1
                    ##
                    self.f.append(face)

            f.close()
        except IOError:
            print(".obj file not found.")