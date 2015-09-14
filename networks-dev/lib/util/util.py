
import os
import sys
import osm
import networkx as nx
import random

import matplotlib.pyplot as plt

filename = 'heroes.osm'
#filename = 'map_graph_test.osm'

osm_path_file = os.path.abspath(os.path.join('..','..','projects','tobalaba_min','rsc','osm',filename))
print osm_path_file

nw = osm.OsmNetwork(osm_path_file)
 
G, source, sink = nw.get_network_graph_data()

for e in G.edges(keys=True):
        
    points = G.edge[e[0]][e[1]][e[2]]['geometry']
        
    gx = []
    gy = []
     
    for elm in points:
        gx.append(elm[0])
        gy.append(elm[1])
    print gy
    plt.plot(gx, gy, 'r', c = (0.75,0.75,0.75), lw=2)

    if '223965001' in [e[0],e[1]]:
        
        plt.plot(gx, gy, 'r', c = (0.0,0.75,0.0), lw=4)

length,path=nx.single_source_dijkstra(G, source, weight='time')

reachablesFromSource = nx.descendants(G, source)
nodesToRemove = []

for node in G.nodes_iter():
    
    if (node not in reachablesFromSource):
        print node
        print 'found'
        if (node != source):
            nodesToRemove.append(node)

for node in nodesToRemove:
    
    G.remove_node(node)

for e in G.edges(keys=True):
        
    points = G.edge[e[0]][e[1]][e[2]]['geometry']
        
    gx = []
    gy = []
     
    for elm in points:
        gx.append(elm[0])
        gy.append(elm[1])
    print e[0], e[1]
    

    plt.plot(gx, gy, 'r', c = (0.75,0.0,0.0), lw=1)

print sink in reachablesFromSource
print '223965001' in G.nodes()

plt.show()