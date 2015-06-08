import networkx as nx

def custom_graph():
    G=nx.MultiDiGraph()
    G.add_nodes_from("srt")
    G.node['s']['label'] = 0
    G.node['r']['label'] = 0
    G.node['t']['label'] = 0
    G.add_edge('s','r',time= 1, capacity=1.0, flow =0)
    G.add_edge('r','t',time= 2, capacity=1.0, flow =0)
    G.add_edge('r','t',time= 1, capacity=1.0/2.0, flow =0)
    G.add_edge('r','t',time= 1, capacity=1.0/2.0, flow =0)

    return G
