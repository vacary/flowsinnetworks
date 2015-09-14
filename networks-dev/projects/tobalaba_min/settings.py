"""
VISUALIZATION NETWORK SETTINGS

"""

import os, sys
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

import networkx as nx
from numpy import *

# Parameters 

NETWORK_NAME = "tobalaba_min"
TYPE = "network" 

TIME_OF_EVENT = [0.0,500.0]
INPUT_FLOW = [5] 

TIME_STEP = 1
T_MAX_VIS = 100
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

### Call module with processing methods for osm files

import lib.util.osm as osm

# { end required modules }

def network_graph_data():

    # { begin graph definition } [ Example: G = exa.example_Larre() ]
    
#     lib_path_flows_graphs = os.path.abspath(os.path.join(dir_path,'.','data'))
#     
#     network_gml_file_path = os.path.join(lib_path_flows_graphs,'exa.gml')
# 
#     G = nx.read_gml(network_gml_file_path)
#     
#     G = nx.MultiDiGraph(G)
#     
#     source = G.nodes()[0]
#     sink = G.nodes()[-1]

    filename = 'map_graph_test.osm'
    filename = 'full_tobalaba_2.osm'
    #filename = 'heroes.osm'

    osm_path_file = os.path.abspath(os.path.join(dir_path,'rsc','osm',filename))
    nw = osm.OsmNetwork(osm_path_file)
     
    G, source, sink = nw.get_network_graph_data()
    
    # { end graph definition }
    
    return [G, source, sink]

def network_custom_layout(G):

    # This method is applied only if CUSTOM_LAYOUT = 1 
 
    # { begin custom layout method } 
 
    # Example: 
 
    # [ Set graphviz layout parameters ] 


#     A = nx.to_agraph(G) 
#     graphviz_prog = 'dot' # ['dot', 'neato', 'fdp', 'sfdp', 'circo'] 
#  
#     graphviz_args = '-Gnodesep=0.5 -Grankdir=LR -Gsplines=ortho' 
#  
#     # Some other options: 
#     ## graphviz_args = '-Granksep=6.0' 
#     ## graphviz_args = '-Gsplines=spline' 
#  
#     # [ Create file with the layout information ] 
#  
#     gviz_file_path  = os.path.abspath(os.path.join(dir_path,'rsc','gviz',NETWORK_NAME+'_custom.txt')) 
#  
#     # File output 
#     A.draw(gviz_file_path,format='plain', prog=graphviz_prog, args=graphviz_args) # !required 
#  
#     # Image output (optional) 
#     # A.draw(gviz_file_path+'.png',format='png', prog=graphviz_prog, args=graphviz_args) 
#  
#     # [ Load the layout information ] 
#  
#     ## gviz_file_path  = os.path.abspath(os.path.join(dir_path,'rsc','gviz',NETWORK_NAME+'_custom.txt')) # (optional) 
#  
#     splines_degree = 3 
#     numberOfPointsForSpline = 20 
#  
#     gviz_layouts.addGeometryFromGVizFile(G,gviz_file_path,splines_degree,numberOfPointsForSpline) # !required 
 
    # { end custom layout method }

    pass

    return G 

