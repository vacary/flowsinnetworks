"""

VISUALIZATION DATA GENERATOR

"""

import os, sys
import networkx as nx
import time

from numpy import *
import matplotlib.pyplot as plt

def getArrayFromStrList(str_list):

    str_list    = str_list[1:-1]
    output      = [float(elm) for elm in str_list.split(',')]
    
    return output

def binarySearch(theta,xlist,vlist):

    first   = 0
    last    = len(xlist)-1
    
    while (first < last):
        mid = int((first + last)/2)
        if (xlist[mid] < theta):
            first = mid + 1
        else:
            last = mid

    return first

def getArrayOfValuesOvertime(required_values,xArray,vArray,time_step,N):
    
    output = zeros([N+1,2])
    
    if (required_values == 'f_e_minus_overtime' or required_values == 'f_e_plus_overtime'):
        
        x_data = []
        y_data = []
        
        for i in xrange(len(xArray)-1):
            x_data.append(xArray[i])
            y_data.append(vArray[i])
            x_data.append(xArray[i+1])
            y_data.append(vArray[i])
        
        if (required_values == 'f_e_minus_overtime'):
            plt.plot(x_data,y_data,'ro')
        else:
            plt.plot(x_data,y_data,'go')
        
        for i in xrange(N+1):
            theta = i*time_step 
            output[i,0] = theta
            output[i,1] = getSampledValue(theta, xArray, vArray)
                       
    if (required_values == 'z_e_overtime'):
        
        for i in xrange(N+1):
            theta = i*time_step
            output[i,0] = theta
            output[i,1] = getSampledQValue(theta,xArray,vArray)        
        
    return output

def getSampledValue(theta,xlist,vlist):
    
    if (theta < min(xlist)):
        value   = 0.0
    elif (theta > max(xlist)):
        value   = -1.0
    else:
        # index from binary search
        k = binarySearch(theta,xlist,vlist) - 1
        # value
        if (theta == xlist[0]):
            value = vlist[0]
        else:
            value = vlist[k]
        value = max(value,0.0)
        if (value < 10**-10):
            value = 0.0
        
    return value

def getSampledQValue(theta,xlist,vlist):
    
    if (theta < min(xlist)):
        value   = 0.0
    elif (theta > max(xlist)):
        value   = -1.0
    else:
        # index from binary search
        k = binarySearch(theta,xlist,vlist) - 1
        # value
        if (theta == xlist[0]):
            value = vlist[0]
        else:
            if (xlist[k] != xlist[-1]):
                if (xlist[k] != xlist[k+1]):
                    p       = [xlist[k],vlist[k]]
                    q       = [xlist[k+1],vlist[k+1]]
                    value   = ((q[1]-p[1])/(q[0]-p[0]))*(theta - p[0]) + p[1]
                else:
                    value   = vlist[k]
            else:                
                value   = vlist[k]
    
        value = max(value,0.0)
        if (value < 10**-10):
            value = 0.0
                
    return value

