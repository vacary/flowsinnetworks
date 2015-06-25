'''

VISUALIZATION DATA MANAGER

'''

import os, sys, re
import networkx as nx
from numpy import *

def get_GUI_info(INTERACTOR_STYLE):
    
    msgTxt = '  Flows In Networks \n\n'
    msgTxt += '  Jun 24, 2015 \n\n\n'
    msgTxt += '  Interactor Style:\n\n'
    
    if (INTERACTOR_STYLE == 'StyleImage'):
    
        msgTxt += '  [ StyleImage ]\n\n'
        msgTxt += '  Controls:\n\n'
        msgTxt += '  Right mouse - Zoom \n'
        msgTxt += '  Control + Left mouse - Rotation (2D) \n'
        msgTxt += '  Middle mouse - Pan \n'
        msgTxt += '  Scroll wheel - Zoom \n'
    
    else:

        msgTxt += '  [ RubberBand3D ]\n\n'
        msgTxt += '  Controls:\n\n'
        msgTxt += '  Right mouse - Rotate \n'
        msgTxt += '  Shift + Right mouse - Zoom \n'
        msgTxt += '  Middle mouse - Pan \n'
        msgTxt += '  Scroll wheel - Zoom \n'
    
    msgTxt = '\n' + msgTxt
    
    return msgTxt

def get_graphFromGMLFile(network_name):
    
    G = nx.MultiDiGraph()
    
    SG = nx.read_gml(os.path.join('.','projects',network_name,'data',str(network_name)+'.gml')) #source graph
    
    c = 0
    
    for n in SG.nodes_iter():
        
        G.add_node(n)
        G.node[n]['id']     = c
        G.node[n]['nlabel'] = str(n)
        str_pos = str(SG.node[n]['pos'])
        aux = str_pos.translate(None,''.join(['[',']'])).split(',')
        pos = [float(aux[0]),float(aux[1]),float(aux[2])] 
        G.node[n]['pos']    = array(pos)
        G.node[n]['type']   = 'r'
                
        c = c + 1
        
    for u,v,data in SG.edges_iter(data=True):
        
        edge_key        = data['edge_key']
        edge_skey       = data['edge_skey']
        
        time        = data['time']
        capacity    = data['capacity']
        
        G.add_edge(u,v, edge_key = edge_key, edge_skey = edge_skey, time = time, capacity = capacity)
        
    return G    

def get_vparameters(network_name):
    
    pars_file_path = os.path.join('.','projects',network_name,'network.py')
    
    pars_name_list = []
    pars_value_list = []
    
    pars = []
    
    f = open(pars_file_path,'r')
    for line in f:
        if re.search(r"[A-Z]",line):
            aux = line.split()
            if (len(aux) == 3 and len(aux[0]) > 1):
                pars_name_list.append(aux[0])
                pars_value_list.append(aux[2])
    f.close()
    
    pars = [pars_name_list,pars_value_list]
    
    return pars

def check_package(string_name,msg):
    
    package = string_name
    found   = False
    
    try:
        __import__(package)
        found = True
        print '[*] '+str(package)
 
    except ImportError:
        if (msg == ''):
            msg = '[not found]'
        print '[x] '+str(package)+' '+str(msg)
    
    return found

def check_packages(pck_list,msg_list):
    
    eval = True
    c = 0
    for pck in pck_list:
        check = (check_package(pck,msg_list[c]) and eval)
        eval = check
        c = c + 1
    
    return eval
        
        
        
    
    