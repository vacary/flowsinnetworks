#
# Custom classes using the VTK library for the 'network' style.
#
# The following classes are defined according to the following
# set of layers for the network visualization:
#
# - Background layer
# - Animation layer  
# - Data layer
# - Interaction layer
#
# Each layer is associated with one of the following classes and the
# respective VTK actor.

# Standard library imports
import sys
import os
import random
import math
import json
from copy import deepcopy

# Custom library imports
import display.vis.utils.data as util
import display.vis.utils.colormaps as cmap

#Non standard library imports
import networkx as nx
from numpy import *
import vtk

# INTERACTOR LAYER
 
class VtkNetworkEdgesInteractorLayer:
     
    """Class defined to build a vtkActor to get the simulation data by edge using a VTK interactor
    """
     
    def __init__(self, G, z_index=5):
 
        # Main layer attributes 
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkPolyData = vtk.vtkPolyData()
        self.vtkFilter = vtk.vtkRibbonFilter()
        self.vtkMapper = vtk.vtkPolyDataMapper()
        self.vtkActor = vtk.vtkActor()
     
        # Edge info
        self.vtkData        = vtk.vtkStringArray()
        self.vtkData.SetName('CellData')
     
        self._initialize(G, z_index)
     
    def _initialize(self, G, z_index):
         
        # Network data is processed using the information for each edge.
         
        # Process graph data and set the vtkCells for each edge 
         
        for edge in list(G.edges(keys=True)):
             
            edge_tail   = G.node[edge[0]]
            edge_head   = G.node[edge[1]]
            edge_id     = edge[2]
             
            # Available access to graph attributes with the format: 
            # G.edge[edge[0]][edge[1]][edge_id]['attr']
 
            current_edge = G.edge[edge[0]][edge[1]][edge_id]
                 
            ### Get geometry information (list of points) for the edge
            ### * Graph list data is available as string
             
            # full list of points for the edge
            edge_geometry = util.get_points_from_string_list(current_edge['geometry']) 
             
            self.setEdgeVtkCells(edge_geometry, edge, z_index)
            self.setEdgeVtkCellData(G, edge, edge_id)
             
        # Set PolyData
         
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkCells)
         
        # Add data
         
        self.vtkPolyData.GetCellData().AddArray(self.vtkData)
         
        # Apply RibbonFilter
         
        if (vtk.VTK_MAJOR_VERSION <= 5):
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
             
        self.vtkFilter.UseDefaultNormalOn() # To prevent change of orientation for the ribbons 
        self.vtkFilter.SetAngle(0)
         
        self.vtkFilter.SetWidth(1)
         
        # Mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        self.vtkActor.SetMapper(self.vtkMapper)
         
        self.vtkActor.GetProperty().SetColor(0.0,0.0,1.0)
        self.vtkActor.GetProperty().SetOpacity(0.0001)
         
    def setEdgeVtkCells(self, edge_geometry, edge, z_index):
         
        cellPointsIds = []
         
        for point in edge_geometry:
             
            point[2] = z_index # increase position z-coordinate
             
            self.vtkPoints.InsertNextPoint(point) # add point to be used in the PolyData definition
             
            pointId = self.vtkPoints.GetNumberOfPoints() - 1
            cellPointsIds.append(pointId)
             
        # create polyline for cell
         
        cellNumberOfPoints = len(cellPointsIds)
         
        polyline = vtk.vtkPolyLine()
        polyline.GetPointIds().SetNumberOfIds(cellNumberOfPoints)
         
        for i in xrange(cellNumberOfPoints):
            polyline.GetPointIds().SetId(i,cellPointsIds[i])
         
        self.vtkCells.InsertNextCell(polyline)
         
         
    def setEdgeVtkCellData(self, G, edge, edge_id):
         
        # Get edge data from graph
 
        ntail_id  = edge[0]
        nhead_id  = edge[1]
         
        label_ntail = G.node[ntail_id]['nlabel']
        label_nhead = G.node[nhead_id]['nlabel']
         
        ntail_label_overtime    = util.getFloatListFromStrList(G.node[ntail_id]['label_overtime'])
        nhead_label_overtime    = util.getFloatListFromStrList(G.node[nhead_id]['label_overtime'])
        f_e_plus_overtime       = util.getFloatListFromStrList(G.edge[ntail_id][nhead_id][edge_id]['f_e_plus_overtime'])
        f_e_minus_overtime      = util.getFloatListFromStrList(G.edge[ntail_id][nhead_id][edge_id]['f_e_minus_overtime'])
        switching_times         = util.getFloatListFromStrList(G.edge[ntail_id][nhead_id][edge_id]['switching_times'])
        z_e_overtime            = util.getFloatListFromStrList(G.edge[ntail_id][nhead_id][edge_id]['z_e_overtime'])
         
        aux_dict = {}
         
        aux_dict['selected_edge']           = '(%s, %s) "%i"' %(label_ntail,label_nhead,edge_id)
        aux_dict['ntail_label_overtime']    = ntail_label_overtime 
        aux_dict['nhead_label_overtime']    = nhead_label_overtime
        aux_dict['f_e_plus_overtime']       = f_e_plus_overtime
        aux_dict['f_e_minus_overtime']      = f_e_minus_overtime
        aux_dict['switching_times']         = switching_times
        aux_dict['z_e_overtime']            = z_e_overtime
        aux_dict['time']                    = G.edge[ntail_id][nhead_id][edge_id]['time']
        aux_dict['capacity']                = G.edge[ntail_id][nhead_id][edge_id]['capacity']
        
        try:
            aux_dict['name'] = G.edge[ntail_id][nhead_id][edge_id]['name']
        except:
            aux_dict['name'] = ''
            
        data = json.dumps(aux_dict)
         
        j = self.vtkCells.GetNumberOfCells() - 1
        self.vtkData.InsertNextValue(data)


# ANIMATION LAYER

