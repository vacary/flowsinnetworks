

import pyproj
import vtk

from numpy import *
import math

def merc_x(lon):
    r_major=6378137.000
    return r_major*math.radians(lon)
 
def merc_y(lat):
    if lat>89.5:lat=89.5
    if lat<-89.5:lat=-89.5
    r_major=6378137.000
    r_minor=6356752.3142
    temp=r_minor/r_major
    eccent=math.sqrt(1-temp**2)
    phi=math.radians(lat)
    sinphi=math.sin(phi)
    con=eccent*sinphi
    com=eccent/2
    con=((1.0-con)/(1.0+con))**com
    ts=math.tan((math.pi/2-phi)/2)/con
    y=0-r_major*math.log(ts)
    return y

jpegfile = "./map.jpeg"

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(480,480)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

sphere = vtk.vtkSphereSource()
sphere.SetThetaResolution(12)
sphere.SetPhiResolution(12)

map_N = -33.3992 
map_S = -33.4375
map_W = -70.6421
map_E = -70.5832

ox = merc_x(map_W)
oy = merc_y(map_S)
p1x = merc_x(map_E)
p1y = merc_y(map_S)
p2x = merc_x(map_W)
p2y = merc_y(map_N)

plane = vtk.vtkPlaneSource()
plane.SetOrigin(ox,oy,0.0)
plane.SetPoint1(p1x,p1y,0.0)
plane.SetPoint2(p2x,p2y,0.0)
#plane.SetCenter(-70.6126,-33.4184,0.0)
plane.SetNormal(0.0,0.0,1.0)

reader = vtk.vtkJPEGReader()
reader.SetFileName(jpegfile)

texture = vtk.vtkTexture()
if vtk.VTK_MAJOR_VERSION <= 5:
    texture.SetInput(reader.GetOutput())
else:
    texture.SetInputConnection(reader.GetOutputPort())

texturePlane = vtk.vtkTextureMapToPlane()
if vtk.VTK_MAJOR_VERSION <= 5:
    texturePlane.SetInput(plane.GetOutputPort())
else:
    texturePlane.SetInputConnection(plane.GetOutputPort())


mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(texturePlane.GetOutput())
else:
    mapper.SetInputConnection(texturePlane.GetOutputPort())


# Create actor and set the mapper and the texture
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)

ren.AddActor(actor)

iren.SetInteractorStyle(vtk.vtkInteractorStyleImage())
iren.Initialize()
renWin.Render()
iren.Start()

del ren
del iren