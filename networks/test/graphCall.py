
import os, sys
import networkx as nx

lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

import projects.Larre.network as nw

Z = nw.network_graph_data()

print Z[0].nodes()
print Z[0].edges()