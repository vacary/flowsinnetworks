# flowsinnetworks is a program dedicated to modeling and simulation
# of dynamic equilibrium of flows in networks
#
# Copyright 2016 INRIA, INRIA Chile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# contact vincent.acary@inria.fr
#
# Network visualization layout

# Standard library imports
import os
import sys
import time

# Non standard library imports 
import networkx as nx

# Comment:
# Requires PROJECT_DIR_PATH

def check_empty_entries(arg_lst):
    
    valid_entries = True
    entry_filename = arg_lst[0]
    entry_network_name = arg_lst[1]
    entry_project_dir_path = arg_lst[2]
    
    if (entry_network_name == ''):
        valid_entries = False
        print '[MSG] Required network name'
    
    return valid_entries    

if __name__ == "__main__":

    """ Network visualization layout 
    
    Program to set the network visualization layout 
    (node positions and geometry for each edge)
    
    """

    entry_filename = ''
    entry_network_name = ''
    entry_project_dir_path = ''
    arg_lst = [entry_filename, entry_network_name, entry_project_dir_path]
    
    c = 0
    for arg in sys.argv:
        arg_lst[c] = sys.argv[c]
        c = c + 1
    
    valid_entries = check_empty_entries(arg_lst)
    
    if (valid_entries == True):
        
        NETWORK_NAME   = str(arg_lst[1])
        VROOT_DIR_PATH = vroot_dir_path # important!
        sys.path.append(PROJECT_DIR_PATH)

        try:
            
            try:

                import settings as ns
                import databuilder.layouts.utils.gviz as gviz_layouts # to be used when custom_layout = 0
                import databuilder.layouts.utils.geometry as gvtk
                
                data_path = os.path.join(PROJECT_DIR_PATH,'data')
                rsc_path = os.path.join(PROJECT_DIR_PATH,'rsc')
                
                TIME_STEP = ns.TIME_STEP

            except:
                
                print '[MSG] set.py : Import modules error.'

            try:

                try:
                    network_gml_file_path = os.path.join(data_path,NETWORK_NAME+'.gml')     
                    
                    G = nx.MultiDiGraph(nx.read_gml(network_gml_file_path))
                        
                except:

                    print '[MSG] set.py : Graph data not found. Build update needed. [~$ python update.py %s -b ] ' %( NETWORK_NAME )
                
                custom_layout = ns.CUSTOM_LAYOUT
                
                print "Loading layout data ..."
                
                tstart  = time.time()
                
                if (custom_layout == 1):
                    
                    # CUSTOM_LAYOUT = 1
                    
                    print "Loading custom layout ... (CUSTOM_LAYOUT = 1)"
                    
                    try: 
                        
                        ns.network_custom_layout(G)
                        ##########
                        # Process geometry for VTK
                        gvtk.tracerFilter(G, TIME_STEP)
                        ##########                        
                        nx.write_gml(G, network_gml_file_path)
                        
                        print '>> Available %s layout data' %( NETWORK_NAME )
                    
                    except:
                        
                        print (sys.exc_info())
                        print '[MSG] set.py - layout'
    
                else:
                    
                    # CUSTOM_LAYOUT = 0
                    
                    print "Loading default layout ... (CUSTOM_LAYOUT = 0)"
                    
                    try:
                         
                        A = nx.to_agraph(G)

                        if (G.number_of_nodes() <= 10):
                            graphviz_prog = 'dot'
                            graphviz_args = '-Grankdir=LR -Goverlap=prism'
                        else:
                            graphviz_prog = 'sfdp'
                            graphviz_args = '-Goverlap=prism'
                        
                        gviz_file_path = os.path.abspath(os.path.join(rsc_path, 'gviz', NETWORK_NAME+'.txt'))
                        A.draw(gviz_file_path, format='plain', prog=graphviz_prog, args=graphviz_args)
                        #A.draw(gviz_file_path.replace('.','')+'.png',format='png', prog = graphviz_prog, args=graphviz_args)
                        gviz_layouts.addGeometryFromGVizFile(G, gviz_file_path)
                        ##########
                        # Process geometry for VTK
                        gvtk.tracerFilter(G, TIME_STEP)
                        ##########
                        nx.write_gml(G, network_gml_file_path)
                        
                    except:
                        print (sys.exc_info())
                        print '[MSG] set.py - layout'

                rtime = time.time() - tstart
                
                print '>> Time: %s [s]' %( rtime )

            except:
                print (sys.exc_info())
                print '[MSG] set.py : Error '

        except:
            
            print (sys.exc_info())
            print '[MSG] set.py - Folder Flows/test || network.py : import error'
            
