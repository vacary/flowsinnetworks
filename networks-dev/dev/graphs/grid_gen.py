
import sys, os
import networkx as nx
import random

def genGridGraph(N):

    G = nx.MultiDiGraph()
    
    # nodes
    for i in xrange(N):
    
        G.add_node(i)
    
    # edges
    for i in xrange(N):
        
        for j in xrange(N):
            
            k = i*N + j
            
            time        = 1.0
            capacity    = 1.0   
            
            if (i != N-1 and j != N-1):
                
                G.add_edge(k,k+1, time = time, capacity = capacity)
                G.add_edge(k,k+N, time = time, capacity = capacity)
                G.add_edge(k,k+N+1, time = time, capacity = capacity)
                G.add_edge(k+1,k+N+1, time = time, capacity = capacity)
                G.add_edge(k+N,k+N+1, time = time, capacity = capacity)
                
                G.add_edge(k+1,k, time = time, capacity = capacity)
                G.add_edge(k+N,k, time = time, capacity = capacity)
                G.add_edge(k+N+1,k, time = time, capacity = capacity)
                G.add_edge(k+N+1,k+1, time = time, capacity = capacity)
                G.add_edge(k+N+1,k+N, time = time, capacity = capacity)
    
    return G

G = genGridGraph(2)

