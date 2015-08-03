"""

VISUALIZATION STYLE - NETWORKS1

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
import lib.vis.Vtk.n1 as n1

def setScene(G,renderer,pars):

    # STYLE METHODS
        
    gen.addInfoAnnotations(G,renderer,pars)
    gen.setBackgroundStyle(renderer)

    # STYLE PARAMETERS
    
    NODE_SIZE           = 0.25
    NODE_OPACITY        = 1.0
    NODE_LABEL_FONTSIZE = gen.getLabelSize(G)

    # VTK SCENE
    
    node_source_label   = pars['NODE_SOURCE_LABEL']
    node_sink_label     = pars['NODE_SINK_LABEL']
    
    vtkNodes = vfc.VtkNodesElements(G,NODE_SIZE,NODE_OPACITY,NODE_LABEL_FONTSIZE,node_source_label,node_sink_label)
    vtkNodes.vtkActor.GetProperty().SetColor(1,1,1)
    
    renderer.AddActor(vtkNodes.vtkActor)
    renderer.AddActor2D(vtkNodes.vtkActor2D)
    renderer.AddActor2D(vtkNodes.vtkActor2Dst)
    
    nw      = n1.VtkNetwork(G)
    renderer.AddActor(nw.vtkActor)

    return nw
    
def update(time_id,G,nw,fminus_data,pars,globalNumberOfSteps):

    edges_dict = nw.edges_dict
    
    time_step               = pars['TIME_STEP']
      
    globalNumberOfTimeSteps = globalNumberOfSteps
      
      
    for e in sorted(set(G.edges_iter())):
          
        edges = G.edge[e[0]][e[1]]
          
        edge_id = 0
         
        while (edge_id < len(edges)):
         
            key     = edges[edge_id]['edge_key']    
            time    = edges[edge_id]['time']
             
            listOfEdgeCellIDs = edges_dict[(e[0],e[1],edge_id)][0]
            listOfPointIDs  = edges_dict[(e[0],e[1],edge_id)][1]
               
            numberOfDivisions = int(ceil(time/time_step))
            
            for i in xrange(numberOfDivisions):

                fminus_value = 0.0

                if (time_id > 0):
                                     
                    if (time_id-1 - i >= 0):
                         
                        fminus_value = fminus_data[time_id-i-1,key]
                                                 
                if (fminus_value > 0):
                    color = [0,255,0,255]
                else:
                    color = [100,100,100,20]
                     
                cell_id = listOfEdgeCellIDs[i]
                nw.setCellColorByID(cell_id,color)
                
                width = fminus_value
                
                points  = listOfPointIDs[i]
                for k in xrange(len(points)):
                    nw.setPointWidthByID(points[k],width)
      
            edge_id = edge_id + 1

    return None
