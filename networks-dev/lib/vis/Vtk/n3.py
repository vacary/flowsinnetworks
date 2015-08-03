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
        self.vtkLineCells   = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        
        self.edges_dict     = {}
        self.cells_colors   = vtk.vtkUnsignedCharArray()
    
        self._initialize(G)
        
    def _initialize(self,G):
    
        inf_point_index = 0
        sup_point_index = 0
      
        edge_log = {}
          
        edge_counter    = 0
        point_id        = 0    
        cell_id         = 0

        for edge in G.edges_iter():

            #print edge
   
            edge_tail = G.node[edge[0]]
            edge_head = G.node[edge[1]]
            
            if edge not in edge_log:
                edge_log[edge] = 0
            else:
                edge_log[edge] = edge_log[edge] + 1
                
            edge_id = edge_log[edge]
                
            str_edge_geometry   = G.edge[edge[0]][edge[1]][edge_id]['geometry']
            str_edge_keys       = G.edge[edge[0]][edge[1]][edge_id]['geometry_keys']
                
            edge_geometry = gen.getPointsFromStrList(str_edge_geometry)
            edge_keys     = gen.getArrayFromStrList(str_edge_keys)
            
            #local geometry
            
            local_point_id  = 0
            
            kc      = 0
            inf_key = int(edge_keys[kc])
            sup_key = int(edge_keys[kc+1])
            
            # for edge points classification 
            localCellPointsIDs = []
            aux_stack = []
            
            edgeCellIDs = []
            edgeCellPointsIDs = []
            
            for point in edge_geometry:
                
                self.vtkPoints.InsertNextPoint(point)
                
                # edge points manager
            
                if (len(aux_stack)> 0):
            
                    localCellPointsIDs.append(aux_stack.pop())
                
                if (local_point_id <= sup_key):
                    
                    localCellPointsIDs.append(point_id)
                    
                    if (local_point_id == sup_key):
                        
                        aux_stack.append(point_id)

                        # create polyline for cell
                        cell_numberOfPoints = len(localCellPointsIDs)
                        polyLine = vtk.vtkPolyLine()
                        polyLine.GetPointIds().SetNumberOfIds(cell_numberOfPoints)
                        for i in xrange(cell_numberOfPoints):
                            polyLine.GetPointIds().SetId(i,localCellPointsIDs[i])
                        self.vtkLineCells.InsertNextCell(polyLine)                        
                        
                        edgeCellPointsIDs.append(localCellPointsIDs)
                        edgeCellIDs.append(cell_id)
                        
                        cell_id = cell_id + 1
                        
                        localCellPointsIDs   = []
                
                        if (sup_key != int(edge_keys[-1])):
                            kc      = kc + 1
                            inf_key = int(edge_keys[kc])
                            sup_key = int(edge_keys[kc+1])
                            
                local_point_id  = local_point_id + 1
                point_id        = point_id + 1
                
            sup_point_index = inf_point_index + len(edge_geometry) - 1
            inf_point_index = sup_point_index + 1
            
            #########
            self.edges_dict[(edge[0],edge[1],edge_id)] = [edgeCellIDs,edgeCellPointsIDs]
            
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLineCells)

        vtkFilter = vtk.vtkRibbonFilter()
        
        # colors 
        
        self.cells_colors.SetNumberOfComponents(4)
        self.cells_colors.SetName('Colors')

        for i in xrange(self.vtkLineCells.GetNumberOfCells()):
            nColor = [int(255*(random.random())),int(255*(random.random())),int(255*(random.random())),200]
            self.cells_colors.InsertNextTupleValue(nColor)
        self.vtkPolyData.GetCellData().AddArray(self.cells_colors)
 
#         # filter
#   
#         if (vtk.VTK_MAJOR_VERSION <= 5):   
#             vtkFilter.SetInput(self.vtkPolyData)
#         else:
#             vtkFilter.SetInputData(self.vtkPolyData)
#               
#         vtkFilter.UseDefaultNormalOn()        
#         vtkFilter.SetAngle(0) 
#           
#         vtkFilter.SetWidth(0.09)
#         #vtkFilter.SetVaryWidth(1)
#   
#         # mapper
#   
#         self.vtkMapper.SetInputConnection(vtkFilter.GetOutputPort())
#         self.vtkMapper.ScalarVisibilityOn()
#         self.vtkMapper.SetScalarModeToUseCellFieldData()
#         self.vtkMapper.SelectColorArray('Colors')

        if (vtk.VTK_MAJOR_VERSION <= 5):
            self.vtkMapper.SetInput(self.vtkPolyData)
        else:
            self.vtkMapper.SetInputData(self.vtkPolyData)

        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUseCellFieldData()
        self.vtkMapper.SelectColorArray('Colors')
        
        self.vtkActor.SetMapper(self.vtkMapper)
        #self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        #self.vtkActor.GetProperty().SetSpecular(0.25)
        #self.vtkActor.GetProperty().SetAmbient(0.25)
        #self.vtkActor.GetProperty().SetDiffuse(0)

    def setCellColorByID(self,cell_id,color_tuple):
        
        self.vtkPolyData.GetCellData().GetArray('Colors').SetTuple(cell_id,color_tuple)
        
        
        
        
        
