
import os, sys
import matplotlib.pyplot as plt
from numpy import *
import random
import networkx as nx

lib_path = os.path.abspath(os.path.join('..','..'))
sys.path.append(lib_path)
import lib.maps as mp



osm_file_path = os.path.join('.','map_graph_test.osm')
G = mp.get_graphFromOSMFile2(osm_file_path,0.1)
G = nx.MultiDiGraph(G)

edge = G.edge[43][17]

def get_ListOfPointsFromGeoString(edge):

    geo = edge[0]['geometry']
    geo = geo.replace(' ','')
    geo = geo.replace('[[','[')
    geo = geo.replace(']]',']')
    
    str_list = geo.split(']')
    str_list.pop()
    
    output = []
    for elem in str_list:
        
        elem = elem.replace('[','')
        
        aux = elem.split(',')
        
        if (aux[0] == ''):
            
            aux.pop(0)
            
        pos = array([float(aux[0]),float(aux[1]),float(aux[2])])
        output.append(pos)
    
    return output


def get_ListOfKeysFromGeoKeyString(edge):
    
    geo = edge[0]['geometry_keys']
    geo = geo.replace(' ','')
    geo = geo.replace('[','')
    geo = geo.replace(']','')
    
    str_list = geo.split(',')
    
    output = []
    for elem in str_list:
        
        key = float(elem)
        output.append(key)
        
    return output
    
points = get_ListOfPointsFromGeoString(edge)

for point in points:
    
    plt.plot([point[0]],[point[1]],'ro')
    
plt.show()




    
    
    
    
    