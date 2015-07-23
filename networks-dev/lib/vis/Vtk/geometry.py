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
        
        mcv = 50
        
        for edge in G.edges_iter():
            
            edge_color = [int(mcv+(255-mcv)*random.random()),int(mcv+(255-mcv)*random.random()),int(mcv+(255-mcv)*random.random())]
           
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
             
        #### other properties
        
        self.vtkPointsActor.GetProperty().SetPointSize(1.25)
        self.vtkPointsActor.GetProperty().SetOpacity(0.75)
        
        #####################

        
        
        
        
        
        
        
        
        
        
        