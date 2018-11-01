import PhotoScan


def cross(a, b):
    result = PhotoScan.Vector([a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x])
    return result


doc = PhotoScan.app.document
chunk = doc.chunk
model = chunk.model
vertices = chunk.model.vertices

T0 = chunk.transform.matrix

camera = chunk.cameras[0]  # camera index
marker_2D = (2000, 1000)  # projections of marker on the given photo

marker = chunk.addMarker()
marker.projections[camera] = marker_2D

point_2D = marker.projections[camera].coord
vect = camera.sensor.calibration.unproject(point_2D)
vect = camera.transform.mulv(vect)
center = camera.center

# estimating ray and surface intersection
for face in model.faces:

    v = face.vertices

    E1 = PhotoScan.Vector(vertices[v[1]].coord - vertices[v[0]].coord)
    E2 = PhotoScan.Vector(vertices[v[2]].coord - vertices[v[0]].coord)
    D = PhotoScan.Vector(vect)
    T = PhotoScan.Vector(center - vertices[v[0]].coord)
    P = cross(D, E2)
    Q = cross(T, E1)
    result = PhotoScan.Vector([Q * E2, P * T, Q * D]) / (P * E1)

    if (0 < result[1]) and (0 < result[2]) and (result[1] + result[2] <= 1):
        t = (1 - result[1] - result[2]) * vertices[v[0]].coord
        u = result[1] * vertices[v[1]].coord
        v_ = result[2] * vertices[v[2]].coord

        point_3D = T0.mulp(u + v_ + t)
        if chunk.crs:
            point_3D = chunk.crs.project(point_3D)
        break

if chunk.crs:
    point = chunk.crs.unproject(point_3D)
point = T0.inv().mulp(point)

for cur_camera in chunk.cameras:

    if (cur_camera == camera) or not cur_camera.transform:
        continue
    cur_proj = cur_camera.project(point)

    if (0 <= cur_proj[0] < camera.sensor.width) and (0 <= cur_proj[1] < camera.sensor.height):
        marker.projections[cur_camera] = cur_proj

print("Script finished")