"""
VISUALIZATION NETWORK SETTINGS

"""

import os, sys
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

import networkx as nx
from numpy import *

# Parameters 

NETWORK_NAME = "test3"
TYPE = "interactor" 

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
import lib.layouts.graph as graph_layouts 
import lib.layouts.gviz as gviz_layouts 

### Required instructions to get a network graph from Flows/examples.py  

lib_path_flows = os.path.abspath(os.path.join(dir_path,'..','..','..'))
sys.path.append(lib_path_flows)
import Flows.examples as exa

### Path to call a graph from the folder Flows/graphs  

lib_path_flows_graphs = os.path.abspath(os.path.join(dir_path,'..','..','..','Flows','graphs'))

# { end required modules }

def network_graph_data():

    G = nx.MultiDiGraph()

    source = 0
    sink = 3

    # { begin graph definition } [ Example: G = exa.example_Larre() ]

    G.add_edge(0,1, time = 1.0, capacity = 1.0) 
    G.add_edge(0,1, time = 1.0, capacity = 1.0) 
    G.add_edge(0,1, time = 1.0, capacity = 1.0) 
    G.add_edge(0,1, time = 1.0, capacity = 1.0) 
    G.add_edge(1,2, time = 1.0, capacity = 1.0)
    G.add_edge(2,0, time = 1.0, capacity = 1.0)
    G.add_edge(0,2, time = 1.0, capacity = 1.0)   
    G.add_edge(2,3, time = 1.0, capacity = 1.0) 
    G.add_edge(3,2, time = 1.0, capacity = 1.0) 

    # { end graph definition }

    return [G,source,sink]

def network_custom_layout(G):

    # This method is applied only if CUSTOM_LAYOUT = 1 

    # { begin custom layout method } 

    # Example: 

    # [ Set graphviz layout parameters ] 

    A = nx.to_agraph(G) 
    graphviz_prog = 'dot' # ['dot', 'neato', 'fdp', 'sfdp', 'circo'] 

    graphviz_args = '-Gnodesep=0.5 -Grankdir=LR -Gsplines=ortho' 

    # Some other options: 
    ## graphviz_args = '-Granksep=6.0' 
    ## graphviz_args = '-Gsplines=spline' 

    # [ Create file with the layout information ] 

    gviz_file_path  = os.path.abspath(os.path.join(dir_path,'rsc','gviz',NETWORK_NAME+'_custom.txt')) 

    # File output 
    A.draw(gviz_file_path,format='plain', prog=graphviz_prog, args=graphviz_args) # !required 

    # Image output (optional) 
    # A.draw(gviz_file_path+'.png',format='png', prog=graphviz_prog, args=graphviz_args) 

    # [ Load the layout information ] 

    ## gviz_file_path  = os.path.abspath(os.path.join(dir_path,'rsc','gviz',NETWORK_NAME+'_custom.txt')) # (optional) 

    splines_degree = 3 
    numberOfPointsForSpline = 20 

    gviz_layouts.addGeometryFromGVizFile(G,gviz_file_path,splines_degree,numberOfPointsForSpline) # !required 

    # { end custom layout method }

    return G 

