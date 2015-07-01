##
#
# Inria Chile - Flows In Networks
# 
# Dynamic flow visualization
#
# * Visualization functions and classes
#
#

import vtk
import networkx as nx
import random

from numpy import *
import math
import vfc

# MAPS

# Scaled MERCATOR functions (http://wiki.openstreetmap.org/wiki/Mercator)

def merc_x(lon):
    r_major=6378137.000
    return r_major*math.radians(lon)/100000.0
 
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
    return y/100000.0

def add_map_WGS84Background(ren,jpeg_map_path,W,S,E,N):
    
    # crop_bounds = [W,S,E,N]

    jpegfile = jpeg_map_path

    map_N = N
    map_S = S
    map_W = W
    map_E = E
    
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
    plane.SetNormal(0.0,0.0,1.0)
    plane.SetCenter(0.5*(ox+p1x),0.5*(oy+p2y),-1E-8)
    
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
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetTexture(texture)

    ren.AddActor(actor)
    
    ren.GetActiveCamera().SetPosition(0.5*(ox+p1x),0.5*(oy+p2y),0.033)
    ren.GetActiveCamera().SetFocalPoint(0.5*(ox+p1x),0.5*(oy+p2y),0.0)
     
    return None
    
def get_ListOfPointsFromGeoString(edge):

    geo = edge[0]['geometry']
    geo = geo.replace(' ','')
    geo = geo.replace('[[','[')
    geo = geo.replace(']]',']')
    
    str_list = geo.split(']')
    str_list.pop()
    
    output = []
    for elem in str_list:
        
        elem = elem.replace('[','')
        
        aux = elem.split(',')
        
        if (aux[0] == ''):
            
            aux.pop(0)
            
        pos = array([float(aux[0]),float(aux[1]),float(aux[2])])
        output.append(pos)
    
    return output

def get_ListOfKeysFromGeoKeyString(edge):
    
    geo = edge[0]['geometry_keys']
    geo = geo.replace(' ','')
    geo = geo.replace('[','')
    geo = geo.replace(']','')
    
    str_list = geo.split(',')
    
    output = []
    for elem in str_list:
        
        key = float(elem)
        output.append(key)
        
    return output

# CLASSES

''' EDGE CLASSES
'''

def get_CustomVTKGraphGeoLine(G,edges,node_0,node_1,time_step,globalNumberOfTimeSteps,width,scale,pars):
    
    # Pair of nodes connected by one arc
    
    points = get_ListOfPointsFromGeoString(edges)
    geometry_keys = get_ListOfKeysFromGeoKeyString(edges)
    
    p0 = points[0]
    p1 = points[1]
    
    numberOfTimeDivisions = int(floor(edges[0]['time']/time_step))
    
    # DYNAMIC
    el = vtkGeoFlowRibbonLine(edges[0]['edge_key'],points,width)
    el.vtkFilter.SetWidth(width)
       
    alpha_pos   = pars[0]
    qbox_height = pars[1]
    qbox_dist   = pars[2]
    qbox_width  = pars[3]
        
    rPos        = alpha_pos*array(p0)+(1-alpha_pos)*array(p1)
    qHeight     = qbox_height
    qDistance   = qbox_dist
    qWidth      = qbox_width
    
    queue   = vfc.vtkQueueRibbonUsingRefPosition(p0,p1,rPos,qHeight,qDistance,qWidth)
    qbox    = vfc.vtkQueueBoxUsingRefPosition(p0,p1,rPos,qHeight,qDistance,qWidth)
     
    nodeStart                   = G.node[node_0]['nlabel']
    nodeEnd                     = G.node[node_1]['nlabel']
    edgeID                      = edges[0]['edge_key']#['id']
    edgeKey                     = edges[0]['edge_skey']#['key']
    globalNumberOfTimeDivisions = globalNumberOfTimeSteps
    numberOfTimeStepsForEdge    = numberOfTimeDivisions
    time_step                   = time_step
    vtkElement                  = el
    vtkQueue                    = queue

    edgeElement = GeoEdgeElement(nodeStart,nodeEnd,edgeID,edgeKey,numberOfTimeStepsForEdge,globalNumberOfTimeDivisions,time_step,geometry_keys,vtkQueue,vtkElement,qbox)
    
    return edgeElement