class EdgeAnimationData:
    
    """Auxiliary class to store required data for the network animation
    """
    
    def __init__(self):

        self.edgeCellIds = None
        self.edgeCellPointIds = None
        self.queuePointIds = None 
        self.queueRefPoints = None
        self.queueMaxHeight = None
        self.queueRefDirection = None
        self.queueMaxQValue = None 
        self.queueBoxCellId = None
        self.queueCellId = None
    
class VtkNetworkAnimationLayer:
    
    """Class to set the animation actor

    Dynamic layer. Changes on color and width for the edges according
    to the simulation data. In this case, a set of PolyLines is associated to
    each edge, depending on the number of time_steps necessary to reach the
    edge travel time.
    """

    def __init__(self, G, sim_data_pars, z_index=1):
        
        # VTK Elements 
        
        ### Edges 
        
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkPolyData = vtk.vtkPolyData()
        self.vtkFilter = vtk.vtkRibbonFilter()
        self.vtkMapper = vtk.vtkPolyDataMapper()
        self.vtkActor = vtk.vtkActor()
                
        ### Queue boxes (QBoxes) 

        self.vtkQBoxesPoints = vtk.vtkPoints()
        self.vtkQBoxesCells = vtk.vtkCellArray()
        self.vtkQBoxesPolyData = vtk.vtkPolyData()
        self.vtkQBoxesFilter = vtk.vtkRibbonFilter()
        self.vtkQBoxesMapper = vtk.vtkPolyDataMapper()
        self.vtkQBoxesActor = vtk.vtkActor()

        ### Queues

        self.vtkQPoints = vtk.vtkPoints()
        self.vtkQCells = vtk.vtkCellArray()
        self.vtkQPolyData = vtk.vtkPolyData()
        self.vtkQFilter = vtk.vtkRibbonFilter()
        self.vtkQMapper = vtk.vtkPolyDataMapper()
        self.vtkQActor = vtk.vtkActor()

        # Data arrays
        
        self.vtkRadiusFactors = vtk.vtkDoubleArray()
        self.vtkColors = vtk.vtkUnsignedCharArray()
        
        self.vtkQBoxesCellsColors = vtk.vtkUnsignedCharArray()
        self.vtkQCellsColors = vtk.vtkUnsignedCharArray()
        
        # Others
        
        self.edge_counter = 0
        self.edge_animation_temp_data = EdgeAnimationData() # auxiliary element to store the edge animation data
        
        self.edges_dict = {} # dictionary to store point ids and cell ids associated to each edge
        
        self.edges_max_capacity = 0
        self.edges_max_width = 1.0
        self.edges_max_f_e_minus = 0.0

        self.edges_queues_qratio = 0.22 # qbox distance from reference point
        self.edges_queues_widthFactor = 0.075*0.5 # qbox width
        self.edges_queues_distanceFactor = 0.0 # qbox distance from edge
        self.edges_queues_h = 1.25*self.edges_queues_widthFactor # qbox height
         
        self.lut = vtk.vtkLookupTable()
        self.vtkColorBarActor = vtk.vtkScalarBarActor()
        
        self._initialize(G, sim_data_pars, z_index)
    
    def _initialize(self, G, sim_data_pars, z_index):

        # Set max capacity 
                
        for edge in list(G.edges(keys=True)):
            
            capacity = G.edge[edge[0]][edge[1]][edge[2]]['capacity']
            self.edges_max_capacity = max(self.edges_max_capacity, capacity)

        # Set max flow rate
        
        self.edges_max_f_e_minus = sim_data_pars['max_f_e_minus']

        # Data array setup
        
        self.vtkRadiusFactors.SetName('Radius')
        self.vtkColors.SetName('Colors')
        self.vtkColors.SetNumberOfComponents(4)
        
        self.vtkQBoxesCellsColors.SetName('QBoxesColors')
        self.vtkQBoxesCellsColors.SetNumberOfComponents(4)        
        
        self.vtkQCellsColors.SetName('QColors')
        self.vtkQCellsColors.SetNumberOfComponents(4)        
                                          
        # Network data process
        # The network data is processed using the information of each edge
        
        for edge in list(G.edges(keys=True)):
             
            edge_tail   = G.node[edge[0]]
            edge_head   = G.node[edge[1]]
            edge_id     = edge[2]
            
            # Available access to edge attributes using the format: 
            # G.edge[edge[0]][edge[1]][edge_id]['attr']

            current_edge = G.edge[edge[0]][edge[1]][edge_id]
                
            ### Get geometry information (list of points) and capacity for the edge

            # full list of points for the edge
            edge_geometry = util.get_points_from_string_list(current_edge['geometry']) 
            
            # list of references to recognize time divisions for each edge
            edge_keys = util.get_int_array_from_string_list(current_edge['geometry_keys'])
            
            # Use VTK cells to store the edge information and setup queues geometry and topology
            
            edge_capacity = current_edge['capacity'] 
            
            edge_cells_pointIds = self.set_edge_vtk_cells(edge_geometry, edge_keys, z_index)
            self.set_edge_vtk_cells_radius_data(edge_cells_pointIds, edge_capacity)
            self.set_edge_vtk_queue_and_qbox_geometry_and_topology(edge_geometry, sim_data_pars, z_index)
        
            # Store the animation data created with the previous methods in the edges' dictionary
            
            aux = deepcopy(self.edge_animation_temp_data)
            self.edges_dict[(edge[0],edge[1],edge_id)] = aux 
        
            self.edge_counter = self.edge_counter + 1
        
        # PolyData setup
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkCells)
        self.vtkPolyData.GetCellData().AddArray(self.vtkColors)
        self.vtkPolyData.GetPointData().AddArray(self.vtkRadiusFactors)
        self.vtkPolyData.GetPointData().SetActiveScalars('Radius')
        
        self.vtkQBoxesPolyData.SetPoints(self.vtkQBoxesPoints)
        self.vtkQBoxesPolyData.SetLines(self.vtkQBoxesCells)
        self.vtkQBoxesPolyData.GetCellData().AddArray(self.vtkQBoxesCellsColors)  
        
        self.vtkQPolyData.SetPoints(self.vtkQPoints)
        self.vtkQPolyData.SetLines(self.vtkQCells)
        self.vtkQPolyData.GetCellData().AddArray(self.vtkQCellsColors)        
        
        # Filters
        
        if (vtk.VTK_MAJOR_VERSION <= 5):
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
        self.vtkFilter.UseDefaultNormalOn() # To prevent a change in the orientation of the ribbons
        self.vtkFilter.SetAngle(0)
        self.vtkFilter.SetWidth(self.edges_max_width) # Default reference width
        self.vtkFilter.SetVaryWidth(1)

        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkQFilter.SetInput(self.vtkQPolyData)
        else:
            self.vtkQFilter.SetInputData(self.vtkQPolyData)
        self.vtkQFilter.UseDefaultNormalOn()        
        self.vtkQFilter.SetAngle(0) 
        self.vtkQFilter.SetWidth(0.5*self.edges_queues_widthFactor)
        
        # Mapper setup

        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUseCellFieldData()
        self.vtkMapper.SelectColorArray('Colors')        
        
        if (vtk.VTK_MAJOR_VERSION <= 5):
            self.vtkQBoxesMapper.SetInput(self.vtkQBoxesPolyData)
        else:
            self.vtkQBoxesMapper.SetInputData(self.vtkQBoxesPolyData)
        self.vtkQBoxesMapper.ScalarVisibilityOn()
        self.vtkQBoxesMapper.SetScalarModeToUseCellFieldData()
        self.vtkQBoxesMapper.SelectColorArray('QBoxesColors')
        
        self.vtkQMapper.SetInputConnection(self.vtkQFilter.GetOutputPort())
        self.vtkQMapper.ScalarVisibilityOn()
        self.vtkQMapper.SetScalarModeToUseCellFieldData()
        self.vtkQMapper.SelectColorArray('QColors')
                        
        # Actor
        
        self.vtkActor.SetMapper(self.vtkMapper)        
        self.vtkActor.GetProperty().SetColor(1, 0.0, 0.0)
        self.vtkActor.GetProperty().SetOpacity(1)

        self.vtkQBoxesActor.SetMapper(self.vtkQBoxesMapper)
        self.vtkQBoxesActor.GetProperty().SetLineWidth(2)        
        
        self.vtkQActor.SetMapper(self.vtkQMapper)
        
        # ScalarBar
        
        max_color = 1.0
        min_color = 0.55
        
        numberOfTuples = 20
        self.lut.SetNumberOfTableValues(numberOfTuples)
        
        delta_color = (max_color - min_color)/(1.0*numberOfTuples)
        
        for i in xrange(numberOfTuples+1):
            color = (0,0*min_color + 0*i*delta_color,min_color + i*delta_color,1)
            self.lut.SetTableValue(i,color[0],color[1],color[2],color[3])
            
        self.vtkMapper.SetScalarRange(0,self.edges_max_f_e_minus)
        self.vtkMapper.SetLookupTable(self.lut)

        self.vtkColorBarActor.SetLookupTable(self.vtkMapper.GetLookupTable())
        self.vtkColorBarActor.SetTitle("Flow rate")
        self.vtkColorBarActor.SetMaximumWidthInPixels(80)
        self.vtkColorBarActor.SetMaximumHeightInPixels(500)
        self.vtkColorBarActor.SetOrientationToVertical()
        self.vtkColorBarActor.GetTitleTextProperty().SetFontSize(100)
        self.vtkColorBarActor.GetTitleTextProperty().SetLineOffset(25)
        self.vtkColorBarActor.SetLabelFormat('%.1f')
        self.vtkColorBarActor.SetNumberOfLabels(5)
        self.vtkColorBarActor.UseOpacityOn()

        self.vtkColorBarActor.GetProperty().SetOpacity(1)
        self.vtkColorBarActor.GetTitleTextProperty().SetOpacity(1)

        self.vtkColorBarActor.SetLookupTable(self.lut)
        

    def set_edge_vtk_cells(self, edge_geometry, edge_keys, z_index):
        
        """ From the edge geometry (list of points for the edge) creates a set of
        vtkPolyLines which are stored in several components of the vtkCellArray
        """
        
        edge_firstCellId = self.vtkCells.GetNumberOfCells()
        edge_firstPointId = self.vtkPoints.GetNumberOfPoints()
        
        # Build polylines and store them in cells

        if (edge_keys[0] == 0):
            self.edge_animation_temp_data.edgeCellPointIds = []

        for k in xrange(len(edge_keys)-1):
            
            local_edge_firstPointId = self.vtkPoints.GetNumberOfPoints()
            
            # Add points to vtkPoints
                    
            for i in xrange(edge_keys[k],edge_keys[k+1]+1):
                
                point = edge_geometry[i]
                point[2] = z_index 
                self.vtkPoints.InsertNextPoint(point)
    
            local_edge_lastPointId = self.vtkPoints.GetNumberOfPoints()-1
            
            cellPointIds = range(local_edge_firstPointId,local_edge_lastPointId+1)
            cellNumberOfPoints = len(cellPointIds)
            polyline = vtk.vtkPolyLine()
            polyline.GetPointIds().SetNumberOfIds(cellNumberOfPoints)
            
            for i in xrange(cellNumberOfPoints):
                polyline.GetPointIds().SetId(i, cellPointIds[i])
            
            self.vtkCells.InsertNextCell(polyline)

            # Add the color tuple for the cell
            color = [int(255*random.random()),int(255*random.random()),int(255*random.random()),int(255*0)]
            self.vtkColors.InsertNextTupleValue(color)
            
            # Save animation data

            self.edge_animation_temp_data.edgeCellPointIds.append(cellPointIds)
            
        edge_lastPointId = self.vtkPoints.GetNumberOfPoints()-1
        edge_lastCellId = self.vtkCells.GetNumberOfCells()-1
        
        edge_cells_cellIds = range(edge_firstCellId, edge_lastCellId+1)
        edge_cells_pointIds = range(edge_firstPointId, edge_lastPointId+1)

        # Save animation data
        
        self.edge_animation_temp_data.edgeCellIds = edge_cells_cellIds
                
        return edge_cells_pointIds

    def set_edge_vtk_cells_radius_data(self, edge_cells_pointIds, edge_capacity):
        
        for pointId in edge_cells_pointIds:
            
            self.vtkRadiusFactors.InsertNextValue(0.0) # increase number of components
            
            defaultWidth_multiplier = edge_capacity/self.edges_max_capacity # temporal factor  
            
            self.vtkRadiusFactors.SetTuple1(pointId, defaultWidth_multiplier) # assign radius factor to point
        
    def set_edge_vtk_queue_and_qbox_geometry_and_topology(self, edge_geometry, sim_data_pars, z_index):
        
        # Parameters
        
        qratio = self.edges_queues_qratio # qbox distance from reference point
        widthFactor = self.edges_queues_widthFactor # qbox width
        distanceFactor = self.edges_queues_distanceFactor # qbox distance from edge
        h = self.edges_queues_h # qbox height
        z_aux = z_index + 0.1 # corrected z_index for the queue elements
        
        # Queue box
        
        ### reference points
        p = array(edge_geometry[0])
        q = array(edge_geometry[1])
        
        u = (q-p)/linalg.norm(q-p)
        
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
        
        qm = p + u*qratio + distanceFactor*w
        
        qbp = qm + 0.5*widthFactor*w + 0.5*h*u 
        qbm = qm - 0.5*widthFactor*w + 0.5*h*u
        qhp = qbp - h*u
        qhm = qbm - h*u   
        
        qbp[2] = z_aux
        qbm[2] = z_aux
        qhp[2] = z_aux
        qhm[2] = z_aux
        
        ### add points for the box (qbox geometry)     
        self.vtkQBoxesPoints.InsertNextPoint(qhm)
        self.vtkQBoxesPoints.InsertNextPoint(qbm)
        self.vtkQBoxesPoints.InsertNextPoint(qbp)
        self.vtkQBoxesPoints.InsertNextPoint(qhp)
        
        ### create polyline and store it in a cell
        q_inf_key = 4*self.edge_counter
        polyLine = vtk.vtkPolyLine()
        polyLine.GetPointIds().SetNumberOfIds(4)
        polyLine.GetPointIds().SetId(0,q_inf_key)
        polyLine.GetPointIds().SetId(1,q_inf_key+1)
        polyLine.GetPointIds().SetId(2,q_inf_key+2)
        polyLine.GetPointIds().SetId(3,q_inf_key+3)
        self.vtkQBoxesCells.InsertNextCell(polyLine)
    
        ### add color associated to this cell
        
        color = [int(255*0),int(255*1),int(255*0),int(255)]
        self.vtkQBoxesCellsColors.InsertNextTupleValue(color)

        # Queue
        
        qb = 0.5*(qbp + qbm)
        qh = qb - h*u
        
        qb[2] = z_aux
        qh[2] = z_aux 
        
        ### add points for queue element (queue geometry)
        self.vtkQPoints.InsertNextPoint(qb)
        self.vtkQPoints.InsertNextPoint(qh)
        
        ### create polyline for queue
        q_inf_key = 2*self.edge_counter
        polyLine = vtk.vtkPolyLine()
        polyLine.GetPointIds().SetNumberOfIds(2)
        polyLine.GetPointIds().SetId(0,q_inf_key)
        polyLine.GetPointIds().SetId(1,q_inf_key+1)
        self.vtkQCells.InsertNextCell(polyLine)
        
        ### add color associated to this cell
        
        color = [int(255*0.25),int(255*0.25),int(255*0.25),int(255*0)]
        self.vtkQCellsColors.InsertNextTupleValue(color)
        
        # Animation data
        
        queue_pointIds = [q_inf_key,q_inf_key+1] # extreme pointIds for queue
        queue_refPoints = [qb,qh] # reference points for queue
        queue_maxHeight = linalg.norm(qh-qb)
        queue_refDirection = (qh-qb) / queue_maxHeight
        queue_maxQValue = sim_data_pars['max_z_e']
        
        queue_boxCellId = self.edge_counter
        queue_cellId = self.edge_counter
                
        # Save animation data
        
        self.edge_animation_temp_data.queuePointIds = queue_pointIds
        self.edge_animation_temp_data.queueRefPoints = queue_refPoints
        self.edge_animation_temp_data.queueMaxHeight = queue_maxHeight
        self.edge_animation_temp_data.queueRefDirection = queue_refDirection
        self.edge_animation_temp_data.queueMaxQValue = queue_maxQValue
        self.edge_animation_temp_data.queueBoxCellId = queue_boxCellId
        self.edge_animation_temp_data.queueCellId = queue_cellId

    def setCellColorById(self, cell_id, flow_value):
        
        color = [0,0,1]
        
        self.lut.GetColor(flow_value,color)
        
        ref_value = flow_value/self.edges_max_f_e_minus
        
        if (flow_value < 1E-8):
            alpha = int(255*0)
            color_tuple = [int(1*255),int(0*255),int(0*255),alpha]
            
            if (flow_value < 0):
                color_tuple = [int(1*255),int(0*255),int(0*255),255]            
        else:
            alpha = int(255*0.825)
            color_tuple = [int(color[0]*255),int(color[1]*255),int(color[2]*255),alpha]
        
        self.vtkPolyData.GetCellData().GetArray('Colors').SetTuple(cell_id, color_tuple)

    def setPointWidthById(self, point_id, flow_value):
        
        defaultWidth_multiplier = max(flow_value/self.edges_max_capacity,1E-6)
        self.vtkPolyData.GetPointData().GetArray('Radius').SetTuple1(point_id, defaultWidth_multiplier)
        
    def setQBoxCellColorById(self, cell_id, queue_value):
        
        color_tuple = [int(255*0.75),int(255*0.0),int(255*0.0),int(255*1)]
        if (queue_value < 1E-10):
            #color_tuple = [int(255*0.25),int(255*0.25),int(255*0.25),255]
            color_tuple = [int(255*0.0),int(255*0.8),int(255*0),int(255)]
        
        if (queue_value < 0):
            color_tuple = [int(255*0.2),int(255*0.2),int(255*0.2),int(255)]
            
        self.vtkQBoxesPolyData.GetCellData().GetArray('QBoxesColors').SetTuple(cell_id, color_tuple)
        
    def setQCellColorById(self, cell_id, queue_value):

        color_tuple = [int(255*1.0),int(0),int(0),int(255*1)]
        if (queue_value < 1E-10):
            color_tuple = [int(255*0),int(0.5*255),int(0.0),int(255*1)]
            
        if (queue_value < 0):
            color_tuple = [int(255*0.25),int(255*0.25),int(255*0.25),int(255)]
        #color_tuple[3] = int(0*random.random()*255)
        self.vtkQPolyData.GetCellData().GetArray('QColors').SetTuple(cell_id, color_tuple)


