"""
VISUALIZATION NETWORK SETTINGS

"""

import os, sys
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

import networkx as nx
from numpy import *

# Parameters 

NETWORK_NAME = "test2"
TYPE = "interactor" 

TIME_OF_EVENT = [0.0,5.0,200.0]
INPUT_FLOW = [10.0,0.0] 

TIME_STEP = 0.1 
T_MAX_VIS = 50.0
FPS = 24 

PRIORITY_GRAPHVIZ_LAYOUT = 1
SIMULATION_DATA_AVAILABLE = 1

CUSTOM_LAYOUT = 1

# Required modules / packages 

# { begin required modules }

lib_path = os.path.abspath(os.path.join(dir_path,'..','..'))
sys.path.append(lib_path)
import lib.layouts.gviz as gviz_layouts 

lib_path_flows_graphs = os.path.abspath(os.path.join(dir_path,'..','..','..','Flows','graphs'))

# { end required modules }

def network_graph_data():

    G = nx.MultiDiGraph()

    #filename = 'G_d3_n200_gen.gml'
    #filename = 'G_d4_n400_gen.gml'
    #filename = 'G_d6_n600_gen.gml'
    #filename = 'G_gen_decrease.gml'
    #filename = 'G_gen_decrease0.gml'
    #filename = 'G_gen_decrease1.gml'
    #filename = 'G_gen_decrease2.gml'
    #filename = 'G_gen_decrease3.gml'
    #filename = 'G_gen_decrease4.gml'
    #filename = 'G_gen_decrease5.gml'
    #filename = 'G_gen_decrease6.gml'
    filename = 'G_gen_infinite.gml'
    #filename = 'G1_gen.gml'
    #filename = 'G10_gen.gml'
    #filename = 'G2_gen.gml'
    #filename = 'G3_gen.gml'
    #filename = 'G4_gen.gml'
    #filename = 'G5_gen.gml'
    #filename = 'G6_gen.gml'
    #filename = 'G7_gen.gml'
    #filename = 'G8_gen.gml'
    #filename = 'Galpha_gen.gml'
    #filename = 'Galpha0_gen.gml'
    #filename = 'Glong_gen.gml'
    #filename = 'Gmedium_gen.gml'
    

    network_gml_file_path = os.path.join(lib_path_flows_graphs,filename)

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
    
    graphviz_prog = 'dot'
    #graphviz_args = '-Gnodesep=3.0 -Granksep=6.0 -Gsplines=spline'
    #graphviz_args = '-Gnodesep=0.5 -Gsplines=polyline'    
    graphviz_args = '-Gnodesep=0.5 -Gsplines=ortho -Nfixedsize=true -Nheight=0.05'

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

