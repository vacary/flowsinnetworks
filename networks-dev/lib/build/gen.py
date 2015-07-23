"""

VISUALIZATION DATA GENERATOR

"""

import os, sys
import networkx as nx

from numpy import *


def getFlowValue(theta,x_data,y_data):

    z = 0.0
    
    if (theta < x_data[0]):
        
        z = 0.0
        
    elif (theta > x_data[-1]):
            
        z = -1.0
        
    else:
        
        i = 0
        stop = 0
        while ( i < len(x_data)-1 and stop == 0 ):
    
            if (x_data[i] <= theta and theta < x_data[i+1]):
                
                p1 = [x_data[i],y_data[i]]
                p2 = [x_data[i+1],y_data[i+1]]
                                
                stop = 1
    
            i = i + 1
        
        if (p2[0] != p1[0]):
            z = ((p2[1]-p1[1])/(p2[0]-p1[0]))*(theta - p1[0]) + p1[1]
            
        else:
            z = max(p1[1],p2[1])

    return z

def getQValue(theta,arrayOfPoints):

    z = 0.0
    
    if (theta < arrayOfPoints[0][0] ):
        
        z = 0.0
        
    elif (theta > arrayOfPoints[-1][0]  ):
            
        z = -1.0
        
    else:
        
        i = 0
        stop = 0
        while ( i < arrayOfPoints.shape[0]-1 and stop == 0 ):
    
            if (arrayOfPoints[i][0] <= theta and theta <= arrayOfPoints[i+1][0]):
                
                p1 = arrayOfPoints[i]
                p2 = arrayOfPoints[i+1]
                                
                stop = 1
    
            i = i + 1
        
        if (p2[0] != p1[0]):
            z = ((p2[1]-p1[1])/(p2[0]-p1[0]))*(theta - p1[0]) + p1[1]
        else:
            z = p2[1]

    return z

def getArrayOfValuesOvertime(required_value,xArray,vArray,time_step,N,G):
    
    ans = zeros([N+1,2])
    
    if (required_value == 'f_e_minus_overtime' or required_value == 'f_e_plus_overtime'):
        
        x_data = []
        y_data = []
        listOfPoints = []
        
        for i in xrange(0,len(xArray)-1):
            x_data.append(xArray[i])
            y_data.append(vArray[i])
            x_data.append(xArray[i+1])
            y_data.append(vArray[i])

        for i in xrange(N+1):
            theta = i*time_step
            ans[i,0] = theta
            ans[i,1] = getFlowValue(theta,x_data,y_data)
            plt.plot([theta,theta],[0,ans[i,1]],'r')
                
    if (required_value == 'z_e_overtime'):
        
        arrayOfPoints = zeros([len(vArray),2])
    
        for i in xrange(0,len(vArray)):
            arrayOfPoints[i,0] = xArray[i] 
            arrayOfPoints[i,1] = vArray[i]

        for i in xrange(N+1):
            theta = i*time_step
            ans[i,0] = theta
            ans[i,1] = getQValue(theta, arrayOfPoints)
   
    return ans

def genDataFilesFromMultiDiGraphFile(G,time_step,Tmax,NETWORK_NAME,data_path):
    
    # Read graph
    
    network_gml_file_path = os.path.join(data_path,NETWORK_NAME+'.gml')
    
    G = nx.read_gml(network_gml_file_path)
    G = nx.MultiDiGraph(G)
    
    # Data arrays
    
    globalNumberOfTimeSteps = int(Tmax / time_step)

    arrayOfQueues           = zeros([globalNumberOfTimeSteps+1,G.number_of_edges()])
    arrayOf_f_e_minus       = zeros([globalNumberOfTimeSteps+1,G.number_of_edges()])
    arrayOf_f_e_plus        = zeros([globalNumberOfTimeSteps+1,G.number_of_edges()])
    
    edge_key = 0 # global edge counter
    
    for e in sorted(set(G.edges_iter())):

        edges = G.edge[e[0]][e[1]]
        
        edge_skey    = 0 # counter for multiple edges connecting two nodes
    
        c = 0
        
        while (c < len(edges)):  
            
            edges[c]['edge_key']    = edge_key
            edges[c]['edge_skey']   = c             # edge secondary key counter

            # get data

            if (edge_key >= 0): # (edge_key = 0, 1, 2...) # 

                # QUEUE VALUES OVERTIME
                 
                required_value  = 'z_e_overtime'
                xArray          = edges[c]['switching_times']
                vArray          = edges[c]['z_e_overtime']
                N               = globalNumberOfTimeSteps
                
                #vze             = getArrayOfValuesOvertime(required_value,xArray,vArray,time_step,N,G)
                #arrayOfQueues[:,edge_key] = vze[:,1]
                
                # f PLUS VALUES OVERTIME
                  
                required_value  = 'f_e_plus_overtime'
                xArray          = G.node[e[0]]['label_overtime']
                vArray          = edges[c]['f_e_plus_overtime'] 
                N               = globalNumberOfTimeSteps

                #vfep            = getArrayOfValuesOvertime(required_value,xArray,vArray,time_step,N,G)
                #arrayOf_f_e_plus[:,edge_key] = vfep[:,1]    
                
                # f MINUS VALUES OVERTIME
                
                for t in xrange(len(arrayOf_f_e_plus[:,edge_key])):
                
                    fe_minus_value = 0.0
                    
                    if (arrayOfQueues[t,edge_key] > 1E-10):
                        fe_minus_value = edges[c]['capacity']
                    else:
                        fe_minus_value = min(arrayOf_f_e_plus[t,edge_key],edges[c]['capacity'])
                    
                    arrayOf_f_e_minus[t,edge_key] = fe_minus_value

            #
            ###    
            
            c           = c + 1
            edge_key    = edge_key + 1  # update edge key counter
    
    
    # Create data files

    fm = file(''.join([os.path.join(data_path,NETWORK_NAME),'_','f_e_minus.dat']),'wb')    
    save(fm,arrayOf_f_e_minus)
    fm.close()

    q = file(''.join([os.path.join(data_path,graphName),'_','z_e.dat']),'wb')
    save(q,arrayOfQueues)
    q.close()    
    
    # Save graph
    
    nx.write_gml(G,network_gml_file_path)
    
    return None
    
    
NETWORK_NAME = 'G3'

network_gml_file_path = os.path.abspath(os.path.join('..','..','projects',NETWORK_NAME,'data',NETWORK_NAME+'.gml'))

G = nx.read_gml(network_gml_file_path)
G = nx.MultiDiGraph(G)

print network_gml_file_path
print G.nodes()

#genDataFilesFromMultiDiGraphFile(G,time_step = 0.1,Tmax = 10,NETWORK_NAME,data_path)



