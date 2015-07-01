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

# VISUALIZATION

def get_CustomVTKGraphLine(G,edges,node_0,node_1,time_step,globalNumberOfTimeSteps,width,scale,pars):
    
    # Pair of nodes connected by one arc
    
    p0 = G.node[node_0]['pos']
    p1 = G.node[node_1]['pos']
    
    numberOfTimeDivisions = int(floor(edges[0]['time']/time_step))
    
    # DYNAMIC
    el = vtkFlowRibbonLine(p0,p1,numberOfTimeDivisions,width)
    el.vtkFilter.SetWidth(width)
    
    alpha_pos   = pars[0]
    qbox_height = pars[1]
    qbox_dist   = pars[2]
    qbox_width  = pars[3]
        
    rPos        = alpha_pos*array(p0)+(1-alpha_pos)*array(p1)
    qHeight     = qbox_height
    qDistance   = qbox_dist
    qWidth      = qbox_width
    
    queue   = vtkQueueRibbonUsingRefPosition(p0,p1,rPos,qHeight,qDistance,qWidth)
    qbox    = vtkQueueBoxUsingRefPosition(p0,p1,rPos,qHeight,qDistance,qWidth)
    
    if (G.node[node_0]['type'] == 'd'):
        queue.vtkActor.GetProperty().SetOpacity(0)
        qbox.vtkActor.GetProperty().SetOpacity(0)
    
    
    nodeStart                   = G.node[node_0]['nlabel']
    nodeEnd                     = G.node[node_1]['nlabel']
    edgeID                      = edges[0]['edge_key']#['id']
    edgeKey                     = edges[0]['edge_skey']#['key']
    globalNumberOfTimeDivisions = globalNumberOfTimeSteps
    numberOfTimeStepsForEdge    = numberOfTimeDivisions
    time_step                   = time_step
    vtkQueue                    = queue
    vtkElement                  = el    

    edgeElement = EdgeElement(nodeStart,nodeEnd,edgeID,edgeKey,numberOfTimeStepsForEdge,globalNumberOfTimeDivisions,time_step,vtkQueue,vtkElement,qbox)
    
    return edgeElement

def get_CustomVTKGraphArc(G,edges,n_edge,node_0,node_1,plusFactor,angleForArc,time_step,globalNumberOfTimeSteps,width,scale,pars):

    # Pair of nodes connected by several arcs
                
    p0 = G.node[node_0]['pos']
    p1 = G.node[node_1]['pos']
    
    numberOfTimeDivisions = int(floor(edges[n_edge]['time']/time_step))
    
    # DYNAMIC
    
    el = vtkFlowRibbonArc(p0,p1,numberOfTimeDivisions,angleForArc,plusFactor)
    el.vtkFilter.SetWidth(width)
    
    nArcPoints = el.vtkPoints.GetNumberOfPoints()
    
    if (nArcPoints % 2 == 1):
        
        box_position    = el.vtkPoints.GetPoint(int(0.5*(nArcPoints-1)))
        rPos            = array(box_position)
    
    else:
        
        box_position_0  = el.vtkPoints.GetPoint(int(0.5*nArcPoints - 1))
        box_position_1  = el.vtkPoints.GetPoint(int(0.5*nArcPoints))
        rPos            = 0.5*(array(box_position_0)+array(box_position_1))                        

    qbox_height = pars[1]
    qbox_dist   = pars[2]
    qbox_width  = pars[3]
        
    qHeight     = qbox_height
    qDistance   = qbox_dist*(-1*plusFactor)
    qWidth      = qbox_width
    
    queue   = vtkQueueRibbonUsingRefPosition(p0,p1,rPos,qHeight,qDistance,qWidth)
    qbox    = vtkQueueBoxUsingRefPosition(p0,p1,rPos,qHeight,qDistance,qWidth)
    
    if (G.node[node_0]['type'] == 'd'):
        queue.vtkActor.GetProperty().SetOpacity(0)
        qbox.vtkActor.GetProperty().SetOpacity(0)
        
    nodeStart                   = G.node[node_0]['nlabel']
    nodeEnd                     = G.node[node_1]['nlabel']
    edgeID                      = edges[n_edge]['edge_key']#['id']
    edgeKey                     = edges[n_edge]['edge_skey']#['key']
    globalNumberOfTimeDivisions = globalNumberOfTimeSteps
    numberOfTimeStepsForEdge    = numberOfTimeDivisions
    time_step                   = time_step
    vtkQueue                    = queue
    vtkElement                  = el

    edgeElement = EdgeElement(nodeStart,nodeEnd,edgeID,edgeKey,numberOfTimeStepsForEdge,globalNumberOfTimeDivisions,time_step,vtkQueue,vtkElement,qbox)

    return edgeElement

# FUNCTIONS

def lambdaPoint(vlambda,p0,vector):

    z = array(p0) + vlambda*array(vector)

    return z

def unitNormal2DVectorToLine(p0,p1,z):
    
    d = array(p1) - array(p0)
    
    u = d/linalg.norm(d)
    
    v = zeros(3)
    
    if (abs(u[0])> 0):
    
        v[0] = -u[1]/u[0]
        v[1] = 1.0
        v[2] = z
    
    else:
        
        v[0] = 1.0
        v[1] = 0
        v[2] = z
    
    w = v/linalg.norm(v)
    
    return w

