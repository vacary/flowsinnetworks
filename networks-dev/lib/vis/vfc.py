"""

VISUALIZATION METHODS AND CLASSES

"""

import vtk
import networkx as nx
import random

from numpy import *
import math

class VtkNodesElements:
    
    def __init__(self,nxGraph,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label):

        self.node_flag          = 0

        self.vtkPoints          = vtk.vtkPoints()
        self.vtkVertices        = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkGlyph3D()
        self.vtkMapper          = vtk.vtkPolyDataMapper()   
        self.vtkActor           = vtk.vtkActor()      
        self.vtkActor2D         = vtk.vtkActor2D()
        
        self.vtkActor2Dst       = vtk.vtkActor2D()

        self._initialize(nxGraph,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label)

    def _initialize(self,G,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label):
    
        st_vtkPoints = vtk.vtkPoints()
        st_vtkPoints.SetNumberOfPoints(2)
    
        # geometry and labels
         
        labels = vtk.vtkStringArray()
        labels.SetNumberOfValues(G.number_of_nodes())
        labels.SetName("labels")
        
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(4)
        colors.SetName("Colors")
        
        radius = vtk.vtkDoubleArray()
        radius.SetNumberOfTuples(G.number_of_nodes())
        radius.SetName("Radius")

        c = 0
                
        for i in G.nodes_iter():
            
            posX = G.node[i]['pos'][0] 
            posY = G.node[i]['pos'][1]
            posZ = G.node[i]['pos'][2] + 0.0
            self.vtkPoints.InsertPoint(G.node[i]['id'],posX,posY,posZ)
            
            if (G.node[i]['nlabel'] == node_source_label):
                
                color   = [255,0,0,255]
                scale   = 1.0
                label   = ''#str(G.node[i]['nlabel'])
                
                st_vtkPoints.SetPoint(0,[posX,posY,posZ])
                
            elif (G.node[i]['nlabel'] == node_sink_label ):
                
                color   = [0,0,255,255]
                scale   = 1.0
                label   = ''#str(G.node[i]['nlabel'])
                
                st_vtkPoints.SetPoint(1,[posX,posY,posZ])
                
            else:
                
                color   = [50,50,50,255]
                scale   = 0.75
                label = str(G.node[i]['nlabel'])
                
            labels.SetValue(c,label)
                
            colors.InsertNextTupleValue(color)
            radius.SetTuple1(c,scale)
            
            self.vtkVertices.InsertNextCell(1)
            self.vtkVertices.InsertCellPoint(c)
            
            c = c + 1
            
        # polydata
            
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkVertices)
        
        self.vtkPolyData.GetPointData().AddArray(labels)
        self.vtkPolyData.GetPointData().AddArray(colors)
        self.vtkPolyData.GetPointData().AddArray(radius)
        
        self.vtkPolyData.GetPointData().SetActiveScalars("Radius")
        
        # filter
                    
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
        self.vtkFilter.SetScaleFactor(1)
 
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())

        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUsePointFieldData()
        self.vtkMapper.SelectColorArray("Colors")
           
        # actor

        self.vtkActor.SetMapper(self.vtkMapper)

        #self.vtkActor.GetProperty().SetColor(1,1,1)
        #self.vtkActor.GetProperty().SetPointSize(50)
        self.vtkActor.GetProperty().SetSpecularColor(0,0,0)
        self.vtkActor.GetProperty().SetSpecular(0.1)
        self.vtkActor.GetProperty().SetAmbient(0.1)
        self.vtkActor.GetProperty().SetDiffuse(0.1)
        self.vtkActor.GetProperty().SetOpacity(opacity)
        #self.vtkActor.GetProperty().LightingOff()
        
        # 2D Actor

        labelMapper = vtk.vtkLabeledDataMapper()
        labelMapper.SetInputData(self.vtkPolyData)
        labelMapper.SetLabelModeToLabelFieldData()
        tprop = labelMapper.GetLabelTextProperty()
        
        nodes_N = G.number_of_nodes() 
        nodes_N_limit = 75
        
        
        if (nodes_N <= nodes_N_limit):
            tprop.SetColor(0.8,0.8,0.8)
        else:
            tprop.SetColor(0.5,0.5,0.5)
        
        tprop.SetFontSize(lbFontSize)
        tprop.SetBold(1)
        tprop.SetItalic(0)
        tprop.SetShadow(0)
        tprop.SetJustificationToCentered()
        tprop.SetVerticalJustificationToCentered()

        self.vtkActor2D.SetMapper(labelMapper)
        
        #### Labels for source and sink node
        
        st_label = vtk.vtkStringArray()
        st_label.SetNumberOfValues(2)
        st_label.SetName("label")
        
        st_verts = vtk.vtkCellArray()
        st_verts.InsertNextCell(1)
        st_verts.InsertCellPoint(0)
        st_verts.InsertNextCell(1)
        st_verts.InsertCellPoint(1)
        
        st_label.SetValue(0,node_source_label)
        st_label.SetValue(1,node_sink_label)
        
        st_pointData  = vtk.vtkPolyData()   
        st_pointData.SetPoints(st_vtkPoints)          
        st_pointData.SetVerts(st_verts)         
        
        st_pointData.GetPointData().AddArray(st_label)            
         
        st_mapper = vtk.vtkPolyDataMapper()
        
        if (vtk.VTK_MAJOR_VERSION <= 5):
            st_mapper.SetInput(st_pointData)
        else:
            st_mapper.SetInputData(st_pointData)
                        
        st_labelMapper = vtk.vtkLabeledDataMapper()
        st_labelMapper.SetInputData(st_pointData)
        st_labelMapper.SetLabelModeToLabelFieldData()
        tprop = st_labelMapper.GetLabelTextProperty()
        tprop.SetFontSize(lbFontSize)
        tprop.SetBold(1)
        tprop.SetItalic(0)
        
        if (nodes_N <= nodes_N_limit):
            tprop.SetShadow(0)
        else:
            tprop.SetShadow(1)
        
        tprop.SetJustificationToCentered()
        tprop.SetVerticalJustificationToCentered()
        
        self.vtkActor2Dst.SetMapper(st_labelMapper)


