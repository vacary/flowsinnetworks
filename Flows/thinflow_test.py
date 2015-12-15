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

import math,itertools

def tranversality_check(G,E1,E2,l1,l2):
    pass
    


def test0():
    print( '################ start test 11 ###############')
    G=examples.example_KochSkutella2011_Fig3_Fig4()
    b= {} # dictionary of flows in nodes
    b['s'] = 3.0
    b['v'] = 0
    b['w'] = 0
    b['t'] = -3.0
    demand=3.0
    
    # G=examples.example_Fig1_Cominetti()
    # G=examples.example_Fig1_Cominetti_variant1()
    # #display_graph(G)
    # b['s'] = 1.0
    # b['r'] = 0
    # b['t'] = -1.0
    # demand=1.0

    


    param=flows.parameters()
    param.tol_thin_flow=1e-08
    param.tol_lp=1e-08
    param.tol_cut=1e-09
    
    flows.compute_thin_flow_without_resetting(G,'s',b,demand,param)
    #flows.congestion_labels(G,'s',flow='thin_flow')
    flows.display_graph(G)
    flows.assert_thin_flow_without_resetting(G,'s',b,demand,param)
    result_list=[]
    for r in range(G.number_of_edges()):
        for l in itertools.combinations(G.edges(keys=True), r):
            print("edge in E1=",l)
            # resetting graph
            E1=nx.MultiDiGraph()
            for e in l:
                #print("adding edge ",e,"in E1")
                E1.add_edge(e[0],e[1],keys=e[2])

            #flows.display_graph(E1)


            flows.compute_thin_flow(G,'s',b,E1,demand,param,echo=False)
            #flows.congestion_labels(G,'s',flow='thin_flow')
            #flows.display_graph(G)
            flows.assert_thin_flow(G,'s',b,E1,demand,param)
            labels={}
            x={}
            for n in G.nodes():
                labels[n]=G.node[n]['label_thin_flow']
            for e in G.edges(keys=True):
                x[e] = G[e[0]][e[1]][e[2]]['thin_flow']
            print('label_thin_flow=', labels)
            result_list.append((E1,labels,x))
    #print(result_list)

    # check transversality
    for result_ref in result_list:
        E1_ref=result_ref[0]
        l1_ref=result_ref[1]
        
        print("\n\n #################\n l1_ref",l1_ref)
        for result_comp in result_list:
            E1_comp=result_comp[0]
            l1_comp=result_comp[1]
            s_ref = set(E1_ref.edges(keys=True))
            s_comp = set(E1_comp.edges(keys=True))
            if s_ref.issubset(s_comp):
                # some edges of E1_ref entered in E1_comp
                print(s_ref,s_comp)
                print(len(s_comp.difference(s_ref)), "edges are entering in R ")
                for e in s_comp.difference(s_ref):
                    print("edge ",e, "is entering in R")
                    print("with ref labels", l1_ref[e[0]], l1_ref[e[1]], "and comp labels", l1_comp[e[0]], l1_comp[e[1]])
                    print("and ref thin flow",result_ref[2][e],"and comp thin flow",result_comp[2][e] )
                    check_val = (l1_ref[e[0]]- l1_ref[e[1]])*(l1_comp[e[0]]- l1_comp[e[1]])
                    if (check_val < 0.0) :
                        print("tranversality warning", check_val)
                    if (l1_ref[e[1]]- l1_ref[e[0]] > 0):
                        if (abs(l1_ref[e[1]]-l1_comp[e[1]])) >= 1e-07  or (abs(l1_ref[e[1]]-l1_comp[e[1]]) >= 1e-07 ):
                            print("############# Discontinuity when entering ...")
                            raw_input()
                        else:
                            print("############# Continuity when entering ...")

    print( '################ end test 11 ###############'  )
    

if __name__ == '__main__':




    test0()

