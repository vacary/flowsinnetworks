"""
NETWORK SETTINGS

"""

NETWORK_NAME = "doubleparallel"
TYPE = "0" 

TIME_OF_EVENT = [0.0,10.0,20.0]
INPUT_FLOW = [4.0,4.0] 

TIME_STEP = 0.1 
T_MAX_VIS = 15 
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

def network_graph_data():

    G = nx.MultiDiGraph()

    source = 's'
    sink = 't' 

    # { begin graph definition } [ Example: G = exa.example_Larre() ]

    G = exa.example_doubleparallelpath()

    # { end graph definition }

    if (TYPE == "0"):
        graphviz_layout = 'dot'
        layouts.addNodePositionsToGraph(G,TYPE,PRIORITY_GRAPHVIZ_LAYOUT, graphviz_layout)

    #else:
    #    { procedure to set node positions }

    return [G,source,sink]

