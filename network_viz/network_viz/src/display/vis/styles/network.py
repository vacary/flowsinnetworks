#
# Setup and update functions for 'network' style.

# Standard library imports
import os
import sys
import random

# Non standard library imports
import networkx as nx
from numpy import *
import vtk

# Custom library imports

import display.vis.utils as util
import display.vis.utils.annotations as vtk_info
import display.vis.utils.background as set_bck
import display.vis.VTK.network as VTK

def scene_setup(G, renderer, pars, sim_data_pars):
    
    """ Set the elements for the visualization style
    """
    
    scene_edges_layers = []
    scene_edges_interactor_layers = []
    
    # Add Background Layer
    
    nw_bck = VTK.VtkNetworkBackgroundLayer(G, z_index=0)
    renderer.AddActor(nw_bck.vtkActor)
    scene_edges_layers.append(nw_bck)
    
    # Add Data Layers

    ## times
    nw_data_times = VTK.VtkNetworkDataTimesLayer(G, z_index=1)
    
    #renderer.AddActor(nw_data_times.vtkActor)
    #renderer.AddActor2D(nw_data_times.vtkColorBarActor)
    
    nw_data_times.vtkColorBarActor.GetPositionCoordinate().SetValue(0.92,0.04)
    nw_data_times.vtkColorBarActor.SetWidth(0.05)
    nw_data_times.vtkColorBarActor.SetHeight(0.4)
    
    scene_edges_layers.append(nw_data_times)

    ## capacities
    nw_data_capacities = VTK.VtkNetworkDataCapacitiesLayer(G, z_index=2)

    #renderer.AddActor(nw_data_capacities.vtkActor)
    #renderer.AddActor2D(nw_data_capacities.vtkColorBarActor)
    
    nw_data_capacities.vtkColorBarActor.GetPositionCoordinate().SetValue(0.92,0.04)
    nw_data_capacities.vtkColorBarActor.SetWidth(0.05)
    nw_data_capacities.vtkColorBarActor.SetHeight(0.4)
    
    scene_edges_layers.append(nw_data_capacities)
    
    # Add Animation Layer

    nw = VTK.VtkNetworkAnimationLayer(G, sim_data_pars, z_index=3)
    
    renderer.AddActor(nw.vtkActor)
    renderer.AddActor(nw.vtkQBoxesActor)
    renderer.AddActor(nw.vtkQActor)
    renderer.AddActor2D(nw.vtkColorBarActor)
    
    nw.vtkColorBarActor.GetPositionCoordinate().SetValue(0.92,0.04)
    nw.vtkColorBarActor.SetWidth(0.05)
    nw.vtkColorBarActor.SetHeight(0.4)    
    
    scene_edges_layers.append(nw)
    
    # Add Interaction Layer
    
    nw_edgesInteractorLayer = VTK.VtkNetworkEdgesInteractorLayer(G, z_index=4)
    renderer.AddActor(nw_edgesInteractorLayer.vtkActor)
    scene_edges_interactor_layers.append(nw_edgesInteractorLayer)
        
    # ----------
    
    # Scale correction for final display
    
    renderer.ResetCamera()
     
    camera_position = renderer.GetActiveCamera().GetPosition()
    zPos = camera_position[2]
     
    EDGE_WIDTH = zPos/1000.0
    NODE_SIZE = 0.9*max(min(1.1*EDGE_WIDTH,0.15),0.15)
    
    for layer in scene_edges_layers:
        layer.vtkFilter.SetWidth(0.5*EDGE_WIDTH)
    
    for layer in scene_edges_interactor_layers:
        layer.vtkFilter.SetWidth(1*EDGE_WIDTH)
    
    renderer.ResetCamera()    
    
    # -----------

    # Add Nodes Layer
    
    ## nodes
    node_source_label = pars['NODE_SOURCE_LABEL'] 
    node_sink_label = pars['NODE_SINK_LABEL']
    nw_nodes = VTK.VtkNetworkNodesLayer(G, node_source_label, node_sink_label, NODE_SIZE, z_index=5)
    renderer.AddActor(nw_nodes.vtkActor)
    
    ## labels
    renderer.AddActor2D(nw_nodes.vtkActor_st_labels)
    #renderer.AddActor2D(nw_nodes.vtkActor_non_st_labels)
    
    # -----------
    
    # Network and interactor annotations
    
    annotation_info_nw, annotation_info_iren = vtk_info.infoAnnotations(G,renderer,pars)
    
    # Set background color
    
    set_bck.setBackground(renderer)
    
    # Set vtk elements to be considered in the visualization
    
    vtkElements = {}
    vtkElements['nw'] = nw
    vtkElements['nw_bck'] = nw_bck
    vtkElements['nw_data_times'] = nw_data_times
    vtkElements['nw_data_capacities'] = nw_data_capacities
    vtkElements['nw_nodes'] = nw_nodes
    vtkElements['annotation_info_nw'] = annotation_info_nw
    vtkElements['annotation_info_iren'] = annotation_info_iren

    return vtkElements
    
