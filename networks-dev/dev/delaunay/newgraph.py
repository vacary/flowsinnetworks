'''

Test

* Networkx graph generation from Delaunay triangulation 

* Based on the comments from stackoverflow

http://stackoverflow.com/questions/26681899/how-to-make-networkx-graph-from-delauney-preserving-attributes-of-the-input-node

'''

import networkx as nx
import scipy.spatial

from numpy import *

N = 50       # number of nodes will be N**2
points = []

x_limit = 50
y_limit = 50

dx = x_limit/(1.0*N)
dy = y_limit/(1.0*N)

for i in xrange(N):
    
    y_min = i*dy
    y_max = (i+1)*dy
    
    for j in xrange(N):
        
        x_min = j*dx
        x_max = (j+1)*dx
        
        ### point sampled from the square (x_min,y_min),(x_max,y_max)
        point = [random.uniform(x_min,x_max),random.uniform(y_min,y_max)]
        
        ### middle point  
        #point = [0.5*(x_min + x_max), 0.5*(y_min + y_max)]
        
        points.append(point)
    
delTri = scipy.spatial.Delaunay(points)
edges = set()

for n in xrange(delTri.nsimplex):
     
    edge = sorted([delTri.vertices[n,0],delTri.vertices[n,1]])
    edges.add((edge[0],edge[1]))
    edge = sorted([delTri.vertices[n,0],delTri.vertices[n,2]])
    edges.add((edge[0],edge[1]))
    edge = sorted([delTri.vertices[n,1],delTri.vertices[n,2]])
    edges.add((edge[0],edge[1]))
    
G = nx.Graph(list(edges))
G = nx.MultiDiGraph(G)

print G.number_of_nodes()
print G.number_of_edges()

import matplotlib.pyplot as plt
pointIDXY = dict(zip(range(len(points)),points))
nx.draw(G,pointIDXY)
plt.show()
#     
# A = nx.to_agraph(G)
# A.draw('test.png',format='png',prog='sfdp',args='-Granksep=3;-Goverlap=prism;')
#A.draw('test.png',format='png',prog='sfdp',args='-Granksep=0.1;-Gnodesep=1;-Goverlap=prism;')

#

     