def genDataFiles(G,time_step,Tmax,NETWORK_NAME,data_path):
    
    # Data arrays
    
    globalNumberOfTimeSteps = int(ceil(Tmax / time_step))

    N = globalNumberOfTimeSteps
    
    arrayOf_Queues          = zeros([N+1,G.number_of_edges()])
    arrayOf_f_e_plus        = zeros([N+1,G.number_of_edges()])
    arrayOf_f_e_minus       = zeros([N+1,G.number_of_edges()])

    # Read simulation data from graph

    edge_log = {}
    edge_key = 0

    for edge in  G.edges_iter():
        
        edge_tail = G.node[edge[0]]
        edge_head = G.node[edge[1]]
        
        if edge not in edge_log:
            edge_log[edge] = 0
        else:
            edge_log[edge] = edge_log[edge] + 1
        
        edge_id = edge_log[edge]
            
        # *** Set edge key to associate the simulation data with the respective edge ***
        
        G.edge[edge[0]][edge[1]][edge_id]['edge_key'] = edge_key
        
        # Get values and create files
        
        str_label_overtime_fe_plus  = G.node[edge[0]]['label_overtime']
        str_label_overtime_fe_minus = G.node[edge[1]]['label_overtime']
        str_f_e_plus_overtime       = G.edge[edge[0]][edge[1]][edge_id]['f_e_plus_overtime']
        str_f_e_minus_overtime      = G.edge[edge[0]][edge[1]][edge_id]['f_e_minus_overtime']
        str_z_e_overtime            = G.edge[edge[0]][edge[1]][edge_id]['z_e_overtime']
        str_switching_times         = G.edge[edge[0]][edge[1]][edge_id]['switching_times']

        #------------------------------
        # queue values
        #------------------------------
        
        required_values = "z_e_overtime"
        xArray  = getArrayFromStrList(str_switching_times)
        vArray  = getArrayFromStrList(str_z_e_overtime)
        
        data    = getArrayOfValuesOvertime(required_values, xArray, vArray, time_step, N)
        #plt.plot(data[:,0],data[:,1],'b*',c=[random.random(),random.random(),random.random()])
        
        arrayOf_Queues[:,edge_key] = data[:,1] 
         
        #------------------------------
        # f plus values overtime 
        #------------------------------ 
        required_values = "f_e_plus_overtime"
        xArray  = getArrayFromStrList(str_label_overtime_fe_plus)
        vArray  = getArrayFromStrList(str_f_e_plus_overtime)
         
        data    = getArrayOfValuesOvertime(required_values, xArray, vArray, time_step, N)
        #plt.plot(data[:,0],data[:,1],'bx',c=[random.random(),random.random(),random.random()])
         
        arrayOf_f_e_plus[:,edge_key] = data[:,1] 
        
        #-------------------------------
        # f minus values overtime 
        #-------------------------------
        
        required_values = "f_e_minus_overtime"
        for t in xrange(len(arrayOf_f_e_plus[:,edge_key])):
              
            fe_minus_value = 0.0
              
            capacity = float(G.edge[edge[0]][edge[1]][edge_id]['capacity'])
              
            if (arrayOf_Queues[t,edge_key] > 1E-10):
                fe_minus_value = capacity
            else:
                fe_minus_value = min(arrayOf_f_e_plus[t,edge_key],capacity)
              
            arrayOf_f_e_minus[t,edge_key] = fe_minus_value
          
        arrayOf_f_e_minus[:,edge_key] = data[:,1]
        #plt.plot(data[:,0],arrayOf_f_e_minus[:,edge_key],'bx',c=[random.random(),random.random(),random.random()],markersize=20)
        
        # *** end key assignation ***
         
        edge_key = edge_key + 1

        #plt.show()
        
    # Create .dat files
    
    fm = file(''.join([os.path.join(data_path,NETWORK_NAME),'_','f_e_minus.dat']),'wb')
    save(fm,arrayOf_f_e_minus)
    fm.close()
    
    fz = file(''.join([os.path.join(data_path,NETWORK_NAME),'_','z_e.dat']),'wb')
    save(fz,arrayOf_Queues)
    fz.close()
        
    # Save graph
    
    output_gml_file_path = os.path.abspath(os.path.join(data_path,NETWORK_NAME+'.gml'))
    nx.write_gml(G,output_gml_file_path)
    
    return None

def check_empty_entries(arg_lst):
    
    valid_entries       = True
    entry_filename      = arg_lst[0]
    entry_network_name  = arg_lst[1]
    entry_call_flag     = arg_lst[2]
    
    if (entry_network_name == ''):
        valid_entries = False
        print '[MSG] Required network name'
    
    return valid_entries    

def appendAndGetRequiredPaths(callFromUpdate,NETWORK_NAME):
    
    if (callFromUpdate == '1'):
        network_path        = os.path.abspath(os.path.join('.','projects',NETWORK_NAME))
        lib_path            = os.path.abspath(os.path.join('.','lib'))
    else:
        network_path        = os.path.abspath(os.path.join('..','..','projects',NETWORK_NAME))
        lib_path            = os.path.abspath(os.path.join('..','..','lib'))

    sys.path.append(network_path)
    sys.path.append(lib_path)

    return network_path

if __name__ == "__main__":

    entry_filename      = ''
    entry_network_name  = ''
    entry_call_flag     = ''
    arg_lst             = [entry_filename,entry_network_name,entry_call_flag]
    
    c = 0
    for arg in sys.argv:
        arg_lst[c] = sys.argv[c]
        c = c + 1
    
    valid_entries = check_empty_entries(arg_lst)
    
    if (valid_entries == True):
        
        NETWORK_NAME    = str(arg_lst[1])
        callFromUpdate  = str(arg_lst[2])
        
        network_path    = appendAndGetRequiredPaths(callFromUpdate,NETWORK_NAME)

        try:
            
            tstart = time.time()
            
            import settings as ns
            
            data_path       = os.path.abspath(os.path.join(network_path,'data'))
            
            G               = nx.read_gml(os.path.abspath(os.path.join(data_path,NETWORK_NAME+'.gml')))
            G               = nx.MultiDiGraph(G)
            
            T_MAX           = ns.T_MAX_VIS
            TIME_STEP       = ns.TIME_STEP
            
            if (len(G.nodes())) > 0:
                
                # CREATE VISUALIZATION DATA FILES
                        
                try:
                
                    print "Creating data files ... [This might take several minutes]"
                
                    genDataFiles(G,TIME_STEP,T_MAX,NETWORK_NAME,data_path)
                    
                    print '>> Available "'+NETWORK_NAME+'" network .dat files'
                    
                except:
                
                    print (sys.exc_info())
                    print "[MSG] gen.py -data error"
            
            else:
          
                print "[MSG] Empty graph for the network"            
                
            rtime = time.time() - tstart
            
            print '>> Time: '+str(rtime)+' [s]'
                
        except:
            
            print (sys.exc_info())
            print '[MSG] gen.py - import error'
        







