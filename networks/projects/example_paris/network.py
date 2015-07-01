"""
VISUALIZATION NETWORK SETTINGS

"""

import os, sys
import networkx as nx
from numpy import *

# Parameters 

NETWORK_NAME = "example_paris"
TYPE = "custom" 

TIME_OF_EVENT = [0.0,50.0]
INPUT_FLOW = [5.0] 

TIME_STEP = 0.15
T_MAX_VIS = 25
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

def network_graph_data():

    # Must return graph G with positions for each node (pos = [p[0],p[1],0.0]) 

    source = 'X'
    sink = 'La Defense' 

    # { begin graph definition } [ Example: G = exa.example_Larre() ]

    G = nx.MultiDiGraph()
    G.add_node('X')
    G.add_node('CiteU')
    G.add_node('Denfert')
    G.add_node('Chatelet')
    G.add_node('Versailles')
    G.add_node('Montparnasse')
    G.add_node('Etoile')
    G.add_node('Issy')
    G.add_node('La Defense')

    G.node['La Defense']['label'] = 0
    G.node['Etoile']['label'] = 0
    G.node['Chatelet']['label'] = 0
    G.node['Montparnasse']['label'] = 0
    G.node['Denfert']['label'] = 0
    G.node['Issy']['label'] = 0
    G.node['CiteU']['label'] = 0
    G.node['Versailles']['label'] = 0
    G.node['X']['label'] = 0
 
    G.add_edge('X','CiteU',time= 5.0, capacity=3., flow =0)
    G.add_edge('X','Versailles',time= 4.0, capacity=3., flow =0)
    G.add_edge('CiteU','Denfert',time= 2., capacity=3., flow =0)
    G.add_edge('CiteU','Issy',time= 3., capacity=2., flow =0)
    G.add_edge('Denfert','Chatelet',time= 4., capacity=3., flow =0)
    G.add_edge('Denfert','Montparnasse',time= 1., capacity=2., flow =0)
    G.add_edge('Chatelet','Etoile',time= 3., capacity=2., flow =0)
    G.add_edge('Versailles','Montparnasse',time= 4., capacity=3., flow =0)
    G.add_edge('Versailles','Issy',time= 2., capacity=3., flow =0)
    G.add_edge('Montparnasse','Etoile',time= 3., capacity=2., flow =0)
    G.add_edge('Montparnasse','Chatelet',time= 3., capacity=2., flow =0)
    G.add_edge('Montparnasse','Issy',time= 2., capacity=2., flow =0)
    G.add_edge('Issy','Montparnasse',time= 2., capacity=2., flow =0)
    G.add_edge('Issy','La Defense',time= 4., capacity=2., flow =0)
    G.add_edge('Etoile','La Defense',time= 2., capacity=0.5, flow =0)
    
    

    # { end graph definition }

    if (TYPE == "0"):
        graphviz_layout = 'sfdp'
        layouts.addNodePositionsToGraph(G,TYPE,PRIORITY_GRAPHVIZ_LAYOUT, graphviz_layout)

    #else:
    #    { procedure to set node positions }

    G.node['La Defense']['pos']     = "[0.0,200.0,0.0]"
    G.node['Etoile']['pos']         = "[50.0,200.0,0.0]"
    G.node['Chatelet']['pos']       = "[100.0,200.0,0.0]"
    G.node['Montparnasse']['pos']   = "[50.0,150.0,0.0]"
    G.node['Denfert']['pos']        = "[100.0,150.0,0.0]"
    G.node['Issy']['pos']           = "[25.0,50.0,0.0]"
    G.node['CiteU']['pos']          = "[100.0,100.0,0.0]"
    G.node['Versailles']['pos']     = "[50.0,25.0,0.0]"
    G.node['X']['pos']              = "[100.0,25.0,0.0]"

    return [G,source,sink]

