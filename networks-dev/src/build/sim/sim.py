#
# Network visualization source data generator

# Standard library imports
import os
import sys
import time

# Non standard library imports
import networkx as nx

def check_empty_entries(arg_lst):
    
    valid_entries       = True
    entry_filename      = arg_lst[0]
    entry_network_name  = arg_lst[1]
    entry_call_flag     = arg_lst[2]
    
    if (entry_network_name == ''):
        valid_entries = False
        print '[MSG] Required network name'
    
    return valid_entries

def graphFilter(G,node_source,node_sink):
    
    H = nx.MultiDiGraph()

    # node data
    
    for n in G.nodes_iter():
        H.add_node(n)
        H.node[n]['label_thin_flow_overtime'] = str(G.node[n]['label_thin_flow_overtime'])
        H.node[n]['label_overtime'] = str(G.node[n]['label_overtime'])
        H.node[n]['nlabel'] = str(n)
        
        try:
            H.node[n]['pos'] = str(G.node[n]['pos'])
        except:
            H.node[n]['pos'] = '' 
            
    # edges data
        
    for u,v,data in G.edges_iter(data=True):
                
        time        = data['time']
        capacity    = data['capacity']
        
        sw_time     = str(data['switching_times'])
        z_e_time    = str(data['z_e_overtime'])
        f_e_plus    = str(data['f_e_plus_overtime'])
        f_e_minus   = str(data['f_e_minus_overtime'])
        
        try: 
            geometry = str(data['geometry'])
        except:
            geometry = '[]'
        
        try:
            name = data['name']
        except:
            name = '[]'
                
        H.add_edge(u,v, time = time, capacity = capacity, switching_times = sw_time, z_e_overtime = z_e_time, f_e_plus_overtime = f_e_plus, f_e_minus_overtime = f_e_minus, geometry=geometry, name=name)

    return H

def appendAndGetRequiredPaths(callFromUpdate,NETWORK_NAME):
    
    if (callFromUpdate == '1'):
        dir_path_root = os.path.abspath(os.path.join('..'))
        network_path = os.path.abspath(os.path.join('.','projects',NETWORK_NAME))
    else:
        dir_path_root = os.path.abspath(os.path.join('..','..','..'))
        network_path = os.path.abspath(os.path.join('..','..','projects',NETWORK_NAME))
        
    sys.path.append(dir_path_root)
    sys.path.append(network_path)

    return network_path

if __name__ == "__main__":
    
    """ Networks visualization source data generator
    
    This program creates a gml file with data provides by the simulation
    of the network dynamic flow according to the program available in 'Flows/flows.py'
    
    """

    entry_filename      = ''
    entry_network_name  = ''
    entry_call_flag     = ''
    arg_lst             = [entry_filename, entry_network_name, entry_call_flag]
    
    c = 0
    for arg in sys.argv:
        arg_lst[c] = sys.argv[c]
        c = c + 1
    
    valid_entries = check_empty_entries(arg_lst)
    
    if (valid_entries == True):
        
        NETWORK_NAME = str(arg_lst[1])
        callFromUpdate = str(arg_lst[2])
        
        network_path = appendAndGetRequiredPaths(callFromUpdate, NETWORK_NAME) # important for library imports!

        try:
            
            tstart = time.time()
            
            import Flows.test as ftest
            import settings as ns
            
            graph_data      = ns.network_graph_data()
            data_path       = os.path.abspath(os.path.join(network_path,'data'))
            
            G               = graph_data[0]
            node_source     = graph_data[1]
            node_sink       = graph_data[2]
            TIME_OF_EVENT   = ns.TIME_OF_EVENT
            INPUT_FLOW      = ns.INPUT_FLOW
            
            if (len(G.nodes())) > 0:
                        
                # CREATE SIMULATION DATA FILE
                        
                try:
                                    
                    # Create graph file with simulation data    
                    
                    network_gml_file_path = os.path.abspath(os.path.join(data_path, NETWORK_NAME+'.gml'))
                
                    ###################
                    
                    print "Running simulation ... [This might take several minutes]"
                    
                    #sys.stdout = open(os.devnull,"w") # to avoid print
                    
                    ftest.general_test_dev(G, node_source, node_sink, TIME_OF_EVENT, INPUT_FLOW, network_gml_file_path) # add simulation data to graph
                    
                    #sys.stdout = sys.__stdout__

                    ###################
                    
                    G = graphFilter(G,node_source,node_sink)
                    
                    nx.write_gml(G, network_gml_file_path)
                    
                    print '>> Available %s network graph file' %( NETWORK_NAME )
                    
                except:
                
                    print (sys.exc_info())
                    print "[MSG] build.py - Simulation"
            
            else:
          
                print "[MSG] Empty graph for the network"            
                
            rtime = time.time() - tstart
            
            print '>> Time: %f [s]' %( rtime )
                
        except:
            
            print (sys.exc_info())
            print '[MSG] sim.py - Folder Flows/test || network.py : import error'
        