# STATIC LAYER

class VtkNetworkStaticLayer:
    
    """ Superclass. This layer displays the edges of the network with different
    widths according to the capacity of each edge.
    """    
    
    def __init__(self, G, z_index=0):
        
        # main VTK elements 
        
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkPolyData = vtk.vtkPolyData()
        self.vtkFilter = vtk.vtkRibbonFilter()
        self.vtkMapper = vtk.vtkPolyDataMapper()
        self.vtkActor = vtk.vtkActor()
        
        # Data arrays
        
        self.vtkRadiusFactors = vtk.vtkDoubleArray()
        self.vtkColors = vtk.vtkUnsignedCharArray()
                
        # Others
        
        self.edge_to_cell_dict ={}
        self.edges_max_capacity = 0.0 # to set the width of the edges according to the network capacities 
        self.edges_max_width = 1.0
        self.edges_max_time = 0.0
        
        # initialize
        
        self._initialize(G, z_index)
        
    def _initialize(self, G, z_index):

        # Set max capacity and time
                
        for edge in list(G.edges(keys=True)):
            
            capacity = G.edge[edge[0]][edge[1]][edge[2]]['capacity']
            time = G.edge[edge[0]][edge[1]][edge[2]]['time']
            
            self.edges_max_capacity = max(self.edges_max_capacity, capacity)
            self.edges_max_time = max(self.edges_max_time, time)

        # Data array setup
        
        self.vtkRadiusFactors.SetName('Radius')
        self.vtkColors.SetName('Colors')
        self.vtkColors.SetNumberOfComponents(4)
                                            
        # Network data process
        # The network data is processed using the information of each edge
        
        for edge in list(G.edges(keys=True)):
             
            edge_tail   = G.node[edge[0]]
            edge_head   = G.node[edge[1]]
            edge_id     = edge[2]
            
            # Available access to edge attributes using the format: 
            # G.edge[edge[0]][edge[1]][edge_id]['attr']

            current_edge = G.edge[edge[0]][edge[1]][edge_id]
                
            ### Get geometry information (list of points) and capacity for the edge

            edge_geometry = util.get_points_from_string_list(current_edge['geometry']) # full list of points for the edge
            edge_capacity = current_edge['capacity']
            edge_time = current_edge['time']
            
            self.edges_max_capacity = max(self.edges_max_capacity, edge_capacity) # update edges max capacity
            self.edges_max_time = max(self.edges_max_time, edge_time) # update edges max time
            
            # Use VTK cells to store the edge information
            
            edge_cell_pointIds = self.set_edge_vtk_cells(edge_geometry, z_index)
            self.set_edge_vtk_cells_radius_and_color_data(edge_cell_pointIds, edge_capacity)
     
            # Store cell id
            
            self.edge_to_cell_dict[(edge[0],edge[1],edge_id)] = self.vtkCells.GetNumberOfCells() - 1
     
        # PolyData setup
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkCells)
        self.vtkPolyData.GetPointData().AddArray(self.vtkRadiusFactors)
        self.vtkPolyData.GetPointData().SetActiveScalars('Radius')
        self.vtkPolyData.GetCellData().AddArray(self.vtkColors)
        
        # Apply RibbonFilter
        
        if (vtk.VTK_MAJOR_VERSION <= 5):
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
            
        self.vtkFilter.UseDefaultNormalOn() # To prevent a change in the orientation of the ribbons
        self.vtkFilter.SetAngle(0)
        self.vtkFilter.SetWidth(self.edges_max_width) # Default reference width
        self.vtkFilter.SetVaryWidth(1)
        
        # Mapper setup
        
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUseCellFieldData()
        self.vtkMapper.SelectColorArray('Colors')
        
        # Actor
        
        self.vtkActor.SetMapper(self.vtkMapper)        
        #self.vtkActor.GetProperty().SetColor(0.35, 0.35, 0.35)
        self.vtkActor.GetProperty().SetOpacity(1)
        
    def set_edge_vtk_cells(self, edge_geometry, z_index):
        
        """ From the edge geometry (list of points for the edge) creates
        a vtkPolyLine which is stored in a component of the vtkCellArray
        """

        # Create a list with the point ids to create the polyline

        cellPointIds = []
        
        for point in edge_geometry:
            
            point[2] = z_index
            
            self.vtkPoints.InsertNextPoint(point) # add point to vtkPoints
            
            pointId = self.vtkPoints.GetNumberOfPoints()-1 # get the id and append to the list
            cellPointIds.append(pointId)
            
        # Create the polyline and store it in the cell
            
        cellNumberOfPoints = len(cellPointIds)
        
        polyline = vtk.vtkPolyLine()
        polyline.GetPointIds().SetNumberOfIds(cellNumberOfPoints)
        
        for i in xrange(cellNumberOfPoints):
            polyline.GetPointIds().SetId(i, cellPointIds[i])
        
        self.vtkCells.InsertNextCell(polyline)
        
        return cellPointIds

    def set_edge_vtk_cells_radius_and_color_data(self, edge_cell_pointIds, edge_capacity):
        
        for pointId in edge_cell_pointIds:
            
            self.vtkRadiusFactors.InsertNextValue(0.0) # increase number of components
            
            default_width_multiplier = edge_capacity/self.edges_max_capacity
            self.vtkRadiusFactors.SetTuple1(pointId, default_width_multiplier) # assign radius factor to point

        color = [int(0.35*255),int(0.35*255),int(0.35*255),int(255)]
        self.vtkColors.InsertNextTupleValue(color)

    def setCellColorById(self, cell_id, color_tuple):
        
        self.vtkPolyData.GetCellData().GetArray('Colors').SetTuple(cell_id, color_tuple)

