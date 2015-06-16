'''

 Inria Chile - Flows In Networks
 
 Dynamic flow visualization

 * User Parameters 

- Comments :

* Graphs data can be found in the original folder /Flows/examples.py
* Note: "example1" is not considered in the list (no time data)
* This version can execute the file "test.py" in the original folder Flows and get the required data for the visualization
(enabled changes on T_MAX and TIME_STEP)

'''

#graph = 'example2'
#graph = 'example3'
#graph = 'example4'
#graph = 'example5'
#graph = 'example_KochSkutella2011_Fig3_Fig4'
#graph = 'example_simple1'
#graph = 'example_Fig1_Cominetti' # (visualization demo available)
#graph = 'example_Fig1_Cominetti_variant1'
#graph = 'example_Larre' # (visualization demo available)
#graph = 'example_Larre_bis'
#graph = 'example_parallelpath'
#graph = 'custom_graph'
graph  = 'example_doubleparallelpath' 

#graph = 'example_map_Tobalaba' # (map data available - work in progress)


##############################

NETWORK_GRAPH   = graph
T_MAX           = 25.0
TIME_STEP       = 0.1
FPS             = 25

ADD_DUMMY_SOURCE_NODE       = 0 # 0 or 1 [ on evaluation / for now, no changes if ADD_DUMMY_SOURCE_NODE = 1 ] 
PRIORITY_GRAPHVIZ_LAYOUT    = 1 # 0 or 1
INTERACTOR_STYLE            = 'StyleImage' # 'StyleImage' or 'RubberBand3D'
#INTERACTOR_STYLE            = 'RubberBand3D'

##############################
