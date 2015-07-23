"""

VISUALIZATION METHODS AND CLASSES

networks1

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
     
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkCells       = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
    
        self._initialize(G)
        
    def _initialize(self,G):
    
        inf_point_index = 0
        sup_point_index = 0
      
        edge_log = {}
          
        edge_counter = 0
          
        for edge in G.edges_iter():
           
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
                  
            sup_point_index = inf_point_index + len(edge_geometry) - 1
              
            #local topology
              
            numberOfPoints = len(edge_geometry)
            polyLine = vtk.vtkPolyLine()
            polyLine.GetPointIds().SetNumberOfIds(numberOfPoints)
            for i in xrange(numberOfPoints):
                polyLine.GetPointIds().SetId(i,inf_point_index + i)
            self.vtkCells.InsertNextCell(polyLine)
               
            inf_point_index = sup_point_index + 1
         
     
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkCells)

        vtkFilter = vtk.vtkRibbonFilter()

        colors             = vtk.vtkUnsignedCharArray()
        radius             = vtk.vtkDoubleArray()

        colors.SetNumberOfComponents(4)
        colors.SetName('Colors')
        radius.SetNumberOfTuples(self.vtkPoints.GetNumberOfPoints())
        radius.SetName('Radius')
        
        for i in xrange(self.vtkCells.GetNumberOfCells()):
            nColor = [int(255*(random.random())),int(255*(random.random())),int(255*(random.random())),100]
            colors.InsertNextTupleValue(nColor)
            
        for i in xrange(self.vtkPoints.GetNumberOfPoints()):
            radius.SetTuple1(i,random.random())

        self.vtkPolyData.GetCellData().AddArray(colors)
        
        self.vtkPolyData.GetPointData().AddArray(radius)
        self.vtkPolyData.GetPointData().SetActiveScalars('Radius')

        # filter
 
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            vtkFilter.SetInput(self.vtkPolyData)
        else:
            vtkFilter.SetInputData(self.vtkPolyData)
             
        vtkFilter.UseDefaultNormalOn()        
        vtkFilter.SetAngle(0) 
         
        vtkFilter.SetWidth(0.5)
        vtkFilter.SetVaryWidth(1)
  
        # mapper
  
        self.vtkMapper.SetInputConnection(vtkFilter.GetOutputPort())
        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUseCellFieldData()
        self.vtkMapper.SelectColorArray('Colors')
        
        # actor
        
        self.vtkActor.SetMapper(self.vtkMapper)
        #self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        #self.vtkActor.GetProperty().SetSpecular(0.25)
        #self.vtkActor.GetProperty().SetAmbient(0.5)
        #self.vtkActor.GetProperty().SetDiffuse(0.1)
        
        #self.vtkActor.GetProperty().SetOpacity(1)
        
#         p0 = [1,0,0]
#         p1 = [0,1,0]
#         p2 = [0,1,2]
#         p3 = [1,2,3]
#         p4 = [2,3,4]
#         p5 = [6,7,8]
#         p6 = [8,6,5]
#         p7 = [1,2,8]
#         
#         points = vtk.vtkPoints()
#         points.InsertNextPoint(p0)
#         points.InsertNextPoint(p1)
#         points.InsertNextPoint(p2)
#         points.InsertNextPoint(p3)
#         points.InsertNextPoint(p4)
#         points.InsertNextPoint(p5)
#         points.InsertNextPoint(p6)
#         points.InsertNextPoint(p7)
#         
#         cells = vtk.vtkCellArray()
#          
#         polyLine = vtk.vtkPolyLine()
#         polyLine.GetPointIds().SetNumberOfIds(4)
#         for i in xrange(4):
#             polyLine.GetPointIds().SetId(i,i)
#     
#         cells.InsertNextCell(polyLine)
# 
#         polyLine = vtk.vtkPolyLine()
#         polyLine.GetPointIds().SetNumberOfIds(4)
#         for i in xrange(4):
#             polyLine.GetPointIds().SetId(i,i+4)
#               
#         cells.InsertNextCell(polyLine)
#        
#         polyData = vtk.vtkPolyData()
#         polyData.SetPoints(points)
#         polyData.SetLines(cells)
#         
#         colors = vtk.vtkUnsignedCharArray()
#         colors.SetNumberOfComponents(3)
#         colors.SetName("Colors")
#         
#         for i in xrange(points.GetNumberOfPoints()):
#             nColor = [int(255*random.random()),int(255*random.random()),int(255*random.random())]
#             colors.InsertNextTupleValue(nColor)
# 
#         polyData.GetCellData().SetScalars(colors)
#          
#         mapper = vtk.vtkPolyDataMapper()
#         
#         if (vtk.VTK_MAJOR_VERSION <= 5):
#             mapper.SetInput(polyData)
#         else:
#             mapper.SetInputData(polyData)
#      
#         self.vtkActor.SetMapper(mapper)            
            
            
            