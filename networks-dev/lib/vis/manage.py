"""

Methods to manage visualization data

"""

import os, sys, re
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

import networkx as nx
from numpy import *
    
def get_vparameters(visualization_settings_path):
    
    sys.path.append(visualization_settings_path)
    import settings as vset
    
    # set parameters
    
    pars = {}
    
    pars['NETWORK_NAME']                = vset.NETWORK_NAME
    pars['TIME_STEP']                   = vset.TIME_STEP
    pars['T_MAX_VIS']                   = vset.T_MAX_VIS
    pars['FPS']                         = vset.FPS
    pars['SIMULATION_DATA_AVAILABLE']   = vset.SIMULATION_DATA_AVAILABLE
    pars['PRIORITY_GRAPHVIZ_LAYOUT']    = vset.PRIORITY_GRAPHVIZ_LAYOUT
    pars['TYPE']                        = vset.TYPE
     
    gdata = vset.network_graph_data()
    
    G = gdata[0]
    
    pars['NODE_SOURCE_LABEL']   = str(gdata[1])
    pars['NODE_SINK_LABEL']     = str(gdata[2])
        
    return pars


def get_graphFromGMLFile(network_gml_file_path):
    
    G = nx.MultiDiGraph()
    
    SG = nx.read_gml(network_gml_file_path) #source graph
    
    c = 0
    
    for n in SG.nodes_iter():
        
        G.add_node(n)
        G.node[n]['id']     = c
        
        G.node[n]['nlabel'] = SG.node[n]['nlabel']
        
        str_pos = str(SG.node[n]['pos'])
        aux = str_pos.translate(None,''.join(['[',']'])).split(',')
        pos = [float(aux[0]),float(aux[1]),float(aux[2])] 
        G.node[n]['pos']    = array(pos)
        G.node[n]['type']   = 'r'
                
        c = c + 1
        
    for u,v,data in SG.edges_iter(data=True):
                
        time        = data['time']
        capacity    = data['capacity']

        edge_key        = -1
        edge_skey       = -1
                
        geometry        = ''
        geometry_keys   = ''
        
        try:
            edge_key        = data['edge_key']
        except:
            pass
        
        try:
            edge_skey       = data['edge_skey']
        except:
            pass
        
        try:
            geometry        = data['geometry']
        except:
            pass
        
        try:
            geometry_keys   = data['geometry_keys']
        except:
            pass
            
        G.add_edge(u,v, edge_key = edge_key, edge_skey = edge_skey, time = time, capacity = capacity, geometry = geometry, geometry_keys = geometry_keys)
        
    return G



