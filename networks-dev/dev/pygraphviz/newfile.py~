"""

GRAPHVIZ LAYOUT

plain text output

- Types of statements:

graph    scale width height
node     name x y width height label style shape color fillcolor
edge     tail head n x1 y1 ... xn yn [label x1 y1] style color
stop

"""

import os, sys
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)


import networkx as nx
from numpy import *

import pylab as plt


#NETWORK_NAME = "Larre"
#network_gml_file_path = os.path.abspath(os.path.join(dir_path,'..','..','projects',NETWORK_NAME,'data',NETWORK_NAME+'.gml'))   

#NETWORK_NAME = "Fig1_Cominetti"
#G=nx.MultiDiGraph()
#G.add_nodes_from("srt")
#G.node['s']['label'] = 0
#G.node['r']['label'] = 0
#G.node['t']['label'] = 0
#G.add_edge('s','r',time= 1, capacity=1.0, flow =0)
#G.add_edge('r','t',time= 2, capacity=1.0, flow =0)
#G.add_edge('r','t',time= 1, capacity=1.0/2.0, flow =0)

NETWORK_NAME = "G_d4_n400_gen"
network_gml_file_path = os.path.abspath(os.path.join(dir_path,'..','..','..','Flows','graphs',NETWORK_NAME+'.gml'))    
G = nx.read_gml(network_gml_file_path)


A = nx.to_agraph(G)
graphviz_prog = 'sfdp'
#graphviz_args = '-Gnodesep=0.5 -Granksep=0.75 -Grankdir=LR -Gsplines=ortho -Goverlap=prism -Nshape=box'
#graphviz_args = '-Gnodesep=1.0 -Granksep=1 -Grankdir=LR -Nshape=circle -Goverlap=voronoi'
#graphviz_args = '-Goverlap=prism'
#graphviz_args = '-Gmode=KK -Granksep=10 -Goverlap=prism'
graphviz_args = '-Granksep=15 -Goverlap=prism'
A.draw(NETWORK_NAME+'.txt',format='plain', prog = graphviz_prog, args = graphviz_args)
A.draw(NETWORK_NAME+'.png',format='png', prog = graphviz_prog, args = graphviz_args)