### BACKGROUND AND DATA LAYERS

class VtkNetworkBackgroundLayer(VtkNetworkStaticLayer):
    
    def __init__(self, G, z_index=0):
        
        VtkNetworkStaticLayer.__init__(self, G, z_index)

class VtkNetworkDataTimesLayer(VtkNetworkStaticLayer):
    
    def __init__(self, G, z_index=3):
        
        VtkNetworkStaticLayer.__init__(self, G, z_index)
        
        self.lut = vtk.vtkLookupTable()
        self.vtkColorBarActor = vtk.vtkScalarBarActor()
        self.set_lut_and_colorbar()
        self.vtkColorBarActor.GetProperty().SetOpacity(1)
        self.vtkColorBarActor.GetTitleTextProperty().SetOpacity(1)
        
        self.G = G
        self.displayEdgeTimes()
        self.vtkActor.GetProperty().SetOpacity(1)

    def set_lut_and_colorbar(self):

        lut_colors = cmap.get_color_map('autumn')
        lut_colors.reverse()
        self.lut.SetNumberOfTableValues(len(lut_colors))
        
        i = 0
        for color in lut_colors:
            self.lut.SetTableValue(i,color[0],color[1],color[2],color[3])
            i = i + 1
        
        self.vtkMapper.SetScalarRange(0,self.edges_max_capacity)
        self.vtkMapper.SetLookupTable(self.lut)

        self.vtkColorBarActor.SetLookupTable(self.vtkMapper.GetLookupTable())
        self.vtkColorBarActor.SetTitle("Time    ")
        self.vtkColorBarActor.SetMaximumWidthInPixels(60)
        self.vtkColorBarActor.SetMaximumHeightInPixels(500)
        self.vtkColorBarActor.SetOrientationToVertical()
        self.vtkColorBarActor.GetTitleTextProperty().SetFontSize(100)
        self.vtkColorBarActor.GetTitleTextProperty().SetLineOffset(25)
        self.vtkColorBarActor.SetLabelFormat('%.1f')
        self.vtkColorBarActor.SetNumberOfLabels(5)
        self.vtkColorBarActor.UseOpacityOn()

        self.vtkColorBarActor.SetLookupTable(self.lut)
                        
    def displayEdgeTimes(self):
        
        for edge in list(self.G.edges(keys=True)):

            cell_id = self.edge_to_cell_dict[edge]
            edge_time = self.G.edge[edge[0]][edge[1]][edge[2]]['time']
            aux_value = edge_time/self.edges_max_time
            #color_tuple = [0,int(255*aux_value),0,255]
            color = [0,0,0]
            self.lut.GetColor(aux_value, color)
            color_tuple = [int(255*color[0]),int(255*color[1]),int(255*color[2]),255]
            
            self.setCellColorById(cell_id, color_tuple)

