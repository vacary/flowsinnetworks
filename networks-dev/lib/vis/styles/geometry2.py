"""

VISUALIZATION STYLE - GEOMETRY2 [previous version]

"""

import os, sys
import networkx as nx
import random

import numpy as np

lib_path = os.path.abspath(os.path.join('..','..','..','lib'))
sys.path.append(lib_path)

import lib.vis.vfc as vfc
import lib.vis.general as gen

def setScene(G,renderer,pars):

    # STYLE METHODS
        
    gen.addInfoAnnotations(G,renderer,pars)
    gen.setBackgroundStyle(renderer)

    # STYLE PARAMETERS
    
    NODE_SIZE           = 0.25
    NODE_OPACITY        = 1.0
    NODE_LABEL_FONTSIZE = gen.getLabelSize(G)
    
    EDGE_WIDTH   = 0.5*NODE_SIZE
    
    POINT_SIZE = 2

    # VTK SCENE
    
    node_source_label   = pars['NODE_SOURCE_LABEL']
    node_sink_label     = pars['NODE_SINK_LABEL']
    
    vtkNodes = vfc.VtkNodesElements(G,NODE_SIZE,NODE_OPACITY,NODE_LABEL_FONTSIZE,node_source_label,node_sink_label)
    vtkNodes.vtkActor.GetProperty().SetColor(1,1,1)
    
    renderer.AddActor(vtkNodes.vtkActor)
    renderer.AddActor2D(vtkNodes.vtkActor2D)
    renderer.AddActor2D(vtkNodes.vtkActor2Dst)

    edge_log = {}


    for edge in G.edges_iter():
 
        edge_tail = G.node[edge[0]]
        edge_head = G.node[edge[1]]
        
        if edge not in edge_log:
            edge_log[edge] = 0
        else:
            edge_log[edge] = edge_log[edge] + 1
        
        edge_id = edge_log[edge]
        
        edge_geometry = G.edge[edge[0]][edge[1]][edge_id]['geometry']
        
        listOfPoints = gen.getPointsFromStrList(edge_geometry)
          
        vtkLines = vfc.VtkLines(listOfPoints,EDGE_WIDTH)
        vtkLines.vtkActor.GetProperty().SetColor(0.75*random.random(),0.75*random.random(),0.75*random.random())
        renderer.AddActor(vtkLines.vtkActor)

        vtkPoints = vfc.VtkPoints(listOfPoints,POINT_SIZE)
        vtkPoints.vtkActor.GetProperty().SetColor(0.75*random.random(),0.75*random.random(),0.75*random.random())
        renderer.AddActor(vtkPoints.vtkActor)
        
    return None
    
def update():
    
    return None
