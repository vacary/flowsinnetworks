"""
GRAPH WITH SIMULATION DATA GENERATOR

"""
import os, sys
import networkx as nx
import time

def check_empty_entries(arg_lst):
    
    valid_entries       = True
    entry_filename      = arg_lst[0]
    entry_network_name  = arg_lst[1]
    entry_call_flag     = arg_lst[2]
    
    if (entry_network_name == ''):
        valid_entries = False
        print '[MSG] Required network name'
    
    return valid_entries

def applyGraphFilter(G,node_source,node_sink):
    
    H = nx.MultiDiGraph()

    # node data
    
    for n in G.nodes_iter():
        H.add_node(n)
        H.node[n]['label_thin_flow_overtime'] = str(G.node[n]['label_thin_flow_overtime'])
        H.node[n]['label_overtime'] = str(G.node[n]['label_overtime'])
        H.node[n]['nlabel'] = str(n)

    # edges data
        
    for u,v,data in G.edges_iter(data=True):
                
        time        = data['time']
        capacity    = data['capacity']
        
        H.add_edge(u,v, time = time, capacity = capacity)

    return H

def appendAndGetRequiredPaths(callFromUpdate,NETWORK_NAME):
    
    if (callFromUpdate == '1'):
        lib_path_flows      = os.path.abspath(os.path.join('..'))
        lib_path            = os.path.abspath(os.path.join('.','lib'))
        network_path        = os.path.abspath(os.path.join('.','projects',NETWORK_NAME))
    else:
        lib_path_flows      = os.path.abspath(os.path.join('..','..','..'))
        lib_path            = os.path.abspath(os.path.join('..','..','lib'))
        network_path        = os.path.abspath(os.path.join('..','..','projects',NETWORK_NAME))
        
    sys.path.append(lib_path_flows)
    sys.path.append(lib_path)
    sys.path.append(network_path)

    return [lib_path_flows,network_path]

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
        
        NETWORK_NAME                = str(arg_lst[1])
        callFromUpdate              = str(arg_lst[2])
        
        flows_path, network_path    = appendAndGetRequiredPaths(callFromUpdate,NETWORK_NAME)

        try:
            
            tstart = time.time()
            
            import Flows.test as ftest
            import settings as ns
            import layouts.graph as graph_layouts
            
            graph_data      = ns.network_graph_data()
            data_path       = os.path.abspath(os.path.join(network_path,'data'))
            
            G               = graph_data[0]
            node_source     = graph_data[1]
            node_sink       = graph_data[2] 
            
            custom_layout   = ns.CUSTOM_LAYOUT
            
            TIME_OF_EVENT   = ns.TIME_OF_EVENT 
            INPUT_FLOW      = ns.INPUT_FLOW
            T_MAX           = ns.T_MAX_VIS 
            TIME_STEP       = ns.TIME_STEP
            
            if (len(G.nodes())) > 0:
                        
                # CREATE SIMULATION DATA FILES
                        
                try:
                    
                    VDATA_T_MAX = max(T_MAX,1E-12)
                    VDATA_TIME_STEP = max(TIME_STEP,1E-12)
                    VDATA_NGRAPH = str(ns.NETWORK_NAME)
                    VDATA_PATH = str(data_path)
          
                    vpars = [True, VDATA_TIME_STEP,VDATA_T_MAX,VDATA_NGRAPH,VDATA_PATH]
                
                    # Create graph file with simulation data    
                    
                    network_gml_file_path = os.path.abspath(os.path.join(data_path,NETWORK_NAME+'.gml'))
                
                    ###################
                    
                    print "Running simulation ... [This might take several minutes]"
                    
                    sys.stdout = open(os.devnull,"w") # to avoid print
                    
                    ftest.general_test_dev(G,node_source,node_sink,TIME_OF_EVENT,INPUT_FLOW,network_gml_file_path) # add simulation data to graph
                    
                    sys.stdout = sys.__stdout__

                    ###################
                    
                    G = applyGraphFilter(G,node_source,node_sink)
                    
                    nx.write_gml(G,network_gml_file_path)
                    
                    print '>> Available "'+NETWORK_NAME+'" network graph file'
                    
                except:
                
                    print (sys.exc_info())
                    print "[MSG] build.py - Simulation"
            
            else:
          
                print "[MSG] Empty graph for the network"            
                
            rtime = time.time() - tstart
            
            print '>> Time: '+str(rtime)+' [s]'
                
        except:
            
            print (sys.exc_info())
            print '[MSG] sim.py - Folder Flows/test || network.py : import error'
        
