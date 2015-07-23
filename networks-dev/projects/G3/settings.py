"""
VISUALIZATION NETWORK SETTINGS

"""

import os, sys
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

import networkx as nx
from numpy import *

# Parameters 

NETWORK_NAME = "G3"
TYPE = "n1" 

TIME_OF_EVENT = [0.0,10.0,20.0]
INPUT_FLOW = [4.0,4.0] 

TIME_STEP = 0.1 
T_MAX_VIS = 15 
FPS = 24

PRIORITY_GRAPHVIZ_LAYOUT = 1
SIMULATION_DATA_AVAILABLE = 1

CUSTOM_LAYOUT = 1

# Required modules / packages 

# { begin required modules }

lib_path = os.path.abspath(os.path.join(dir_path,'..','..'))
sys.path.append(lib_path)
import lib.layouts.gviz as gviz_layouts 

###

lib_path_flows_graphs = os.path.abspath(os.path.join(dir_path,'..','..','..','Flows','graphs'))

# { end required modules }

def network_graph_data():

    network_gml_file_path = os.path.join(lib_path_flows_graphs,'G3_gen.gml')

    G = nx.read_gml(network_gml_file_path)
    
    G = nx.MultiDiGraph(G)
    
    source = G.nodes()[0]
    sink = G.nodes()[-1]

    # { begin graph definition } [ Example: G = exa.example_Larre() ]

    # { end graph definition }

    return [G,source,sink]

def network_custom_layout(G):

    # This method is applied only if CUSTOM_LAYOUT = 1 

    # Must return the input graph G with positions for each node with the format: 
    # pos = "[p[0],p[1],0.0]" 

    # { begin custom layout method } 

    # Example: 
    # graphviz_layout = "circo" 
    # graph_layouts.addNodePositionsToGraph(G,PRIORITY_GRAPHVIZ_LAYOUT,graphviz_layout) 

    gviz_file_path = os.path.abspath(os.path.join(dir_path,'rsc','gviz','G3_gen.txt'))

    gviz_layouts.addGeometryFromGVizFile(G,gviz_file_path)

    # { end custom layout method }

    return G 