def getPointFrom2DRotation(x,y,angleInRads):
    
    newX = x*cos(angleInRads) - y*sin(angleInRads)
    newY = x*sin(angleInRads) + y*cos(angleInRads)
    
    return array([newX,newY,0])

def getListOfPointsForArc(p0,p1,angle,numberOfDivisions,plusFactor):

    ''' Add points to draw the arc from p0 to p1
    '''
    
    # angle take values in the open interval (0, 180)

    radsAngle   = angle*(pi/180.0)
    step        = radsAngle/(1.0*numberOfDivisions)
    
    # arcCenter
    middlePoint = 0.5*(array(p0) + array(p1))
    distance    = linalg.norm(array(p0) - array(p1))
    kFactor     = 0.5*distance/tan(0.5*radsAngle)
    u           = unitNormal2DVectorToLine(p0,p1,0.0)
    
    arcCenter   = middlePoint + plusFactor*kFactor*u
    
    # listOfPoints
    
    points  = []
    points.append(p0)
    
    c2mp        = middlePoint - arcCenter
    direction   = array(p1) - array(p0)
    xcr         = cross(c2mp,direction)
    
    if (xcr[2] < 0):
        angleSign = -1.0
    else:
        angleSign = 1.0
    
    tp0         = p0 - arcCenter
    tp          = zeros(3)
    
    for k in xrange(1,numberOfDivisions):
        
        subRadsAngle = step*k
        tp = getPointFrom2DRotation(tp0[0],tp0[1],angleSign*subRadsAngle)
        point = tp + arcCenter
        points.append(point)
        
    points.append(p1)
    
    return points


# CLASSES

''' EDGE CLASSES
'''

class EdgeElement:
    
    def __init__(self,nodeStart,nodeEnd,edgeID,edgeKey,numberOfTimeStepsForEdge,globalNumberOfTimeDivisions,time_step,vtkQueue,vtkElement,vtkQBox):
        
        self.ID = edgeID
        self.key = edgeKey
        self.nodeStart = nodeStart
        self.nodeEnd = nodeEnd
        self.time_step = time_step
        self.globalNumberOfTimeDivisions = int(globalNumberOfTimeDivisions)
        self.numberOfTimeStepsForEdge = int(numberOfTimeStepsForEdge)
        self.vtkQueue = vtkQueue
        self.vtkElement = vtkElement
        self.vtkQBox = vtkQBox

        self.FlowData = zeros([globalNumberOfTimeDivisions+1,numberOfTimeStepsForEdge+1])
        
    def getData(self,id_time,i):
        
        return self.FlowData[id_time][i]

''' STATIC ELEMENTS
'''
    
class label2D:
    
    def __init__(self,x,y,z,label,text_h,text_v):
        
        self.point  = vtk.vtkPoints()
        self.vert   = vtk.vtkCellArray()
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor  = vtk.vtkActor()
        self.actor2D = vtk.vtkActor2D()
    
        self._initialize(x,y,z,label,text_h,text_v)
    
    def _initialize(self,x,y,z,strLabel,text_h,text_v):
    
        id_point    = self.point.InsertNextPoint(x,y,z)
        
        label = vtk.vtkStringArray()
        label.SetNumberOfValues(1)
        label.SetName("label")
        
        self.vert.InsertNextCell(1)
        self.vert.InsertCellPoint(id_point)
        label.SetValue(0,strLabel)
        
        pointData  = vtk.vtkPolyData()        
        pointData.SetPoints(self.point)          
        pointData.SetVerts(self.vert)         
        
        pointData.GetPointData().AddArray(label)            
         
        if (vtk.VTK_MAJOR_VERSION <= 5):
            self.mapper.SetInput(pointData)
        else:
            self.mapper.SetInputData(pointData)
        
        self.actor.SetMapper(self.mapper)     
        self.actor.GetProperty().SetPointSize(2.5)          
        self.actor.GetProperty().SetColor(1,0,0)          
                
        labelMapper = vtk.vtkLabeledDataMapper()
        labelMapper.SetInputData(pointData)
        labelMapper.SetLabelModeToLabelFieldData()
        tprop = labelMapper.GetLabelTextProperty()
        tprop.SetFontSize(11)
        tprop.SetBold(1)
        tprop.SetItalic(0)
        tprop.SetShadow(0)
        
        
        if (text_h == 'c'):
            tprop.SetJustificationToCentered()
        if (text_h == 'l'):
            tprop.SetJustificationToLeft()
        if (text_h == 'r'):
            tprop.SetJustificationToRight()
            
        if (text_v == 'u'):
            tprop.SetVerticalJustificationToTop()
        if (text_v == 'b'):
            tprop.SetVerticalJustificationToBottom()
        if (text_v == 'c'):
            tprop.SetVerticalJustificationToCentered()            
            
        self.actor2D.SetMapper(labelMapper)
        

    
class vtkLines:
    
    def __init__(self,arrayOfPoints,colorRGB, linewidth ,zpos):
        
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkLines       = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        
        self._initialize(arrayOfPoints,colorRGB,linewidth,zpos)
        
    def _initialize(self,data,color,width,zpos):
        
        N = len(data[:,0])
        
        for i in xrange(N):
            self.vtkPoints.InsertNextPoint(data[i,0],data[i,1], zpos)
        
        for i in range(0,self.vtkPoints.GetNumberOfPoints()-1): # create lines
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)
         
        self.vtkPolyData = vtk.vtkPolyData()                   # polydata object
        self.vtkPolyData.SetPoints(self.vtkPoints)                     # set geometry
        self.vtkPolyData.SetLines(self.vtkLines)                       # set topology  
        
        if (vtk.VTK_MAJOR_VERSION <= 5):                # check VTK version
            self.vtkMapper.SetInput(self.vtkPolyData)
        else:
            self.vtkMapper.SetInputData(self.vtkPolyData)
        
        self.vtkActor.SetMapper(self.vtkMapper)
        self.vtkActor.GetProperty().SetLineWidth(5)
        self.vtkActor.GetProperty().SetColor(color[0],color[1],color[2])
        self.vtkActor.GetProperty().SetLineWidth(width)        
        
