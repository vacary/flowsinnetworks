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

from __future__ import print_function

try:
    reload(flows)
except:
    import flows

try:
    reload(decomposition)
except:
    import decomposition


import networkx as nx

###############################################################
# About new lines of code for visualization
#
# - added 'pars' variable for selected test functions, for instance 'def test15()'--> 'def test15(pars)'
# - added [] list in calls for selected test functions, for instance 'test15()' --> 'test15([])'
# - added "try / except" lines in the definition of selected functions
# - ./vdata/manage.py : file with functions to generate visualization data

import vdata.manage as vdata # (for visualization)
###############################################################

import matplotlib.pyplot as plt


try:
    reload(examples)
except:
    import examples

import math

def general_test_dev(G,node_src,node_sink,TIME_OF_EVENT,INPUT_FLOW,network_gml_file_path):

    #G=examples.example_Larre()

    source = node_src
    sink = node_sink

    timeofevent = TIME_OF_EVENT
    inputflow = INPUT_FLOW

    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12

    param.nmax =500

    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param)
    print("timeofevent=",timeofevent)
    print("inputflow=",inputflow)

    with_draw=True
    if with_draw :
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)

    flows.postprocess_flows_queues_cumulativeflows(G)
    flows.display_graph(G)

    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows(G)

    if with_draw :
        plt.figure("Flows, Extra values", figsize = [8,10])
        flows.postprocess_extravalues(G, source, sink)
        flows.plot_extravalues(G)

    return None

def general_test(G,node_src,node_sink,TIME_OF_EVENT,INPUT_FLOW,vpars):

    #G=examples.example_Larre()

    source = node_src
    sink = node_sink

    timeofevent = TIME_OF_EVENT
    inputflow = INPUT_FLOW

    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12

    param.nmax =500

    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param)
    print("timeofevent=",timeofevent)
    print("inputflow=",inputflow)

    with_draw=True
    if with_draw :
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)

    flows.postprocess_flows_queues_cumulativeflows(G)
    flows.display_graph(G)

    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows(G)

    if with_draw :
        plt.figure("Flows, Extra values", figsize = [8,10])
        flows.postprocess_extravalues(G, source, sink)
        flows.plot_extravalues(G)

    try:
        if (vpars[0] == True):
            vdata.genVData2(G,vpars[1],vpars[2],vpars[3],vpars[4])
    except:
        import sys
        print(sys.exc_info())
        print('[ MSG ] test.py ')

    return None


def test1():
    print( '################ start test1 ###############')
    G=nx.path_graph(5)
    flows.display_graph(G)
    print((nx.dijkstra_path(G,0,4)))
    length,path=nx.single_source_dijkstra(G,0)
    print( length)
    print( path)
    print( '################ start test1 ###############')


def test2():
    G= examples.example1()
    flows.display_graph(G)
    print((nx.dijkstra_path(G,'s','t')))

    length,path=nx.single_source_dijkstra(G,'s','t')

    print( 'path=',path)
    print( 'length=',length)
    print( 'The path', path['t'], 'is the shortest path from s to t of length',length['t'] )
    print( '################ end test2 ###############')


def test3():
    print( '################ start test3 ###############')
    G= examples.example2()
    flows.display_graph(G)
    print((nx.dijkstra_path(G,'s','t', weight='time')))
    length,path=nx.single_source_dijkstra(G,'s','t', weight='time')

    print( 'path=',path)
    print( 'length=',length)
    print( 'The path', path['t'], 'is the shortest path from s to t of length',length['t'] )
    print( '################ end test3 ###############')




