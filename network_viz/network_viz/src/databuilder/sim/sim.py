#
# Network visualization source data generator

# Standard library imports
import os
import sys
import time

# Non standard library imports
import networkx as nx

# Comment:
# Requires ROOT_DIR_PATH (to call the simulation program)
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

def remove_non_reachable_G_nodes_from_source(G, source):

    reachablesFromSource = nx.descendants(G, source)
    nodesToRemove = []

    for node in G.nodes_iter():
        if (node not in reachablesFromSource):
            if (node != source):
                nodesToRemove.append(node)

    for node in nodesToRemove:
        G.remove_node(node)

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

        try:
            osm_geometry = data['osm_geometry']
        except:
            osm_geometry = '[]'

        H.add_edge(u, v,
                    time=time,
                    capacity=capacity,
                    switching_times=sw_time,
                    z_e_overtime=z_e_time,
                    f_e_plus_overtime=f_e_plus,
                    f_e_minus_overtime=f_e_minus,
                    geometry=geometry,
                    osm_geometry=osm_geometry,
                    name=name)

    return H

if __name__ == "__main__":

    """ Networks visualization source data generator

    This program creates a gml file with data provides by the simulation
    of the network dynamic flow according to the program available in 'Flows/flows.py'

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

        NETWORK_NAME = arg_lst[1]
        ROOT_DIR_PATH = root_dir_path # important! [to find the simulation program]
        sys.path.append(ROOT_DIR_PATH)
        sys.path.append(PROJECT_DIR_PATH)

        try:

            tstart = time.time()

            import Flows.test as ftest
            import settings as ns

            graph_data      = ns.network_graph_data()
            data_path       = os.path.join(PROJECT_DIR_PATH,'data')

            G               = nx.MultiDiGraph(graph_data[0])
            node_source     = graph_data[1]
            node_sink       = graph_data[2]
            TIME_OF_EVENT   = ns.TIME_OF_EVENT
            INPUT_FLOW      = ns.INPUT_FLOW

            remove_non_reachable_G_nodes_from_source(G, node_source) #important!

            if (len(G.nodes())) > 0:

                # CREATE SIMULATION DATA FILE

                try:

                    # Create graph file with simulation data

                    network_gml_file_path = os.path.abspath(os.path.join(data_path, ''.join((NETWORK_NAME,'.gml'))))

                    ###################

                    print "Running simulation ... [This might take several minutes]"

                    sys.stdout = open(os.devnull,"w") # to avoid print

                    ftest.general_test_dev(G, node_source, node_sink, TIME_OF_EVENT, INPUT_FLOW, network_gml_file_path) # add simulation data to graph

                    sys.stdout = sys.__stdout__

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
