'''

Inria Chile - Flows In Networks

Program for new visualization environment

~$ python new.py name_visualization

'''
import os
import sys

def set_vis_content(file,vname):
    
    file.write('"""\n')
    file.write('VISUALIZATION NETWORK SETTINGS\n\n')
    file.write('"""\n\n')

    file.write('import os, sys\n')
    file.write('path = os.path.abspath(__file__)\n')
    file.write('dir_path = os.path.dirname(path)\n\n')
    
    file.write('import networkx as nx\n')
    file.write('from numpy import *\n\n')
    
    file.write('# Parameters \n\n')
    file.write('NETWORK_NAME = "'+str(vname)+'"\n')
    file.write('TYPE = "network" \n\n')
    file.write('TIME_OF_EVENT = [0.0,10.0,20.0]\n')
    file.write('INPUT_FLOW = [4.0,4.0] \n\n')
    file.write('TIME_STEP = 0.1 \n')
    file.write('T_MAX_VIS = 15 \n')
    file.write('FPS = 24 \n\n')
    file.write('PRIORITY_GRAPHVIZ_LAYOUT = 1\n')
    file.write('SIMULATION_DATA_AVAILABLE = 1\n\n')
    file.write('CUSTOM_LAYOUT = 0\n\n')
     
    file.write('# Required modules / packages \n\n')

    file.write("# { begin required modules }\n\n")
    file.write("lib_path = os.path.abspath(os.path.join(dir_path,'..','..'))\n")
    file.write('sys.path.append(lib_path)\n')
    file.write('import lib.layouts.graph as graph_layouts \n\n')
    
    file.write("### Required instructions to get a network graph from Flows/examples.py  \n\n")
    file.write("lib_path_flows = os.path.abspath(os.path.join(dir_path,'..','..','..'))\n")
    file.write('sys.path.append(lib_path_flows)\n')
    file.write('import Flows.examples as exa\n\n')
    file.write("# { end required modules }\n\n")
    
    file.write('def network_graph_data():\n\n')
    file.write('    G = nx.MultiDiGraph()\n\n')
    file.write("    source = 's'\n")
    file.write("    sink = 't' \n\n")    
    file.write('    # { begin graph definition } [ Example: G = exa.example_Larre() ]\n\n\n\n')
    file.write('    # { end graph definition }\n\n')
    file.write('    return [G,source,sink]\n\n')

    file.write('def network_custom_layout(G):\n\n')
    file.write('    # This method is applied only if CUSTOM_LAYOUT = 1 \n\n')
    file.write('    # Must return the input graph G with positions for each node with the format: \n')
    file.write('    # pos = "[p[0],p[1],0.0]" \n\n')
    file.write('    # { begin custom layout method } \n\n')
    
    file.write('    # Example: \n')
    file.write('    # graphviz_layout = "circo" \n')
    file.write('    # graph_layouts.addNodePositionsToGraph(G,PRIORITY_GRAPHVIZ_LAYOUT,graphviz_layout) \n\n')
    file.write('    # { end custom layout method }\n\n')
    file.write('    return G \n\n')
    
    return None
    
def set_map_bounds(file):
    
    file.write('"""\n')
    file.write('Map crop bounds \n\n')
    file.write('"""\n\n')
    file.write('W = 0.0\n')
    file.write('S = 0.0\n')
    file.write('E = 0.0\n')
    file.write('N = 0.0\n')
    
    return None

if __name__ == "__main__":
    
    try: 
        vname = str(sys.argv[1])
        
        if (vname == ''):
            print '[MSG] Empty name'
        else:
            
            new_main_path = os.path.abspath(os.path.join(vname))
            
            if not os.path.exists(new_main_path):
                
                # Create files and folders
                os.makedirs(new_main_path)
                os.makedirs(os.path.abspath(os.path.join(vname,'data')))
                os.makedirs(os.path.abspath(os.path.join(vname,'rsc')))
                os.makedirs(os.path.abspath(os.path.join(vname,'rsc','map')))
                os.makedirs(os.path.abspath(os.path.join(vname,'rsc','osm')))
                os.makedirs(os.path.abspath(os.path.join(vname,'rsc','gviz')))
                f = open(os.path.abspath(os.path.join(vname,'rsc','map','bounds.py')),'w')
                set_map_bounds(f)
                f.close()         
                f = open(os.path.abspath(os.path.join(vname,'__init__.py')),'w')
                f.close()                
                f = open(os.path.abspath(os.path.join(vname,'settings.py')),'w')
                set_vis_content(f,vname)
                f.close()
            
            else:
                
                print '[MSG] A folder with this name already exists.'
            
    except:
        
        print '[Error] Non-valid visualization name'