class VtkTubes:
    
    def __init__(self,listOfPoints,width):
        
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkLines       = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkFilter      = vtk.vtkTubeFilter()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        
        self._initialize(listOfPoints,width)
        
    def _initialize(self,listOfPoints,width):
            
        for i in xrange(len(listOfPoints)):
            point = listOfPoints[i]
            self.vtkPoints.InsertNextPoint(point)
        
        for i in range(0,self.vtkPoints.GetNumberOfPoints()-1): # create lines
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)
         
        self.vtkPolyData = vtk.vtkPolyData()                   # polydata object
        self.vtkPolyData.SetPoints(self.vtkPoints)                     # set geometry
        self.vtkPolyData.SetLines(self.vtkLines)                       # set topology  
        
        
        # filter
 
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
             
        self.vtkFilter.SetRadius(width)
        self.vtkFilter.SetNumberOfSides(20)
        self.vtkFilter.CappingOff()
        
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        self.vtkActor.SetMapper(self.vtkMapper)
        self.vtkActor.GetProperty().SetLineWidth(1)
        self.vtkActor.GetProperty().SetColor(random.random(),random.random(),random.random())    

class VtkRibbons:
    
    def __init__(self,listOfPoints,width):
        
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkLines       = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkFilter      = vtk.vtkRibbonFilter()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        
        self._initialize(listOfPoints,width)
        
    def _initialize(self,listOfPoints,width):
            
        for i in xrange(len(listOfPoints)):
            point = listOfPoints[i]
            self.vtkPoints.InsertNextPoint(point)
        
        for i in range(0,self.vtkPoints.GetNumberOfPoints()-1): # create lines
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0,i)
            line.GetPointIds().SetId(1,i+1)
            self.vtkLines.InsertNextCell(line)
         
        self.vtkPolyData = vtk.vtkPolyData()                   # polydata object
        self.vtkPolyData.SetPoints(self.vtkPoints)                     # set geometry
        self.vtkPolyData.SetLines(self.vtkLines)                       # set topology  
        
        
        # filter
 
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
             
        self.vtkFilter.UseDefaultNormalOn()        
        self.vtkFilter.SetAngle(0) 
        self.vtkFilter.SetWidth(0.25*width)
        
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        self.vtkActor.SetMapper(self.vtkMapper)
        self.vtkActor.GetProperty().SetLineWidth(1)
        self.vtkActor.GetProperty().SetColor(random.random(),random.random(),random.random())    
        
        self.vtkActor.GetProperty().SetOpacity(0.99)
        
#         self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
#         self.vtkActor.GetProperty().SetSpecular(0.5)
#         self.vtkActor.GetProperty().SetAmbient(0.5)
#         self.vtkActor.GetProperty().SetDiffuse(0.1)        
        
    
class VtkLines:
    
    def __init__(self,listOfPoints,width):
        
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkLines       = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        
        self._initialize(listOfPoints,width)
        
    def _initialize(self,listOfPoints,width):
            
        for i in xrange(len(listOfPoints)):
            point = listOfPoints[i]
            self.vtkPoints.InsertNextPoint(point)
        
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
        self.vtkActor.GetProperty().SetLineWidth(width)
        self.vtkActor.GetProperty().SetColor(0.5,0.5,0.5)    


class VtkPoints:
        
    def __init__(self,listOfPoints,pointSize):

        self.vtkPoints          = vtk.vtkPoints()
        self.vtkVertices        = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkMapper          = vtk.vtkPolyDataMapper()   
        self.vtkActor           = vtk.vtkActor()          

        self._initialize(listOfPoints,pointSize)

    def _initialize(self,listOfPoints,pointSize):

        # geometry and topology
        
        for i in xrange(len(listOfPoints)):
            point = listOfPoints[i]
            self.vtkPoints.InsertNextPoint(point)
            
 
        for i in xrange(0,self.vtkPoints.GetNumberOfPoints()):
            self.vtkVertices.InsertNextCell(1)
            self.vtkVertices.InsertCellPoint(i)
        
        # polydata
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkVertices)
        
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
        
        for i in xrange(self.vtkPoints.GetNumberOfPoints()):
            nColor = [0,255,0]
            colors.InsertNextTupleValue(nColor)

        self.vtkPolyData.GetPointData().AddArray(colors)
    
        # mapper
        
        if (vtk.VTK_MAJOR_VERSION <= 5):        # check VTK version
            self.vtkMapper.SetInput(self.vtkPolyData)
        else:
            self.vtkMapper.SetInputData(self.vtkPolyData)
        
        #self.vtkMapper.ScalarVisibilityOn()
        #self.vtkMapper.SetScalarModeToUsePointFieldData()
        #self.vtkMapper.SelectColorArray("Colors")
        
        # actor

        self.vtkActor.SetMapper(self.vtkMapper)

        #self.vtkActor.GetProperty().SetColor(0,1*random.random(),0)
        self.vtkActor.GetProperty().SetPointSize(pointSize)
        #self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        #self.vtkActor.GetProperty().SetSpecular(0.25)
        #self.vtkActor.GetProperty().SetAmbient(0.2)
        #self.vtkActor.GetProperty().SetDiffuse(0.1)

        
        
        