def test4():
    print( '################ start test4 ###############')
    G=examples.example2()
    print( "G :")
    flows.display_graph(G)
    print( 'cycles in G =', list(nx.simple_cycles(G)))
    E,Estar,E_comp=flows.current_shortest_path_graph(G)
    print( "E :")
    flows.display_graph(E)
    print( "E_comp :")
    flows.display_graph(E_comp)

    print( "Estar :")
    flows.display_graph(Estar)

    print( 'cycles in E =', list(nx.simple_cycles(E)))


    with_draw=False
    if with_draw :
        Gpos=nx.pydot_layout(G)
        nx.draw_graphviz(G,pos=Gpos,node_color='#A0CBE2', with_labels=True, with_edge_labels=True)
        #nx.draw_graphviz(G,node_color='#A0CBE2', with_labels=True, with_edge_labels=True)
        #labels=nx.draw_networkx_labels(G,pos=nx.pydot_layout(G))

        newpos=dict(Gpos)
        print( newpos)

        def func(x):
            #print( x)
            #print( 'x[1][0]=',x[1][0]
            return float(x[1][0] )

        xmax =   func(max(newpos.items(),key=func)   )
        xmin =   func(min(newpos.items(),key=func)   )

        for n,npos in newpos.items():
            newpos[n] = (npos[0]+(xmax-xmin)*1.1,) + npos[1:]

        nx.draw(E,pos=newpos,node_color='#A0CBE2', with_labels=True)
        labels=nx.draw_networkx_edge_labels(E,pos=newpos)

        labels=nx.draw_networkx_edge_labels(G,pos=Gpos)

        #nx.draw_shell(G)#,pos=nx.pydot_layout(G))
        #labels=nx.draw_networkx_labels(G,pos=nx.shell_layout(G))
        #nx.draw_circular(G)#,pos=nx.pydot_layout(G))
        #labels=nx.draw_networkx_labels(G,pos=nx.circular_layout(G))

        plt.draw()
        plt.show()

    print( '################ end test4 ###############')

def test5():
    print( '################ start test5 ###############')
    G=examples.example2()
    flows.congestion_labels(G,'s')
    flows.display_graph(G)
    print( '################ end test5 ###############')

def test5_pathmethod():
    print( '################ start test5 ###############')
    G=examples.example2()
    flows.congestion_labels_pathmethod(G,'s')
    flows.display_graph(G)
    print( '################ end test5 ###############')


def test6():
    print( '################ start test6 ###############')
    G=examples.example3()
    #display_graph(G)

    b= {} # dictionary of flows in nodes
    b['s'] = 9
    b['v'] = 0
    b['w'] = 0
    b['t'] = -9

    congestion,cut,comp_cup = flows.sparsest_cut(G,b,'s')

    print( 'congestion= ', congestion)
    print( 'sparset cut= ', cut)

    print( '################ end test6 ###############'    )


def test7():
    print( '################ start test7 ###############')
    G=examples.example4()
    flows.display_graph(G)

    b= {} # dictionary of flows in nodes
    b['s'] = 9
    b['v'] = 0
    b['w'] = 0
    b['t'] = -9

    congestion,cut,comp_cut = flows.sparsest_cut(G,b,'s')

    print( 'congestion= ', congestion)
    print( 'sparset cut= ', cut)

    print( '################ end test7 ###############'    )

def test8():
    print( '################ start test8 ###############')
    G=examples.example5()
    flows.display_graph(G)

    value,X = flows.maxflow_mincut_by_lp(G,'s','t')
    print( 'Max Flow value= ', value)
    print( 'Min cut= ', X)
    print( '################ end test8 ###############'    )




def test9():
    print( '################ start test 9 ###############')
    G=examples.example3()
    #display_graph(G)

    b= {} # dictionary of flows in nodes
    b['s'] = 9.0
    b['v'] = 0
    b['w'] = 0
    b['t'] = -9.0
    #compute_thin_flow_without_resetting(G,'s',b)
    flows.compute_thin_flow_without_resetting(G,'s',b,9)
    flows.congestion_labels(G,'s',flow='thin_flow')
    flows.display_graph(G)

    print( '################ end test 9 ###############'    )


def test10():
    print( '################ start test 10 ###############')
    G=examples.example_KochSkutella2011_Fig3_Fig4()
    #display_graph(G)

    b= {} # dictionary of flows in nodes
    b['s'] = 3.0
    b['v'] = 0
    b['w'] = 0
    b['t'] = -3.0
    #compute_thin_flow_without_resetting(G,'s',b)
    flows.compute_thin_flow_without_resetting(G,'s',b,3)
    flows.congestion_labels(G,'s',flow='thin_flow')
    flows.display_graph(G)

    print( '################ end test 10 ###############'  )

