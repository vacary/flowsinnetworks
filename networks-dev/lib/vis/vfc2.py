"""

VISUALIZATION METHODS AND CLASSES

"""

import vtk
import networkx as nx
import random

from numpy import *
import math

class VtkNodesElementGlyph:
    
    def __init__(self,nxGraph,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label):

        self.node_flag          = 0

        self.vtkPoints          = vtk.vtkPoints()
        self.vtkVertices        = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkGlyph3D()
        self.vtkMapper          = vtk.vtkPolyDataMapper()   
        self.vtkActor           = vtk.vtkActor()      
        self.vtkActor2D         = vtk.vtkActor2D()    

        self._initialize(nxGraph,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label)

    def _initialize(self,G,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label):
    
        # geometry and labels
        
        labels = vtk.vtkStringArray()
        labels.SetNumberOfValues(G.number_of_nodes())
        labels.SetName("labels")
        
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
        
        k = 0
        for i in G.nodes_iter():
            
            posX = G.node[i]['pos'][0] 
            posY = G.node[i]['pos'][1]
            posZ = G.node[i]['pos'][2]
            
            self.vtkPoints.InsertPoint(G.node[i]['id'],posX,posY,posZ)
            
            if (G.node[i]['nlabel']==node_source_label):
                color = [255,0,0]
            elif (G.node[i]['nlabel']==node_sink_label):
                color = [0,0,255]
            else:
                color = [100,100,100]
            
            colors.InsertNextTupleValue(color)
            
            self.vtkVertices.InsertNextCell(1)
            self.vtkVertices.InsertCellPoint(k)
            
            k = k + 1
            
        # polydata
            
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkVertices)
        
        self.vtkPolyData.GetPointData().AddArray(labels)
        self.vtkPolyData.GetPointData().AddArray(colors)

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
        tprop.SetFontSize(lbFontSize)
        tprop.SetBold(1)
        tprop.SetItalic(0)
        tprop.SetShadow(0)
        tprop.SetJustificationToCentered()
        tprop.SetVerticalJustificationToCentered()

        self.vtkActor2D.SetMapper(labelMapper)




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
    
    def __init__(self,listOfPoints):
        
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkLines       = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        
        self._initialize(listOfPoints)
        
    def _initialize(self,listOfPoints):
            
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
        self.vtkActor.GetProperty().SetLineWidth(1.5)
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

        
        
        