'''

 Inria Chile - Flows In Networks
 
 Dynamic flow visualization

 * User Parameters 

- Comments :

* The following graphs can be displayed by the visualization program
* Graphs data can be found in /sim/Flows/examples.py  
* Currently, only one visualization demo is available for "example_Larre"
* Note: "example1" is not considered in the list (no time data)

'''

#graph = 'example2'
#graph = 'example3'
#graph = 'example4'
#graph = 'example5'
#graph = 'example_KochSkutella2011_Fig3_Fig4'
#graph = 'example_simple1'
#graph = 'example_Fig1_Cominetti'
#graph = 'example_Fig1_Cominetti_variant1'
graph = 'example_Larre'
#graph = 'example_Larre_bis'
#graph = 'example_parallelpath'

#graph = 'custom_graph'

##############################

NETWORK_GRAPH   = graph
T_MAX           = 25.0
TIME_STEP       = 0.1
FPS             = 25

ADD_DUMMY_SOURCE_NODE       = 0 # 0 or 1
PRIORITY_GRAPHVIZ_LAYOUT    = 1 # 0 or 1
INTERACTOR_STYLE            = 'StyleImage' # 'StyleImage' or 'RubberBand3D'
#INTERACTOR_STYLE            = 'RubberBand3D'

##############################