def test11():
    print( '################ start test 11 ###############')
    G=examples.example_KochSkutella2011_Fig3_Fig4()
    #display_graph(G)

    b= {} # dictionary of flows in nodes
    b['s'] = 3.0
    b['v'] = 0
    b['w'] = 0
    b['t'] = -3.0


    # resetting graph
    E1 = nx.MultiDiGraph()
    E1.add_edge('s','v')
    E1.add_edge('v','w')

    param=flows.parameters()
    param.tol_thin_flow=1e-08
    param.tol_lp=1e-08
    param.tol_cut=1e-09


    demand=3
    flows.compute_thin_flow(G,'s',b,E1,demand,param)

    flows.congestion_labels(G,'s',flow='thin_flow')
    flows.display_graph(G)
    flows.assert_thin_flow(G,'s',b,E1,3,param)

    print( '################ end test 11 ###############'  )


def test12():
    print( '################ start test 12 ###############')
    G=examples.example_simple1()
    #display_graph(G)

    b= {} # dictionary of flows in nodes
    b['s'] = 1.0
    b['v'] = 0
    b['t'] = -1.0

    # for e in G.edges():
    #     G[e[0]][e[1]]['thin_flow'] = -1.0
    # for n in G.nodes():
    #     G.node[n]['label']=-1.0

    # compute_thin_flow_without_resetting_withnonzerosourcelabel(G,'s',b,1)

    E1 = nx.MultiDiGraph()
    E1.add_edge('v','t')




    for e in G.edges(keys=True):
        G[e[0]][e[1]][e[2]]['thin_flow'] = -1.0
    for n in G.nodes():
        G.node[n]['label']=-1.0



    flows.compute_thin_flow(G,'s',b,E1,1)
    flows.congestion_labels(G,'s',flow='thin_flow')
    flows.display_graph(G)

    print( '################ end test 12 ###############'  )



    return G


def test13(pars):
    print( '################ start test 13 ###############')
    G=examples.example_Fig1_Cominetti()
    #G=examples.example_Fig1_Cominetti_variant1()


    source = 's'
    sink = 't'
    #Original values
    timeofevent=[0.0,1.0,2.0,20.0]
    inputflow=[2.0,0.0,1.0]

    # timeofevent=[0.0,1.0,2.0,6.0,10.0]
    # inputflow=[3.0,0.0,1.0,0.0]


    # timeofevent=[0.0,1.0,2.0,6.0,10.0]
    # inputflow=[3.0,0.0,3.0,0.0]

    #timeofevent=[0.0,1.0,2.0,3.0,4.0,5.0,7.0,8.0,15.0]
    #inputflow=[3.0,0.0,3.0,0.0,3.0,0.0,1.0,0.0]
    timeofevent=[0.0,1.0,2.0,3.0,10.0]
    inputflow=[0.9,0.9,0.9,0.9]


    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow)
    print("timeofevent=",timeofevent)
    print("inputflow=",inputflow)

    # plot floas and labels
    with_draw=True
    if with_draw :
        plt.ion()
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)


    # post processing
    flows.postprocess_flows_queues_cumulativeflows(G)
    flows.display_graph(G)

    plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
    flows.plot_flows_queues_cumulativeflows(G)

    plt.figure("Flows, Cumulative flows and queues for edge =('s','r'), key =0 ", figsize = [18,14])
    flows.plot_flows_queues_cumulativeflows(G,('s','r'),0)

    plt.figure("Flows, Cumulative flows and queues for edge =('r','t'), key =0 ", figsize = [18,14])
    flows.plot_flows_queues_cumulativeflows(G,('r','t'),0)
    plt.figure("Flows, Cumulative flows and queues for edge =('r','t'), key =1 ", figsize = [18,14])
    flows.plot_flows_queues_cumulativeflows(G,('r','t'),1)

    ###############################
    # for visualization
    #
    try:
        if (pars[0] == True):
            vdata.genVData(G,pars[1],pars[2],pars[3])
    except:
        #import sys
        #print(sys.exc_info())
        print('[ MSG ] test.py')
    #
    ###############################


    print( '################ end test 13 ###############')


