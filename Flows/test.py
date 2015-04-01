from __future__ import print_function

try:
    reload(flows)
except:
    import flows


import networkx as nx

import matplotlib.pyplot as plt
plt.ion()

try:
    reload(examples)
except:
    import examples


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
        nx.draw(G,pos=Gpos,node_color='#A0CBE2', with_labels=True, with_edge_labels=True)
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

    value,X = flows.maxflow_mincut_by_lp(G)
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


def test13():
    print( '################ start test 13 ###############')
    G=examples.example_Fig1_Cominetti()
    G=examples.example_Fig1_Cominetti_variant1()


    source = 's'
    #Original values
    timeofevent=[0.0,1.0,2.0,10.0]
    inputflow=[2.0,0.0,1.0]

    # timeofevent=[0.0,1.0,2.0,6.0,10.0]
    # inputflow=[3.0,0.0,1.0,0.0]


    # timeofevent=[0.0,1.0,2.0,6.0,10.0]
    # inputflow=[3.0,0.0,3.0,0.0]

    timeofevent=[0.0,1.0,2.0,3.0,4.0,5.0,7.0,8.0,15.0]
    inputflow=[3.0,0.0,3.0,0.0,3.0,0.0,1.0,0.0]






    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, timeofevent, inputflow)
    flows.display_graph(G)
    print("timeofevent=",timeofevent)
    print("inputflow=",inputflow)

    # plot floas and labels
    with_draw=True
    if with_draw :
        plt.close('all')
        plt.figure("Thin flows and associated labels", figsize = [8,10])
        flows.plot_thin_flows_and_labels(G,timeofevent)


    # post processing
    flows.postprocess_flows_queues_cumulativeflows(G)

    plt.figure("Flows, Cumulative flows and queues", figsize = [8,10])
    flows.plot_flows_queues_cumulativeflows(G)

    plt.figure("Flows, Cumulative flows and queues for edge =('s','r'), key =0 ", figsize = [18,14])
    flows.plot_flows_queues_cumulativeflows(G,('s','r'),0)
    plt.figure("Flows, Cumulative flows and queues for edge =('r','t'), key =0 ", figsize = [18,14])
    flows.plot_flows_queues_cumulativeflows(G,('r','t'),0)
    plt.figure("Flows, Cumulative flows and queues for edge =('r','t'), key =1 ", figsize = [18,14])
    flows.plot_flows_queues_cumulativeflows(G,('r','t'),1)




    print( '################ end test 13 ###############')


def test14():
    print( '################ start test 14 ###############')

    G=examples.example_KochSkutella2011_Fig3_Fig4()
    source = 's'

    timeofevent=[0.0,20.0]
    inputflow=[3.0,3.0,3.0]


    param=flows.parameters()
    param.tol_thin_flow=1e-10
    param.tol_lp=1e-12
    param.tol_cut=1e-12



    flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, timeofevent, inputflow,param)
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

    print( '################ end test 14 ###############')


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
# # test8()

# test9()
# test10()
test11()
# test12()

test13()
#test14()
