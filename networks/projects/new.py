'''

Inria Chile - Flows In Networks

Program for new visualization environment

~$ python new.py name_visualization

'''
import os
import sys

def set_vis_content(file,vname):
    
    file.write('"""\n')
    file.write('NETWORK SETTINGS\n\n')
    file.write('"""\n\n')
    
    file.write('NETWORK_NAME = "'+str(vname)+'"\n')
    file.write('TYPE = "0" \n\n')
    file.write('TIME_OF_EVENT = [0.0,10.0,20.0]\n')
    file.write('INPUT_FLOW = [4.0,4.0] \n\n')
    file.write('TIME_STEP = 0.1 \n')
    file.write('T_MAX_VIS = 15 \n')
    file.write('FPS = 24 \n\n')
    file.write('PRIORITY_GRAPHVIZ_LAYOUT = 1\n\n')
    file.write('SIMULATION_DATA_AVAILABLE = 1\n\n')
 
    file.write('import os, sys\n')
    file.write('import networkx as nx\n')
    file.write("lib_path = os.path.abspath(os.path.join('..','..'))\n")
    file.write("lib_path_flows = os.path.abspath(os.path.join('..','..','..'))\n")
    file.write('sys.path.append(lib_path)\n')
    file.write('sys.path.append(lib_path_flows)\n')
    file.write('import lib.layouts as layouts\n')
    file.write('import Flows.examples as exa\n\n') 
    
    file.write('def network_graph_data():\n\n')
    file.write('    G = nx.MultiDiGraph()\n\n')
    file.write("    source = 's'\n")
    file.write("    sink = 't' \n\n")    
    file.write('    # { begin graph definition } [ Example: G = exa.example_Larre() ]\n\n\n\n')
    file.write('    # { end graph definition }\n\n')
    file.write('    if (TYPE == "0"):\n')
    file.write("        graphviz_layout = 'dot'\n")
    file.write('        layouts.addNodePositionsToGraph(G,TYPE,PRIORITY_GRAPHVIZ_LAYOUT, graphviz_layout)\n\n')
    file.write('    #else:\n')
    file.write('    #    { procedure to set node positions }\n\n')
    file.write('    return [G,source,sink]\n\n')
    
    return None
    
def set_gen_content(file):
    
    file.write('"""\n')
    file.write('SIMULATION DATA\n\n')
    file.write('"""\n\n')
    
    file.write('import os, sys\n')
    file.write('import network as nw\n')
    file.write('import networkx as nx\n')
    file.write("lib_path = os.path.abspath(os.path.join('..','..'))\n")
    file.write("lib_path_flows = os.path.abspath(os.path.join('..','..','..'))\n")
    file.write('sys.path.append(lib_path)\n')
    file.write('sys.path.append(lib_path_flows)\n\n')
    
    file.write('import Flows.test as ftest\n')
    
    file.write('if __name__ == "__main__":\n\n')
    file.write('    print nw.NETWORK_NAME \n\n')    
    file.write('    graph_data = nw.network_graph_data()\n')
    file.write("    data_path = os.path.abspath(os.path.join('data')) \n")
    file.write('    G = graph_data[0]\n')
    file.write('    node_src = graph_data[1] \n')
    file.write('    node_sink = graph_data[2] \n')
    file.write('    TIME_OF_EVENT = nw.TIME_OF_EVENT \n')
    file.write('    INPUT_FLOW = nw.INPUT_FLOW \n\n')
    file.write('    try:\n')
    file.write('        if len(G.nodes()) > 0:\n\n\n')
    file.write('            VDATA_T_MAX = max(nw.T_MAX_VIS,1E-12)\n')
    file.write('            VDATA_TIME_STEP = max(nw.TIME_STEP,1E-12)\n')
    file.write('            VDATA_NGRAPH = str(nw.NETWORK_NAME)\n')
    file.write('            VDATA_PATH = str(data_path)\n\n')
    file.write('            vpars = [True, VDATA_TIME_STEP,VDATA_T_MAX,VDATA_NGRAPH,VDATA_PATH]\n\n')
    file.write('            ftest.general_test(G,node_src,node_sink,TIME_OF_EVENT,INPUT_FLOW,vpars)\n\n')
    file.write('        else:\n\n')
    file.write('            print "[MSG] Empty graph for the network"\n\n')
    file.write('    except:\n')
    file.write('        print "[MSG] Simulation" \n\n')    
    
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
                os.makedirs(os.path.abspath(os.path.join(vname,'osm')))
                os.makedirs(os.path.abspath(os.path.join(vname,'map')))
                f = open(os.path.abspath(os.path.join(vname,'__init__.py')),'w')
                f.close()                
                f = open(os.path.abspath(os.path.join(vname,'network.py')),'w')
                set_vis_content(f,vname)
                f.close()
                f = open(os.path.abspath(os.path.join(vname,'sim.py')),'w')
                set_gen_content(f)
                f.close()
            
            else:
                
                print '[MSG] A folder with this name already exists.'
            
    except:
        print '[Error] Non-valid visualization name'
