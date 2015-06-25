'''

Functions for graph data

'''

import os, sys
import networkx as nx
from numpy import *

def get_graphFromGMLFile(network_file_path):
    
    G = nx.MultiDiGraph()
    
    SG = nx.read_gml(network_file_path) #source graph
    
    for n in SG.nodes_iter():
        
        G.add_node(n)
        G.node[n]['id']     = SG.node[n]['id']
        G.node[n]['label']  = SG.node[n]['label']
        G.node[n]['nlabel'] = SG.node[n]['label']
        G.node[n]['type']   = 'r'
        
    for u,v,data in SG.edges_iter(data=True):
        
        time        = data['time']
        capacity    = data['capacity']
        
        G.add_edge(u,v, time = time, capacity = capacity)
        
    return G