class vtkRibbons:
    
    def __init__(self,arrayOfPoints,colorRGB, linewidth ,zpos):
        
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkLines       = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkFilter      = vtk.vtkRibbonFilter()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        
        self._initialize(arrayOfPoints,colorRGB,linewidth,zpos)
        
    def _initialize(self,data,color,width,zpos):
        
        N = len(data[:,0])
        
        for i in xrange(N):
            self.vtkPoints.InsertNextPoint(data[i,0],data[i,1], zpos)
        
        for i in range(0,self.vtkPoints.GetNumberOfPoints()-1): # create lines
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)
         
        self.vtkPolyData = vtk.vtkPolyData()                   # polydata object
        self.vtkPolyData.SetPoints(self.vtkPoints)                     # set geometry
        self.vtkPolyData.SetLines(self.vtkLines)                       # set topology  
        
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
        
        self.vtkFilter.SetWidth(0.000025)
        self.vtkFilter.SetAngle(90)
 
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        # actor
        
        self.vtkActor.SetMapper(self.vtkMapper)
        self.vtkActor.GetProperty().SetColor(0.5,0.5,0.5)
        self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        self.vtkActor.GetProperty().SetSpecular(0.75)
        self.vtkActor.GetProperty().SetAmbient(0.75)
        self.vtkActor.GetProperty().SetDiffuse(0.5)

class vtkRibbonLine:
    
    def __init__(self,p0,p1,RGBcolor,width,zpos):

        self.flag               = 0

        self.vtkPoints          = vtk.vtkPoints() 
        self.vtkLines           = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkRibbonFilter()
        self.vtkMapper          = vtk.vtkPolyDataMapper()
        self.vtkActor           = vtk.vtkActor()
        
        self._initialize(p0,p1,RGBcolor,width,zpos)
        
    def _initialize(self,p0,p1,color,width,z):
        
        # geometry and topology
        
        d = array(p1) - array(p0)

        u = d/linalg.norm(d)
        
        v = zeros(3)
        
        if (abs(u[0])> 0):
        
            v[0] = -u[1]/u[0]
            v[1] = 1.0
            v[2] = 0
        
        
        else:
            
            v[0] = 1.0
            v[1] = 0
            v[2] = 0
        
        w = v/linalg.norm(v)

        deltaLambda = 1.0

        for i in xrange(2):

            vlambda = i*deltaLambda
            p = lambdaPoint(vlambda,p0,d)
            point = [p[0],p[1],z]
            self.vtkPoints.InsertNextPoint(point)

        if (p0[0]==p1[0]):
            self.flag = 1
        
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()-1): 
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)

        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLines)

        # filter

        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)

        self.vtkFilter.UseDefaultNormalOn()
        self.vtkFilter.SetWidth(width/2.0)
 
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        # actor
        
        self.vtkActor.SetMapper(self.vtkMapper)
        self.vtkActor.GetProperty().SetColor(color[0],color[1],color[2])
        self.vtkActor.GetProperty().SetSpecularColor(color[0],color[1],color[2])
        self.vtkActor.GetProperty().SetSpecular(0.75)
        self.vtkActor.GetProperty().SetAmbient(0.75)
        self.vtkActor.GetProperty().SetDiffuse(0.5)

class vtkTubes:
    
    def __init__(self,arrayOfPoints,colorRGB, linewidth ,zpos):
        
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkLines       = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkFilter      = vtk.vtkTubeFilter()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        
        self._initialize(arrayOfPoints,colorRGB,linewidth,zpos)
        
    def _initialize(self,data,color,width,zpos):
        
        N = len(data[:,0])
        
        for i in xrange(N):
            self.vtkPoints.InsertNextPoint(data[i,0],data[i,1], zpos)
        
        for i in range(0,self.vtkPoints.GetNumberOfPoints()-1): # create lines
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)
         
        self.vtkPolyData = vtk.vtkPolyData()                   # polydata object
        self.vtkPolyData.SetPoints(self.vtkPoints)                     # set geometry
        self.vtkPolyData.SetLines(self.vtkLines)                       # set topology  
        
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)

        self.vtkFilter.SetRadius(width)
        self.vtkFilter.SetNumberOfSides(20)
        self.vtkFilter.CappingOff()
 
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        # actor
        
        self.vtkActor.SetMapper(self.vtkMapper)
        self.vtkActor.GetProperty().SetColor(color[0],color[1],color[2])
        self.vtkActor.GetProperty().SetSpecularColor(color[0],color[1],color[2])
        self.vtkActor.GetProperty().SetSpecular(0.75)
        self.vtkActor.GetProperty().SetAmbient(0.75)
        self.vtkActor.GetProperty().SetDiffuse(0.5)

