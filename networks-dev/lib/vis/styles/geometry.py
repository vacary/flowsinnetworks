"""

VISUALIZATION STYLE - GEOMETRY

"""

import vtk

import os, sys
import networkx as nx
import random

from numpy import *

lib_path = os.path.abspath(os.path.join('..','..','..','lib'))
sys.path.append(lib_path)

import lib.vis.general as gen
import lib.vis.VTK.geometry as VTK

def setScene(G,renderer,pars):

    # STYLE FUNCTION CALLS
        
    gen.addInfoAnnotations(G,renderer,pars)
    gen.setBackgroundStyle(renderer)

    # PARAMETERS - A PRIORI VALUES
    
    NODE_SIZE           = 0.2
    NODE_OPACITY        = 1.0
    NODE_LABEL_FONTSIZE = 12#gen.getLabelSize(G)
    
    POINTS_SIZE         = 1.2
    POINTS_OPACITY      = 0.9
    
    # VTK SCENE
    
    node_source_label   = pars['NODE_SOURCE_LABEL']
    node_sink_label     = pars['NODE_SINK_LABEL']
        
    vtkNodes = VTK.VtkNodes(G,NODE_SIZE,NODE_OPACITY,NODE_LABEL_FONTSIZE,node_source_label,node_sink_label)
    
    renderer.AddActor(vtkNodes.vtkActor)
    renderer.AddActor2D(vtkNodes.vtkActor2D)
    renderer.AddActor2D(vtkNodes.vtkActor2Dst)
    
    nw = VTK.VtkNetwork(G)
    nw.vtkPointsActor.GetProperty().SetPointSize(POINTS_SIZE)
    nw.vtkPointsActor.GetProperty().SetOpacity(POINTS_OPACITY)
    
    renderer.AddActor(nw.vtkPointsActor)

    return None
    
def update():

    # no update functions for this style
    
    return None


