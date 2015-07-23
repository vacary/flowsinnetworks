
import os, sys
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

import time
import networkx as nx

from numpy import *

'''
Read the geometry data source and create dictionaries

'''

dict_nodes_geometry = {}
dict_edges_geometry = {}

f = open(os.path.abspath(os.path.join(dir_path,'..','..','projects','G3','rsc','gviz','G3_gen.txt')))

for line in f:
    
    aux = line
    aux = aux.replace("\n","")
    list = aux.split(" ")
    
    elm = list[0]
    
    if (elm == 'node'):
        node_id     = int(list[1])
        node_pos_x  = float(list[2])
        node_pos_y  = float(list[3])
        dict_nodes_geometry[node_id] = str([node_pos_x,node_pos_y,0.0])
    
    if (elm == 'edge'):
        edge_tail = int(list[1])
        edge_head = int(list[2])
        edge_npoints = int(list[3])
        geometry = []
        pos_tail = dict_nodes_geometry[edge_tail]
        pos_head = dict_nodes_geometry[edge_head]
        
        geometry.append(pos_tail)
        
        aux = 3
        for c in xrange(edge_npoints):
            pos_x = float(list[aux])
            pos_y = float(list[aux + 1])
            aux = aux + 2
            geometry.append(str([pos_x,pos_y,0.0]))
            
        geometry.append(pos_head)
        
        dict_edges_geometry[(edge_tail,edge_head)] = str(geometry)

f.close()

#print dict_nodes_geometry
# for elm in dict_edges_geometry:
#     
#     print elm

'''
Add the geometry data to the network graph

'''

#NETWORK_NAME = "G3_gen"
#network_gml_file_path = os.path.abspath(os.path.join(dir_path,'..','..','..','Flows','graphs',NETWORK_NAME+'.gml'))
#G = nx.read_gml(network_gml_file_path)

network_gml_file_path = open(os.path.abspath(os.path.join(dir_path,'..','..','projects','Larre','data','Larre.gml')))
network_gml_file_path = open(os.path.abspath(os.path.join(dir_path,'..','..','projects','G200','data','G200.gml')))

network_gml_file_path = open(os.path.abspath(os.path.join(dir_path,'..','..','projects','G3','data','G3.gml')))
G = nx.read_gml(network_gml_file_path)
G = nx.MultiDiGraph(G)

# for node in G.nodes_iter():
#     
#     G.add_node(node,pos=dict_nodes_geometry[node])

# for edge in G.edges_iter():
#     
#     G.add_edge(edge[0],edge[1],geometry=dict_edges_geometry[edge])

xcoords = []
ycoords = []

for node in G.nodes_iter():
    
    pos = G.node[node]['pos'][1:-1].split(',')

    xcoords.append(float(pos[0]))
    ycoords.append(float(pos[1]))
   

xcoords = sorted(xcoords)
ycoords = sorted(ycoords)

radius = max(max(xcoords)-min(xcoords),max(ycoords)-min(ycoords))

print radius

found = 0
i = 0

while (found == 0):
     
    stop = 0
    
    while (stop == 0 and i < 2 + 0*len(xcoords)-1): 
    
        xc_plus_r   = xcoords[i] + radius
        xc_minus_r  = xcoords[i+1] - radius
        
        yc_plus_r   = ycoords[i] + radius
        yc_minus_r  = ycoords[i+1] - radius
        
        i = i + 1
        
        #if (xc_plus_r  >= xc_minus_r or yc_plus_r >= yc_minus_r):
        if (xc_plus_r  >= xc_minus_r ):
        
            stop = 1
            radius = 0.9*radius
            i = 0
        
    if (stop == 0):
        found = 1
    
    print radius
      
print 'final radius'  
print radius
        
    





    
    
    
    
    






