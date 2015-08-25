"""
VISUALIZATION NETWORK SETTINGS

"""

import os, sys
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

import networkx as nx
from numpy import *

# Parameters 

NETWORK_NAME = "test"
TYPE = "interactor" 

TIME_OF_EVENT = [0.0,10.0,100.0]
INPUT_FLOW = [20.0,0.0] 

TIME_STEP = 0.1
T_MAX_VIS = 80
FPS = 24

PRIORITY_GRAPHVIZ_LAYOUT = 1
SIMULATION_DATA_AVAILABLE = 1

CUSTOM_LAYOUT = 1

# Required modules / packages 

# { begin required modules }

lib_path = os.path.abspath(os.path.join(dir_path,'..','..'))
sys.path.append(lib_path)
import lib.layouts.graph as graph_layouts 

### Required instructions to get a network graph from Flows/examples.py  

lib_path_flows = os.path.abspath(os.path.join(dir_path,'..','..','..'))
sys.path.append(lib_path_flows)
import Flows.examples as exa

lib_path = os.path.abspath(os.path.join(dir_path,'..','..'))
sys.path.append(lib_path)
import lib.layouts.gviz as gviz_layouts 

# { end required modules }

def network_graph_data():

    G = nx.MultiDiGraph()

    source = 2
    sink = 7

    # { begin graph definition } [ Example: G = exa.example_Larre() ]
    
    G.add_edge(0,1, time = 0.125, capacity = 5.0)
    G.add_edge(1,0, time = 0.125, capacity = 5.0)
    
    G.add_edge(0,2, time = 2.0, capacity = 5.0)
    G.add_edge(2,0, time = 2.0, capacity = 5.0)
    
    G.add_edge(0,7, time = 2.0, capacity = 5.0)
    G.add_edge(7,0, time = 2.0, capacity = 5.0)
    
    G.add_edge(1,2, time = 0.1, capacity = 5.0)
    G.add_edge(2,1, time = 0.1, capacity = 5.0)
    
       
#     G.add_edge(3,4, time = 1.0, capacity = 20.0)
#     G.add_edge(3,4, time = 1.0, capacity = 20.0)
#     G.add_edge(3,4, time = 0.5, capacity = 20.0)
#     G.add_edge(3,6, time = 10.0, capacity = 20.0)
#     G.add_edge(3,6, time = 10.0, capacity = 20.0)
#     G.add_edge(3,6, time = 10.0, capacity = 20.0)
#       
#     G.add_edge(4,3, time = 0.23, capacity = 2.0)
#     G.add_edge(4,5, time = 10.0, capacity = 5.0)
#     G.add_edge(4,6, time = 1.0, capacity = 2.0)
#     G.add_edge(5,6, time = 15.0, capacity = 5.0)
#     G.add_edge(6,7, time = 1.0, capacity = 5.0)
#   
#     G.add_edge(4,3, time = 0.23, capacity = 2.0)
#     G.add_edge(4,5, time = 10.0, capacity = 5.0)
#     G.add_edge(4,6, time = 4.0, capacity = 2.0)
#     G.add_edge(5,6, time = 15.0, capacity = 5.0)
#     G.add_edge(6,5, time = 1.0, capacity = 5.0)
#     G.add_edge(6,7, time = 1.0, capacity = 5.0)
#      
#     G.add_edge(2,4, time = 4.0, capacity = 0.25)
#     #G.add_edge(2,6, time = 1.0, capacity = 5.0)
#     G.add_edge(2,7, time = 1.0, capacity = 5.0)
#     G.add_edge(1,7, time = 1.0, capacity = 5.0)
    
    # { end graph definition }

    return [G,source,sink]

def network_custom_layout(G):

    # This method is applied only if CUSTOM_LAYOUT = 1

    # { begin custom layout method } 

    # Example: 
    
    # [ Set graphviz layout parameters ]
    graphviz_prog = 'dot'
    graphviz_args = '-Gnodesep=0.5 -Grankdir=LR -Gsplines=ortho'

    # [ Create file with the layout information ]
    
    gviz_file_path  = os.path.abspath(os.path.join(dir_path,'rsc','gviz',NETWORK_NAME+'_custom.txt'))
    
    A = nx.to_agraph(G)
    A.draw(gviz_file_path,format='plain', prog = graphviz_prog, args=graphviz_args)
    A.draw(gviz_file_path.replace('.','')+'.png',format='png', prog = graphviz_prog, args=graphviz_args) # graphviz image
    
    # [ Load the file with the layout information ]
    
    gviz_file_path  = os.path.abspath(os.path.join(dir_path,'rsc','gviz',NETWORK_NAME+'_custom.txt'))
    gviz_layouts.addGeometryFromGVizFile(G,gviz_file_path,4) # !important

    # { end custom layout method }

    return G 

