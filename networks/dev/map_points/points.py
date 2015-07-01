
import os, sys
import matplotlib.pyplot as plt
from numpy import *
import random

lib_path = os.path.abspath(os.path.join('..','..'))
sys.path.append(lib_path)
import lib.maps as mp

def translatorNodePos(node,fullListOfNodes,fullListOfPos):
    
    c = fullListOfNodes.index(node)
    
    return fullListOfPos[c]

def getEdgeGeometryAndKeys(listOfTranslatedEdgePoints,time,time_step):
    
    points = listOfTranslatedEdgePoints
    
    # start with point analysis
    numberOfDivisionsForEdge = int(floor(time/time_step))
    
    total_dist = 0
    for i in xrange(len(points)-1):
        pi = array(points[i])
        pi1 = array(points[i+1])
        total_dist = total_dist + linalg.norm(pi1 - pi)
     
    delta_dist = total_dist/(1.0*numberOfDivisionsForEdge)
    
    k       = 0
    p       = array(points[k])
    dif     = array(points[k+1]) - array(points[k])
    ndif    = linalg.norm(dif)
    u       = dif/ndif
    step    = delta_dist
     
    total_drec = 0
    drec = 0
    counter = 0
    
    output = []
    keys = [0]
    output.append(points[0])
    while (abs(total_drec - total_dist) > 1E-10):
        q       = p + step*u
        drec    = drec + linalg.norm(q - p)
        if (drec > ndif and k < len(points)-2):
            k           = k + 1
            prev        = p
            p           = points[k]
            output.append(p)
            drec        = 0
            dif         = array(points[k+1]) - array(points[k])
            ndif        = linalg.norm(dif)
            u           = dif/ndif
            step        = linalg.norm(p - q)
        else:
            output.append(q)
            keys.append(len(output)-1)
            total_drec  = total_drec + delta_dist
            p           = q
            step        = delta_dist
        counter = counter + 1
    
    output.append(points[-1])

    return [output,keys]

osm_file_path = os.path.join('.','map_graph_test.osm')
datalist = mp.osm2graphData(osm_file_path)

edge_data = datalist[3]
nedge = 17
edge = edge_data[nedge]

# translate list of osm nodes to list of points
listOfEdgeOSMPoints = edge[-1]
points = []
for osm_node in listOfEdgeOSMPoints:
    point = translatorNodePos(osm_node, datalist[0], datalist[1])
    points.append(point)

time = 1.0
time_step = 0.1

output, keys = getEdgeGeometryAndKeys(points,time,time_step)
     
for point in output:
    
    plt.plot(point[0],point[1],'bo') 
    
plt.show()
    
print output
print keys


    
    