class vtkEdgeRibbonLine:
    
    def __init__(self,p0,p1):

        self.flag               = 0

        self.vtkPoints          = vtk.vtkPoints() 
        self.vtkLines           = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkRibbonFilter()
        self.vtkMapper          = vtk.vtkPolyDataMapper()
        self.vtkActor           = vtk.vtkActor()
        
        self._initialize(p0,p1)
        
    def _initialize(self,p0,p1):
        
        # geometry and topology
        
        d = array(p1) - array(p0)

        deltaLambda = 1.0

        for i in xrange(2):

            vlambda = i*deltaLambda
            p = lambdaPoint(vlambda,p0,d)
            point = [p[0],p[1],0]
            self.vtkPoints.InsertNextPoint(point)

        if (p0[0]==p1[0]):
            self.flag = 1
        
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()-1): 
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)

        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLines)

        # filter

        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
            
        if self.flag == 0:
            self.vtkFilter.SetAngle(90)
        else:
            self.vtkFilter.SetAngle(180) 
        
        self.vtkFilter.SetWidth(0.5)
 
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        # actor
        
        self.vtkActor.SetMapper(self.vtkMapper)
        self.vtkActor.GetProperty().SetColor(0,0,1)
        self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        self.vtkActor.GetProperty().SetSpecular(0.75)
        self.vtkActor.GetProperty().SetAmbient(0.75)
        self.vtkActor.GetProperty().SetDiffuse(0.5)
        
class vtkEdgeRibbonArc:
    
    def __init__(self,p0,p1,angle,plusFactor):

        self.flag               = 0

        self.vtkPoints          = vtk.vtkPoints() 
        self.vtkLines           = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkRibbonFilter()
        self.vtkMapper          = vtk.vtkPolyDataMapper()
        self.vtkActor           = vtk.vtkActor()
        
        self._initialize(p0,p1,angle,plusFactor)
        
    def _initialize(self,p0,p1,angle,plusFactor):
        
        # geometry and topology
        
        numberOfDivisions = 10
        
        points = getListOfPointsForArc(p0,p1,angle,numberOfDivisions,plusFactor)
        
        
        for i in xrange(len(points)):

            point = [points[i][0],points[i][1],0.0]
            self.vtkPoints.InsertNextPoint(point)

        if (p0[0]==p1[0]):
            self.flag = 1
        
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()-1): 
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)

        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLines)

        # filter

        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
            
        self.vtkFilter.SetAngle(90)
        
        self.vtkFilter.SetWidth(0.5)
 
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        # actor
        
        self.vtkActor.SetMapper(self.vtkMapper)
        self.vtkActor.GetProperty().SetColor(0,0,1)
        self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        self.vtkActor.GetProperty().SetSpecular(0.5)
        self.vtkActor.GetProperty().SetAmbient(0.75)
        self.vtkActor.GetProperty().SetDiffuse(0.5)
            
class vtkNodesElementGlyph:
    
    def __init__(self,nxGraph,nodeRadius,opacity,lbFontSize):

        self.colorsArrayName    = "Colors"
        self.widthArrayName     = "Radius"
        self.node_flag          = 0

        self.vtkPoints          = vtk.vtkPoints()
        self.vtkVertices        = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkGlyph3D()
        self.vtkMapper          = vtk.vtkPolyDataMapper()   
        self.vtkActor           = vtk.vtkActor()      
        self.vtkActor2D         = vtk.vtkActor2D()    

        self._initialize(nxGraph,nodeRadius,opacity,lbFontSize)

    def _initialize(self,G,nodeRadius,opacity,lbFontSize):
    
        # geometry and labels
        
        labels = vtk.vtkStringArray()
        labels.SetNumberOfValues(G.number_of_nodes())
        labels.SetName("labels")
        
        c = 0
        dummy_id = -1
        for i in G.nodes_iter():
            
            posX = G.node[i]['pos'][0] 
            posY = G.node[i]['pos'][1]
            posZ = G.node[i]['pos'][2] + 0.0
            self.vtkPoints.InsertPoint(G.node[i]['id'],posX,posY,posZ)
            
            if (G.node[i]['type']!='d'):
                labels.SetValue(c,str(G.node[i]['nlabel']))
            else:
                dummy_id = G.node[i]['id']
                self.node_flag = 1
                labels.SetValue(c,'')
            
            c = c + 1
    
        # topology
            
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()):
            self.vtkVertices.InsertNextCell(1)
            self.vtkVertices.InsertCellPoint(i)
            
        # polydata
            
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkVertices)
        
        self.vtkPolyData.GetPointData().AddArray(labels)
        
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName(self.colorsArrayName)
        
        for i in xrange(self.vtkPoints.GetNumberOfPoints()):
            if (self.node_flag==1 and i == dummy_id):
                nColor = [0,0,0]
            else:
                xcolor = int(255*0.25)
                nColor = [xcolor,xcolor,xcolor]
            colors.InsertNextTupleValue(nColor)         

        self.vtkPolyData.GetPointData().AddArray(colors)

        radius = vtk.vtkDoubleArray()
        radius.SetNumberOfTuples(self.vtkPoints.GetNumberOfPoints()+1)
        radius.SetName(self.widthArrayName)
        
        for i in xrange(self.vtkPoints.GetNumberOfPoints()):
            if (self.node_flag==1 and i == dummy_id):
                radius.SetTuple1(i,0.0)
            else:
                radius.SetTuple1(i,1)

        self.vtkPolyData.GetPointData().AddArray(radius)
        self.vtkPolyData.GetPointData().SetActiveScalars(self.widthArrayName)
        
        # filter
        
        #elm = 'cube'
        elm  ='sphere'
        
        if (elm == 'cube'):
        
            source = vtk.vtkCubeSource()
            source.SetXLength(nodeRadius)
            source.SetYLength(nodeRadius)
            source.SetZLength(nodeRadius*0.5)

        if (elm == 'sphere'):
            
            source = vtk.vtkSphereSource()
            source.SetRadius(nodeRadius)
            source.SetPhiResolution(16)
            source.SetThetaResolution(16)
            
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
            self.vtkFilter.SetSource(source.GetOutput())
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
            self.vtkFilter.SetSourceConnection(source.GetOutputPort())
        
        self.vtkFilter.ScalingOn()
        self.vtkFilter.SetScaleModeToScaleByScalar()
        self.vtkFilter.SetScaleFactor(0.35)
 
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())

        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUsePointFieldData()
        self.vtkMapper.SelectColorArray(self.colorsArrayName)
           
        # actor

        self.vtkActor.SetMapper(self.vtkMapper)

        self.vtkActor.GetProperty().SetColor(1,1,1)
        self.vtkActor.GetProperty().SetPointSize(50)
        self.vtkActor.GetProperty().SetSpecularColor(0.25,0.25,0.25)
        self.vtkActor.GetProperty().SetSpecular(0.25)
        self.vtkActor.GetProperty().SetAmbient(0.1)
        self.vtkActor.GetProperty().SetDiffuse(0.1)
        self.vtkActor.GetProperty().SetOpacity(opacity)
        
        # 2D Actor

        labelMapper = vtk.vtkLabeledDataMapper()
        labelMapper.SetInputData(self.vtkPolyData)
        labelMapper.SetLabelModeToLabelFieldData()
        tprop = labelMapper.GetLabelTextProperty()
        tprop.SetFontSize(lbFontSize)
        tprop.SetBold(1)
        tprop.SetItalic(0)
        tprop.SetShadow(0)
        tprop.SetJustificationToCentered()
        tprop.SetVerticalJustificationToCentered()

        self.vtkActor2D.SetMapper(labelMapper)