def test14():
    print( '################ start test 14 ###############')

    G=examples.example_KochSkutella2011_Fig3_Fig4()
    source = 's'
    sink = 't'
    timeofevent=[0.0,20.0]
    inputflow=[3.0,3.0,3.0]


    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12



    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param)
    print("timeofevent=",timeofevent)
    print("inputflow=",inputflow)

    with_draw=True
    if with_draw :
        plt.ion()
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)


    flows.postprocess_flows_queues_cumulativeflows(G)
    flows.display_graph(G)


    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows(G)

    print( '################ end test 14 ###############')

def test15(pars):
    print( '################ start test 15 ###############')

    G=examples.example_Larre()
    source ='s'
    sink = 't'



    timeofevent=[0.0,0.5,1.5,20.0]
    inputflow=[4.0, 4.0 ,4.0,4.0]


    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12



    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param)
    print("timeofevent=",timeofevent)
    print("inputflow=",inputflow)

    with_draw=True
    if with_draw :
        plt.ion()
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)


    flows.postprocess_flows_queues_cumulativeflows(G)
    flows.display_graph(G)


    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows(G)

    if with_draw :
        plt.figure("Flows, Extra values", figsize = [8,10])
        flows.postprocess_extravalues(G, source, 't')
        flows.plot_extravalues(G)


    ###############################
    # for visualization
    #
    try:
        if (pars[0] == True):
            vdata.genVData(G,pars[1],pars[2],pars[3])
    except:
        #import sys
        #print(sys.exc_info())
        print('[ MSG ] test.py')
    #
    ###############################

    print( '################ end test 15 ###############')


def test16():
    print( '################ start test 16 ###############')

    G=examples.example_parallelpath()
    source = 's'
    sink = 't'
    timeofevent=[0.0,5.0]
    inputflow=[5.0, 5.0]


    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12



    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param)
    print("timeofevent=",timeofevent)
    print("inputflow=",inputflow)

    with_draw=True
    if with_draw :
        plt.ion()
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)


    flows.postprocess_flows_queues_cumulativeflows(G)
    flows.display_graph(G)


    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows(G)

    print( '################ end test 16 ###############')


def test17():
    print( '################ start test 17 ###############')

    G=examples.example_Larre_bis()
    source = 's'
    sink = 't'
    l=decomposition.build_inputflow(decomposition.g,0,3,0.3)

    timeofevent=l[0]
    inputflow=l[1]

    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12



    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param)
    print("timeofevent=",timeofevent)
    print("inputflow=",inputflow)

    with_draw=True
    if with_draw :
        plt.ion()
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)


    flows.postprocess_flows_queues_cumulativeflows(G)
    flows.display_graph(G)


    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows(G)

    print( '################ end test 17 ###############')



def flow_input_function_Fig1_Cominetti(t):
    input_flow=0.0
    if t <= 1 :
        input_flow=2.0
    if t>=2 :
        input_flow=1.0
    return input_flow




def test_TS1():
    print( '################ start test 18 ###############')

    G=examples.example_Larre_bis()
    G=examples.example_Larre()
    G=examples.example_Fig1_Cominetti()
    source = 's'
    sink = 't'
    # l=decomposition.build_inputflow(decomposition.g,0,3,0.3)

    # timeofevent=l[0]
    # inputflow=l[1]

    t0=0.0
    N=100
    h=0.1

    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12

    flows.compute_dynamic_equilibrium_timestepping(G, source, sink, h, t0, N, flow_input_function_Fig1_Cominetti,param)

    timesteps=[]
    for i in range(N+1):
        timesteps.append(t0+i*h)

    #print("timesteps=",timesteps)


    with_draw=True
    if with_draw :
        plt.ion()
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timesteps)

    flows.postprocess_flows_queues_cumulativeflows_timestepping(G,timesteps)
    #flows.display_graph(G)


    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows_timestepping(G,timesteps)

    print( '################ end test 18 ###############')

