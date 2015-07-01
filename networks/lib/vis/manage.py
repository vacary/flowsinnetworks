"""

Methods to get the required data for the visualization

"""

import os, sys, re
import networkx as nx
from numpy import *

def get_map_crop_bounds(map_coords_path):
   
    pars_name_list = []
    pars_value_list = []   
    
    f = open(map_coords_path,'r')
    for line in f:
        if re.search(r"[A-Z]",line):
            aux = line.split()
            if (len(aux) == 3 and aux[1] == '='):
                pars_name_list.append(aux[0])
                pars_value_list.append(aux[2])
    f.close()
    
    # set parameters
    nList    = pars_name_list
    vList    = pars_value_list

    pars = {}

#     
    for par in nList:
 
        c = nList.index(par)        
         
        if (par == 'W'):
            pars[par] = float(vList[c])
        if (par == 'S'):
            pars[par] = float(vList[c])
        if (par == 'E'):
            pars[par] = float(vList[c])
        if (par == 'N'):
            pars[par] = float(vList[c])
    
    return pars        
    

def get_vparameters(visualization_settings_path):
    
    pars_file_path = visualization_settings_path
    
    pars_name_list = []
    pars_value_list = []
 
    
    f = open(pars_file_path,'r')
    for line in f:
        if re.search(r"[A-Z]",line):
            aux = line.split()
            if (len(aux) == 3 and len(aux[0]) > 1):
                pars_name_list.append(aux[0])
                pars_value_list.append(aux[2])
    f.close()
    
    # set parameters
    nList    = pars_name_list
    vList    = pars_value_list
    
    pars = {}
    
    for par in nList:

        c = nList.index(par)        
        
        if (par == 'NETWORK_NAME'):
            pars[par] = str(vList[c]).replace('"','')
        if (par == 'TIME_STEP'):
            pars[par] = float(vList[c])
        if (par == 'T_MAX_VIS'):
            pars[par] = float(vList[c])
        if (par == 'FPS'):
            pars[par] = int(vList[c])
        if (par == 'SIMULATION_DATA_AVAILABLE'):
            pars[par] = int(vList[c])
        if (par == 'PRIORITY_GRAPHVIZ_LAYOUT'):
            pars[par] = int(vList[c])
        if (par == 'TYPE'):
            pars[par] = str(vList[c]).replace('"','')
    
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
        
        edge_key        = data['edge_key']
        edge_skey       = data['edge_skey']
        
        try:

            time            = data['time']
            capacity        = data['capacity']
            geometry        = data['geometry']
            geometry_keys   = data['geometry_keys']
            
            G.add_edge(u,v, edge_key = edge_key, edge_skey = edge_skey, time = time, capacity = capacity, geometry = geometry, geometry_keys = geometry_keys)  
        
        except:
        
            time        = data['time']
            capacity    = data['capacity']
            
            G.add_edge(u,v, edge_key = edge_key, edge_skey = edge_skey, time = time, capacity = capacity)
        
    return G