class VtkNetworkDataCapacitiesLayer(VtkNetworkStaticLayer):
    
    def __init__(self, G, z_index=2):
        
        VtkNetworkStaticLayer.__init__(self, G, z_index)

        self.lut = vtk.vtkLookupTable()
        self.vtkColorBarActor = vtk.vtkScalarBarActor()
        self.set_lut_and_colorbar()
        self.vtkColorBarActor.GetProperty().SetOpacity(1)
        self.vtkColorBarActor.GetTitleTextProperty().SetOpacity(1)    
        
        self.G = G
        self.displayEdgeCapacities()
        self.vtkActor.GetProperty().SetOpacity(1)

    def set_lut_and_colorbar(self):

        lut_colors = cmap.get_color_map('autumn')
        #lut_colors.reverse()
        self.lut.SetNumberOfTableValues(len(lut_colors))
        
        i = 0
        for color in lut_colors:
            self.lut.SetTableValue(i,color[0],color[1],color[2],color[3])
            i = i + 1
        
        self.vtkMapper.SetScalarRange(0,self.edges_max_capacity)
        self.vtkMapper.SetLookupTable(self.lut)

        self.vtkColorBarActor.SetLookupTable(self.vtkMapper.GetLookupTable())
        self.vtkColorBarActor.SetTitle("Capacity")
        self.vtkColorBarActor.SetMaximumWidthInPixels(80)
        self.vtkColorBarActor.SetMaximumHeightInPixels(500)
        self.vtkColorBarActor.SetOrientationToVertical()
        self.vtkColorBarActor.GetTitleTextProperty().SetFontSize(100)
        self.vtkColorBarActor.GetTitleTextProperty().SetLineOffset(25)
        self.vtkColorBarActor.SetLabelFormat('%.1f')
        self.vtkColorBarActor.SetNumberOfLabels(5)
        self.vtkColorBarActor.UseOpacityOn()

        self.vtkColorBarActor.SetLookupTable(self.lut)


    def displayEdgeCapacities(self):

        for edge in list(self.G.edges(keys=True)):

            cell_id = self.edge_to_cell_dict[edge]
            edge_capacity = self.G.edge[edge[0]][edge[1]][edge[2]]['capacity']
            aux_value = edge_capacity/self.edges_max_capacity
            #color_tuple = [0,int(255*aux_value),0,255]

            color = [0,0,0]
            self.lut.GetColor(aux_value, color)
            color_tuple = [int(255*color[0]),int(255*color[1]),int(255*color[2]),255]
            
            self.setCellColorById(cell_id, color_tuple)