def flow_input_function(t):
    return 4.0
    #return abs(math.sin(t))

def test_TS2():
    print( '################ start test 19 ###############')

    G=examples.example_Larre_bis()
    G=examples.example_Larre()
    source = 's'
    sink ='t'

    # l=decomposition.build_inputflow(decomposition.g,0,3,0.3)

    # timeofevent=l[0]
    # inputflow=l[1]

    t0=0.0
    N=400
    h=0.01

    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12

    flows.compute_dynamic_equilibrium_timestepping(G, source, sink, h, t0, N, flow_input_function,param)

    timesteps=[]
    for i in range(N+1):
        timesteps.append(t0+i*h)

    #print("timesteps=",timesteps)


    with_draw=True
    if with_draw :
        plt.ion()
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timesteps)

    flows.postprocess_flows_queues_cumulativeflows_timestepping(G,timesteps)
    #flows.display_graph(G)


    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows_timestepping(G,timesteps)

    print( '################ end test 19 ###############')

def test21(pars):
    print( '################ start test 21 ###############')

    G=examples.example_doubleparallelpath()
    source = 's'
    sink ='t'

    timeofevent=[0.0,20.0]
    inputflow=[3.7]


    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12



    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param)
    print("timeofevent=",timeofevent)
    print("inputflow=",inputflow)

    with_draw=True
    if with_draw :
        plt.ion()
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)


    flows.postprocess_flows_queues_cumulativeflows(G)
    flows.display_graph(G)


    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows(G)

    if with_draw :
        plt.figure("Flows, Extra values", figsize = [8,10])
        flows.postprocess_extravalues(G, source, 't')
        flows.plot_extravalues(G)
    ###############################
    # for visualization
    #
    try:
        if (pars[0] == True):
            vdata.genVData(G,pars[1],pars[2],pars[3])
    except:
        #import sys
        #print(sys.exc_info())
        print('[ MSG ] test.py')
    #
    ###############################

    print( '################ end test 21 ###############')

def test22(pars):
    print( '################ start test 22 ###############')

    G=examples.example_bridge_one()
    source = 's'
    sink ='t'
    timeofevent=[0.0,6.0]
    inputflow=[4.0]


    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12



    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param)
    print("timeofevent=",timeofevent)
    print("inputflow=",inputflow)

    with_draw=True
    if with_draw :
        plt.ion()
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)


    flows.postprocess_flows_queues_cumulativeflows(G)
    flows.display_graph(G)


    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows(G)

    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows(G)


    if with_draw :
        plt.figure("Flows, Extra values", figsize = [8,10])
        flows.postprocess_extravalues(G, source, 't')
        flows.plot_extravalues(G)


    ###############################
    # for visualization
    #
    try:
        if (pars[0] == True):
            vdata.genVData(G,pars[1],pars[2],pars[3])
    except:
        #import sys
        #print(sys.exc_info())
        print('[ MSG ] test.py')
    #
    ###############################

    print( '################ end test 22 ###############')

