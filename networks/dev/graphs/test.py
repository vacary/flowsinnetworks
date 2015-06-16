import networkx as nx

def custom_graph():
    G=nx.MultiDiGraph()
    G.add_nodes_from("srt")
    G.node['s']['label'] = 's'
    G.node['r']['label'] = 'r'
    G.node['t']['label'] = 't'
    G.add_edge('s','r',time= 1, capacity=1.0, flow =0)
    G.add_edge('r','t',time= 2, capacity=1.0, flow =0)
    G.add_edge('r','t',time= 1, capacity=1.0/2.0, flow =0)
    G.add_edge('r','t',time= 1, capacity=1.0/2.0, flow =0)

    return G

def custom_graph_simple():
    G=nx.MultiDiGraph()
    G.add_nodes_from("srt")
    G.node['s']['label'] = 's'
    G.node['r']['label'] = 'r'
    G.node['t']['label'] = 't'
    G.add_edge('s','r',time= 1, capacity=1.0, flow =0)
    G.add_edge('r','t',time= 2, capacity=1.0, flow =0)
    
    return G
