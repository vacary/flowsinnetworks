
import os, sys
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

import networkx as nx
from numpy import *

#NETWORK_NAME = 'G3'
NETWORK_NAME = 'Larre'

#vsettings_path = os.path.join('.','projects',NETWORK_NAME)
vsettings_path = os.path.join('..','..','projects',NETWORK_NAME)
sys.path.append(vsettings_path)
print vsettings_path

import settings

print settings.NETWORK_NAME
print settings.TYPE

gdata = settings.network_graph_data()

G = gdata[0]

print G.nodes(data = True)