
import sys, os
import networkx as nx
from numpy import *

import matplotlib.pyplot as plt

def getPointsFromStrList(str_list):
    
    str_list = str_list[2:-2].replace(' ','').replace("'",'').split('],[')
    points = []

    pos_x = []
    pos_y = []
    for str_point in str_list:
        aux = str_point.split(',')
        point = [float(aux[0]),float(aux[1]),float(aux[2])]    
        points.append(point)
    
    return points

def tracerFilter(G,time_step):
    
    edge_log = {}

    flag = 0

    for edge in  G.edges_iter():
        
        edge_tail = G.node[edge[0]]
        edge_head = G.node[edge[1]]
    
        if edge not in edge_log:
            edge_log[edge] = 0
        else:
            edge_log[edge] = edge_log[edge] + 1
            
        edge_id = edge_log[edge]
            
        time                = G.edge[edge[0]][edge[1]][edge_id]['time']
        str_edge_geometry   = G.edge[edge[0]][edge[1]][edge_id]['geometry']
        route_points        = getPointsFromStrList(str_edge_geometry)
        
        numberOfDivisions   = int(floor(time/time_step))
        
        ##############
        
        idCounter       = 0
        newRoutePoints  = []
        listOfIds       = [0]
        
        route_length = 0.0
        points = route_points
        for i in xrange(len(points)-1):
            pi  = array(points[i])
            pi1 = array(points[i+1])
            route_length = route_length + linalg.norm(pi1 - pi)
             
        partition_route_length = route_length/(1.0*numberOfDivisions)
         
        k           = 0
        correction  = 0.0
        dTotal      = 0.0
        
        if (numberOfDivisions == 1):
            
            for k in xrange(len(points)):
                newRoutePoints.append(points[k])
                idCounter = idCounter + 1
            listOfIds.append(idCounter-1)
                
        else:
        
            for i in xrange(numberOfDivisions-1):
     
                d2Travel = partition_route_length - correction
                dTotal = 0.0
      
                while (d2Travel > 0):
                               
                    pos     = array(points[k])
                    npos    = array(points[k+1])
                                 
                    dTravelled      = linalg.norm(npos-pos)
                    d2Travel        = d2Travel - dTravelled
                     
                    if (d2Travel >= 0):
                        dTotal = dTotal + dTravelled
                     
                    k = k + 1
             
                    newRoutePoints.append(pos.tolist()) #########
                    idCounter = idCounter + 1
                     
                     
                if (d2Travel < 0):
                     
                    u_direction = (pos - npos)/linalg.norm(pos - npos)
                    final_pos   = npos + u_direction*abs(d2Travel)
                    dTravelled  = linalg.norm(final_pos-pos)
                    dTotal      = dTotal + dTravelled
                     
                    correction  = abs(d2Travel)
                 
                else:
                     
                    final_pos   = npos
                     
                newRoutePoints.append(final_pos.tolist()) #########
                listOfIds.append(idCounter)
                idCounter = idCounter + 1
             
            k = k + 1
        
            while (k < len(points)-1):
                newRoutePoints.append(points[k])
                idCounter = idCounter + 1
                k = k + 1
            listOfIds.append(idCounter)
                
        if (linalg.norm(array(newRoutePoints[-1]) - array(points[-1])) > 1E-5):

            newRoutePoints.append(points[-1])
            idCounter = idCounter + 1
            listOfIds.append(idCounter)
    
#         for point in points:
#             plt.plot(point[0],point[1],'ro')
#             
#         for gpoint in newRoutePoints:
#             plt.plot(gpoint[0],gpoint[1],'bx')
        
#         print edge_tail['pos']
#         print newRoutePoints[0]
#         print edge_head['pos']
#         print newRoutePoints[-1]
#         print listOfIds
        
        new_geometry = newRoutePoints
        geometry_ids = listOfIds
        
        #plt.show()
        
        #print geometry_ids
        
        G.edge[edge[0]][edge[1]][edge_id]['geometry'] = str(new_geometry)
        G.edge[edge[0]][edge[1]][edge_id]['geometry_keys'] = str(geometry_ids)

    #print G.edges(data=True)[0]

    return G

