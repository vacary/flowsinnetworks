

import pyproj
import vtk

isn2004=pyproj.Proj("+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")
wgs84=pyproj.Proj("+init=EPSG:4326")
osgb36=pyproj.Proj("+init=EPSG:27700") 
UTM26N=pyproj.Proj("+init=EPSG:32626") 
UTM27N=pyproj.Proj("+init=EPSG:32627") 
UTM28N=pyproj.Proj("+init=EPSG:32628")
MERCATOR=pyproj.Proj("+init=EPSG:3785") # spherical mercator

jpegfile = "map.jpeg"

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

ox, oy = pyproj.transform(wgs84,MERCATOR,map_W,map_S)
p1x, p1y = pyproj.transform(wgs84,MERCATOR,map_E,map_S)
p2x, p2y = pyproj.transform(wgs84,MERCATOR,map_W,map_N)

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