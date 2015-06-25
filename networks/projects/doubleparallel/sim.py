"""
SIMULATION DATA

"""

import os, sys
import network as nw
import networkx as nx
lib_path = os.path.abspath(os.path.join('..','..'))
lib_path_flows = os.path.abspath(os.path.join('..','..','..'))
sys.path.append(lib_path)
sys.path.append(lib_path_flows)

import Flows.test as ftest
if __name__ == "__main__":

    print nw.NETWORK_NAME 

    graph_data = nw.network_graph_data()
    data_path = os.path.abspath(os.path.join('data')) 
    G = graph_data[0]
    node_src = graph_data[1] 
    node_sink = graph_data[2] 
    TIME_OF_EVENT = nw.TIME_OF_EVENT 
    INPUT_FLOW = nw.INPUT_FLOW 

    try:
        if len(G.nodes()) > 0:


            VDATA_T_MAX = max(nw.T_MAX_VIS,1E-12)
            VDATA_TIME_STEP = max(nw.TIME_STEP,1E-12)
            VDATA_NGRAPH = str(nw.NETWORK_NAME)
            VDATA_PATH = str(data_path)

            vpars = [True, VDATA_TIME_STEP,VDATA_T_MAX,VDATA_NGRAPH,VDATA_PATH]

            ftest.general_test(G,node_src,node_sink,TIME_OF_EVENT,INPUT_FLOW,vpars)

        else:

            print "[MSG] Empty graph for the network"

    except:
        print "[MSG] Simulation" 

