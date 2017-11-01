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
import networkx as nx
import matplotlib.pyplot as plt
import random
import flows

def generate_graph(d,n,graph_file):
    H=nx.random_graphs.random_regular_graph(d,n)

    l = list( nx.simple_paths.all_simple_paths(H,H.nodes()[0],H.nodes()[-1], cutoff=2))

    #print(l)

    for path in list(l):
        if (len(path)==2):
            H.remove_edge(path[0],path[1])
        if (len(path)>=2):
            for i in range(1,len(path)-1):
                print path[i]
                try:
                    H.remove_node(path[i])
                except:
                    print('node was already')

    G=nx.MultiDiGraph(H)

    for e in G.in_edges(0,keys=True):
        G.remove_edge(*e)

    for e in G.edges(keys=True):
        G[e[0]][e[1]][e[2]]['time']=random.randint(1,30)*0.1
        G[e[0]][e[1]][e[2]]['capacity']=random.randint(1,30)*0.1

    if (len(list(nx.connected_components(nx.MultiGraph(G))))==1):
        nx.write_gml(G, graph_file)

    #plt.figure()
    #plt.ion()
    #nx.draw_networkx(G)
    #flows.display_graph(G)
    #plt.show()


