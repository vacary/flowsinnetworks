"""
VISUALIZATION NETWORK SETTINGS

"""

import os, sys
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

import networkx as nx
from numpy import *

# Parameters 

NETWORK_NAME = "Larre"
TYPE = "geometry"

TIME_OF_EVENT = [0.0,10.0,20.0]
INPUT_FLOW = [4.0,4.0] 

TIME_STEP = 0.1 
T_MAX_VIS = 15 
FPS = 24 

PRIORITY_GRAPHVIZ_LAYOUT = 1
SIMULATION_DATA_AVAILABLE = 1

CUSTOM_LAYOUT = 0

# Required modules / packages 

# { begin required modules }

### Required instructions to get a network graph from Flows/examples.py 

lib_path_flows = os.path.abspath(os.path.join(dir_path,'..','..','..'))
sys.path.append(lib_path_flows)
import Flows.examples as exa

lib_path = os.path.abspath(os.path.join(dir_path,'..','..'))
sys.path.append(lib_path)
import lib.layouts.graph as graph_layouts

lib_path = os.path.abspath(os.path.join(dir_path,'..','..'))
sys.path.append(lib_path)
import lib.layouts.gviz as gviz_layouts 

###

lib_path_flows_graphs = os.path.abspath(os.path.join(dir_path,'..','..','..','Flows','graphs'))

# { end required modules }

def network_graph_data():

    G = nx.MultiDiGraph()

    source = 's'
    sink = 't' 

    # { begin graph definition } [ Example: G = exa.example_Larre() ]

    G = exa.example_Larre()

    # { end graph definition }

    return [G,source,sink]

def network_custom_layout(G):

    # This method is applied only if CUSTOM_LAYOUT = 1 

    # Must return the input graph G with positions for each node with the format: 
    # pos = "[p[0],p[1],0.0]" 

    # { begin custom layout method } 
    
    gviz_file_path = os.path.abspath(os.path.join(dir_path,'rsc','gviz','Larre.txt'))

    gviz_layouts.addGeometryFromGVizFile(G,gviz_file_path)

    # { end custom layout method }

    return G 

