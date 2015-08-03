"""
ADD LAYOUT DATA METHOD

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
        
        NETWORK_NAME                = str(arg_lst[1])
        callFromUpdate              = str(arg_lst[2])
        
        network_path    = appendAndGetRequiredPaths(callFromUpdate,NETWORK_NAME)

        try:
            
            try:

                import settings as ns
                import lib.layouts.gviz as gviz_layouts
                import lib.layouts.geometry as gvtk
                
                graph_data      = ns.network_graph_data()
                data_path       = os.path.abspath(os.path.join(network_path,'data'))
                rsc_path        = os.path.abspath(os.path.join(network_path,'rsc'))
                
                TIME_STEP       = ns.TIME_STEP

            except:
                
                print '[MSG] set.py : Import modules error.'

            try:

                try:
                    network_gml_file_path = os.path.join(data_path,NETWORK_NAME+'.gml')     
                    
                    G = nx.read_gml(network_gml_file_path)
                    G = nx.MultiDiGraph(G)
                        
                except:

                    print '[MSG] set.py : Graph data not found. Build update needed. [~$ python update.py '+NETWORK_NAME+ ' -b ] '
                
                custom_layout = ns.CUSTOM_LAYOUT
                
                print "Loading layout data ..."
                
                tstart  = time.time()
                
                if (custom_layout == 1):
                    
                    print "Loading custom layout ... (CUSTOM_LAYOUT = 1)"
                    
                    try: 
                        
                        G = ns.network_custom_layout(G)
                        ##########
                        # Process geometry for VTK
                        G = gvtk.tracerFilter(G,TIME_STEP)
                        ##########                        
                        nx.write_gml(G,network_gml_file_path)
                        
                        print '>> Available "'+NETWORK_NAME+'" layout data'
                    
                    except:
                        
                        print (sys.exc_info())
                        print '[MSG] set.py - layout'
    
                else:
                    
                    print "Loading default layout ... (CUSTOM_LAYOUT = 0)"
                    
                    try:
                         
                        A = nx.to_agraph(G)
                        
                        if (G.number_of_nodes() <= 50):
                            graphviz_prog = 'dot'
                            graphviz_args = '-Nshape=circle -Granksep=3.0 -Grankdir=LR'
                        else:
                            graphviz_prog = 'sfdp'
                            graphviz_args = '-Goverlap=prism'
                            
                        gviz_file_path = os.path.abspath(os.path.join(rsc_path,'gviz',NETWORK_NAME+'.txt'))
                        A.draw(gviz_file_path,format='plain', prog = graphviz_prog, args=graphviz_args)
                        #A.draw(gviz_file_path.replace('.','')+'.png',format='png', prog = graphviz_prog, args=graphviz_args)
                        gviz_layouts.addGeometryFromGVizFile(G,gviz_file_path)
                        ##########
                        # Process geometry for VTK
                        G = gvtk.tracerFilter(G,TIME_STEP)
                        ##########
                        nx.write_gml(G,network_gml_file_path)
                        
                    except:
                        
                        print '[MSG] set.py - layout'

                rtime = time.time() - tstart
                
                print '>> Time: '+str(rtime)+' [s]'

            except:
                
                print '[MSG] set.py : Error '

        except:
            
            print (sys.exc_info())
            print '[MSG] set.py - Folder Flows/test || network.py : import error'
            
            
            
            
            
            
            