class vtkPositionPointsElement:
    
    def __init__(self,p0,p1,numberOfTimeDivisions):

        self.colorsArrayName    = "Colors"

        self.vtkPoints          = vtk.vtkPoints()
        self.vtkVertices        = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkMapper          = vtk.vtkPolyDataMapper()   
        self.vtkActor           = vtk.vtkActor()          

        self._initialize(p0,p1,numberOfTimeDivisions)

    def _initialize(self,p0,p1,numberOfTimeDivisions):

        # geometry and topology
        
        d = array(p1) - array(p0)

        deltaLambda = 1.0/(1.0*numberOfTimeDivisions)

        for i in xrange(numberOfTimeDivisions+1):

            vlambda = i*deltaLambda
            p = lambdaPoint(vlambda,p0,d)
            point = [p[0],p[1],0.0]
            self.vtkPoints.InsertNextPoint(point)
 
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()):
            self.vtkVertices.InsertNextCell(1)
            self.vtkVertices.InsertCellPoint(i)
        
        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkVertices)
        
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName(self.colorsArrayName)
        
        for i in xrange(self.vtkPoints.GetNumberOfPoints()):
            nColor = [int(255*random.random()),int(255*random.random()),int(255*random.random())]
            colors.InsertNextTupleValue(nColor)         

        self.vtkPolyData.GetPointData().AddArray(colors)
    
        # mapper
        
        if (vtk.VTK_MAJOR_VERSION <= 5):        # check VTK version
            self.vtkMapper.SetInput(self.vtkPolyData)
        else:
            self.vtkMapper.SetInputData(self.vtkPolyData)
        
        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUsePointFieldData()
        self.vtkMapper.SelectColorArray(self.colorsArrayName)
        
        # actor

        self.vtkActor.SetMapper(self.vtkMapper)

        self.vtkActor.GetProperty().SetColor(0,1*random.random(),0)
        self.vtkActor.GetProperty().SetPointSize(10)
        self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        self.vtkActor.GetProperty().SetSpecular(0.25)
        self.vtkActor.GetProperty().SetAmbient(0.2)
        self.vtkActor.GetProperty().SetDiffuse(0.1)



class vtkText:
    
    def __init__(self,posX,posY,text):
        
        self.txtActor = vtk.vtkTextActor()
        self.posX = posX
        self.posY = posY
        self.text = text
        
        self._initialize()
        
    def _initialize(self):
        
        self.txtActor.SetInput(self.text)
        self.txtActor.GetTextProperty().SetFontFamilyToArial()
        self.txtActor.GetTextProperty().SetFontSize(16)
        self.txtActor.GetTextProperty().SetColor(1,1,1)
        self.txtActor.SetDisplayPosition(self.posX,self.posY)        
        
    def getTextActor(self):
        
        return self.txtActor
    

''' DYNAMIC ELEMENTS
'''
            
