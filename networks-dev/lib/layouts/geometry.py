
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

    for edge in  [G.edges()[20]]:#G.edges_iter():
        
        edge_tail = G.node[edge[0]]
        edge_head = G.node[edge[1]]
        
        print edge_tail['pos']
        print edge_head['pos']
        
        plt.plot(edge_tail['pos'][0],edge_tail['pos'][1],'go',markersize=20)
        plt.plot(edge_head['pos'][0],edge_head['pos'][1],'ro',markersize=20)
        
        if edge not in edge_log:
            edge_log[edge] = 0
        else:
            edge_log[edge] = edge_log[edge] + 1
            
        edge_id = edge_log[edge]
            
        time                = G.edge[edge[0]][edge[1]][edge_id]['time']
        str_edge_geometry   = G.edge[edge[0]][edge[1]][edge_id]['geometry']
        route_points        = getPointsFromStrList(str_edge_geometry)
        
        numberOfDivisions   = int(ceil(time/time_step))
        
        ########
        
        route_length = 0.0
        points = route_points
        for i in xrange(len(points)-1):
            pi  = array(points[i])
            pi1 = array(points[i+1])
            route_length = route_length + linalg.norm(pi1 - pi)
             
        partition_route_length = route_length/(1.0*numberOfDivisions)
        
        print '----'
        print route_length
        print partition_route_length
        print numberOfDivisions
        print '----'
         
        k           = 0
        
        correction  = 0.0
        dTotal      = 0.0
        
        for i in xrange(numberOfDivisions-1):
        
        #while (k < len(points)-1):
            colorset = [random.random(),random.random(),random.random()]
        
            d2Travel = partition_route_length - correction
            dTotal = 0.0
 
            while (d2Travel > 0):
            
                points_set = []
              
                pos     = array(points[k])
                npos    = array(points[k+1])
                
                plt.plot(pos[0],pos[1],'go')
                #plt.plot(npos[0],npos[1],'r*',markersize=20)
                
                dTravelled      = linalg.norm(npos-pos)
                d2Travel  = d2Travel - dTravelled
                
                if (d2Travel >= 0):
                    dTotal = dTotal + dTravelled
                
                k = k + 1
                
            if (d2Travel < 0):
                
                u_direction = (pos - npos)/linalg.norm(pos - npos)
                final_pos = npos + u_direction*abs(d2Travel)
                dTravelled  = linalg.norm(final_pos-pos)
                dTotal = dTotal + dTravelled
                
                correction = abs(d2Travel)
            
            else:
                
                final_pos = npos
            
            plt.plot(final_pos[0],final_pos[1],'bo')
        
        print dTotal
        plt.axis('equal')
        
    return G



import sys, os
import networkx as nx
import matplotlib.pyplot as plt


import random


from numpy import *

lib_path = os.path.abspath(os.path.join('..','..'))
sys.path.append(lib_path)
print lib_path
import lib.vis.manage as vis_mn

nname = 'G3'
gml_file_path = os.path.join('..','..','projects',nname,'data',nname+'.gml')
G = vis_mn.get_graphFromGMLFile(gml_file_path)         
G = nx.MultiDiGraph(G)   
time_step = 0.1


tracerFilter(G,time_step)
plt.show()