# NODES        
    
class VtkNetworkNodesLayer:
    
    """Class with the vtk elements to display flat polygons as the nodes of the
    current network
    """
    
    def __init__(self, G, node_source_label, node_sink_label, nodes_size, z_index=5):
        
        # main VTK elements
        
        self.vtkPoints = vtk.vtkPoints()
        self.vtkVertices = vtk.vtkCellArray()
        self.vtkPolyData = vtk.vtkPolyData()
        self.vtkFilter = vtk.vtkGlyph3D()
        self.vtkMapper = vtk.vtkPolyDataMapper()
        self.vtkActor = vtk.vtkActor()
        
        # Data arrays
        
        self.vtkColors = vtk.vtkUnsignedCharArray()
        
        # Elements for labels

        self.vtkActor_st_labels = vtk.vtkActor2D() # labels for nodes in {source, sink}
        self.vtkActor_non_st_labels = vtk.vtkActor2D() # labels for nodes not {source, sink}
        
        # Others
        
        self.node_source_id = None
        self.node_sink_id = None
        
        # initialize
        
        self._initialize(G, node_source_label, node_sink_label, nodes_size, z_index)
    
    def _initialize(self, G, node_source_label, node_sink_label, nodes_size, z_index):
        
        # Data array setup
        
        self.vtkColors.SetNumberOfComponents(4)
        self.vtkColors.SetName('Colors')
        
        nodes_counter = 0
        
        for i in G.nodes_iter():
            
            self.vtkVertices.InsertNextCell(1)
            self.vtkVertices.InsertCellPoint(nodes_counter)
            
            pos_x = G.node[i]['pos'][0]
            pos_y = G.node[i]['pos'][1]
            pos_z = z_index
            
            self.vtkPoints.InsertPoint(G.node[i]['id'],pos_x,pos_y,pos_z)
             
            if (G.node[i]['nlabel'] == node_source_label):
                
                self.node_source_id = i
                color = [255,0,0,255]
                
            elif (G.node[i]['nlabel'] == node_sink_label):
                
                self.node_sink_id = i
                color = [0,50,255,255]
                
            else:
                
                color = [85,85,85,255]
                
            self.vtkColors.InsertNextTupleValue(color)
            
            nodes_counter = nodes_counter + 1  
            
        # PolyData setup
        
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkVertices)
        self.vtkPolyData.GetPointData().AddArray(self.vtkColors)
        
        # Apply filter
        
        source = vtk.vtkRegularPolygonSource()
        source.SetNumberOfSides(50)
        source.SetRadius(nodes_size)
        
        if (vtk.VTK_MAJOR_VERSION <= 5):
            self.vtkFilter.SetInput(self.vtkPolyData)
            self.vtkFilter.SetSource(source.GetOutput())
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
            self.vtkFilter.SetSourceConnection(source.GetOutputPort())
        
        # Mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUsePointFieldData()
        self.vtkMapper.SelectColorArray('Colors')
        
        # Actor
        
        self.vtkActor.SetMapper(self.vtkMapper)

        self.vtkActor.GetProperty().SetSpecularColor(0,0,0)
        self.vtkActor.GetProperty().SetSpecular(0.1)
        self.vtkActor.GetProperty().SetAmbient(0.05)
        self.vtkActor.GetProperty().SetDiffuse(0.5)
        self.vtkActor.GetProperty().SetOpacity(1)
        
        self.set_st_labels(G, node_source_label, node_sink_label, z_index)
        self.set_non_st_labels(G, node_source_label, node_sink_label, z_index)
        
    def set_st_labels(self, G, node_source_label, node_sink_label, z_index):
        
        # Source and sink nodes labels
        
        ### Geometry
        st_labels_vtkPoints = vtk.vtkPoints()
        st_labels_vtkPoints.SetNumberOfPoints(2)
        
        # // source position 
        posX = G.node[self.node_source_id]['pos'][0]
        posY = G.node[self.node_source_id]['pos'][1]
        posZ = z_index
        st_labels_vtkPoints.SetPoint(0,[posX,posY,posZ])
        
        # // sink position
        posX = G.node[self.node_sink_id]['pos'][0]
        posY = G.node[self.node_sink_id]['pos'][1]
        posZ = z_index
        st_labels_vtkPoints.SetPoint(1,[posX,posY,posZ])
        
        
        ### Topology
        st_labels_vtkVerts = vtk.vtkCellArray()
        st_labels_vtkVerts.InsertNextCell(1)
        st_labels_vtkVerts.InsertCellPoint(0)
        st_labels_vtkVerts.InsertNextCell(1)
        st_labels_vtkVerts.InsertCellPoint(1)

        ### Data Array
        
        st_labels = vtk.vtkStringArray() 
        st_labels.SetNumberOfValues(2)
        st_labels.SetValue(0,'s')#node_source_label)
        st_labels.SetValue(1,'t')#node_sink_label)
        
        ### PolyData
        st_labels_vtkPolyData = vtk.vtkPolyData()
        st_labels_vtkPolyData.SetPoints(st_labels_vtkPoints)
        st_labels_vtkPolyData.SetVerts(st_labels_vtkVerts)
        st_labels_vtkPolyData.GetPointData().AddArray(st_labels)
        
        ### Mapper
        st_labels_vtkMapper = vtk.vtkPolyDataMapper()
        if (vtk.VTK_MAJOR_VERSION <= 5):
            st_labels_vtkMapper.SetInput(st_labels_vtkPolyData)
        else:
            st_labels_vtkMapper.SetInputData(st_labels_vtkPolyData)
                  
        ### Labeled Mapper
        st_labels_vtkLabeledDataMapper = vtk.vtkLabeledDataMapper()
        st_labels_vtkLabeledDataMapper.SetInputData(st_labels_vtkPolyData)
        st_labels_vtkLabeledDataMapper.SetLabelModeToLabelFieldData()
        
        ### Text Properties
        tprop = st_labels_vtkLabeledDataMapper.GetLabelTextProperty()
        tprop.SetColor(1,1,1)
        tprop.SetOpacity(1)
        tprop.SetFontSize(12)
        tprop.SetBold(1)
        tprop.SetItalic(0)
        tprop.SetShadow(0)
        tprop.SetJustificationToCentered()
        tprop.SetVerticalJustificationToCentered()
        
        ### Set actor 
        self.vtkActor_st_labels.SetMapper(st_labels_vtkLabeledDataMapper)
        
    def set_non_st_labels(self, G, node_source_label, node_sink_label, z_index):

        # Non source and sink nodes labels

        if (G.number_of_nodes() <= 2):
            
            pass
        
        else:
        
            ### Geometry, topology and label array
            
            non_st_labels_vtkPoints = vtk.vtkPoints()
            non_st_labels_vtkVerts = vtk.vtkCellArray()
            
            non_st_labels = vtk.vtkStringArray()
            non_st_labels.SetNumberOfValues(G.number_of_nodes()-2)
            
            for i in G.nodes_iter():
                
                if (G.node[i]['nlabel'] not in [node_source_label,node_sink_label]):
                    
                    label = str(G.node[i]['nlabel'])
                    
                    posX = G.node[i]['pos'][0]
                    posY = G.node[i]['pos'][1]
                    posZ = z_index
                    
                    non_st_labels_vtkPoints.InsertNextPoint(posX,posY,posZ)
                    non_st_labels_vtkVerts.InsertNextCell(1)
                    
                    point_id = non_st_labels_vtkPoints.GetNumberOfPoints()-1
                    non_st_labels_vtkVerts.InsertCellPoint(point_id)
                    non_st_labels.SetValue(point_id,label)

            ### PolyData
            non_st_labels_vtkPolyData = vtk.vtkPolyData()
            non_st_labels_vtkPolyData.SetPoints(non_st_labels_vtkPoints)
            non_st_labels_vtkPolyData.SetVerts(non_st_labels_vtkVerts)
            non_st_labels_vtkPolyData.GetPointData().AddArray(non_st_labels)
            
            ### Mapper
            non_st_labels_vtkMapper = vtk.vtkPolyDataMapper()
            if (vtk.VTK_MAJOR_VERSION <= 5):
                non_st_labels_vtkMapper.SetInput(non_st_labels_vtkPolyData)
            else:
                non_st_labels_vtkMapper.SetInputData(non_st_labels_vtkPolyData)
                      
            ### Labeled Mapper
            non_st_labels_vtkLabeledDataMapper = vtk.vtkLabeledDataMapper()
            non_st_labels_vtkLabeledDataMapper.SetInputData(non_st_labels_vtkPolyData)
            non_st_labels_vtkLabeledDataMapper.SetLabelModeToLabelFieldData()
            #non_st_labels_vtkLabeledDataMapper.SetStatic(1)
            
            ### Text Properties
            tprop = non_st_labels_vtkLabeledDataMapper.GetLabelTextProperty()
            tprop.SetColor(1,1,1)
            tprop.SetOpacity(1)
            tprop.SetFontSize(12)
            tprop.SetBold(1)
            tprop.SetItalic(0)
            tprop.SetShadow(0)
            tprop.SetJustificationToCentered()
            tprop.SetVerticalJustificationToCentered()
            
            ### Set actor 
            self.vtkActor_non_st_labels.SetMapper(non_st_labels_vtkLabeledDataMapper)


