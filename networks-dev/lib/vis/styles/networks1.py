"""

VISUALIZATION STYLE - NETWORKS1

"""

import vtk

import os, sys
import networkx as nx
import random

import numpy as np

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
    
    nw = n1.VtkNetwork(G)
    renderer.AddActor(nw.vtkActor)

    return None
    
def update():
    
    return None
