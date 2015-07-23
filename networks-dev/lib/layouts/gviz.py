'''

Methods to get data from GViz files

'''

import sys, os
import networkx as nx
from numpy import *

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)     
lib_path = os.path.abspath(os.path.join(dir_path,'..','..'))
sys.path.append(lib_path)

import lib.layouts.bsplines as bsplines

def addGeometryFromGVizFile(G,gviz_file_path):
    
    N = G.number_of_nodes()
    
    if (N < 5):
        
        splines_degree = 2
    
    else:
        
        splines_degree = 3 
    
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
    
            pos = [node_pos_x,node_pos_y,0.0]
    
            dict_nodes_geometry[node_id] = [node_pos_x,node_pos_y]
    
            G.add_node(node_id,pos=str(pos))
            
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
                controlPoints.append([pos_x,pos_y])
                 
            controlPoints.append(pos_head)
             
            geometry = bsplines.getPointsFromBSplineInterpolation(controlPoints,splines_degree)
            
            edge = (edge_tail,edge_head)
  
            if edge not in edge_log:
                edge_log[edge] = 1
            else:
                edge_log[edge] = edge_log[edge] + 1
              
            edge_id = edge_log[edge]-1
              
            G.edge[edge[0]][edge[1]][edge_id]['geometry'] = str(geometry)

    f.close()    
           
    return G

