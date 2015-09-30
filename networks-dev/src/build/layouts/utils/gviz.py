#
# Network geometry from graphviz file
# 
# Functions to create the network geometry reading a file created 
# with the graphviz library
#  

# Standard libary imports
import sys
import os

# Non standard library imports
import networkx as nx
from numpy import *
import matplotlib.pyplot as plt

# Custom library imports
dir_path = os.path.dirname(os.path.abspath(__file__))     
layouts_path = os.path.abspath(os.path.join(dir_path,'..'))
sys.path.append(layouts_path)

import utils.bsplines as bsplines

def addGeometryFromGVizFile(G, gviz_file_path, splines_degree=3, number_of_points=50):
    
    """ Geometry generator from graphviz file
    
    Input:
    
        G: networkx graph
        gviz_file_path: path for the graphviz file
        splines_degree: degree for the splines
        number_of_points : number of points for each spline
    
    """
    
    N = G.number_of_nodes()
    
    dict_nodes_geometry = {}

    f = open(gviz_file_path)
    
    # build dictionaries with geometry data

    edge_log = {}
    
    for line in f:
        
        aux = line
        aux = aux.replace("\n","")
        list = aux.split(" ")
        
        elm = list[0]
        
        if (elm == 'node'):
            
            node_id     = int(list[1])
            node_pos_x  = float(list[2])
            node_pos_y  = float(list[3])
    
            pos = [node_pos_x, node_pos_y, 0.0]
    
            dict_nodes_geometry[node_id] = [node_pos_x, node_pos_y]
    
            G.add_node(node_id, pos=str(pos))
            
        if (elm == 'edge'):
             
            edge_tail = int(list[1])
            edge_head = int(list[2])
            
            edge_npoints = int(list[3])
            controlPoints = []
            pos_tail = dict_nodes_geometry[edge_tail]
            pos_head = dict_nodes_geometry[edge_head]
            
            controlPoints.append(pos_tail)
            
            aux = 4
            for c in xrange(edge_npoints):
                pos_x = float(list[aux])
                pos_y = float(list[aux + 1])
                aux = aux + 2
                controlPoints.append([pos_x, pos_y])
                 
            controlPoints.append(pos_head)
             
            geometry = bsplines.getPointsFromBSplineInterpolation(controlPoints, splines_degree, number_of_points)
            
            #for point in geometry:
            #    plt.plot(point[0],point[1],'r.')
            
            edge = (edge_tail,edge_head)
            
  
            if edge not in edge_log:
                edge_log[edge] = 1
            else:
                edge_log[edge] = edge_log[edge] + 1
              
            edge_id = edge_log[edge]-1
            
            try:
                G.edge[edge[0]][edge[1]][edge_id]['geometry'] = str(geometry)
            except:
                pass

    f.close()    
    
    #plt.show()
    
    return None
