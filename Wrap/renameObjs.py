import os
import glob

Mesh_Path = "G:\\20181113-CubicMotion-Meshes-Textures-240frames\meshes-scaled-240framesCopy\\"
Delimeter = "Frame"

meshFileNames = glob.glob(os.path.join(Mesh_Path, '*.obj'))

for meshFile in meshFileNames:
    parts = meshFile.split('.')
    if len(parts) == 2:
        parts2 = meshFile.split(Delimeter)
        #delIndex = meshFile.find(Delimeter)
        parts2.insert(1, Delimeter + ".")
        newStringName = ''.join(parts2)
        os.rename(meshFile, newStringName)