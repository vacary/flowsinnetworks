import networkx as nx
import matplotlib.pyplot as plt
import random
import flows

H=nx.random_graphs.random_regular_graph(4,7)
l = list( nx.simple_paths.all_simple_paths(H,H.nodes()[0],H.nodes()[-1], cutoff=2))

print(l)

for path in list(l):
    if (len(path)==2):
        H.remove_edge(path[0],path[1])
    if (len(path)>=2):
        for i in range(1,len(path)-1):
            print path[i]
            try: 
                H.remove_node(path[i])
            except:
                print('node was already')
        
    


G=nx.MultiDiGraph(H)


    


for e in G.edges(keys=True):
    G[e[0]][e[1]][e[2]]['time']=random.randint(10,20)*0.1
    G[e[0]][e[1]][e[2]]['capacity']=random.randint(5,15)*0.1


nx.write_gml(G, 'G_gen.gml')
plt.figure()
plt.ion()
nx.draw_networkx(G)

flows.display_graph(G)


plt.show()



