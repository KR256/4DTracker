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
                    try:
                        face = (int(splitLineFace[1].split('/')[0]), int(splitLineFace[2].split('/')[0]),int(splitLineFace[3].split('/')[0]))
                    except:
                        face = (int(splitLineFace[1].split('/')[0]), int(splitLineFace[2].split('/')[0]),int(splitLineFace[3].split('/')[0]), int(splitLineFace[4].split('/')[0]))

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