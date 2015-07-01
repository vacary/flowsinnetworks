"""
VISUALIZATION NETWORK SETTINGS

"""

import os, sys
import networkx as nx
from numpy import *

# Parameters 

NETWORK_NAME = "map"
TYPE = "map" 

TIME_OF_EVENT = [0.0,50.0]
INPUT_FLOW = [4.0] 

TIME_STEP = 0.2
T_MAX_VIS = 30 
FPS = 24 

PRIORITY_GRAPHVIZ_LAYOUT = 1
SIMULATION_DATA_AVAILABLE = 1

# Required modules / packages 

lib_path = os.path.abspath(os.path.join('..','..'))
lib_path_flows = os.path.abspath(os.path.join('..','..','..'))
sys.path.append(lib_path)
sys.path.append(lib_path_flows)

import lib.layouts.graph as layouts
import Flows.examples as exa

import lib.layouts.maps as mp

def network_graph_data():

    # Must return graph G with positions for each node with format pos = "[p[0],p[1],0.0]" 

    G = nx.MultiDiGraph()

    source = 0
    sink = 1
    
    # { begin graph definition } [ Example: G = exa.example_Larre() ]

    osm_file_path = os.path.join('.','osm','map_graph_test.osm')
    G = mp.get_graphFromOSMFile2(osm_file_path, TIME_STEP)

    # { end graph definition }


    return [G,source,sink]