class vtkFlowRibbonLine:

    def __init__(self,p0,p1,numberOfTimeDivisions,width):

        self.flag               = 0

        self.vtkPoints          = vtk.vtkPoints() 
        self.vtkLines           = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkRibbonFilter()
        self.vtkMapper          = vtk.vtkPolyDataMapper()
        self.vtkActor           = vtk.vtkActor()
        
        self.colors             = vtk.vtkUnsignedCharArray()
        self.radius             = vtk.vtkDoubleArray()
        
        self._initialize(p0,p1,numberOfTimeDivisions,width)
        
    def _initialize(self,p0,p1,numberOfTimeDivisions,width):
        

        # geometry and topology
        
        d = array(p1) - array(p0)

        deltaLambda = 1.0/(1.0*numberOfTimeDivisions)

        for i in xrange(numberOfTimeDivisions+1):

            vlambda = i*deltaLambda
            p = lambdaPoint(vlambda,p0,d)
            point = [p[0],p[1],0]
            self.vtkPoints.InsertNextPoint(point)
            
        if (p0[0]==p1[0]):
            self.flag = 1
        
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
            aux = 70
            nColor = [aux,aux,aux,255]
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


class vtkFlowRibbonArc:

    def __init__(self,p0,p1,numberOfTimeDivisions,angle,plusFactor):

        self.colorsArrayName    = "Colors"
        self.widthArrayName     = "Radius"
        self.flag               = 0

        self.vtkPoints          = vtk.vtkPoints() 
        self.vtkLines           = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkRibbonFilter()
        self.vtkMapper          = vtk.vtkPolyDataMapper()
        self.vtkActor           = vtk.vtkActor()
        
        self._initialize(p0,p1,numberOfTimeDivisions,angle,plusFactor)
        
    def _initialize(self,p0, p1,numberOfTimeDivisions, angle, plusFactor):
        
        # geometry and topology
        

        points = getListOfPointsForArc(p0, p1, angle, numberOfTimeDivisions, plusFactor)

        for i in xrange(len(points)):
            point = [points[i][0],points[i][1],0.0]
            self.vtkPoints.InsertNextPoint(point)

        if (p0[0]==p1[0]):
            self.flag = 1
        
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()-1): 
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)

        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLines)

        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(4)
        colors.SetName(self.colorsArrayName)

        radius = vtk.vtkDoubleArray()
        radius.SetNumberOfTuples(self.vtkPoints.GetNumberOfPoints()+1)
        radius.SetName(self.widthArrayName)
        
        for i in xrange(self.vtkPoints.GetNumberOfPoints()):
            aux = 70
            nColor = [aux,aux,aux,255]
            colors.InsertNextTupleValue(nColor)
            radius.SetTuple1(i,1.0 + 1.0/(1.0+i))

        self.vtkPolyData.GetPointData().AddArray(colors)
        self.vtkPolyData.GetPointData().AddArray(radius)
        self.vtkPolyData.GetPointData().SetActiveScalars(self.widthArrayName)

        # filter

        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
            
        self.vtkFilter.UseDefaultNormalOn()        
        self.vtkFilter.SetAngle(0) 
        
        self.vtkFilter.SetWidth(0.5)
        self.vtkFilter.SetVaryWidth(1)
 
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUsePointFieldData()
        self.vtkMapper.SelectColorArray(self.colorsArrayName)
        
        # actor
        
        self.vtkActor.SetMapper(self.vtkMapper)
        #self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        #self.vtkActor.GetProperty().SetSpecular(0.25)
        #self.vtkActor.GetProperty().SetAmbient(0.5)
        #self.vtkActor.GetProperty().SetDiffuse(0.1)
        
        self.vtkActor.GetProperty().SetOpacity(0.995)
           
    def setColorById(self,i,colorTuple):

        self.vtkPolyData.GetPointData().GetArray(self.colorsArrayName).SetTuple(i,colorTuple)

    def setWidthById(self,i,value):

        self.vtkPolyData.GetPointData().GetArray(self.widthArrayName).SetTuple1(i,value)
        

class vtkQueueBox:
    
    def __init__(self,p0,p1,pos,h,distanceFactor,widthFactor):
        
        self.vtkPoints          = vtk.vtkPoints()
        self.vtkLines           = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkMapper          = vtk.vtkPolyDataMapper()  
        self.vtkActor           = vtk.vtkActor()
        
        self._initialize(p0, p1, pos, h, distanceFactor, widthFactor)
        
    def _initialize(self,p0,p1,pos,h,distanceFactor,widthFactor):
        
        # geometry and topology

        d = array(p1) - array(p0)
        
        u = d/linalg.norm(d)
        
        v = zeros(3)
        
        if (abs(u[0])> 0):
        
            v[0] = -u[1]/u[0]
            v[1] = 1.0
            v[2] = 0
        
        
        else:
            
            v[0] = 1.0
            v[1] = 0
            v[2] = 0
        
        w = v/linalg.norm(v)
        
        vl = pos
        qm = (1-vl)*array(p0)+vl*array(p1)
        
        q0 = qm + (h/2.0)*u + distanceFactor*w
        q1 = qm - (h/2.0)*u + distanceFactor*w
        
        q1_minus = lambdaPoint( widthFactor, q1, -w)
        q0_minus = lambdaPoint( widthFactor, q0, -w)
        q0_plus  = lambdaPoint( widthFactor, q0, +w)
        q1_plus  = lambdaPoint( widthFactor, q1, +w)         
        
        z_aux = 1*1E-5
        q1_minus[2] = z_aux
        q0_minus[2] = z_aux
        q0_plus[2] = z_aux
        q1_plus[2] = z_aux
        
        self.vtkPoints.InsertNextPoint(q1_minus)
        self.vtkPoints.InsertNextPoint(q0_minus)
        self.vtkPoints.InsertNextPoint(q0_plus)
        self.vtkPoints.InsertNextPoint(q1_plus)
         
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()-1):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)
        
        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLines)
        
        # mapper
    
        self.vtkMapper = vtk.vtkPolyDataMapper()   
 
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkMapper.SetInput(self.vtkPolyData)
        else:
            self.vtkMapper.SetInputData(self.vtkPolyData)
        
        # actor
        
        self.vtkActor.SetMapper(self.vtkMapper)
        self.vtkActor.GetProperty().SetLineWidth(2)    
        self.vtkActor.GetProperty().SetColor(0.5,0.5,0.5)

