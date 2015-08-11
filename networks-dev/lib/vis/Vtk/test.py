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
import lib.vis.Vtk.rsc.colormaps as cmap

class VtkNetworkBck:
     
    def __init__(self,G,style_pars):
     
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkLineCells   = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkFilter      = vtk.vtkRibbonFilter()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        self.vtkColorBar    = vtk.vtkScalarBarActor()
        
        self.edges_dict     = {}
        self.cells_colors   = vtk.vtkUnsignedCharArray()
        
        self.lut            = vtk.vtkLookupTable()
    
        self._initialize(G,style_pars)
        
    def _initialize(self,G,style_pars):
    
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
         
        # filter
        
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
                
        self.vtkFilter.UseDefaultNormalOn()        
        self.vtkFilter.SetAngle(0) 
            
        self.vtkFilter.SetWidth(1)
        #self.vtkFilter.SetVaryWidth(1)
        
        # mapper
        
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUseCellFieldData()
        self.vtkMapper.SelectColorArray('Colors')

        self.vtkActor.SetMapper(self.vtkMapper)
        
        if (G.number_of_nodes() <= 75):
            self.vtkActor.GetProperty().SetColor(0.2,0.2,0.2)
        else:
            self.vtkActor.GetProperty().SetColor(0.1,0.1,0.1)

class VtkNetwork:
     
    def __init__(self,G,style_pars):
     
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkLineCells   = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkFilter      = vtk.vtkRibbonFilter()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        self.vtkColorBar    = vtk.vtkScalarBarActor()
        
        self.edges_dict     = {}
        self.cells_colors   = vtk.vtkUnsignedCharArray()
        
        self.lut            = vtk.vtkLookupTable()
    
        self._initialize(G,style_pars)
        
    def _initialize(self,G,style_pars):
    
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
        
        # colors 
        
        self.cells_colors.SetNumberOfComponents(4)
        self.cells_colors.SetName('Colors')

        for i in xrange(self.vtkLineCells.GetNumberOfCells()):
            #nColor = [int(255*(random.random())),int(255*(random.random())),int(255*(random.random())),200]
            nColor = [int(255*0.15),int(255*0.15),int(255*0.15),int(255*0)]
            self.cells_colors.InsertNextTupleValue(nColor)
        self.vtkPolyData.GetCellData().AddArray(self.cells_colors)
 
        useFilter = True
        
        if (useFilter == True):
 
            # filter
   
            if (vtk.VTK_MAJOR_VERSION <= 5):   
                self.vtkFilter.SetInput(self.vtkPolyData)
            else:
                self.vtkFilter.SetInputData(self.vtkPolyData)
                    
            self.vtkFilter.UseDefaultNormalOn()        
            self.vtkFilter.SetAngle(0) 
                
            self.vtkFilter.SetWidth(1)
            #self.vtkFilter.SetVaryWidth(1)
   
            # mapper
        
            self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        else:

            # mapper
            
            if (vtk.VTK_MAJOR_VERSION <= 5):                # check VTK version
                self.vtkMapper.SetInput(self.vtkPolyData)
            else:
                self.vtkMapper.SetInputData(self.vtkPolyData)

        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUseCellFieldData()
        self.vtkMapper.SelectColorArray('Colors')

        self.vtkActor.SetMapper(self.vtkMapper)
        
        # scalarbar
        
        self.vtkColorBar.SetLookupTable(self.vtkMapper.GetLookupTable())
        self.vtkColorBar.SetTitle("Flow rate")
        self.vtkColorBar.SetMaximumWidthInPixels(60)
        #self.vtkColorBar.SetMaximumHeightInPixels(500)
        self.vtkColorBar.SetOrientationToVertical()
        self.vtkColorBar.GetTitleTextProperty().SetFontSize(100)
        self.vtkColorBar.GetTitleTextProperty().SetLineOffset(25)
        self.vtkColorBar.SetLabelFormat('%.1f')
        self.vtkColorBar.SetNumberOfLabels(5)
        self.vtkColorBar.UseOpacityOn()

        colorMap = cmap.getColorMap(5)

        self.lut.SetNumberOfTableValues(len(colorMap))
  
        i = 0
        for rgbColor in colorMap:
            c = rgbColor
            self.lut.SetTableValue(i,c[0],c[1],c[2],0.825)
            i = i + 1
    

        self.lut.Build()
                
        self.vtkMapper.SetScalarRange(0,style_pars['max_f_e_minus'])
        self.vtkMapper.SetLookupTable(self.lut)
        self.vtkColorBar.SetLookupTable(self.lut)
        
    def setCellColorByID2(self,cell_id,color_tuple):
        
        self.vtkPolyData.GetCellData().GetArray('Colors').SetTuple(cell_id,color_tuple)
        
    def setCellColorByID(self,cell_id,flow_value):
        
        color = [0,0,0]
        self.lut.GetColor(flow_value,color)
        if (flow_value < 1E-8):
            alpha = int(255*0)
            color_tuple = [int(1*255),int(0*255),int(0*255),alpha]
            #color_tuple = [int(0*255),int(0*255),int(0*255),alpha]
            #color_tuple = [int(0.32*255),int(0.32*255),int(0.32*255),alpha]
            #color_tuple = [int(255),int(0*255),int(0*255),alpha]       
            #color_tuple = [int(color[0]*255),int(color[1]*255),int(color[2]*255),alpha]
        else:
            alpha = int(255*0.825)
            color_tuple = [int(color[0]*255),int(color[1]*255),int(color[2]*255),alpha]
        
        self.vtkPolyData.GetCellData().GetArray('Colors').SetTuple(cell_id,color_tuple)
        
        
        
        