def update(time_id, G, nw, fminus_data, ze_data, pars, globalNumberOfSteps):
    
    """Animation update procedure for the elements considered in the 'scene_setup' function
    """

    DYNAMIC_WIDTH = True
    
    time_step = pars['TIME_STEP']
      
    globalNumberOfTimeSteps = globalNumberOfSteps
      
    edge_counter = 0
    
    for e in sorted(set(G.edges_iter())):
          
        edges = G.edge[e[0]][e[1]]
          
        edge_id = 0
         
        while (edge_id < len(edges)):
            
            key = edges[edge_id]['edge_key']
            
            max_edge_fminus_value = fminus_data[:,key].max()
            
            if (max_edge_fminus_value > 0):
            
                edge_animation_data = nw.edges_dict[(e[0],e[1],edge_id)]
                    
                time = edges[edge_id]['time']
                
                listOfEdgeCellIds = edge_animation_data.edgeCellIds 
                listOfEdgePointIds = edge_animation_data.edgeCellPointIds
                   
                numberOfDivisions = int(floor(time/time_step))
    
                for i in xrange(numberOfDivisions):
    
                    fminus_value = 0.0
    
                    if (time_id > 0):
                                         
                        if (time_id-1 - i >= 0):
                             
                            fminus_value = fminus_data[time_id-i-1,key]
                            
                        
                    cell_id = listOfEdgeCellIds[i]
                    nw.setCellColorById(cell_id, fminus_value)
                
                    if (DYNAMIC_WIDTH):
                 
                        for pointId in listOfEdgePointIds[i]:
                             
                            nw.setPointWidthById(pointId, fminus_value)
                
                # queue update
                
                queue_value = ze_data[time_id,key]        
                
                qPointsIDs = edge_animation_data.queuePointIds
                qPoints = edge_animation_data.queueRefPoints
                q_max_h = edge_animation_data.queueMaxHeight
                q_u = edge_animation_data.queueRefDirection
                q_max_qvalue = edge_animation_data.queueMaxQValue
                qBoxID = edge_animation_data.queueBoxCellId
                qID = edge_animation_data.queueCellId
    
                if (queue_value > 0 and q_max_qvalue > 0):
                    
                    h = max(q_max_h*(queue_value/q_max_qvalue), 1E-5)
                    
                    newPoint = qPoints[0] + q_u*h
                        
                    nw.vtkQPoints.SetPoint(qPointsIDs[1], newPoint)
                    
                else:
                    
                    newPoint = qPoints[0] + q_u*0.001
                    nw.vtkQPoints.SetPoint(qPointsIDs[1], newPoint)
                
                nw.setQBoxCellColorById(qBoxID, queue_value)
                nw.setQCellColorById(qID, queue_value)
            
            edge_id = edge_id + 1
        
    return None


