
from numpy import *

import matplotlib.pyplot as plt
import networkx as nx
import os

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
    
            if (x_data[i] <= theta and theta <= x_data[i+1]):
                
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

def getQueueDataFromSimulationByEdge(G,ntail,nhead,time_step,Tmax):


    vQ = G[ntail][nhead][0]['z_e_overtime'][:]
    vtheta = G[ntail][nhead][0]['switching_times'][:]

    arrayOfPoints = zeros([len(vQ),2])

    for i in xrange(0,len(vQ)):
        arrayOfPoints[i,0] = vtheta[i] 
        arrayOfPoints[i,1] = vQ[i]

    N = int(Tmax / time_step)

    lst = zeros([N+1,2])

    for i in xrange(N+1):
        theta = i*time_step
        lst[i,0] = theta
        lst[i,1] = getQValue(theta, arrayOfPoints)

    plt.plot(lst[:,0],lst[:,1],'bo')

    return lst

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
            #print([xArray[i],vArray[i]])
            #print([xArray[i+1],vArray[i]])

        for i in xrange(N+1):
            theta = i*time_step
            ans[i,0] = theta
            ans[i,1] = getFlowValue(theta,x_data,y_data)
        
        plt.subplot(512)
        plt.plot(x_data,y_data,'bo')
        plt.plot(ans[:,0],ans[:,1],'rx')
        
    if (required_value == 'z_e_overtime'):
        
        arrayOfPoints = zeros([len(vArray),2])
    
        for i in xrange(0,len(vArray)):
            arrayOfPoints[i,0] = xArray[i] 
            arrayOfPoints[i,1] = vArray[i]

        for i in xrange(N+1):
            theta = i*time_step
            ans[i,0] = theta
            ans[i,1] = getQValue(theta, arrayOfPoints)
   
        plt.subplot(515)
        plt.plot(arrayOfPoints[:,0],arrayOfPoints[:,1],'bo')
        plt.plot(ans[:,0],ans[:,1],'rx')
    
    return ans
    
def genDataFromMultiGraphStructure(G,time_step,Tmax,graphName):

    data_path = os.path.abspath(os.path.join('data'))
    #data_path = '/home/max/workspace/flowsinnetworks/Sandbox/networks/data'

    fm = file(''.join([os.path.join(data_path,graphName),'_','f_e_minus.dat']),'wb')
    fp = file(''.join([os.path.join(data_path,graphName),'_','f_e_plus.dat']),'wb')
    q = file(''.join([os.path.join(data_path,graphName),'_','z_e.dat']),'wb')

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

            ###
            # creating data files for visualization

            # get data

            if (edge_key >= 0): # (edge_key = 0, 1, 2...) # 

                # QUEUE VALUES OVERTIME
                 
                required_value  = 'z_e_overtime'
                xArray          = edges[c]['switching_times']
                vArray          = edges[c]['z_e_overtime']
                N               = globalNumberOfTimeSteps
                vze             = getArrayOfValuesOvertime(required_value,xArray,vArray,time_step,N,G)

                arrayOfQueues[:,edge_key] = vze[:,1]
                 
                # F MINUS VALUES OVERTIME
                 
                required_value  = 'f_e_minus_overtime'
                xArray          = G.node[e[1]]['label_overtime']
                vArray          = edges[c]['f_e_minus_overtime'] 
                N               = globalNumberOfTimeSteps
                vfem            = getArrayOfValuesOvertime(required_value,xArray,vArray,time_step,N,G)
    
                arrayOf_f_e_minus[:,edge_key] = vfem[:,1]    

                # F PLUS VALUES OVERTIME
                 
                required_value  = 'f_e_plus_overtime'
                xArray          = G.node[e[0]]['label_overtime']
                vArray          = edges[c]['f_e_plus_overtime'] 
                N               = globalNumberOfTimeSteps
                vfep            = getArrayOfValuesOvertime(required_value,xArray,vArray,time_step,N,G)

                arrayOf_f_e_plus[:,edge_key] = vfep[:,1]    


            #
            ###    
            
            c           = c + 1
            edge_key    = edge_key + 1  # update edge key counter
    

    save(fm,arrayOf_f_e_minus)
    fm.close()
    
    save(fp,arrayOf_f_e_plus)
    fp.close()
    
    save(q,arrayOfQueues)
    q.close()
    
    return G


def genVData(G,time_step,Tmax,graphName):

    # Paths for output files

    data_path = os.path.abspath(os.path.join('data'))
    temp_path = os.path.abspath(os.path.join('temp'))
    
    #data_path = '/home/max/workspace/flowsinnetworks/Sandbox/networks/data'
    #temp_path = '/home/max/workspace/flowsinnetworks/Sandbox/networks/temp'
    
    # Add graph edges keys and create data files for visualization
    
    G = genDataFromMultiGraphStructure(G,time_step,Tmax,graphName)

    
    ''' Modifications in graph data according to the required file output format
    '''
    
    # node data
    
    for n in G.nodes_iter():

        G.node[n]['label_thin_flow_overtime'] = str(G.node[n]['label_thin_flow_overtime'])
        G.node[n]['label_overtime'] = str(G.node[n]['label_thin_flow_overtime'])
        G.node[n]['nlabel'] = str(n)

    # edges data

    for e in sorted(set(G.edges_iter())):

        edges = G.edge[e[0]][e[1]]
    
        c = 0
        
        while (c < len(edges)):  
                        
            # graph data modifications for file output
            edges[c]['x_overtime']              = str(edges[c]['x_overtime'])
            edges[c]['thin_flow_overtime']      = str(edges[c]['thin_flow_overtime'])
            edges[c]['switching_times']         = str(edges[c]['switching_times'])
            edges[c]['F_e_minus_overtime']      = str(edges[c]['F_e_minus_overtime'])
            edges[c]['F_e_plus_overtime']       = str(edges[c]['F_e_plus_overtime'])
            edges[c]['f_e_plus_overtime']       = str(edges[c]['f_e_plus_overtime'])
            edges[c]['f_e_minus_overtime']      = str(edges[c]['f_e_minus_overtime'])
            edges[c]['z_e_overtime']            = str(edges[c]['z_e_overtime'])                
    
            c = c + 1

    # Save file with the graph data

    nx.write_gml(G,os.path.join(data_path,graphName+".gml"))
    nx.write_gml(G,os.path.join(temp_path,"temp.gml"))
    plt.savefig(os.path.join(temp_path,'test.png'))
    
    #print('[ graph file available ]' )
    