def test_file(pars,graph_file,timeofevent=[0.0,100.0], inputflow=None, with_draw=False):
    print( '################ start test 23 ###############')

    

    G=nx.read_gml(graph_file)
    G=nx.MultiDiGraph(G)

    source = G.nodes()[0]
    sink = G.nodes()[-1]

    if inputflow == None:
        cut_value, X, Xbar = flows.compute_maxflow_mincut(G, source, sink)
        input_value= 0.99*cut_value
        inputflow=[input_value]
    
    #len(list(nx.connected_components(nx.MultiGraph(G))))==1
    #l = list( nx.simple_paths.all_simple_paths(G,0,17))
    #print(l)
    #raw_input()

    G.name= dict([])

    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12

    param.nmax =500

    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param)
    print("timeofevent=",timeofevent)
    print("inputflow[0]=",inputflow[0])

    if with_draw :
        plt.ion()
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)

    print("compute flows and queues ...")
    flows.postprocess_flows_queues_cumulativeflows(G)
    #flows.display_graph(G)


    if with_draw :
        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows(G)

    #print("compute extra values ...")
    #flows.postprocess_extravalues(G, source, sink)

    if with_draw :
        plt.figure("Flows, Extra values", figsize = [8,10])

        flows.plot_extravalues(G)

    print("compute der_phi ...")

    flows.postprocess_extravalues_der_phi(G, source, sink, inputflow)

    ###############################
    # for visualization
    #
    try:
        if (pars[0] == True):
            vdata.genVData(G,pars[1],pars[2],pars[3])
    except:
        #import sys
        #print(sys.exc_info())
        print('[ MSG ] test.py')
    #
    ###############################

    #G.name['isF_Xbar_minus_increasing']=flows.isF_Xbar_minus_increasing(G, param.tol_thin_flow)
    #G.name['isF_Xbar_minus_inE_increasing']=flows.isF_Xbar_minus_inE_increasing(G, param.tol_thin_flow)
    #G.name['isF_sink_minus_increasing']=flows.isF_sink_minus_increasing(G, param.tol_thin_flow)
    #G.name['isTotalTravelTime_increasing']= flows.is_TotalTravelTime_increasing(G,param.tol_thin_flow,source,sink)
    #G.name['isDerTotalTravelTime_decreasing']= flows.is_DerTotalTravelTime_decreasing(G,param.tol_thin_flow,source,sink)
    G.name['is_der_phi_positive']= flows.is_der_phi_positive(G,param.tol_thin_flow,source,sink)
    G.name['is_der_phi_decreasing']= flows.is_der_phi_decreasing(G,param.tol_thin_flow,source,sink)
    #raw_input()
    
    if False:
        # clean up useless edges to simplify
        G_simplified=nx.MultiDiGraph()
        G_simplified.add_nodes_from(G.nodes())
        print("original number of nodes", len(G.nodes()))
        print("original number of edges", len(G.edges()))


        #G_simplified.add_edges_from(G.edges(keys=True))
        for e in G.edges(keys=True):
            val_max =0.0
            for val in G[e[0]][e[1]][e[2]]['f_e_minus_overtime']:
                val_max = max(val,val_max)
            if val_max > 0.0:
                G_simplified.add_edge(*e)
                G_simplified[e[0]][e[1]][e[2]]['time']=G[e[0]][e[1]][e[2]]['time']
                G_simplified[e[0]][e[1]][e[2]]['capacity']=G[e[0]][e[1]][e[2]]['capacity']

        for n in G.nodes():
            if n!= source:
                if G_simplified.in_edges(n,keys=True) == []:
                    G_simplified.remove_node(n)
        import os
        nx.write_gml(G_simplified, os.path.splitext(graph_file)[0]+"_simplified.gml")
        print("simplified number of nodes", len(G_simplified.nodes()))
        print("simplified number of edges", len(G_simplified.edges()))



    return  G


    print( '################ end test 23 ###############')

