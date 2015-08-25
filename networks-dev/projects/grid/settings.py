"""
VISUALIZATION NETWORK SETTINGS

"""

import os, sys
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

import networkx as nx
from numpy import *

# Parameters 

NETWORK_NAME = "grid"
TYPE = "interactor" 

TIME_OF_EVENT = [0.0,70.0]
INPUT_FLOW = [200.0]

TIME_STEP = 0.1
T_MAX_VIS = 50
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

import random

lib_path = os.path.abspath(os.path.join(dir_path,'..','..'))
sys.path.append(lib_path)
import lib.layouts.gviz as gviz_layouts 

# { end required modules }

def genGridGraph(N):

    G = nx.MultiDiGraph()
    
    # nodes
    for i in xrange(N*N):
    
        G.add_node(i)
    
    # edges
    for i in xrange(N):
        
        for j in xrange(N):
            
            k = i*N + j
            time        = 0.1 + random.random()
            capacity    = 0.1 + 10*random.random()
            
            if (i != N-1 and j != N-1):
                
                G.add_edge(k,k+1, time = time, capacity = capacity)
                G.add_edge(k,k+N, time = time, capacity = capacity)
                G.add_edge(k,k+N+1, time = time, capacity = capacity)
                G.add_edge(k+1,k+N, time = time, capacity = capacity)
                             
                G.add_edge(k+1,k, time = time, capacity = capacity)
                G.add_edge(k+N,k, time = time, capacity = capacity)
                G.add_edge(k+N+1,k, time = time, capacity = capacity)
                G.add_edge(k+N,k+1, time = time, capacity = capacity)
    
            if (i == N-1 and j != N-1):
                 
                G.add_edge(k,k+1, time = time, capacity = capacity)
                G.add_edge(k+1,k, time = time, capacity = capacity)
                 
            if (i != N-1 and j == N-1):
                 
                G.add_edge(k,k+N, time = time, capacity = capacity)
                G.add_edge(k+N,k, time = time, capacity = capacity)
    
    return G

def network_graph_data():

    N = 10
    G = genGridGraph(N)

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
    
    graphviz_prog = 'neato'
    graphviz_args = '-Granksep=0.05'    

    # [ Create file with the layout information ]
    
    gviz_file_path  = os.path.abspath(os.path.join(dir_path,'rsc','gviz',NETWORK_NAME+'_custom.txt'))
    
    
    A.draw(gviz_file_path,format='plain', prog = graphviz_prog, args=graphviz_args)
    #A.draw(gviz_file_path.replace('.','')+'.png',format='png', prog = graphviz_prog, args=graphviz_args) # graphviz image
    
    # [ Load the file with the layout information ]
    
    #gviz_file_path  = os.path.abspath(os.path.join(dir_path,'rsc','gviz',NETWORK_NAME+'_custom.txt'))
    gviz_layouts.addGeometryFromGVizFile(G,gviz_file_path,2) # !important

    # { end custom layout method }


    return G 

