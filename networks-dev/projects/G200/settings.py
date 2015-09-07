"""
VISUALIZATION NETWORK SETTINGS

"""

import os, sys
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

import networkx as nx
from numpy import *

# Parameters 

NETWORK_NAME = "G200"
TYPE = "network"

TIME_OF_EVENT = [0.0,10.0,100.0]
INPUT_FLOW = [50.0,0.0] 

TIME_STEP = 0.25
T_MAX_VIS = 75
FPS = 24 

PRIORITY_GRAPHVIZ_LAYOUT = 1
SIMULATION_DATA_AVAILABLE = 1

CUSTOM_LAYOUT = 0

# Required modules / packages 

# { begin required modules }

lib_path = os.path.abspath(os.path.join(dir_path,'..','..'))
sys.path.append(lib_path)
import lib.layouts.gviz as gviz_layouts 

###

lib_path_flows_graphs = os.path.abspath(os.path.join(dir_path,'..','..','..','Flows','graphs'))


# { end required modules }

def network_graph_data():

    network_gml_file_path = os.path.join(lib_path_flows_graphs,'G_d3_n200_gen.gml')

    G = nx.read_gml(network_gml_file_path)
    
    G = nx.MultiDiGraph(G)
    
    source = G.nodes()[0]
    sink = G.nodes()[-1]

    # { begin graph definition } [ Example: G = exa.example_Larre() ]



    # { end graph definition }

    return [G,source,sink]

def network_custom_layout(G):

    # This method is applied only if CUSTOM_LAYOUT = 1

    # { begin custom layout method } 

    # Example: 
    
    # [ Set graphviz layout parameters ]
    
    A = nx.to_agraph(G)
    
    graphviz_prog = 'sfdp'
    graphviz_args = '-Gnodesep=4.0 -Granksep=6.0 -Gsplines=spline'
    #graphviz_args = '-Gnodesep=0.5 -Gsplines=polyline'    
    #graphviz_args = '-Gnodesep=0.5 -Gsplines=ortho -Nfixedsize=true -Nheight=0.05'

    # [ Create file with the layout information ]
    
    gviz_file_path  = os.path.abspath(os.path.join(dir_path,'rsc','gviz',NETWORK_NAME+'_custom.txt'))
    
    
    A.draw(gviz_file_path,format='plain', prog = graphviz_prog, args=graphviz_args)
    #A.draw(gviz_file_path.replace('.','')+'.png',format='png', prog = graphviz_prog, args=graphviz_args) # graphviz image
    
    # [ Load the file with the layout information ]
    
    #gviz_file_path  = os.path.abspath(os.path.join(dir_path,'rsc','gviz',NETWORK_NAME+'_custom.txt'))
    spline_degree           = 4
    spline_numberOfPoints   = 20
    gviz_layouts.addGeometryFromGVizFile(G,gviz_file_path,spline_degree,spline_numberOfPoints) # !important

    # { end custom layout method }

    return G 

