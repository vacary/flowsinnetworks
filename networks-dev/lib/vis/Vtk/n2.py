"""

VISUALIZATION METHODS AND CLASSES

networks2

* Test for colors - using edge divisions from the visualization time step 

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
        self.vtkColorBar    = vtk.vtkScalarBarActor()
        
        self.edges_dict     = {}
        self.cells_colors   = vtk.vtkUnsignedCharArray()
        
        self.lut            = vtk.vtkLookupTable()
    
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
 
        # filter
   
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            vtkFilter.SetInput(self.vtkPolyData)
        else:
            vtkFilter.SetInputData(self.vtkPolyData)
               
        vtkFilter.UseDefaultNormalOn()        
        vtkFilter.SetAngle(0) 
           
        vtkFilter.SetWidth(0.025)
        #vtkFilter.SetVaryWidth(1)
   
        # mapper
   
        self.vtkMapper.SetInputConnection(vtkFilter.GetOutputPort())
        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUseCellFieldData()
        self.vtkMapper.SelectColorArray('Colors')

        self.vtkActor.SetMapper(self.vtkMapper)
        #self.vtkActor.GetProperty().SetSpecularColor(1,1,1)
        #self.vtkActor.GetProperty().SetSpecular(0.25)
        #self.vtkActor.GetProperty().SetAmbient(0.25)
        #self.vtkActor.GetProperty().SetDiffuse(0)
        
        # scalarbar
        
        self.vtkColorBar.SetLookupTable(self.vtkMapper.GetLookupTable())
        self.vtkColorBar.SetTitle("Flow rate")
        self.vtkColorBar.SetNumberOfLabels(4)
        self.vtkColorBar.SetMaximumWidthInPixels(80)
        self.vtkColorBar.SetOrientationToVertical()
        self.vtkColorBar.GetTitleTextProperty().SetLineOffset(25)
        
        
        self.lut = vtk.vtkLookupTable()
        self.lut.SetNumberOfTableValues(120)
        self.lut.SetHueRange(230/360.0,0.0)

        self.lut.Build()
        
#         self.lut.SetTableValue(0,0.2,0.2,0.2,1)
#         self.lut.SetTableValue(1,0.0,1.0,1.0,1)
#         self.lut.SetTableValue(2,0.0,1.0,0.0,1)
#         self.lut.SetTableValue(3,1.0,0.0,0.0,1)
#         self.lut.SetTableValue(1,0.0,1.0,1.0,1)
#         self.lut.SetTableValue(2,0.0,1.0,0.0,1)
#         self.lut.SetTableValue(3,1.0,0.0,0.0,1)
#         self.lut.SetTableValue(1,0.0,1.0,1.0,1)
#         self.lut.SetTableValue(2,0.0,1.0,0.0,1)
#         self.lut.SetTableValue(3,1.0,0.0,0.0,1)        
                
        self.vtkMapper.SetScalarRange(0,10.0)
        self.vtkMapper.SetLookupTable(self.lut)
        self.vtkColorBar.SetLookupTable(self.lut)

    def setCellColorByID(self,cell_id,color_tuple):
        
        self.vtkPolyData.GetCellData().GetArray('Colors').SetTuple(cell_id,color_tuple)
        
    def setCellColorByID2(self,cell_id,flow_value):
        
        color = [0,0,0]
        self.lut.GetColor(flow_value,color)
        if (flow_value < 1E-6):
            alpha = int(255*0.1)
            #color_tuple = [int(0*255),int(0*255),int(0*255),alpha]
            #color_tuple = [int(0*255),int(0*255),int(0*255),alpha]
            color_tuple = [int(0.75*255),int(0.75*255),int(0.75*255),alpha]            
        else:
            alpha = int(255*0.5)
            color_tuple = [int(color[0]*255),int(color[1]*255),int(color[2]*255),alpha]
        
        self.vtkPolyData.GetCellData().GetArray('Colors').SetTuple(cell_id,color_tuple)
        
        
        
        