class GeoEdgeElement:
    
    def __init__(self,nodeStart,nodeEnd,edgeID,edgeKey,numberOfTimeStepsForEdge,globalNumberOfTimeDivisions,time_step,geometry_keys,vtkQueue,vtkElement,vtkQBox):
        
        self.ID = edgeID
        self.key = edgeKey
        self.nodeStart = nodeStart
        self.nodeEnd = nodeEnd
        self.time_step = time_step
        self.globalNumberOfTimeDivisions = int(globalNumberOfTimeDivisions)
        self.numberOfTimeStepsForEdge = int(numberOfTimeStepsForEdge)
        self.geometry_keys = geometry_keys
        self.vtkQueue = vtkQueue
        self.vtkElement = vtkElement
        self.vtkQBox = vtkQBox

        self.FlowData = zeros([globalNumberOfTimeDivisions+1,numberOfTimeStepsForEdge+1])
        
    def getData(self,id_time,i):
        
        return self.FlowData[id_time][i]

    
''' DYNAMIC ELEMENTS
'''
class vtkGeoFlowRibbonLine:

    def __init__(self,id,geometry,width):

        self.vtkPoints          = vtk.vtkPoints() 
        self.vtkLines           = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkRibbonFilter()
        self.vtkMapper          = vtk.vtkPolyDataMapper()
        self.vtkActor           = vtk.vtkActor()
        
        self.colors             = vtk.vtkUnsignedCharArray()
        self.radius             = vtk.vtkDoubleArray()
        
        self._initialize(id,geometry,width)
        
    def _initialize(self,id,points,width):
        
        # geometry and topology
        for i in xrange(len(points)):
            point = points[i]
            self.vtkPoints.InsertNextPoint(point)
#             if ( i < len(points)-1):
#                 dif = linalg.norm(points[i]-points[i+1])
#                 if (dif < 10**-5):
#                     print id
        
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()-1): 
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)

        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLines)

        self.colors.SetNumberOfComponents(4)
        self.colors.SetName('Colors')

        self.radius.SetNumberOfTuples(self.vtkPoints.GetNumberOfPoints()+1)
        self.radius.SetName('Radius')
        
        for i in xrange(self.vtkPoints.GetNumberOfPoints()):
            aux = 255
            nColor = [aux,aux,aux,50]
            self.colors.InsertNextTupleValue(nColor)
            self.radius.SetTuple1(i,1.0 + 1.0/(1.0+i))

        self.vtkPolyData.GetPointData().AddArray(self.colors)
        self.vtkPolyData.GetPointData().AddArray(self.radius)
        self.vtkPolyData.GetPointData().SetActiveScalars('Radius')

        # filter
 
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
             
        self.vtkFilter.UseDefaultNormalOn()        
        self.vtkFilter.SetAngle(0) 
         
        self.vtkFilter.SetWidth(width/2.0)
        self.vtkFilter.SetVaryWidth(1)
  
        # mapper
  
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUsePointFieldData()
        self.vtkMapper.SelectColorArray('Colors')
        
        #self.vtkMapper.SetInputData(self.vtkPolyData)
        
        # actor
        
        self.vtkActor.SetMapper(self.vtkMapper)
        #self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        #self.vtkActor.GetProperty().SetSpecular(0.25)
        #self.vtkActor.GetProperty().SetAmbient(0.5)
        #self.vtkActor.GetProperty().SetDiffuse(0.1)
        
        self.vtkActor.GetProperty().SetOpacity(1)
           
    def setColorById(self,i,colorTuple):

        self.vtkPolyData.GetPointData().GetArray('Colors').SetTuple(i,colorTuple)

    def setWidthById(self,i,value):

        self.vtkPolyData.GetPointData().GetArray('Radius').SetTuple1(i,value)
    
   