def test24(pars):
    print( '################ start test 24 ###############')
    G=examples.example_roberto2()
    G=examples.example_robertoplus()
    timeofevent=[0.0,8.0]
    inputflow=[1.0,1.0]

    #G=examples.example_neil()
    #timeofevent=[0.0,172.0]
    #inputflow=[1.0,1.0]

    # G=examples.example_doubleparallelpath()
    # timeofevent=[0.0,15.0]
    # inputflow=[3.0,3.0]



    source = 's'
    sink = 't'
    #Original values
    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12

    param.nmax =500
    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param)
    print("timeofevent=",timeofevent)
    print("inputflow=",inputflow)



    # post processing
    flows.postprocess_flows_queues_cumulativeflows(G)



    u= {} # dictionary of flows in nodes
    for n in G.nodes():
        u[n] =0.0
    u[source] = inputflow[-1]
    u[sink] = - inputflow[-1]
    flows.display_graph(G)
    steady_cost, steady_thin_flow = flows.steady_state_thin_flow_lp(G, u, source, param.tol_lp)
    assert(flows.compare_steady_thin_flow(G, steady_thin_flow, param.tol_lp))
    print("steady_thin_flow by lp:",flows.drepr(steady_thin_flow))

    cost,queues,labels =flows.steady_state_queues_labels_lp(G,u,source,sink,param.tol_lp, offset=G.node[source]['label'])
    print("steady_labels by lp:",flows.drepr(labels))
    print("steady_queues by lp:",flows.drepr(queues))

    #assert(flows.compare_steady_queues_labels(G, queues, labels, param.tol_lp))



    flows.postprocess_extravalues(G, source, sink)
    #flows.display_graph(G)
    # plot floas and labels
    with_draw=True
    if with_draw :
        plt.ion()
        plt.close('all')
        
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)

        plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
        flows.plot_flows_queues_cumulativeflows(G)

        #plt.figure("Flows, Extra values", figsize = [8,10])
        #flows.plot_extravalues(G)
        flows.plot_label_vs_label(G)
        
        
    flows.postprocess_extravalues_der_phi(G, source, sink, inputflow)

    G.name['is_der_phi_positive']= flows.is_der_phi_positive(G,param.tol_thin_flow,source,sink)
    G.name['is_der_phi_decreasing']= flows.is_der_phi_decreasing(G,param.tol_thin_flow,source,sink)

    
    print("G.name['max_flow']",G.name['max_flow'])
    print("G.name['der_phi']",G.name['der_phi'])
    print("G.name['is_der_phi_positive']",G.name['is_der_phi_positive'][0])
    print("G.name['is_der_phi_decreasing']",G.name['is_der_phi_decreasing'][0])
    
    #

    #assert(flows.is_TotalTravelTime_increasing(G,param.tol_thin_flow,source,sink)[0])
    #assert(flows.is_DerTotalTravelTime_decreasing(G,param.tol_thin_flow,source,sink)[0])
    


    

    ###############################
    # for visualization
    #
    try:
        if (pars[0] == True):
            vdata.genVData(G,pars[1],pars[2],pars[3])
    except:
        #import sys
        #print(sys.exc_info())
        print('[ MSG ] test.py')
    #
    ###############################


    print( '################ end test 24 ###############')


if __name__ == '__main__':


    #whatisadjcency_iter()


    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # test5_pathmethod()

    # test6()

    # test6()
    # test7()
    # test8()

    # test9()
    # test10()
    # test11()
    # test12()

    #test13([])
    #test14()
    #test15([])
    #test16()
    #test17()

    #test21([])
    #test22([])

    #print(test_file([],'./graphs/G1_gen.gml')) #ok

    #print(test_file([],'./graphs/G2_gen.gml'))  #ok


    #print(test_file([],'./graphs/G5_gen.gml')) # ok

    #print(test_file([],'./graphs/G6_gen.gml')) # ok

    #print(test_file([],'./graphs/G8_gen.gml'))  ok

    #print(test_file([],'./graphs/G7_gen.gml'))  # bug  e=in_edges[0] IndexError: list index out of range. fixed in current_shortest_path graph

    #print(test_file([],'./graphs/G3_gen.gml'))  #bug first  e=in_edges[0] IndexError:  and now alpha  ==0

    #print(test_file([],'./graphs/Galpha_gen.gml'))  #minimal test that produced alpha =0.0

    #print(test_file([],'./graphs/Gmedium_gen.gml'))
    #print(test_file([],'./graphs/G_d4_n400_gen.gml'))
    #print(test_file([],'./graphs/G_d6_n600_gen.gml'))

    #print(test_file([],'./graphs/G3_gen.gml'))
    #print(test_file([],'./graphs/G_gen_infinite.gml'))




    # Time-stepping examples.
    #test_TS1() #Similar to test13
    #test_TS2() #Similar to test15
    
    test24([])