class vtkQueueBoxUsingRefPosition:
    
    def __init__(self,p0,p1,pos,h,distanceFactor,widthFactor):
        
        self.vtkPoints          = vtk.vtkPoints()
        self.vtkLines           = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkMapper          = vtk.vtkPolyDataMapper()  
        self.vtkActor           = vtk.vtkActor()
        
        self._initialize(p0, p1, pos, h, distanceFactor, widthFactor)
        
    def _initialize(self,p0,p1,pos,h,distanceFactor,widthFactor):
        
        # geometry and topology

        d = array(p1) - array(p0)
        
        u = d/linalg.norm(d)
        
        v = zeros(3)
        
        if (abs(u[0])> 0):
        
            v[0] = -u[1]/u[0]
            v[1] = 1.0
            v[2] = 0
        
        
        else:
            
            v[0] = 1.0
            v[1] = 0
            v[2] = 0
        
        w = v/linalg.norm(v)
        
        qm = pos + distanceFactor*w
        
        qbp = qm + 0.5*widthFactor*w + 0.5*h*u 
        qbm = qm - 0.5*widthFactor*w + 0.5*h*u
        qhp = qbp - h*u
        qhm = qbm - h*u   
        
        z_aux = 1*1E-5
        qbp[2] = z_aux
        qbm[2] = z_aux
        qhp[2] = z_aux
        qhm[2] = z_aux
        
        self.vtkPoints.InsertNextPoint(qhm)
        self.vtkPoints.InsertNextPoint(qbm)
        self.vtkPoints.InsertNextPoint(qbp)
        self.vtkPoints.InsertNextPoint(qhp)
        
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()-1):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)
        
        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLines)
        
        # mapper
    
        self.vtkMapper = vtk.vtkPolyDataMapper()   
 
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkMapper.SetInput(self.vtkPolyData)
        else:
            self.vtkMapper.SetInputData(self.vtkPolyData)
        
        # actor
        
        self.vtkActor.SetMapper(self.vtkMapper)
        self.vtkActor.GetProperty().SetLineWidth(1.5)    
        self.vtkActor.GetProperty().SetColor(0.5,0.5,0.5)

class vtkQueueRibbonUsingRefPosition:

    def __init__(self,p0,p1,pos,h,distanceFactor,widthFactor):
        
        self.flag               = 0

        self.vtkPoints          = vtk.vtkPoints()
        self.vtkLines           = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkRibbonFilter()
        self.vtkMapper          = vtk.vtkPolyDataMapper()
        self.vtkActor           = vtk.vtkActor()

        self.u                 = array(3)

        self._initialize(p0,p1,pos,h,distanceFactor,widthFactor)

    def _initialize(self,p0,p1,pos,h,distanceFactor,widthFactor):
        
        # geometry and topology 

        d = array(p1) - array(p0)
        
        u = d/linalg.norm(d)

        self.u = u
        
        v = zeros(3)
        
        if (abs(u[0])> 0):
        
            v[0] = -u[1]/u[0]
            v[1] = 1.0
            v[2] = 0.0
        
        else:
            
            v[0] = 1.0
            v[1] = 0
            v[2] = 0  
        
        w = v/linalg.norm(v)
        
        qm = pos + distanceFactor*w
        
        q0 = qm + (h/2.0)*u 
        q1 = qm - (h/2.0)*u 

        z_aux = 1*1E-5
        q0[2] = z_aux
        q1[2] = z_aux

        self.vtkPoints.InsertNextPoint(q0)
        self.vtkPoints.InsertNextPoint(q1)
        
        if (p0[0]==p1[0]):
            self.flag = 1
        
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()-1): 
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)

        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLines)
       
        # filter
       
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
         
        self.vtkFilter.UseDefaultNormalOn()        
        self.vtkFilter.SetAngle(0)  
            
        self.vtkFilter.SetWidth(0.5*widthFactor)
 
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
    
        # actor
    
        self.vtkActor.SetMapper(self.vtkMapper)

        self.vtkActor.GetProperty().SetColor(0,0,1)
        #self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        #self.vtkActor.GetProperty().SetSpecular(0.25)
        #self.vtkActor.GetProperty().SetAmbient(0.75)
        #self.vtkActor.GetProperty().SetDiffuse(0.1)
        self.vtkActor.GetProperty().SetOpacity(1)
        

    def setEndPoint(self,point):

        self.vtkPoints.SetPoint(1, point)

    def setEndPointFromValue(self,value):
 
        point = lambdaPoint(value,self.vtkPoints.GetPoint(0),-self.u)
        self.vtkPoints.SetPoint(1, point)

