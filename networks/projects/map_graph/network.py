"""
NETWORK SETTINGS

"""

NETWORK_NAME = "map_graph"
TYPE = "1" 

TIME_OF_EVENT = [0.0,10.0,100.0]
INPUT_FLOW = [4.0,4.0] 

TIME_STEP = 0.2
T_MAX_VIS = 40 
FPS = 24 

PRIORITY_GRAPHVIZ_LAYOUT = 1

SIMULATION_DATA_AVAILABLE = 1

import os, sys
import networkx as nx
lib_path = os.path.abspath(os.path.join('..','..'))
lib_path_flows = os.path.abspath(os.path.join('..','..','..'))
sys.path.append(lib_path)
sys.path.append(lib_path_flows)
import lib.layouts as layouts
import Flows.examples as exa

# 
import lib.maps as mp

def network_graph_data():

    G = nx.MultiDiGraph()

    source = 0
    sink = 1

    # { begin graph definition } [ Example: G = exa.example_Larre() ]

    #osm_file_path = os.path.join('.','osm','map_graph_test.osm')
    #G = mp.get_graphFromOSMFile(osm_file_path)

    G=nx.read_gml(os.path.join('.','data','map_graph.gml'))
    G = nx.MultiDiGraph(G)

    # { end graph definition }

    if (TYPE == "0"):
        graphviz_layout = 'dot'
        layouts.addNodePositionsToGraph(G,TYPE,PRIORITY_GRAPHVIZ_LAYOUT, graphviz_layout)

    #else:
    #    { procedure to set node positions }

    return [G,source,sink]

