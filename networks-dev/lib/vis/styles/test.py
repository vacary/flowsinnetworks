"""

VISUALIZATION STYLE - TEST

"""

import vtk

import os, sys
import networkx as nx
import random

from numpy import * 

lib_path = os.path.abspath(os.path.join('..','..','..','lib'))
sys.path.append(lib_path)

import lib.vis.vfc as vfc
import lib.vis.general as gen
import lib.vis.Vtk.test as test

def setScene(G,renderer,pars,style_pars):

    # STYLE METHODS
        
    gen.addInfoAnnotations(G,renderer,pars)
    gen.setBackgroundStyle(renderer)

    # STYLE PARAMETERS
    
    NODE_OPACITY        = 1.0
    NODE_LABEL_FONTSIZE = gen.getLabelSize(G)

    # VTK SCENE
    
    nw_bck  = test.VtkNetworkBck(G,style_pars)
    renderer.AddActor(nw_bck.vtkActor)
    
        
    nw      = test.VtkNetwork(G,style_pars)
    renderer.AddActor(nw.vtkQActor)
    renderer.AddActor(nw.vtkQBoxesActor)
    renderer.AddActor(nw.vtkActor)
    
    renderer.ResetCamera()
    
    cameraPosition = renderer.GetActiveCamera().GetPosition()
    zPos = cameraPosition[2]
    
    aux = 10**(ceil(log10(cameraPosition[2])))
    
    EDGE_WIDTH  = 0.8*1.5*zPos/1000.0

    NODE_SIZE   = max(min(1.1*EDGE_WIDTH,0.15),0.15)
         
    nw_bck.vtkFilter.SetWidth(EDGE_WIDTH)
    nw.vtkFilter.SetWidth(EDGE_WIDTH)
    
    

    node_source_label   = pars['NODE_SOURCE_LABEL']
    node_sink_label     = pars['NODE_SINK_LABEL']
    
    vtkNodes = vfc.VtkNodesElements(G,NODE_SIZE,NODE_OPACITY,NODE_LABEL_FONTSIZE,node_source_label,node_sink_label)
    vtkNodes.vtkActor.GetProperty().SetColor(1,1,1)
    
    renderer.AddActor(vtkNodes.vtkActor)
    renderer.AddActor2D(vtkNodes.vtkActor2D)
    renderer.AddActor2D(vtkNodes.vtkActor2Dst)
        
    nw.vtkColorBar.GetPositionCoordinate().SetValue(0.92,0.04)
    nw.vtkColorBar.SetWidth(0.05)
    nw.vtkColorBar.SetHeight(0.4)
    
    renderer.AddActor2D(nw.vtkColorBar)
    renderer.ResetCamera()
    
    return nw
    
def update(time_id,G,nw,fminus_data,ze_data,pars,globalNumberOfSteps):

    edges_dict = nw.edges_dict
    
    time_step               = pars['TIME_STEP']
      
    globalNumberOfTimeSteps = globalNumberOfSteps
      
    edge_counter = 0
    
    for e in sorted(set(G.edges_iter())):
          
        edges = G.edge[e[0]][e[1]]
          
        edge_id = 0
         
        while (edge_id < len(edges)):
         
            key     = edges[edge_id]['edge_key']    
            time    = edges[edge_id]['time']
             
            listOfEdgeCellIDs = edges_dict[(e[0],e[1],edge_id)][0]
               
            numberOfDivisions = int(floor(time/time_step))

            
            for i in xrange(numberOfDivisions):

                fminus_value = 0.0

                if (time_id > 0):
                                     
                    if (time_id-1 - i >= 0):
                         
                        fminus_value = fminus_data[time_id-i-1,key]
                    
                cell_id = listOfEdgeCellIDs[i]
                nw.setCellColorByID(cell_id,fminus_value)
            
            # queue update
            
            queue_value     = ze_data[time_id,key]        
            
            qPointsIDs   = edges_dict[(e[0],e[1],edge_id)][2]
            qPoints      = edges_dict[(e[0],e[1],edge_id)][3]
            q_max_h      = edges_dict[(e[0],e[1],edge_id)][4]
            q_u          = edges_dict[(e[0],e[1],edge_id)][5]
            q_max_qvalue = edges_dict[(e[0],e[1],edge_id)][6]
            qBoxID       = edges_dict[(e[0],e[1],edge_id)][7]
            qID          = edges_dict[(e[0],e[1],edge_id)][8]

            
            if (queue_value > 0 and q_max_qvalue > 0):
                
                h = max( q_max_h*(queue_value/q_max_qvalue) , 1E-5 )
                
                newPoint = qPoints[0] + q_u*h
                    
                nw.vtkQPoints.SetPoint(qPointsIDs[1],newPoint)
                
            else:
                
                newPoint = qPoints[0] + q_u*0.001
                
                nw.vtkQPoints.SetPoint(qPointsIDs[1],newPoint)
            
            nw.setQBoxCellColorByID(qBoxID,queue_value)
            nw.setQCellColorByID(qID,queue_value)
            
            edge_id = edge_id + 1

            
        
    return None
