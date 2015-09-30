#
# Visualization network settings

# Standard library imports
import os
import sys

# Non standard library imports
import networkx as nx

#####################################################
# Network settings
#####################################################

NETWORK_NAME = "tobalaba_min"
TYPE = "network"

TIME_OF_EVENT = [0.0,500.0]
INPUT_FLOW = [5] 

TIME_STEP = 0.5
T_MAX_VIS = 100
FPS = 24 

PRIORITY_GRAPHVIZ_LAYOUT = 1
SIMULATION_DATA_AVAILABLE = 1

CUSTOM_LAYOUT = 1

#####################################################

# Required modules / packages

# { begin required modules }

## Current path
dir_path = os.path.dirname(os.path.abspath(__file__))

# Library imports from the visualization workspace folder
dir_path_vroot = os.path.abspath(os.path.join(dir_path,'..','..'))
sys.path.append(dir_path_vroot)

import src.build.layouts.utils.osm as osm

# { end required modules }

def network_graph_data():

    # { begin graph definition } [ Example: G = exa.example_Larre() ]
  
    filename = 'map_graph_test.osm'
    filename = 'full_tobalaba_2.osm'
    #filename = 'heroes.osm'

    osm_file_path = os.path.abspath(os.path.join(dir_path,'rsc','osm',filename))
    nw = osm.OsmNetwork(osm_file_path)
     
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
#     number_of_points_for_spline = 20 
#  
#     gviz_layouts.addGeometryFromGVizFile(G, gviz_file_path, splines_degree, number_of_points_for_spline) # !required 
 
    # { end custom layout method }

    pass


