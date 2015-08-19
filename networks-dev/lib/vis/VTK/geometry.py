"""

VISUALIZATION METHODS AND CLASSES

geometry

"""

import sys, os

import vtk
import networkx as nx
import random

from numpy import *
import math

lib_path = os.path.abspath(os.path.join('..','..','..','lib'))
sys.path.append(lib_path)

import lib.vis.general as gen

class VtkNodes:
    
    def __init__(self,nxGraph,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label):

        self.node_flag          = 0

        self.vtkPoints          = vtk.vtkPoints()
        self.vtkVertices        = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkGlyph3D()
        self.vtkMapper          = vtk.vtkPolyDataMapper()   
        self.vtkActor           = vtk.vtkActor()    # actor for nodes
            
        self.vtkActor2D         = vtk.vtkActor2D()  # actor for labels (nodes not in {source,sink})
        self.vtkActor2Dst       = vtk.vtkActor2D()  # actor for labels (nodes in {source,sink})

        self._initialize(nxGraph,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label)

    def _initialize(self,G,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label):
    
        # vtkPoints for source and sink labels
    
        st_vtkPoints = vtk.vtkPoints()
        st_vtkPoints.SetNumberOfPoints(2)
    
        # ACTOR FOR NODES
    
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
                
                #color   = [int(1*255),0,0,255]
                color   = [255,0,0,255]
                radius_scale   = 1.5
                label   = ''#str(G.node[i]['nlabel'])
                
                st_vtkPoints.SetPoint(0,[posX,posY,posZ])
                
            elif (G.node[i]['nlabel'] == node_sink_label ):
                
                color   = [0,50,255,255]
                radius_scale   = 1.5
                label   = ''#str(G.node[i]['nlabel'])
                
                st_vtkPoints.SetPoint(1,[posX,posY,posZ])
                
            else:
                
                color   = [50,50,50,255]
                radius_scale   = 0.5
                label = ''#str(G.node[i]['nlabel'])
                
            labels.SetValue(c,label)
                
            colors.InsertNextTupleValue(color)
            radius.SetTuple1(c,radius_scale)
            
            self.vtkVertices.InsertNextCell(1)
            self.vtkVertices.InsertCellPoint(c)
            
            c = c + 1
            
        # polydata
            
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkVertices)
        
        ### add arrays 
        self.vtkPolyData.GetPointData().AddArray(labels)
        self.vtkPolyData.GetPointData().AddArray(colors)
        self.vtkPolyData.GetPointData().AddArray(radius)
        
        self.vtkPolyData.GetPointData().SetActiveScalars("Radius")
        
        # filter for nodes
                    
        source = vtk.vtkSphereSource()
        source.SetRadius(nodeRadius)
        source.SetPhiResolution(16)
        source.SetThetaResolution(40)
            
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
        self.vtkActor.GetProperty().SetSpecularColor(0,0,0)
        self.vtkActor.GetProperty().SetSpecular(0.1)
        self.vtkActor.GetProperty().SetAmbient(0.05)
        self.vtkActor.GetProperty().SetDiffuse(0.5)
        self.vtkActor.GetProperty().SetOpacity(opacity)
        
        # 2D ACTOR FOR LABELS

        labelMapper = vtk.vtkLabeledDataMapper()
        labelMapper.SetInputData(self.vtkPolyData)
        labelMapper.SetLabelModeToLabelFieldData()
        tprop = labelMapper.GetLabelTextProperty()
        
        nodes_N = G.number_of_nodes() 
        nodes_N_limit = 75
        
        if (nodes_N <= nodes_N_limit):
            tprop.SetColor(0.8,0.8,0.8)
        else:
            tprop.SetColor(0.25,0.25,0.25)
        
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
        
        st_label.SetValue(0,'s')#node_source_label)
        st_label.SetValue(1,'t')#node_sink_label)
        
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

class VtkNetwork:
     
    def __init__(self,G):
     
        # Geometry
        self.vtkPoints      = vtk.vtkPoints()
        
        # Topology
        self.vtkVertices    = vtk.vtkCellArray()
        
        # For points
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkPointsActor = vtk.vtkActor()
    
        self._initialize(G)
        
    def _initialize(self,G):
    
        inf_point_index = 0
        sup_point_index = 0
      
        edge_log = {}
        
        point_id = 0
        
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
        
        maxValue = 150 
        minValue = 50
        
        for edge in G.edges_iter():
            
            edge_color = [int((maxValue - minValue)*random.random() + minValue),int((maxValue - minValue)*random.random() + minValue),int((maxValue - minValue)*random.random() + minValue)]
           
            edge_tail = G.node[edge[0]]
            edge_head = G.node[edge[1]]
            
            if edge not in edge_log:
                edge_log[edge] = 0
            else:
                edge_log[edge] = edge_log[edge] + 1
                
            edge_id = edge_log[edge]
                
            str_edge_geometry = G.edge[edge[0]][edge[1]][edge_id]['geometry']
                
            edge_geometry = gen.getPointsFromStrList(str_edge_geometry)
            
            #local geometry
            
            for point in edge_geometry:
                self.vtkPoints.InsertNextPoint(point)
                self.vtkVertices.InsertNextCell(1)
                self.vtkVertices.InsertCellPoint(point_id)
                colors.InsertNextTupleValue(edge_color)
                point_id = point_id + 1
                
            sup_point_index = inf_point_index + len(edge_geometry) - 1
                             
            inf_point_index = sup_point_index + 1
         
        # for points
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkVertices)
        
        if (vtk.VTK_MAJOR_VERSION <= 5):
            self.vtkMapper.SetInput(self.vtkPolyData)
        else:
            self.vtkMapper.SetInputData(self.vtkPolyData)
        
        # points actor
        self.vtkPointsActor.SetMapper(self.vtkMapper)
        
        #### adding colors
        
        self.vtkPolyData.GetPointData().SetScalars(colors)
        
        #####################

        
        
        
        
        
        
        
        
        
        
        