class VtkMapBackground:            

    def __init__(self, map_file_path, ox, oy, p1x, p1y, p2x, p2y):

        self.vtkActor = vtk.vtkActor()
        
        self._initialize(map_file_path, ox, oy, p1x, p1y, p2x, p2y)
        
    def _initialize(self, map_file_path, ox, oy, p1x, p1y, p2x, p2y):
        
        planeSource = vtk.vtkPlaneSource()
        planeSource.SetOrigin(ox,oy,0.0)
        planeSource.SetPoint1(p1x,p1y,0.0)
        planeSource.SetPoint2(p2x,p2y,0.0)
        planeSource.SetNormal(0.0,0.0,1.0)
        planeSource.SetCenter(0.5*(ox+p1x),0.5*(oy+p2y),-1)
        planeSource.Update()
        
        reader = vtk.vtkJPEGReader()
        reader.SetFileName(map_file_path)
          
        texture = vtk.vtkTexture()
        if vtk.VTK_MAJOR_VERSION <= 5:
            texture.SetInput(reader.GetOutput())
        else:
            texture.SetInputConnection(reader.GetOutputPort())
          
        texturePlane = vtk.vtkTextureMapToPlane()
        if vtk.VTK_MAJOR_VERSION <= 5:
            texturePlane.SetInput(plane.GetOutputPort())
        else:
            texturePlane.SetInputConnection(planeSource.GetOutputPort())    
          
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(texturePlane.GetOutput())
        else:
            mapper.SetInputConnection(texturePlane.GetOutputPort())
         
        self.vtkActor.SetMapper(mapper)
        self.vtkActor.SetTexture(texture)
        
    

