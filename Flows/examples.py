import networkx as nx


def example1():
    G=nx.MultiDiGraph()
    G.add_nodes_from("svwt")
    G.add_edge('s','v',weight= 1)
    G.add_edge('s','w',weight= 6)
    G.add_edge('v','w',weight= 1)
    G.add_edge('v','t',weight= 5)
    G.add_edge('w','t',weight= 1)

    return G


def example2():
    G=nx.MultiDiGraph()
    G.add_nodes_from("svwt")
    G.node['s']['label'] = 2
    G.node['v']['label'] = 4
    G.node['w']['label'] = 8
    G.node['t']['label'] = 9
    G.add_edge('s','v',time= 1, capacity=2, flow =10)
    G.add_edge('s','w',time= 6, capacity=1, flow =10)
    G.add_edge('v','w',time= 1, capacity=1, flow =10)
    #G.add_edge('w','v',time= 1, capacity=3, flow =10)
    G.add_edge('v','t',time= 5, capacity=2, flow =10)
    G.add_edge('w','t',time= 1, capacity=1, flow =10)
    return G

def example3():
    G=nx.MultiDiGraph()
    G.add_nodes_from("svwt")
    G.node['s']['label'] = 0
    G.node['v']['label'] = 0
    G.node['w']['label'] = 0
    G.node['t']['label'] = 0
    G.add_edge('s','v',time= 1, capacity=10, flow =0)
    G.add_edge('s','w',time= 6, capacity=10, flow =0)
    G.add_edge('v','w',time= 1, capacity=2, flow =0)
    G.add_edge('v','t',time= 5, capacity=1, flow =0)
    G.add_edge('w','t',time= 1, capacity=2, flow =0)
    return G


def example4():
    G=nx.MultiDiGraph()
    G.add_nodes_from("svwt")
    G.node['s']['label'] = 0
    G.node['v']['label'] = 0
    G.node['w']['label'] = 0
    G.node['t']['label'] = 0
    G.add_edge('s','v',time= 1, capacity=1, flow =0)
    G.add_edge('s','w',time= 6, capacity=1, flow =0)
    G.add_edge('v','w',time= 1, capacity=1, flow =0)
    G.add_edge('v','t',time= 5, capacity=1, flow =0)
    G.add_edge('w','t',time= 1, capacity=1, flow =0)
    return G




def example5():
    G=nx.MultiDiGraph()
    G.add_nodes_from("suvt")
    G.node['s']['label'] = 0
    G.node['u']['label'] = 0
    G.node['v']['label'] = 0
    G.node['t']['label'] = 0
    G.add_edge('s','u',time= 1, capacity=20, flow =0)
    G.add_edge('s','v',time= 6, capacity=10, flow =0)
    G.add_edge('u','v',time= 1, capacity=30, flow =0)
    G.add_edge('u','t',time= 5, capacity=10, flow =0)
    G.add_edge('v','t',time= 1, capacity=20, flow =0)
    return G

def example_KochSkutella2011_Fig3_Fig4():
    G=nx.MultiDiGraph()
    G.add_nodes_from("svwt")
    G.node['s']['label'] = 0
    G.node['v']['label'] = 0
    G.node['w']['label'] = 0
    G.node['t']['label'] = 0
    G.add_edge('s','v',time= 1, capacity=2, flow =0)
    G.add_edge('s','w',time= 6, capacity=1, flow =0)
    G.add_edge('v','w',time= 1, capacity=1, flow =0)
    G.add_edge('v','t',time= 5, capacity=2, flow =0)
    G.add_edge('w','t',time= 1, capacity=1, flow =0)
    return G

def example_simple1():
    G=nx.MultiDiGraph()
    G.add_nodes_from("svt")
    G.node['s']['label'] = 0
    G.node['v']['label'] = 0
    G.node['t']['label'] = 0
    G.add_edge('s','v',time= 1, capacity=1, flow =0)
    G.add_edge('v','t',time= 5, capacity=2, flow =0)
    return G


def example_Fig1_Cominetti():
    G=nx.MultiDiGraph()
    G.add_nodes_from("srt")
    G.node['s']['label'] = 0
    G.node['r']['label'] = 0
    G.node['t']['label'] = 0
    G.add_edge('s','r',time= 1, capacity=1, flow =0)
    G.add_edge('r','t',time= 2, capacity=1, flow =0)
    G.add_edge('r','t',time= 1, capacity=1, flow =0)

    # The access to the attributes to the edges for multiple edges for a given pair of nodes
    # has a additional stage:
    # print('Access to attributes in MultiDiGraph')
    # print('G[\'r\'][\'t\']=', G['r']['t'])
    # print(G['r']['t'][0]['time'])
    # print(G['r']['t'][1]['time'])


    return G

def example_Fig1_Cominetti_variant1():
    G=nx.MultiDiGraph()
    G.add_nodes_from("srt")
    G.node['s']['label'] = 0
    G.node['r']['label'] = 0
    G.node['t']['label'] = 0
    G.add_edge('s','r',time= 1, capacity=1.0, flow =0)
    G.add_edge('r','t',time= 2, capacity=1.0, flow =0)
    G.add_edge('r','t',time= 1, capacity=1.0/2.0, flow =0)
    return G