class vtkQueueRibbonElement:

    def __init__(self,p0,p1,pos,h,distanceFactor,widthFactor):
        
        self.flag               = 0

        self.vtkPoints          = vtk.vtkPoints()
        self.vtkLines           = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkRibbonFilter()
        self.vtkMapper          = vtk.vtkPolyDataMapper()
        self.vtkActor           = vtk.vtkActor()

        self.u                 = array(3)

        self._initialize(p0,p1,pos,h,distanceFactor,widthFactor)

    def _initialize(self,p0,p1,pos,h,distanceFactor,widthFactor):
        
        # geometry and topology 


        d = array(p1) - array(p0)
        
        u = d/linalg.norm(d)

        self.u = u
        
        v = zeros(3)
        
        if (abs(u[0])> 0):
        
            v[0] = -u[1]/u[0]
            v[1] = 1.0
            v[2] = 0.0
        
        else:
            
            v[0] = 1.0
            v[1] = 0
            v[2] = 0  
        
        w = v/linalg.norm(v)
        
        vl = pos
        qm = (1-vl)*array(p0)+vl*array(p1)
        
        q0 = qm + (h/2.0)*u + distanceFactor*w
        q1 = qm - (h/2.0)*u + distanceFactor*w

        z_aux = 1*1E-12
        q0[2] = z_aux
        q1[2] = z_aux

        self.vtkPoints.InsertNextPoint(q0)
        self.vtkPoints.InsertNextPoint(q1)
        
        if (p0[0]==p1[0]):
            self.flag = 1
        
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()-1): 
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)

        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLines)
       
        # filter
       
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
        
        self.vtkFilter.UseDefaultNormalOn()        
        self.vtkFilter.SetAngle(0)
 
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
    
        # actor
    
        self.vtkActor.SetMapper(self.vtkMapper)

        self.vtkActor.GetProperty().SetColor(0,1,0)
        #self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        #self.vtkActor.GetProperty().SetSpecular(0.25)
        #self.vtkActor.GetProperty().SetAmbient(0.75)
        #self.vtkActor.GetProperty().SetDiffuse(0.1)
        self.vtkActor.GetProperty().SetOpacity(1)
        

    def setEndPoint(self,point):

        self.vtkPoints.SetPoint(1, point)

    def setEndPointFromValue(self,value):
 
        point = lambdaPoint(value,self.vtkPoints.GetPoint(0),-self.u)
        self.vtkPoints.SetPoint(1, point)

class vtkPositionPointsElementGlyph:
    
    def __init__(self,p0,p1,numberOfTimeDivisions):

        self.colorsArrayName    = "Colors"
        self.widthArrayName     = "Radius"
        
        self.vtkPoints          = vtk.vtkPoints()
        self.vtkVertices        = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkGlyph3D()
        self.vtkMapper          = vtk.vtkPolyDataMapper()   
        self.vtkActor           = vtk.vtkActor()          

        self._initialize(p0,p1,numberOfTimeDivisions)

    def _initialize(self,p0,p1,numberOfTimeDivisions):

        # geometry and topology
        
        d = array(p1) - array(p0)

        deltaLambda = 1.0/(1.0*numberOfTimeDivisions)

        for i in xrange(numberOfTimeDivisions+1):

            vlambda = i*deltaLambda
            p = lambdaPoint(vlambda,p0,d)
            point = [p[0],p[1],0.0]
            self.vtkPoints.InsertNextPoint(point)
 
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()):
            self.vtkVertices.InsertNextCell(1)
            self.vtkVertices.InsertCellPoint(i)
        
        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkVertices)
        
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName(self.colorsArrayName)
        
        for i in xrange(self.vtkPoints.GetNumberOfPoints()):
            nColor = [255*random.random(),255*random.random(),255*random.random()]
            colors.InsertNextTupleValue(nColor)         

        self.vtkPolyData.GetPointData().AddArray(colors)

        radius = vtk.vtkDoubleArray()
        radius.SetNumberOfTuples(self.vtkPoints.GetNumberOfPoints()+1)
        radius.SetName(self.widthArrayName)
        
        for i in xrange(self.vtkPoints.GetNumberOfPoints()):
            radius.SetTuple1(i,1)

        self.vtkPolyData.GetPointData().AddArray(radius)
        self.vtkPolyData.GetPointData().SetActiveScalars(self.widthArrayName)

        # filter

        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(0.1)
        sphere.SetPhiResolution(16)
        sphere.SetThetaResolution(16)

        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
            
            
        self.vtkFilter.SetSource(sphere.GetOutput())
        self.vtkFilter.ScalingOn()
        self.vtkFilter.SetScaleModeToScaleByScalar()
        self.vtkFilter.SetScaleFactor(0.3)
 
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
           
        self.vtkMapper.ScalarVisibilityOff()
        self.vtkMapper.SetScalarModeToUsePointFieldData()
        self.vtkMapper.SelectColorArray(self.colorsArrayName)
        
        # actor

        self.vtkActor.SetMapper(self.vtkMapper)

        self.vtkActor.GetProperty().SetColor(1,1,1)
        self.vtkActor.GetProperty().SetPointSize(20)
        self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        self.vtkActor.GetProperty().SetSpecular(0.25)
        self.vtkActor.GetProperty().SetAmbient(0.2)
        self.vtkActor.GetProperty().SetDiffuse(0.1)

    def setColorById(self,i,colorTuple):

        self.vtkPolyData.GetPointData().GetArray(self.colorsArrayName).SetTuple(i,colorTuple)

    def setWidthById(self,i,value):

        self.vtkPolyData.GetPointData().GetArray(self.widthArrayName).SetTuple1(i,value)
