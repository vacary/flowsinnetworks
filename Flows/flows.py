from __future__ import print_function
import __builtin__
import networkx as nx
import matplotlib.pyplot as plt

withPulp=False
withScipyOpt=False
withSwiglpk=True

if withPulp:
    import pulp as pulp

if withScipyOpt:
    import numpy as np
    import scipy.optimize as opt

if withSwiglpk:
    import swiglpk


    
#debug_print = True
debug_print = False

#debug_check = True
debug_check = False


import numpy as np
machine_epsilon=np.finfo(float).eps*10


import math




import os
import shutil






swiglpk_f_counter = 0 # counter for filename
flowstmpdir_directory = ".tmp"
if not os.path.exists(flowstmpdir_directory):
    os.makedirs(flowstmpdir_directory)
else:
    #os.removedirs(swiglpk_directory)
    shutil.rmtree(flowstmpdir_directory, ignore_errors=True)
    os.makedirs(flowstmpdir_directory)

class parameters:

    tol_thin_flow = 1e-08
    tol_lp = 1e-08
    tol_cut =1e-09
    nmax = 50

    def __init__(self):
        pass

def print_debug(*args, **kwargs):
    """My custom print() function."""
    # Adding new arguments to the print function signature
    # is probably a bad idea.
    # Instead consider testing if custom argument keywords
    # are present in kwargs

    if debug_print:
        #__builtin__.print('My overridden print() function!')
        return __builtin__.print(*args, **kwargs)


def drepr(x, sort = True, indent = 0):
        """ Provides nice print format for a dictionnary """
	if isinstance(x, dict):
		r = '{\n'
		for (key, value) in (sorted(x.items()) if sort else x.iteritems()):
			r += (' ' * (indent + 4)) + repr(key) + ': '
			r += drepr(value, sort, indent + 4) + ',\n'
		r = r.rstrip(',\n') + '\n'
		r += (' ' * indent) + '}'
	# elif hasattr(x, '__iter__'):
	# 	r = '[\n'
	# 	for value in (sorted(x) if sort else x):
	# 		r += (' ' * (indent + 4)) + drepr(value, sort, indent + 4) + ',\n'
	# 	r = r.rstrip(',\n') + '\n'
	# 	r += (' ' * indent) + ']'
	else:
		r = repr(x)
	return r

def display_graph(G, print_function = print):
    """
    Display graph function

    Parameters
    ----------
    G : graph
       a networkx graph to be displayed. It may be a multigraph.

    print_function : function
       a print function (default = print). print_debug may be used.

    Examples
    --------
    >>> G=nx.DiGraph()
    >>> flows.display_graph(G,flows.print_debug)

    See Also
    --------


    """

    if G.is_multigraph():
        print_function("Graph display : the graph is a multigraph")
    else :
        print_function("Graph display")
    print_function (" #nodes : ", G.number_of_nodes())
    for v in G.nodes():
        print_function (" node :", v, drepr(G.node[v]))
    print_function (" #edges : ", G.number_of_edges())
    if G.is_multigraph():
        for ntail,nbrs in G.adjacency_iter():
            for nhead,eattr in nbrs.items():
                for k,keydata in eattr.items():
                    print_function('  edge : ','(\''+str(ntail)+'\'', ",", '\''+str(nhead)+'\')',  ", key =",k,",", drepr(keydata) )
    else :
        for e in G.edges():
            print_function (" edge :", e, G[e[0]][e[1]])

def current_shortest_path_graph(G, source, sink, label='label'):
    """

    Compute the current shortest path graph and the set of resetting edges
    from the graph G using the given labels
    The computation uses the criteria given in Cominetti et al. (Eq. 13 and 14.) on the
    difference between the static link travel time stored in the edge label 'time' and
    the values of the node labels at the edge.

    Parameters
    ----------

    G : graph
       a networkx multi directed graph.

    label : string
       node label G.node[n][label] that is used to compute the shortest path graph.


    Returns
    -------

    E  :  a networkx acyclic multi directed graph.
       graph  set of edges is the current shortest path

    E_comp : a networkx acyclic multi directed graph.
       the complementary graph to E

    E_star : a networkx acyclic multi directed graph.
       a directed graph whose set of edge is the set of resetting egdes

    Examples
    --------
    >>> [E,E_star,E_comp] = current_shortest_path_graph(G, label='label')

    """
    print_debug( '################ start current_shortest_path_graph ###############')
    display_graph(G, print_debug)


    # Ugly way to parse graph
    # for edge in G.edges():
    #     if (G.node[edge[0]][label] + G[edge[0]][edge[1]]['weight'] <= G.node[edge[1]][label]) :
    #         #print_debug( 'edge = ', edge)
    #         #print_debug( 'edge[0] = ', edge[0])
    #         E.add_edge(edge[0],edge[1])

    if G.is_multigraph():
        # Current shortest path : E
        E = nx.MultiDiGraph()
        E.add_nodes_from(G.nodes(data=True))
        # Complementary graph to E
        E_comp =nx.MultiDiGraph()
        E_comp.add_nodes_from(G.nodes(data=True))
        # resetting graph E_star
        E_star = nx.MultiDiGraph()
        #print_debug(E.nodes())

        for ntail,nbrs in G.adjacency_iter():
            for nhead,eattr in nbrs.items():
                for k,keydata in eattr.items():
                    excess = G.node[nhead][label] - (G.node[ntail][label] + keydata['time'])
                    print_debug('excess =', excess)
                    if (excess <= -machine_epsilon*100 and excess >= -math.sqrt(machine_epsilon)):   
                        print("Warning: curent_shortest_path test: very small negative value of excess")
                    if excess >= -machine_epsilon*100:                        
                        print_debug('add edge (',ntail,nhead,k,') in E')
                        E.add_edge(ntail, nhead, k, keydata)
                        if excess > math.sqrt(machine_epsilon):
                            print_debug('add edge (',ntail,nhead,k,') in Estar')
                            E_star.add_edge(ntail, nhead, k , keydata)
                    else:
                        print_debug('add edge (',ntail,nhead,k,') in E_comp')
                        E_comp.add_edge(ntail, nhead, k,  keydata)

    else:
        raise RuntimeError("Flows module deals only with nx.MultiDiGraph\n \
        If your graph is not a MultiDiGraph, you can copy it with nx.MultiDiGraph.copy(G) ")

    if debug_check:
        for n in E.nodes():
            if n!=source :
                print_debug("list(nx.all_simple_paths(E, source=source, target=n))", list(nx.all_simple_paths(E, source=source, target=n)))
                if list(nx.all_simple_paths(E, source=source, target=n))==[]:
                    raise RuntimeError("current shortest path is not complete")
            
            
    #print_debug( E.edges())
    #print_debug((nx.dijkstra_path(G,source,sink)))
    # print_debug( "E :")
    # display_graph(E,print_debug)
    # print_debug( "E_comp :")
    # display_graph(E_comp,print_debug)
    # print_debug( "E_star :")
    # display_graph(E_star,print_debug)

    print_debug( '################ end current_shortest_path_graph ###############')
    if debug_check:
        assert(len(list(nx.connected_components(nx.MultiGraph(E))))==1)
    return E,E_star,E_comp

def congestion_labels_pathmethod(G,source, flow='flow'):
    """
    congestion_labels_pathmethod(G,source, flow='flow')

    Compute the congestion label for a given graph with a given source by enumerating the paths.
    The congestion label are computed using the node property given  by the label flow

    keyword arguments :
    G -- the graph. It has to be an directed graph.
    source -- the source node. We check that the source is the first node is topological order
    flow -- the label that is used to compute the congestion labels (default flow='flow')

    Returns

    For each node n in G, G.node[n]['congestion_label'] is computed with G.node[source]['congestion_label']=0.0

    """
    if  not(G.is_multigraph() and G.is_directed()):
        raise RuntimeError("Flows module deals only with nx.MultiDiGraph\n \
        If your graph is not a MultiDiGraph, you can copy it with nx.MultiDiGraph.copy(G) ")


    G.node[source]['congestion_label']=0.0
    #print_debug( source, G.node[source])
    for v in G.nodes()[1:len(G.nodes())]:
        list_of_paths=list(nx.all_simple_paths(G, source, v))
        print_debug("list_of_paths", list_of_paths)
        k=0
        for path in list_of_paths:
            congestion = 0
            for i in range(0,len(path)-1):
                for key,keydata in G[path[i]][path[i+1]].items() :
                    congestion = max([congestion, G[path[i]][path[i+1]][key][flow]/G[path[i]][path[i+1]][key]['capacity'] ])
            print_debug( 'congestion=', congestion, 'for k=', k)
            if k==0 :
                mincongestion = congestion
            else :
                mincongestion = min([mincongestion, congestion])
            k=k+1
        G.node[v]['congestion_label'] = mincongestion
        #print_debug( v, G.node[v])

def congestion_labels(G,source, flow='flow'):
    """
    congestion_labels(G,source, flow='flow')

    Compute the congestion label for a given graph by a recursion of the nodes
    in their topological order. The graph needs to be a directed graph without cycles.
    The congestion label are computed using the node property given  by the label flow

    keyword arguments :
    G -- the graph. It has to be an acyclic directed graph since the topological order is needed
    source -- the source node. We check that the source is the first node is topological order
    flow -- the label that is used to compute the congestion labels (default flow='flow')

    Returns

    For each node n in G, G.node[n]['congestion_label'] is computed with G.node[source]['congestion_label']=0.0

    """

    if  not(G.is_multigraph() and G.is_directed()):
        raise RuntimeError("congestion_labels : Flows module deals only with nx.MultiDiGraph\n \
        If your graph is not a MultiDiGraph, you can copy it with nx.MultiDiGraph.copy(G) ")


    if  (list(nx.simple_cycles(G)) != []) :
        raise RuntimeError("congestion_labels : G is not an acyclic directed graph")

    sorted_nodes =  nx.topological_sort(G)
    # we assume that the source is the least node in the topological order
    if (source != sorted_nodes[0]):
        raise RuntimeError( 'congestion_labels(G,source) FAILED\n ')
        #\
        #source = %s\n \
        #sorted_nodes[0] = %s '%source%sorted_nodes[0])

    G.node[source]['congestion_label']=0.0
    #print_debug( source, G.node[source])
    for v in sorted_nodes[1:len(sorted_nodes)]:
        in_edges = G.in_edges(v,keys=True)
        e=in_edges[0]
        if G[e[0]][e[1]][e[2]]['capacity'] < 1e-14 :
            raise ZeroDivisionErrort('problem in computing congestion label with a very small (< 1e-14) capacity')
        label_e = max([G[e[0]][e[1]][e[2]][flow]/G[e[0]][e[1]][e[2]]['capacity'] ,G.node[e[0]]['congestion_label'] ])
        G.node[v]['congestion_label']= label_e
        for e in in_edges[1:len(in_edges)]:
            if G[e[0]][e[1]][e[2]]['capacity'] < 1e-14  :
                raise ZeroDivisionError('problem in computing congestion label with a very small (< 1e-14) capacity')
            label_e = max([G[e[0]][e[1]][e[2]][flow]/G[e[0]][e[1]][e[2]]['capacity'] ,G.node[e[0]]['congestion_label'] ])
            G.node[v]['congestion_label']=  min([label_e, G.node[v]['congestion_label']])
        #print_debug( v, G.node[v] )


def sparsest_cut_withPulp(G,b,source) :


    if  not(G.is_directed()):
        raise RuntimeError("sparsest_cut_withPulp error. G is not a  directed graph")

    if  not(G.is_multigraph()):
        raise RuntimeError("sparsest_cut_withPulp error. G is a  multigraph (not yet implemented)")


    # creation of the LP
    prob = pulp.LpProblem("test1", pulp.LpMinimize)

    #first congestion variable
    q = pulp.LpVariable("q", 0)
    prob += 1*q

    x={}
    for e in G.edges():
        name = 'x_' + e[0]+e[1]
        x[e]=(pulp.LpVariable(name, 0))

    for e in G.edges():
        prob += x[e] - q*G[e[0]][e[1]]['capacity']  <= 0


    #for ntail,nbrs in G.adjacency_iter():
    #    for nhead,eattr in nbrs.items():
    print_debug( "Number of edges ============== :",  G.number_of_edges())
    if G.number_of_edges() ==1 :
        print_debug( "Number of edges ==============1")
        n=G.nodes()[0]
        prob += pulp.lpSum([x[ee]   for ee in G.out_edges(n)]) -  pulp.lpSum([x[ee]   for ee in G.in_edges(n)]) == b[n]
    else:
        for n in G.nodes():
            prob += pulp.lpSum([x[ee]   for ee in G.out_edges(n)]) -  pulp.lpSum([x[ee]   for ee in G.in_edges(n)]) == b[n]

    prob.writeLP("SparsestCut_Pulp.lp")
    #pulp.GLPK().solve(prob)
    pulp.PULP_CBC_CMD().solve(prob)
    # Solution
    for v in prob.variables():
        print_debug( v.name, "=", '%.17f' %  v.varValue)

    # set the flow on the edge
    flow={}
    for  e in G.edges():
        flow[e] =   x[e].varValue
        G[e[0]][e[1]]['flow'] = flow[e]

    return q.varValue, flow

def sparsest_cut_withScipyOpt(G,b,source) :
    raise RuntimeError("withScipyOpt Failed")

    if  not(G.is_directed()):
        raise RuntimeError("sparsest_cut_withPulp error. G is not a  directed graph")

    if  not(G.is_multigraph()):
        raise RuntimeError("sparsest_cut_withPulp error. G is a  multigraph (not yet implemented)")



    # vectorization of edges
    i=1
    vec={}
    for e in G.edges():
        vec[e]=i
        i=i+1
    i=0
    nodes={}
    for e in G.nodes():
        nodes[e]=i
        i=i+1


    size =len(G.edges())+1
    cost = np.zeros(size)
    cost[0] =1.0

    #Our cost function
    fun = lambda x: np.sum(x*cost)
    print_debug('fun=',fun)



    cond =[]
    # constraints
    i=0
    for e in G.edges():
        cond.append({'type': 'ineq', 'fun': lambda x : -x[vec[e]] + x[0]*G[e[0]][e[1]]['capacity']})
        i=i+1

    y = np.array([ 0.,  1.,  0.,  0.,  0., -10.,  0.])
    bb = np.array([ 0.,  1.,  0.,  0.,  0., -10.,  0.])
    for n in G.nodes():
        bb[nodes[n]] = b[n]


    A= {}
    for n in G.nodes():
        A[n] = np.zeros(len(G.edges())+1)
        for ee in G.out_edges(n):
            A[n][vec[ee]]=1.
        for ee in G.in_edges(n):
            A[n][vec[ee]]=-1.
        print_debug(A[n])
        #A=np.transpose(A)
        print_debug(b[n])
        print_debug("A[n]*y",A[n]*y)
        print_debug("A[n]*y- b[n]",np.sum(A[n]*y)-b[n])
        #cond.append({'type': 'eq', 'fun': lambda x : np.sum(A[n]*x) - b[n] })
        cond.append({'type': 'eq', 'fun': lambda x : x[vec[ee]] - bb[nodes[n]] })
        print_debug('[cond[',i,'][\'fun\'](y)]=',[cond[i]['fun'](y)])
        i=i+1
    #cond= tuple(cond)
    for n in G.nodes():
        print_debug(b[n])
        print_debug("A[n]*y",A[n]*y)

    print_debug('[cond[',i-3,'][\'fun\'](y)]=',[cond[i-3]['fun'](y)])
    print_debug([cond[j]['fun'](y) for j in range(0,11) ])
    # print cond[7]['fun']([0,0,0,0,0,0,0])
    # print cond[7]['fun']([0,0,0,0,0,0,0])
    # print cond[7]['fun']([0,0,0,0,0,0,0])
    # print cond[7]['fun']([0,0,0,0,0,0,0])
    # print cond[7]['fun']([0,0,0,0,0,0,0])

    bnds =[]
    for ne in range(1,size+1):
        bnds.append((0,1e+24))
    bnds=tuple(bnds)

    # bnds = ((0,100),(0,100),(0,100))
    guess = np.zeros(size)
    res =opt.minimize(fun, guess, method='SLSQP', bounds=bnds, constraints = cond)

    print_debug(type(res)                )
    print_debug(res)

    toto
    if res.success==False:
        raise RuntimeError("opt.minimize FAILED")

def sparsest_cut_withSwiglpk(G,b,source,tol) :

    if (debug_print==False):
        #swiglpk.glp_msg_lev(swiglpk.GLP_MSG_OFF)
        #swiglpk.glp_smcp.msg_lev =0
        swiglpk.glp_term_out(swiglpk.GLP_OFF)

    print_debug('################ start sparsest_cut_withSwiglpk(G,b,source,tol) ###############')
    display_graph(G,print_debug)

    lp = swiglpk.glp_create_prob();
    swiglpk.glp_set_prob_name(lp, "sparsestcut")
    swiglpk.glp_set_obj_dir(lp, swiglpk.GLP_MIN);

    ncol=G.number_of_edges()+1
    nrow=G.number_of_edges()+G.number_of_nodes()+1

    if (ncol ==0 or nrow ==0):
        print('Warning: no edges in the problem of sparsest cut')
        #quit()
        return 0.0,[],[n for n in G.edges()]

    swiglpk.glp_add_cols(lp, ncol);
    swiglpk.glp_set_col_name(lp, 1, "q");
    swiglpk.glp_set_col_bnds(lp, 1, swiglpk.GLP_LO, 0.0, 0.0);
    swiglpk.glp_set_obj_coef(lp, 1, 1.0);


    # size of the sparse storage of A
    nnz=2*G.number_of_edges()
    for n in G.nodes():
        for ee in G.out_edges(n):
            nnz=nnz+1
        for ee in G.in_edges(n):
            nnz=nnz+1

    nnz=nnz+1
    #nnz=nnz+1

    #print_debug('nnz=',nnz)
    ia = swiglpk.intArray(nnz); ja = swiglpk.intArray(nnz); ar = swiglpk.doubleArray(nnz);

    i=1
    x_edge={}
    for e in G.edges(keys=True):
        i=i+1
        name = 'x_' + str(e[0])+'_'+str(e[1])+'_'+str(e[2])
        # if (e[0]==source and e[1]=='s'):
        #     x_init=i
        x_edge[e]=i
        swiglpk.glp_set_col_name(lp, i, name);
        swiglpk.glp_set_col_bnds(lp, i, swiglpk.GLP_LO, 0.0, 0.0);
        swiglpk.glp_set_obj_coef(lp, i, 0.0);

    #print_debug("x_edge:", drepr(x_edge))


    swiglpk.glp_add_rows(lp,nrow);
    i=0
    nz=0
    for e in G.edges(keys=True):
       i=i+1
       name = 'capacity_' + str(e[0])+'_'+str(e[1])+'_'+str(e[2])+'_'+str(i)
       swiglpk.glp_set_row_name(lp, i, name);
       swiglpk.glp_set_row_bnds(lp, i, swiglpk.GLP_UP, 0.0, 0.0);
       nz=nz+1
       #print_debug("ia[",nz,"] = ",i,"; ja[",nz,"] = ",1 ,"; ar[",nz,"] =", -G[e[0]][e[1]][e[2]]['capacity'])

       ia[nz] = i; ja[nz] = 1; ar[nz] = -G[e[0]][e[1]][e[2]]['capacity']; # a[i,1] = -G[e[0]][e[1]][e[2]]['capacity']
       nz=nz+1
       #print_debug("ia[",nz,"] = ",i,"; ja[",nz,"] = ",i+1 ,"; ar[",nz,"] = -1.0")
       ia[nz] = i; ja[nz] = i+1; ar[nz] = 1.0; # a[i,i+1] = 1.0


    for n in G.nodes():
        i=i+1
        name = 'balance_' + str(n)
        swiglpk.glp_set_row_name(lp, i, name);
        swiglpk.glp_set_row_bnds(lp, i, swiglpk.GLP_FX,b[n] ,b[n]);
        for ee in G.out_edges(n,keys=True):
            nz=nz+1
            #print_debug("ia[",nz,"] = ",i,"; ja[",nz,"] = x_edge[",ee,"] = ", x_edge[ee] ,"; ar[",nz,"] = 1.0")
            ia[nz] = i; ja[nz] = x_edge[ee]; ar[nz] = 1.0
        for ee in G.in_edges(n,keys=True):

            nz=nz+1
            #print_debug("ia[",nz,"] = ",i,"; ja[",nz,"] = x_edge[",ee,"] = ", x_edge[ee] ,"; ar[",nz,"] = -1.0")
            ia[nz] = i; ja[nz] = x_edge[ee]; ar[nz] = -1.0; # a[i,i+1] = -1.0

    # i=i+1
    # swiglpk.glp_set_row_name(lp, i, 'fixed_init');
    # swiglpk.glp_set_row_bnds(lp, i, swiglpk.GLP_FX, G[source]['s']['capacity'] , G[source]['s']['capacity']);
    # nz=nz+1
    # ia[nz] = i; ja[nz] = x_init; ar[nz] = 1.0; # a[i,i+1] = 1.0

    #for i in range(1,nz+1)    :
    #    print_debug( ia[i], ja[i], ar[i])
    #print_debug'nz =', nz)
    #print_debug([ (ia[i], ja[i], ar[i]) for i in  range(1,nz) ] )

    swiglpk.glp_load_matrix(lp, nz, ia, ja, ar);
    if debug_check:
        global swiglpk_f_counter
        swiglpk_f_counter +=1
        if (swiglpk_f_counter >= 0):
            s_filename = flowstmpdir_directory + '/sparsest_glpk_'+str(swiglpk_f_counter).zfill(5)+'.lp'
            print("s_filename", s_filename)
            swiglpk.glp_write_lp(lp, None, s_filename);


        if (swiglpk_f_counter < -1) : # >= 185):

            fig = plt.figure()
            #nx.draw_graphviz(G)

            nx.draw_graphviz(G,node_color='#A0CBE2', with_labels=True, with_edge_labels=True)
            #nx.draw_networkx_edge_labels(G,pos=nx.spring_layout(G))

            fig_filename = flowstmpdir_directory + '/sparsest_glpk_'+str(swiglpk_f_counter).zfill(5)+'.png'
            plt.savefig(fig_filename)
            plt.close(fig)
            gml_filename = flowstmpdir_directory + '/sparsest_glpk_'+str(swiglpk_f_counter).zfill(5)+'.gml'
            GG = nx.MultiDiGraph()
            GG.add_nodes_from(G.nodes())
            GG.add_edges_from(G.edges())
            for e in G.edges(keys=True):
                GG[e[0]][e[1]][e[2]]['capacity']=  G[e[0]][e[1]][e[2]]['capacity']
            nx.write_gml(GG,gml_filename)

            b_numpy= np.zeros(len(b))
            i=0
            for n in G.nodes():
                b_numpy[i]= b[n]
                i=i+1
            b_filename = flowstmpdir_directory + '/sparsest_glpk_'+str(swiglpk_f_counter).zfill(5)+'_b.npy'
            np.save(b_filename,b_numpy)



            
    parm = swiglpk.glp_smcp()
    swiglpk.glp_init_smcp(parm)
    parm.tol_bnd=tol

    
    print_debug("parm.tol_bnd = ", parm.tol_bnd )


    swiglpk.glp_simplex(lp, parm);

    STATUS = swiglpk.glp_get_status(lp);
    if STATUS != swiglpk.GLP_OPT:
        raise RuntimeError("GLPK simplex failed !!!! \n")
    
    congestion = swiglpk.glp_get_obj_val(lp)
    i=1
    flow={}
    for e in G.edges(keys=True):
        i=i+1
        name = 'x_' + str(e[0])+'_'+str(e[1])+'_'+str(e[2])
        flow[e] = swiglpk.glp_get_col_prim(lp, i)
        print_debug(name, '=', flow[e])
        
    # for j  in range(1,ncol+1)  :
    #     col_name = swiglpk.glp_get_col_name(lp,j)
    #     col_stat = swiglpk.glp_get_col_stat(lp,j)
    #     col_prim = swiglpk.glp_get_col_prim(lp,j)
    #     col_dual = swiglpk.glp_get_col_dual(lp,j)
    #     print_debug("status of col var:",col_name, '=', col_stat)
    #     print_debug("col_prim of :",col_name, '=', col_prim)
    #     print_debug("col_dual of :",col_name, '=', col_dual)

    #     if col_stat==swiglpk.GLP_BS :
    #         print_debug("The variable ",col_name, 'is a basic variable')
    #     elif col_stat==swiglpk.GLP_NL :
    #         print_debug("The variable ",col_name, 'is a non-basic variable on its lower bound')
    #     elif col_stat==swiglpk.GLP_NU :
    #         print_debug("The variable ",col_name, 'is a non-basic variable on its upper bound')
    #     elif col_stat==swiglpk.GLP_NF :
    #         print_debug("The variable ",col_name, 'is a non-basic free (unbounded) variable')
    #     elif col_stat==swiglpk.GLP_NS :
    #         print_debug("The variable ",col_name, 'is a non-basic fixed  variable')

    # for i  in range(1,nrow+1)  :
    #     row_name = swiglpk.glp_get_row_name(lp,i)
    #     row_stat = swiglpk.glp_get_row_stat(lp,i)
    #     row_prim = swiglpk.glp_get_row_prim(lp,i)
    #     row_dual = swiglpk.glp_get_row_dual(lp,i)
    #     print_debug("status of row var:",row_name, '=', row_stat)
    #     print_debug("row_prim of :",row_name, '=', row_prim)
    #     print_debug("row_dual of :",row_name, '=', row_dual)
    #     if row_stat==swiglpk.GLP_BS :
    #         print_debug("The variable ",row_name, 'is a basic variable')
    #     elif row_stat==swiglpk.GLP_NL :
    #         print_debug("The variable ",row_name, 'is a non-basic variable on its lower bound')
    #     elif row_stat==swiglpk.GLP_NU :
    #         print_debug("The variable ",row_name, 'is a non-basic variable on its upper bound')
    #     elif row_stat==swiglpk.GLP_NF :
    #         print_debug("The variable ",row_name, 'is a non-basic free (unbounded) variable')
    #     elif row_stat==swiglpk.GLP_NS :
    #         print_debug("The variable ",row_name, 'is a non-basic fixed  variable')


    #for j in range(1,nrow)  :
    #    print_debug'swiglpk.glp_get_row_dual(lp, ',j,')= ',swiglpk.glp_get_row_dual(lp, j) )

    swiglpk.glp_delete_prob(lp);


    if debug_check:
        for n in G.nodes():
            balance = b[n]
            for ee in G.out_edges(n,keys=True):
                balance = balance-flow[ee]
            for ee in G.in_edges(n,keys=True):
                balance =balance+flow[ee]
            assert(abs(balance)<tol)
        for e in G.edges(keys=True):
            assert(flow[e] - congestion*G[e[0]][e[1]][e[2]]['capacity'] <= tol)
        



    
    return congestion,flow


def sparsest_cut_withSwiglpk_dual(G,b,source,tol) :

    if (debug_print==False):
        #swiglpk.glp_msg_lev(swiglpk.GLP_MSG_OFF)
        #swiglpk.glp_smcp.msg_lev =0
        swiglpk.glp_term_out(swiglpk.GLP_OFF)

    print_debug('################ start sparsest_cut_withSwiglpk_dual(G,b,source,tol) ###############')
    display_graph(G,print_debug)

    lp = swiglpk.glp_create_prob();
    swiglpk.glp_set_prob_name(lp, "sparsestcut_dual")
    swiglpk.glp_set_obj_dir(lp, swiglpk.GLP_MAX);


    ncol=G.number_of_edges()+G.number_of_nodes()

    nrow=G.number_of_edges()+1

    swiglpk.glp_add_cols(lp, ncol);
    swiglpk.glp_add_rows(lp, nrow);

    if (ncol ==0 or nrow ==0):
        print('Warning: no edges in the problem of sparsest cut')
        #quit()
        return 0.0,[],[n for n in G.edges()]

    i=0
    node_dict={}
    for n in G.nodes():
        i=i+1
        name = 'pi_' + n
        node_dict[n]=i
        swiglpk.glp_set_col_name(lp, i, name);
        swiglpk.glp_set_col_bnds(lp, i, swiglpk.GLP_FR,0.0,0.0);
        swiglpk.glp_set_obj_coef(lp, i, -b[n]);

    gamma_edge={}
    for e in G.edges(keys=True):
        i=i+1
        name = 'gamma_' + str(e[0])+str(e[1])+'_'+str(e[2])
        gamma_edge[e]=i
        swiglpk.glp_set_col_name(lp, i, name);
        swiglpk.glp_set_col_bnds(lp, i, swiglpk.GLP_LO, 0.0, 0.0);
        swiglpk.glp_set_obj_coef(lp, i, 0.0);


    # size of the sparse storage of A
    nnz=G.number_of_edges() + 3 * G.number_of_edges()+1

    print_debug('nnz=',nnz)
    ia = swiglpk.intArray(nnz); ja = swiglpk.intArray(nnz); ar = swiglpk.doubleArray(nnz);

    j=0
    nz=0
    name = 'q'
    swiglpk.glp_set_row_name(lp, 1, name);
    swiglpk.glp_set_row_bnds(lp, 1, swiglpk.GLP_FX, 1.0, 1.0);


    for e in G.edges(keys=True):
       j=j+1
       nz=nz+1
       #print_debug("ia[",nz,"] = ",1,"; ja[",nz,"] = ",gamma_edge[e],"; ar[",nz,"] =", G[e[0]][e[1]][e[2]]['capacity'])
       ia[nz] = 1; ja[nz] = gamma_edge[e]; ar[nz] = G[e[0]][e[1]][e[2]]['capacity'];


    i=1
    for e in G.edges(keys=True):
       i=i+1
       nz=nz+1
       #print_debug("ia[",nz,"] = ",i,"; ja[",nz,"] = ",node_dict[e[0]] ,"; ar[",nz,"] =",1.0)

       ia[nz]=i; ja[nz]=node_dict[e[0]]; ar[nz]=1.0;
       nz=nz+1
       #print_debug("ia[",nz,"] = ",i,"; ja[",nz,"] = ",node_dict[e[1]] ,"; ar[",nz,"] =",-1.0)

       ia[nz]=i; ja[nz]=node_dict[e[1]]; ar[nz]=-1.0;
       nz=nz+1

       #print_debug("ia[",nz,"] = ",i,"; ja[",nz,"] = ",gamma_edge[e] ,"; ar[",nz,"] =",1.0)

       ia[nz]=i; ja[nz]=gamma_edge[e]; ar[nz]=1.0;

       name = 'x_' + str(e[0])+str(e[1])+'_'+str(e[2])

       swiglpk.glp_set_row_name(lp, i, name);
       swiglpk.glp_set_row_bnds(lp, i, swiglpk.GLP_LO, 0.0, 0.0);


    #print_debug([ (ia[i], ja[i], ar[i]) for i in  range(1,nz) ] )

    swiglpk.glp_load_matrix(lp, nz, ia, ja, ar);

    swiglpk.glp_write_lp(lp, None, 'sparsest_glpk_dual.lp');

    parm = swiglpk.glp_smcp()
    swiglpk.glp_init_smcp(parm)
    parm.tol_bnd=tol

    print_debug("parm.tol_bnd = ", parm.tol_bnd )

    swiglpk.glp_simplex(lp, parm);

    congestion = swiglpk.glp_get_obj_val(lp)

    pi={}
    for n in G.nodes():
        name = 'pi_' + n
        i = node_dict[n]
        pi[n] = swiglpk.glp_get_col_prim(lp, i)
        print_debug(name, '=', pi[n])


    gamma={}
    for e in G.edges(keys=True):
        name = 'gamma_' + str(e[0])+str(e[1])+'_'+str(e[2])
        i = gamma_edge[e]
        gamma[e] = swiglpk.glp_get_col_prim(lp, i)
        print_debug(name, '=', gamma[e])



    i=1
    for j  in range(1,ncol+1)  :
        col_name = swiglpk.glp_get_col_name(lp,j)
        col_stat = swiglpk.glp_get_col_stat(lp,j)
        col_prim = swiglpk.glp_get_col_prim(lp,j)
        col_dual = swiglpk.glp_get_col_dual(lp,j)
        print_debug("status of col var:",col_name, '=', col_stat)
        print_debug("col_prim of :",col_name, '=', col_prim)
        print_debug("col_dual of :",col_name, '=', col_dual)

        if col_stat==swiglpk.GLP_BS :
            print_debug("The variable ",col_name, 'is a basic variable')
        elif col_stat==swiglpk.GLP_NL :
            print_debug("The variable ",col_name, 'is a non-basic variable on its lower bound')
        elif col_stat==swiglpk.GLP_NU :
            print_debug("The variable ",col_name, 'is a non-basic variable on its upper bound')
        elif col_stat==swiglpk.GLP_NF :
            print_debug("The variable ",col_name, 'is a non-basic free (unbounded) variable')
        elif col_stat==swiglpk.GLP_NS :
            print_debug("The variable ",col_name, 'is a non-basic fixed  variable')

    for i  in range(1,nrow+1)  :
        row_name = swiglpk.glp_get_row_name(lp,i)
        row_stat = swiglpk.glp_get_row_stat(lp,i)
        row_prim = swiglpk.glp_get_row_prim(lp,i)
        row_dual = swiglpk.glp_get_row_dual(lp,i)
        print_debug("status of row var:",row_name, '=', row_stat)
        print_debug("row_prim of :",row_name, '=', row_prim)
        print_debug("row_dual of :",row_name, '=', row_dual)
        if row_stat==swiglpk.GLP_BS :
            print_debug("The variable ",row_name, 'is a basic variable')
        elif row_stat==swiglpk.GLP_NL :
            print_debug("The variable ",row_name, 'is a non-basic variable on its lower bound')
        elif row_stat==swiglpk.GLP_NU :
            print_debug("The variable ",row_name, 'is a non-basic variable on its upper bound')
        elif row_stat==swiglpk.GLP_NF :
            print_debug("The variable ",row_name, 'is a non-basic free (unbounded) variable')
        elif row_stat==swiglpk.GLP_NS :
            print_debug("The variable ",row_name, 'is a non-basic fixed  variable')


    #for j in range(1,nrow)  :
    #    print_debug'swiglpk.glp_get_row_dual(lp, ',j,')= ',swiglpk.glp_get_row_dual(lp, j) )

    swiglpk.glp_delete_prob(lp);


    return congestion


def congestion_of_cut(G,b,cut):
    congestion_num=0.0
    congestion_denom=0.0
    comp_cut = set.difference(set(G.nodes()),cut)
    for n in cut:
        congestion_num += b[n]
    out_edges =  set.intersection(set(G.out_edges(cut,keys=True)),set(G.in_edges(comp_cut,keys=True)))
    if len(out_edges) ==0 :
        return 0.0
    for e in out_edges:
        congestion_denom += G[e[0]][e[1]][e[2]]['capacity']
        congestion  =  congestion_num /congestion_denom
    return congestion

from itertools import chain, combinations

def powerset(iterable):
  xs = list(iterable)
  # note we return an iterator rather than a list
  return chain.from_iterable( combinations(xs,n) for n in range(len(xs)+1) )


def sparsest_cut_by_enumeration(G,b,source):        
    nodes_set = set(G.nodes())
    print(nodes_set)
    list_of_cutsets =[]

    for subset in powerset(nodes_set):
        #    print(subset)
        if source in subset:
                #if len(subset) >= 2 :
                #    if not sink in subset:
                #        list_of_cutsets.append(subset)
                #else:
            list_of_cutsets.append(set(subset))
    #print (list_of_cutsets)
    max_congestion = 0.0

    for cut in list_of_cutsets:
        congestion = congestion_of_cut(G,b,cut)
        if (congestion >= max_congestion ):
            max_congestion=congestion

    cut_max=nodes_set
    for cut in list_of_cutsets:
        congestion = congestion_of_cut(G,b,cut)
        if (abs(congestion - max_congestion) <= machine_epsilon ):
            if (len(cut) <= len(cut_max)):
                cut_max=cut
                

    comp_cut_max=set.difference(nodes_set,cut_max)
            
    #print("max_congestion =",max_congestion, "for cut =", cut_max , "and comp_cut", comp_cut_max )
    
    return max_congestion, cut_max, comp_cut_max
    
def sparsest_cut(G,b,source,tol=1e-12,tol_cut=1e-12) :
    congestion=0.0
    cut = set()
    comp_cut = set()

    # particular case that raises issue in LP solve.
    if G.number_of_edges() ==1 :
        e = G.edges()[0]
        if (e[0]!= source) :
             print('Warning.  sparsest_cut(G,b,source).  Something strange happens')
        b_sum = b[e[0]]+b[e[1]]
        if (abs(b_sum) > tol ):
            print('Warning.  sparsest_cut(G,b,source).  One edge graph with sum(b) >tol')
        if (b[source] <=0 ):
            print('Warning.  sparsest_cut(G,b,source).  One edge graph with b[source] <= 0')
        cut.add(source)
        comp_cut.add(e[1])
        congestion= b[source]/G[e[0]][e[1]][0]['capacity']
        return congestion, cut, comp_cut
    elif G.number_of_edges() ==0:
         print('Warning.  sparsest_cut(G,b,source). No edge graph !')
         if G.number_of_nodes() ==1 :
             cut.add(source)
             return congestion, cut, comp_cut
         elif  G.number_of_nodes() ==0 :
             print('Warning.  sparsest_cut(G,b,source). No node graph !')
             return congestion, cut, comp_cut


    if withPulp :
        congestion, flow = sparsest_cut_withPulp(G,b,source)

    elif withScipyOpt:
        congestion, flow = sparsest_cut_withScipyOpt(G,b,source)

    elif withSwiglpk:
        congestion, flow = sparsest_cut_withSwiglpk(G,b,source,tol)
        #congestion = sparsest_cut_withSwiglpk_dual(G,b,source,tol)

    print_debug('congestion=', congestion)
    #print_debug('flow=', flow)

    # affect the flow
    for e in G.edges(keys=True):
        G[e[0]][e[1]][e[2]]['flow'] = flow[e]

    # compute congestion label
    congestion_labels(G,source)

    #congestion_labels_pathmethod(G,source)
    # GG=nx.MultiGraph(G)
    for n in G.nodes():
        print_debug("comparaison = ", G.node[n]['congestion_label'] - congestion )
        if G.node[n]['congestion_label'] < congestion - tol_cut  :
            #if (G.node[n]['congestion_label'] >= congestion - math.sqrt(tol_cut)  ):
            if (G.node[n]['congestion_label'] >= congestion - 100*(tol_cut)  ):
                print('Warning: sparsest cut comparison is difficult. Values just under the congestion threshold')
            print_debug(  'G.node[n][\'congestion_label\']', G.node[n]['congestion_label'])
            cut.add(n)
        else:
            comp_cut.add(n)

    nloop=0
    while (abs(congestion_of_cut(G,b,cut)-congestion)>=tol_cut and nloop< 10*len(G.nodes())):
        nloop=nloop+1
        print_debug("set in intersection", set.intersection(set(G.in_edges(cut,keys=True)),set(G.out_edges(comp_cut,keys=True))) )
        for e in set.intersection(set(G.in_edges(cut,keys=True)),set(G.out_edges(comp_cut,keys=True))) :
            if (abs(G[e[0]][e[1]][e[2]]['flow']) >= tol_cut):
                print_debug( 'e from comp_cut to cut',e, "with flow =", G[e[0]][e[1]][e[2]]['flow']  )
                cut.add(e[0])
                comp_cut.remove(e[0])
                break
        print_debug("set in intersection", set.intersection(set(G.out_edges(cut,keys=True)),set(G.in_edges(comp_cut,keys=True))) )        
        for e in set.intersection(set(G.out_edges(cut,keys=True)),set(G.in_edges(comp_cut,keys=True))) :
            if (abs(G[e[0]][e[1]][e[2]]['flow']-congestion*G[e[0]][e[1]][e[2]]['capacity']  ) >= tol_cut):
                print_debug( 'e from cut to comp_cut',e, "with flow =", G[e[0]][e[1]][e[2]]['flow']  )
                cut.add(e[1])
                comp_cut.remove(e[1])
                break
        print_debug("while loop",nloop," -- congestion=", congestion," congestion of cut =",congestion_of_cut(G,b,cut), "for cut =", cut, "and comp_cut", comp_cut)

            
            
        
    # sur_comp_cut=[]
    # sur_cut =[]
    # for n in G.nodes():
    #     print_debug( "comparaison = ", G.node[n]['congestion_label'] - congestion )
    #     if (abs(G.node[n]['congestion_label'] - congestion) >= 10 *tol_cut and abs(G.node[n]['congestion_label'] - congestion) <= 1000 *tol_cut  ):
    #         print('Warning: COMPARISON IS DIFFICULT')
    #     if G.node[n]['congestion_label'] < congestion - tol_cut  :
    #         print_debug(  'G.node[n][\'congestion_label\']', G.node[n]['congestion_label'])
    #         sur_cut.append(n)
    #     else:
    #         sur_comp_cut.append(n)
    # print("sur_cut", sur_cut)
    # print("sur_comp_cut", sur_comp_cut)
            
    # cutting_edges=set()
    # for e in set.intersection(set(G.out_edges(sur_cut,keys=True)),set(G.in_edges(sur_comp_cut,keys=True))) :
    #     print ("criteria=",congestion* G[e[0]][e[1]][e[2]]['capacity'] - G[e[0]][e[1]][e[2]]['flow'])
    #     if (abs(congestion* G[e[0]][e[1]][e[2]]['capacity'] - G[e[0]][e[1]][e[2]]['flow']) <= tol_cut ):
    #         cutting_edges.add(e)
    # print("cutting_edges", cutting_edges)
    
    # for e in set.intersection(set(G.out_edges(sur_comp_cut,keys=True)),set(G.in_edges(sur_cut,keys=True))) :
    #     print("G[e[0]][e[1]][e[2]]['flow']",G[e[0]][e[1]][e[2]]['flow'], e)
    #     if (abs(G[e[0]][e[1]][e[2]]['flow']) <= tol_cut ):
    #         cutting_edges.add(e)
    # print("cutting_edges", cutting_edges)
    # print(G.edges())
      
    # GG=nx.MultiGraph(G)
    # for e in  cutting_edges:
    #     GG.remove_edge(*e)
        
    # cut= nx.node_connected_component(GG,source)

    # comp_cut = list(set.difference(set(GG.nodes()),set(cut)))
    # print(cut)
    # print(comp_cut)
    # print(sorted(nx.connected_components(GG), key = len, reverse=True)  )
                
    if debug_check :
        congestion_check  =  congestion_of_cut(G,b,cut)
        print_debug("congestion_check", congestion_check)
        assert(abs(congestion_check-congestion)<=tol_cut)
        #congestion_enum, cut_enum, comp_cut_enum = sparsest_cut_by_enumeration(G,b,source)
        #assert(abs(congestion_enum-congestion)<=tol_cut)
        #assert(cut_enum==cut)
        #assert(comp_cut_enum==comp_cut)
            
            
    print_debug("congestion=", congestion, "sparsest_cut = ", cut, "complementary set = ", comp_cut)

    return  congestion,cut, comp_cut



def maxflow_mincut_by_lp(G,source,sink) :



    if  not(G.is_multigraph()):
        raise RuntimeError("sparsest_cut_withPulp error. G is a  multigraph (not yet implemented)")


    # creation of the Primal LP
    prob = pulp.LpProblem("primal", pulp.LpMaximize)

    #first congestion variable
    vf = pulp.LpVariable("vf", 0)

    prob += vf
    x={}

    for e in G.edges():
        name = 'x_' + e[0]+e[1]
        print_debug( name)
        x[e]=(pulp.LpVariable(name, 0))

    print_debug( x)
    for e in G.edges():
        prob += x[e] - G[e[0]][e[1]]['capacity']  <= 0


    for n in G.nodes():
        if (n == source):
            prob += pulp.lpSum([x[ee]   for ee in G.out_edges(n)]) -  pulp.lpSum([x[ee]   for ee in G.in_edges(n)]) == vf
        elif (n == sink):
            prob += pulp.lpSum([x[ee]   for ee in G.out_edges(n)]) -  pulp.lpSum([x[ee]   for ee in G.in_edges(n)]) == -vf
        else :
            prob += pulp.lpSum([x[ee]   for ee in G.out_edges(n)]) -  pulp.lpSum([x[ee]   for ee in G.in_edges(n)]) == 0

    prob.writeLP("MaxFlowMinCut_primal.lp")
    print_debug( pulp.GLPK().solve(prob))

    # Solution
    for v in prob.variables():
        print_debug( v.name, "=", v.varValue)

    # creation of the Dual LP
    dual_prob = pulp.LpProblem("primal", pulp.LpMinimize)

    gamma={}

    for e in G.edges():
        name = 'gamma_' + e[0]+e[1]
        print_debug( name)
        gamma[e]=(pulp.LpVariable(name, 0))

    pi={}
    for n in G.nodes():
        name = 'pi_' + n
        print_debug( name)
        pi[n]=(pulp.LpVariable(name, 0))

    print_debug( gamma, pi)

    dual_prob += pulp.lpSum([gamma[ee]*G[ee[0]][ee[1]]['capacity'] for ee in G.edges()])

    dual_prob += -pi[source] + pi[sink] >=1

    for e in G.edges():
        dual_prob += gamma[e]  >= 0
        dual_prob += pi[e[0]]- pi[e[1]]+ gamma[e]  >= 0

    dual_prob.writeLP("MaxFlowMinCut_dual.lp")

    pulp.GLPK.msg = False
    pulp.GLPK().solve(dual_prob)

    # Solution
    for v in dual_prob.variables():
        print_debug( v.name, "=", v.varValue)


    X = []
    comp_X = []
    # computation of the min cut
    for n in G.nodes():
        if (pi[n].varValue == 0) :
            X.append(n)
        else :
            comp_X=append(n)
    return  vf.varValue,X, comp_X



def compute_thin_flow_without_resetting(G,source,b, demand=None, param=None):
    """
    compute_thin_flow_without_resetting(G,source,b, demand=None, param=None)

    Compute the thin flow without resetting and its associated labels given
    a acyclic directed graph.
    The method that is implemented is the method of Koch, R. (PhD, TU Berlin, 2012, page 215).
    The thin flow is computed by iterating computations of the sparsest cut and modifing the
    b-flow b.

    keyword arguments :
    G -- the graph. It has to be an acyclic directed graph.

    source -- the source node. We check that the source is the first node is topological order

    b -- the b-flow that models the source and the sink.

    demand -- the demand at the source node. (default value = None). If demand=None, the demand is considered
    to be infinite  and the node label of the source is equal to zero. Otherwise, it is equal to b[source]/demand and
    we add a dummy source 's0' to come back to the first case

    param : class parameters
      numerical parameters (tolerances and max number of iterations )

    Returns

    For each node n in G, G.node[n]['label_thin_flow']
    for each edge e in G  G[e[0]][e[1]]['thin_flow']

    """

    print_debug( '################ start compute_thin_flow_without_resetting ###############')

    if  not(G.is_multigraph() and G.is_directed()):
        raise RuntimeError("Flows module deals only with nx.MultiDiGraph\n \
        If your graph is not a MultiDiGraph, you can copy it with nx.MultiDiGraph.copy(G) ")

    if (list(nx.simple_cycles(G)) != [])  :
        raise RuntimeError("Compute_thin_flow_without_resetting FAILED. G is not an acyclic directed graph")


    if param==None:
        param = parameters()

    # case with a nonvanishing label (label_thin_flow at the source node)
    if demand != None:
        # we compute a thin flow with a nonlabel vanishing source label
        # equal to b[source]/demand
        # For computing such a thin flow, we come back to the first example
        # adding a dummy source node s0 with a new edge of capacity equl to demand.
        # Doing that the label of the source is equal to b[source]/demand
        if (source=='s0'):
            raise RuntimeError
        G.add_node('s0')

        G.add_edge('s0',source, flow = 0,  capacity = demand)
        b['s0']= b[source]
        b[source] = 0.0
        oldsource =source
        source = 's0'

    # else :   # we compute a thin flow with a vanishing source label
        # the demand is considered to be infinity
        # and the source node label is equal to zero
    #display_graph(G,print_debug)

    Gi=nx.MultiDiGraph.copy(G)
    bi=dict(b)
    k=1

    print_debug("b =", b)
    continue_while=True
    nmax=Gi.number_of_nodes()

    #for e in G.edges(keys=True):
    #    G[e[0]][e[1]][e[2]]['thin_flow']=1e+48

    while continue_while:
        print_debug( "iteration number :", k)
        for n in Gi.nodes() :
            if abs(bi[n]) <= machine_epsilon :
                bi[n]=0.0
        print_debug( 'bi (restricted)=', [[n, bi[n]] for n in Gi.nodes()]     )
        sumb = 0
        i_positive=0
        if debug_check :
            for n in Gi.nodes() :
                if bi[n] >= machine_epsilon :
                    i_positive += 1
                sumb = sumb + bi[n]
            assert(abs (sumb) < machine_epsilon*10)
            assert(i_positive == 1)
                
        congestion,cut,comp_cut = sparsest_cut(Gi,bi,source,param.tol_lp,param.tol_cut)
        #display_graph(Gi)
        print_debug( 'congestion,cut, comp_cut=',congestion,",",cut,",", comp_cut)

        # assign bflow
        # print_debug( 'Gi.out_edges(cut)=',Gi.out_edges(cut))

        # edges from cut to comp_cut
        for e in set.intersection(set(Gi.out_edges(cut,keys=True)),set(Gi.in_edges(comp_cut,keys=True))) :
            print_debug( 'e from cut to comp_cut=',e, "with flow",Gi[e[0]][e[1]][e[2]]['flow']   )
            bi[e[0]] = bi[e[0]] - Gi[e[0]][e[1]][e[2]]['flow']

        # edges from comp_cut to cut
        for e in set.intersection(set(Gi.in_edges(cut,keys=True)),set(Gi.out_edges(comp_cut,keys=True))) :
            print_debug( 'e from comp_cut to cut',e, "with flow =",Gi[e[0]][e[1]][e[2]]['flow']  )
            if (abs(Gi[e[0]][e[1]][e[2]]['flow']) > param.tol_cut):
                print('ERROR: e from comp_cut to cut',e, 'with positive flow = ',Gi[e[0]][e[1]][e[2]]['flow'])
                raise RuntimeError("Error in computation Sparsest cut \n")
            bi[e[1]] = bi[e[1]] + Gi[e[0]][e[1]][e[2]]['flow']
            G[e[0]][e[1]][e[2]]['thin_flow'] = Gi[e[0]][e[1]][e[2]]['flow']

        for e in Gi.in_edges(comp_cut,keys=True):
            G[e[0]][e[1]][e[2]]['thin_flow'] = Gi[e[0]][e[1]][e[2]]['flow']

        #for e in Gi.edges(comp_cut,keys=True):
        #    G[e[0]][e[1]][e[2]]['thin_flow'] = Gi[e[0]][e[1]][e[2]]['flow']

        for n in comp_cut:
            G.node[n]['label_thin_flow']=congestion
            Gi.remove_node(n)
        k=k+1

        # plt.figure(k)
        # Gpos=nx.pydot_layout(Gi)
        # nx.draw(Gi,pos=Gpos,node_color='#A0CBE2', with_labels=True, with_edge_labels=True)
        # plt.draw()
        # plt.show()
        #raw_input()
        continue_while = (bi[source] > param.tol_lp and k < nmax)
        #continue_while = (cut!=[source] and k < nmax and cut!=[])


        if (bi[source] > param.tol_lp and  continue_while==False ):
            print('Warning cut =[source] but bi[source] > param.tol_lp ')

    for n in cut:
        G.node[n]['label_thin_flow']=0.0
    for e in Gi.edges(keys=True):
        G[e[0]][e[1]][e[2]]['thin_flow'] = Gi[e[0]][e[1]][e[2]]['flow']


    print_debug( "number of iterations =", k-1)

    print_debug( 'bi=',bi)
    print_debug( 'G:')
    display_graph(G, print_debug)
    print_debug( 'congestion= ', congestion)
    print_debug( 'sparset cut= ', cut)



    if demand != None :
        G.remove_node('s0')
        source=oldsource
        b[source]=b['s0']
        b['s0']=None



    print_debug( '################ end compute_thin_flow_without_resetting ###############'    )


def compute_thin_flow(G, source, b, E1, demand=None, param = None):
    """
    compute_thin_flow(G,source,b, E1, tol=default_tol)

    The method compute the thin flow ('thin_flow') on the egdes and the associated
    node labels ('label_thin_flow') for an acyclic graph G with the resetting set of edges
    given by E1.

    The method that is implemented is the method of Koch, R. (PhD, TU Berlin, 2012, Section 6.2).
    It uses fixed point iteration on the anchored networks.


    keyword arguments :
    G -- the graph. It has to be an acyclic directed graph.

    source -- the source node. We check that the source is the first node is topological order

    b -- the b-flow that models the source and the sink.

    E1 -- the resetting graph

    demand -- the demand at the source node. (default value = None). If demand=None, the demand is considered
    to be infinite  and the node label of the source is equal to zero. Otherwise, it is equal to b[source]/demand and
    we add a dummy source 's0' to come back to the first case

    tol -- tolerance of the fixed point iteration

    Returns

    For each node n in G, G.node[n]['label_thin_flow']
    For each edge e in G  G[e[0]][e[1]]['thin_flow']

    """
    print_debug('################ start compute_thin_flow ###############')

    if  not(G.is_multigraph() and G.is_directed()):
        raise RuntimeError("Flows module deals only with nx.MultiDiGraph\n \
        If your graph is not a MultiDiGraph, you can copy it with nx.MultiDiGraph.copy(G) ")

    if list(nx.simple_cycles(G)) != []:
        raise RuntimeError("G is not an acyclic graph")

    if param==None:
        param = parameters()

    # case with a nonvanishing label (label_thin_flow at the source node)
    if demand != None:
        # we compute a thin flow with a nonlabel vanishing source label
        # equal to b[source]/demand
        # For computing such a thin flow, we come back to the first example
        # adding a dummy source node s0 with a new edge of capacity equl to demand.
        # Doing that the label of the source is equal to b[source]/demand
        G.add_node('s0')
        G.add_edge('s0',source, flow = 0,  capacity = demand)
        b['s0']= b[source]
        b[source] = 0.0
        oldsource=source
        source = 's0'
    #else :
        # we compute a thin flow with a vanishing source label
        # the demand is considered to be infinity
        # and the source node label is equal to zero


    G_anchored=nx.MultiDiGraph.copy(G)
    # for ntail,nbrs in E1.adjacency_iter():
    #         for nhead,eattr in nbrs.items():
    #             for k,keydata in eattr.items():
    #                 key = E1[ntail][nhead]['key']
    #                 G_anchored.remove_edge(ntail,head,key)
    #                 G_anchored.add_edge(source,nhead, flow = 0,capacity=G[e[0]][e[1]][key]['capacity'])


    for e in E1.edges(keys=True):
        print_debug( "e in E1", e)
        G_anchored.remove_edge(e[0],e[1],e[2])
        keys_anchored=0
        for e_anchored in  G_anchored.edges(source, keys=True):
            if e_anchored[1] == e[1]:
                keys_anchored += 1                
        G_anchored.add_edge(source,e[1],keys_anchored, flow = 0,capacity=G[e[0]][e[1]][e[2]]['capacity'])
        G[e[0]][e[1]][e[2]]['anchored_edge']=(source,e[1],keys_anchored)
        

    #print_debug("G_anchored")
    #print_debug("b =", b)
    #display_graph(G_anchored,print_debug)


    # Fixed point method
    bi=dict(b)

    err = float('Inf')
    k=1
    while (err >= param.tol_thin_flow and k < param.nmax):
        print_debug( '#################################################################################')
        print( "  Fixed point iteration number :", k, 'erreur :', err, '>=', param.tol_thin_flow)

        biold=dict(bi)
        compute_thin_flow_without_resetting(G_anchored,source,bi,param=param)
        assert_thin_flow_without_resetting(G_anchored,source,bi)
        #update b flows
        bi=dict(b)

        # construct the set of edges in E1 with the key of G to perform the intersection
        #E1_edges_with_right_keys = set( [(e[0],e[1],E1[e[0]][e[1]][e[2]]['key']) for e in E1.edges(keys=True)])

        for e in E1.edges(keys=True):
            a_e = G[e[0]][e[1]][e[2]]['anchored_edge']
            bi[source]= bi[source] + G_anchored[a_e[0]][a_e[1]][a_e[2]]['thin_flow']

        for n in G.nodes():
            for e in set.intersection(set(G.out_edges(n,keys=True)), set(E1.edges(keys=True))) :
                print_debug('e in intersection(set(G.out_edges(n)), set(E1.edges()))', e   )
                a_e = G[e[0]][e[1]][e[2]]['anchored_edge']
                bi[n] = bi[n] -  G_anchored[a_e[0]][a_e[1]][a_e[2]]['thin_flow']

        # test enumeration
        # tol_enumeration = 10e-6
        # P=[]
        # T=[]
        # for e in G.edges(keys=True):
        #     if e in  E1.edges(keys=True) :
        #         G[e[0]][e[1]][e[2]]['thin_flow']=G_anchored[source][e[1]][e[2]]['thin_flow']
        #     else:
        #         G[e[0]][e[1]][e[2]]['thin_flow']=G_anchored[e[0]][e[1]][e[2]]['thin_flow']

        # for n in  G_anchored.nodes():
        #     G.node[n]['label_thin_flow'] =  G_anchored.node[n]['label_thin_flow']

        # for e in G.edges(keys=True):
        #     if G[e[0]][e[1]][e[2]]['thin_flow'] >= tol_enumeration :
        #         P.append(e)
        # for e in E1.edges(keys=True):
        #     T.append(e)
        # for e in  set.difference (set(G.edges(keys=True)), set(E1.edges(keys=True)) ):
        #     if (G.node[e[0]]['label_thin_flow'] <= G[e[0]][e[1]][e[2]]['thin_flow']/G_anchored[e[0]][e[1]][e[2]]['capacity'] ):
        #         T.append(e)

        # print("P=",P)
        # print("T=",T)
        err = 0.0
        #print_debug( "biold = ", biold)
        #print_debug( "bi = ", bi)
        for n in  G.nodes():
            err = err + abs(bi[n]-biold[n])
        #err= err/G.number_of_nodes()
        #raw_input()
        k =k+1

    if (k < param.nmax) :
        print( "  Fixed point suceeded. number of iterations :", k, 'erreur :', err, '<=', param.tol_thin_flow)
    else:
        print( "  Fixed point number of iterations max reached :", k, 'erreur :', err, '>', param.tol_thin_flow)

    for e in G.edges(keys=True):
        if e in  E1.edges(keys=True) :
            a_e = G[e[0]][e[1]][e[2]]['anchored_edge']
            G[e[0]][e[1]][e[2]]['thin_flow']=G_anchored[a_e[0]][a_e[1]][a_e[2]]['thin_flow']
        else:
            G[e[0]][e[1]][e[2]]['thin_flow']=G_anchored[e[0]][e[1]][e[2]]['thin_flow']

    for n in  G_anchored.nodes():
        G.node[n]['label_thin_flow'] =  G_anchored.node[n]['label_thin_flow']


    # if debug_check :
    #     b_check=dict(bi)
    #     for e in E1.edges(keys=True):
    #         b_check[source]= b_check[source] - G_anchored[source][e[1]][e[2]]['thin_flow']

    #     for n in G.nodes():
    #         for e in set.intersection(set(G.out_edges(n,keys=True)), set(E1.edges(keys=True))) :
    #             print_debug('e in intersection(set(G.out_edges(n)), set(E1.edges()))', e   )
    #             b_check[n] = b_check[n] +  G_anchored[source][e[1]][e[2]]['thin_flow']

    #     for n in G.nodes():
    #         assert(abs(b_check[n]-b[n]) <= param.tol_thin_flow)
        
    #print_debug('G:')
    #display_graph(G,print_debug)


    if demand!=None :
        G.remove_node('s0')
        source=oldsource
        b[source]=b['s0']
        b['s0']=None


    print_debug('################ end compute_thin_flow ###############')




def compute_thin_flow_ofzerosize(G, source, b, E1):
    """

    """
    print_debug('################ start compute_thin_flow_ofzerosize ###############')
    if  not(G.is_multigraph() and G.is_directed()):
        raise RuntimeError("Flows module deals only with nx.MultiDiGraph\n \
        If your graph is not a MultiDiGraph, you can copy it with nx.MultiDiGraph.copy(G) ")

    if (list(nx.simple_cycles(G)) != [])  :
        raise RuntimeError("Compute_thin_flow_ofzerosize FAILED. G is not an acyclic directed graph")


    # set the trivial value for the thin_flow
    for ntail,nbrs in G.adjacency_iter():
        G.node[ntail]['label_thin_flow'] = None
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                G[ntail][nhead][k]['thin_flow'] = 0.0

    # compute the associated label in topological order
    sorted_nodes =  nx.topological_sort(G)

    if (source != sorted_nodes[0]):
        raise RuntimeError( ' compute_thin_flow_ofzerosize(G,source, b, E1) FAILED\n \
        source = %s\n \
        sorted_nodes[0]= %s '%source%sorted_nodes[0])


    G.node[source]['label_thin_flow']=1.0

    for v in sorted_nodes[1:len(sorted_nodes)]:
        in_edges = G.in_edges(v,keys=True)
        e=in_edges[0]
        if G[e[0]][e[1]][e[2]]['capacity'] < 1e-14 :
            print('problem in computing congestion label with a very small (< 1e-14) capacity')
            raise ZeroDivisionError
        if e in set(E1.edges(keys=True)):
            label_e = G[e[0]][e[1]][e[2]]['thin_flow']/G[e[0]][e[1]][e[2]]['capacity']
        else :
            label_e = max([G[e[0]][e[1]][e[2]]['thin_flow']/G[e[0]][e[1]][e[2]]['capacity'] ,G.node[e[0]]['label_thin_flow'] ])
        G.node[v]['label_thin_flow']= label_e
        for e in in_edges[1:len(in_edges)]:
            if G[e[0]][e[1]][e[2]]['capacity'] < 1e-14  :
                print('problem in computing congestion label with a very small (< 1e-14) capacity')
                raise ZeroDivisionError
            if e in set(E1.edges(keys=True)):
                label_e = G[e[0]][e[1]][e[2]]['thin_flow']/G[e[0]][e[1]][e[2]]['capacity']
            else :
                label_e = max([G[e[0]][e[1]][e[2]]['thin_flow']/G[e[0]][e[1]][e[2]]['capacity'] ,G.node[e[0]]['label_thin_flow'] ])
            G.node[v]['label_thin_flow']=  min([label_e, G.node[v]['label_thin_flow']])

    print_debug('################ end compute_thin_flow_ofzerosize ###############')


def assert_thin_flow(G,source,b,E1,d,param):
    
    if param==None:
        param = parameters()

    tol = param.tol_thin_flow*10
    
    balance = 0.0
    for n in G.nodes():
        balance += b[n]
    assert(abs(balance) <= tol)
    
    for n in G.nodes():
        balance=b[n]
        for e in G.out_edges(n,keys=True):
            balance = balance - G[e[0]][e[1]][e[2]]['thin_flow']
        for e in G.in_edges(n,keys=True):
            balance = balance + G[e[0]][e[1]][e[2]]['thin_flow']
        assert(abs(balance) <= tol), ("node balance =", balance )
        
    if (d==0.0):
        assert(abs((G.node[source]['label_thin_flow']- 1.0)) <= tol)
    else:
        assert(abs((G.node[source]['label_thin_flow']- b[source]/d)) <= tol)
        
    for e in E1.edges(keys=True):
        assert(abs((G.node[e[1]]['label_thin_flow']- G[e[0]][e[1]][e[2]]['thin_flow']/G[e[0]][e[1]][e[2]]['capacity']) <= tol))

    for e in set.difference(set(G.edges(keys=True)),set(E1.edges(keys=True))):
        if (G[e[0]][e[1]][e[2]]['thin_flow'] >0) :
            assert(abs((G.node[e[1]]['label_thin_flow']-\
                         max([G[e[0]][e[1]][e[2]]['thin_flow']/G[e[0]][e[1]][e[2]]['capacity'],\
                              G.node[e[0]]['label_thin_flow']]))\
                         <= tol))
        else:
            assert(  G.node[e[1]]['label_thin_flow'] <= G.node[e[0]]['label_thin_flow'] )


def assert_thin_flow_without_resetting(G,source,b,d=None, param=None):

    if param==None:
        param = parameters()

    tol = param.tol_thin_flow
    balance = 0.0
    for n in G.nodes():
        balance += b[n]
    assert(abs(balance) <= tol)

    
    for n in G.nodes():
        balance=b[n]
        for e in G.out_edges(n,keys=True):
            balance = balance - G[e[0]][e[1]][e[2]]['thin_flow']
        for e in G.in_edges(n,keys=True):
            balance = balance + G[e[0]][e[1]][e[2]]['thin_flow']
        assert(abs(balance) <= tol), "node" 


    if (d==None):
        assert (abs((G.node[source]['label_thin_flow']- 0.0)) <= tol)
    else:
        if (d==0.0):
            assert (abs((G.node[source]['label_thin_flow']- 1.0)) <= tol)
        else:
            assert(abs((G.node[source]['label_thin_flow']- b[source]/d)) <= tol)

    for e in set(G.edges(keys=True)):
        if (G[e[0]][e[1]][e[2]]['thin_flow'] >0) :
           assert(abs((G.node[e[1]]['label_thin_flow']-\
                         max([G[e[0]][e[1]][e[2]]['thin_flow']/G[e[0]][e[1]][e[2]]['capacity'],\
                              G.node[e[0]]['label_thin_flow']]))\
                         <= tol))
        else:
            assert (  G.node[e[1]]['label_thin_flow'] <= G.node[e[0]]['label_thin_flow'] )




def feasible_time_extension_by_LP(G,E,E_star,E_comp):

    alpha =0.0


    lp = swiglpk.glp_create_prob();
    swiglpk.glp_set_prob_name(lp, "feasible_extension")
    swiglpk.glp_set_obj_dir(lp, swiglpk.GLP_MAX);

    ncol=1
    nrow=E_star.number_of_edges()+ E_comp.number_of_edges()

    if (ncol ==0 or nrow ==0):
        print('Warning: no edges in the problem of sparsest cut')
        #quit()
        return 0.0,[],[n for n in G.edges()]

    swiglpk.glp_add_cols(lp, ncol);
    swiglpk.glp_set_col_name(lp, 1, "alpha");
    swiglpk.glp_set_col_bnds(lp, 1, swiglpk.GLP_LO, 0.0, 0.0);
    swiglpk.glp_set_obj_coef(lp, 1, 1.0);

    # size of the sparse storage of A
    nnz=nrow
    print_debug('nnz=',nnz)

    ia = swiglpk.intArray(nnz); ja = swiglpk.intArray(nnz); ar = swiglpk.doubleArray(nnz);


    swiglpk.glp_add_rows(lp,nrow);
    i=0
    nz=0
    for e in E_star.edges(keys=True):
        i=i+1
        name = 'E_star_' + str(e[0])+str(e[1])
        swiglpk.glp_set_row_name(lp, i, name);
        b = E_star[e[0]][e[1]][e[2]]['time'] - (E.node[e[1]]['label']- E.node[e[0]]['label'])
        #if (abs(b) <= machine_epsilon*10):
        #    b=0.0
        print_debug('b=',b)
        swiglpk.glp_set_row_bnds(lp, i, swiglpk.GLP_LO, b, 0.0);
        nz=nz+1
        ia[nz] = i;
        ja[nz] = 1;
        ar[nz] =  E.node[e[1]]['label_thin_flow']-E.node[e[0]]['label_thin_flow'];

    for e in E_comp.edges(keys=True):
        i=i+1

        name = 'E_comp_' + str(e[0])+str(e[1])
        print_debug('i=',i)

        swiglpk.glp_set_row_name(lp, i, name);
        print_debug('time=',E_comp[e[0]][e[1]][e[2]]['time'])
        b = E_comp[e[0]][e[1]][e[2]]['time'] - (E.node[e[1]]['label']-E.node[e[0]]['label'])
        print_debug('b=',b)
        swiglpk.glp_set_row_bnds(lp, i, swiglpk.GLP_UP, 0.0, b);
        nz=nz+1
        ia[nz] = i;
        ja[nz] = 1;
        ar[nz] =  E.node[e[1]]['label_thin_flow']-E.node[e[0]]['label_thin_flow'];


    print_debug('nz =', nz)
    swiglpk.glp_load_matrix(lp, nz, ia, ja, ar);

    # Write the lp into a file.
    swiglpk.glp_write_lp(lp, None, 'feasible_extension_glpk.lp');

    # solve the lp by simplex
    info = swiglpk.glp_simplex(lp, None);
    if (info):
        raise RuntimeError('GLPK solver failed')
    else :
        print_debug('GLPK solver succeeded')



    # retrieve values
    print_debug('info=',info)
    status = swiglpk.glp_get_status(lp)
    print_debug('status = ', status)
    if (status==swiglpk.GLP_UNBND):
        alpha = float('inf')
    else:
        alpha = swiglpk.glp_get_obj_val(lp)
    print_debug("alpha = ", alpha)

    swiglpk.glp_delete_prob(lp)

    return alpha

def feasible_time_extension(G,E,E_star,E_comp):

    alpha = float('inf')

    for e in E_comp.edges(keys=True):
        denominator = E.node[e[1]]['label_thin_flow']-E.node[e[0]]['label_thin_flow']
        numerator = E_comp[e[0]][e[1]][e[2]]['time'] - (E.node[e[1]]['label']-E.node[e[0]]['label'])
        if denominator > 0 :
            alpha = min(alpha,numerator/denominator)
        #else :
        #    alpha = min(alpha,float('inf'))

    print_debug("alpha (after inequality on E_comp) = ", alpha)

    for e in E_star.edges(keys=True):
        denominator = E.node[e[1]]['label_thin_flow']-E.node[e[0]]['label_thin_flow']
        numerator = E_star[e[0]][e[1]][e[2]]['time'] - (E.node[e[1]]['label']-E.node[e[0]]['label'])
        #if (abs(numerator) < machine_epsilon*10):
        #    numerator = 0.0
        if denominator < 0 :
            alpha = min(alpha,numerator/denominator)

    print_debug("alpha (after inequality on E_star) = ", alpha)
    assert(alpha>0)
    return alpha






def compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow, param=None):

    if param==None:
        param = parameters()



    if G.in_edges(source) != []:
        print_debug("Warning incoming edges in source:")
        print_debug("G.in_edges(source) =",G.in_edges(source))
        for e in G.in_edges(source,keys=True):
            G.remove_edge(*e)
        print_debug("G.in_edges(source) =",G.in_edges(source))
        print_debug("G.out_edges(source) =",G.out_edges(source))
        print_debug("G.is_multigraph",G.is_multigraph())
        print_debug("G.is_directed",G.is_directed)
        #raw_input()

    # The disjkstra algorithm for shortest path seems to be adapted for multigraph
    # it seems that it uses the mimimal weight over the common edges between to nodes
    # a post-processing is then needed to know the edge that is really in the shortest path.
    length,path=nx.single_source_dijkstra(G, source, weight='time')

    N = len(timeofevent)-1  # initial number of events

    # compute the initial labels and flows.
    i = 0 # first events
    t_i= timeofevent[i]
    for ntail,nbrs in G.adjacency_iter():
        G.node[ntail]['label'] = length[ntail]
        G.node[ntail]['label_overtime']=[length[ntail]]
        G.node[ntail]['label_thin_flow_overtime']=[]
        for nhead,eattr in nbrs.items():
             for k,keydata in eattr.items():
                 #print( "node  ntail=",ntail)
                 #print( "node  nhead=",nhead)
                 #print("k=",k)
                 G[ntail][nhead][k]['x']=0.0
                 G[ntail][nhead][k]['x_overtime']=[0.0]
                 G[ntail][nhead][k]['thin_flow_overtime']=[]


    display_graph(G,print_debug)
    Nmax=50
    while (i<N):
        print('#################################################################################')
        print("  Start integration step i = ",i,"<",N ,"on the interval  [", timeofevent[i] , ",", timeofevent[i+1] , "]" )
        print(' ' )
        
        # Compute the current_shortest_path_graph based on label in G
        E,Estar,E_comp=current_shortest_path_graph(G,source,sink)

        print('# nodes =', len(G.nodes()),\
              '     # edges =', len(G.edges()),\
              '     # edges in E =', len(E.edges()),\
              '     # edges in Estar=', len(Estar.edges()))
        print(' ')
        
        print_debug ("E.edges()=", E.edges())
        print_debug ("Estar.edges()=", Estar.edges())
        print_debug ("E_comp.edges()=", E_comp.edges())
        
        
        # set the value of the flow input
        u= {} # dictionary of flows in nodes
        for n in G.nodes():
            u[n] =0.0
        u[source] = inputflow[i]
        u[sink] = - inputflow[i]
        d= inputflow[i]

        # Compute thin flow and associated labels (label_thin_flow) on E
        if (d == 0.0) :
            compute_thin_flow_ofzerosize(E,source,u,Estar)
        else:
            compute_thin_flow(E,source,u,Estar,d, param)

        #display_graph(E)

        assert_thin_flow(E,source,u,Estar,d,param)

        # set the thin flow  and associated labels (label_thin_flow) for the whole graph G
        for ntail,nbrs in E_comp.adjacency_iter():
            for nhead,eattr in nbrs.items():
                for k,keydata in eattr.items():
                    print_debug("Insert thin flow from Ecomp to G for edge", nhead, ntail, "and key", k)
                    G[ntail][nhead][k]['thin_flow'] = 0.0
                    G[ntail][nhead][k]['thin_flow_overtime'].append(0.0)

        for ntail,nbrs in E.adjacency_iter():
            G.node[ntail]['label_thin_flow'] = E.node[ntail]['label_thin_flow']
            G.node[ntail]['label_thin_flow_overtime'].append( E.node[ntail]['label_thin_flow'])
            for nhead,eattr in nbrs.items():
                for k,keydata in eattr.items():
                    print_debug("Insert thin flow from E to G for edge", nhead, ntail, "and key", k)
                    G[ntail][nhead][k]['thin_flow'] =  E[ntail][nhead][k]['thin_flow']
                    G[ntail][nhead][k]['thin_flow_overtime'].append(E[ntail][nhead][k]['thin_flow'])




        #print_debug( "G (after setting the thin flow) :")
        #display_graph(G,print_debug)

        # compute the length of the time--step (alpha).
        alpha = feasible_time_extension(G,E,Estar,E_comp)
        #alpha = feasible_time_extension_by_LP(G,E,Estar,E_comp)
        print_debug ('   alpha=',alpha,"timeofevent=",timeofevent)
        if (alpha <= 1e-12):
            raise RuntimeError("alpha too small")
        
        # compute new time--step.
        h = t_i # store ti
        if (t_i+alpha >= timeofevent[i+1]):
            print_debug('alpha =',alpha,' is greater or equal that the next scheduled step')
            t_i = timeofevent[i+1]
        else:
            print_debug('alpha=',alpha,' is strictly lower that the next scheduled step')
            print_debug('an event is added')

            t_i = t_i + alpha
            timeofevent.insert(i+1,t_i)
            inputflow.insert(i+1,inputflow[i])

            N=N+1
        h = t_i - h

       
        

        # integrate x and labels with respect to time.
        for ntail,nbrs in G.adjacency_iter():
            G.node[ntail]['label'] = G.node[ntail]['label'] + G.node[ntail]['label_thin_flow']*h
            G.node[ntail]['label_overtime'].append(G.node[ntail]['label'])
            for nhead,eattr in nbrs.items():
                for k,keydata in eattr.items():
                    G[ntail][nhead][k]['x']=G[ntail][nhead][k]['x'] + G[ntail][nhead][k]['thin_flow']*h
                    G[ntail][nhead][k]['x_overtime'].append(G[ntail][nhead][k]['x'])

        #print_debug( "G :")
        #display_graph(G,print_debug)

        i=i+1
        print( "  End integration i = ",i-1, "with time--step h=", h," on the interval [", timeofevent[i-1] , ",", timeofevent[i] , "]")
        print( '#################################################################################\n')
        #raw_input()

def compute_dynamic_equilibrium_timestepping(G, source, sink, h, t0, N, flow_function, param=None):

    if param==None:
        param = parameters()

    # The disjkstra algorithm for shortest path seems to be adapted for multigraph
    # it seems that it uses the mimimal weight over the common edges between to nodes
    # a post-processing is then needed to know the edge that is really in the shortest path.
    length,path=nx.single_source_dijkstra(G,source, weight='time')

    
    # compute the initial labels and flows.
    i = 0 # first events
    t_i= t0
    for ntail,nbrs in G.adjacency_iter():
        G.node[ntail]['label'] = length[ntail]
        G.node[ntail]['label_overtime']=[length[ntail]]
        G.node[ntail]['label_thin_flow_overtime']=[]
        for nhead,eattr in nbrs.items():
             for k,keydata in eattr.items():
                 #print( "node  ntail=",ntail)
                 #print( "node  nhead=",nhead)
                 #print("k=",k)
                 G[ntail][nhead][k]['x']=0.0
                 G[ntail][nhead][k]['x_overtime']=[0.0]
                 G[ntail][nhead][k]['thin_flow_overtime']=[]

    display_graph(G,print_debug)

    while (i<N):
        print('#################################################################################')
        print("  Start integration step i = ",i,"<",N ,"on the interval  [", t_i , ",", t_i + h , "]" )
        #print(' ' )

        # Compute the current_shortest_path_graph based on label in G
        E,Estar,E_comp=current_shortest_path_graph(G)

        print ("E.edges()=", E.edges())
        print ("Estar.edges()=", Estar.edges())
        print ("E_comp.edges()=", E_comp.edges())
 

        # check that the current shortest path is valid
        for v in G.nodes():
            if (v!= source) :
                while  (list(nx.all_simple_paths(E, source, v)) == []):
                    print ("Current shortest path is not complete. no path from source  ",source  ,v)
                    #try to add a path
                    max_excess = -1e+24
                    for e in G.in_edges(v,keys=True) :
                       excess = G.node[e[0]]['label'] - (G.node[e[1]]['label'] + G[e[0]][e[1]][e[2]]['time'])
                       if excess >= max_excess :
                            max_excess =excess
                            e_max=e
                    print("add edge =", e_max)
                    E.add_edge(e_max[0], e_max[1], e_max[2], G[e_max[0]][e_max[1]][e_max[2]])
                    E_comp.remove_edge(e_max[0], e_max[1], e_max[2])
                # if 
                #     E_comp.add_node(v)
                #     for e in E.out_edges(v,keys=True) :
                #          E_comp.add_edge(e[0], e[1], e[2], G[e[0]][e[1]][e[2]])
                #     E.remove_node(v)
                #     Estar.remove_node(v)

                    
        # check that the current shortest path is valid (for tiemstepping)
        #for v in G.nodes():
            #if (E.in_edges(v) ==[]) :
                #print ("Current shortest path is not complete. no edges entering "  ,v)
                #for 
                
                #raise RuntimeError("")            
                
        
        # set the value of the flow input
        u= {} # dictionary of flows in nodes
        for n in G.nodes():
            u[n] =0.0
        u_i = flow_function(t_i)
        u[source] = u_i
        u[sink] = - u_i
        d = u_i

        # Compute thin flow and associated labels (label_thin_flow) on E
        if (abs (u_i) < machine_epsilon  ) :
            compute_thin_flow_ofzerosize(E,source,u,Estar)
        else:
            compute_thin_flow(E,source,u,Estar,d, param)

        #display_graph(E)

        assert_thin_flow(E,source,u,Estar,d,param)

        # set the thin flow  and associated labels (label_thin_flow) for the whole graph G
        for ntail,nbrs in E_comp.adjacency_iter():
            for nhead,eattr in nbrs.items():
                for k,keydata in eattr.items():
                    print_debug("Insert thin flow from Ecomp to G for edge", nhead, ntail, "and key", k)
                    G[ntail][nhead][k]['thin_flow'] = 0.0
                    G[ntail][nhead][k]['thin_flow_overtime'].append(0.0)

        for ntail,nbrs in E.adjacency_iter():
            G.node[ntail]['label_thin_flow'] = E.node[ntail]['label_thin_flow']
            G.node[ntail]['label_thin_flow_overtime'].append( E.node[ntail]['label_thin_flow'])
            for nhead,eattr in nbrs.items():
                for k,keydata in eattr.items():
                    print_debug("Insert thin flow from E to G for edge", nhead, ntail, "and key", k)
                    G[ntail][nhead][k]['thin_flow'] =  E[ntail][nhead][k]['thin_flow']
                    G[ntail][nhead][k]['thin_flow_overtime'].append(E[ntail][nhead][k]['thin_flow'])

        print_debug( "G (after setting the thin flow) :")
        display_graph(G,print_debug)

        # integrate x and labels with respect to time.
        for ntail,nbrs in G.adjacency_iter():
            G.node[ntail]['label'] = G.node[ntail]['label'] + G.node[ntail]['label_thin_flow']*h
            G.node[ntail]['label_overtime'].append(G.node[ntail]['label'])
            for nhead,eattr in nbrs.items():
                for k,keydata in eattr.items():
                    G[ntail][nhead][k]['x']=G[ntail][nhead][k]['x'] + G[ntail][nhead][k]['thin_flow']*h
                    G[ntail][nhead][k]['x_overtime'].append(G[ntail][nhead][k]['x'])

        print_debug( "G :")
        display_graph(G,print_debug)

        i=i+1
        t_i=t_i+h
        print( "  End integration i = ",i-1, "with time--step h=", h," on the interval [", t_i , ",", t_i+h , "]")
        print( '#################################################################################\n')




def plot_thin_flows_and_labels(G,timeofevent):
    plt.subplot(411)
    plt.grid()
    plt.title('x in edges')
    for ntail,nbrs in G.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                plt.plot(timeofevent[:],G[ntail][nhead][k]['x_overtime'][:],label=repr((ntail,nhead,k)))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)


    plt.subplot(412)
    plt.grid()
    plt.title('thin_flow in edges')
    for ntail,nbrs in G.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                x_plot_data = []
                y_plot_data = []
                for i in range(len(timeofevent[:])-1):
                    x_plot_data.append(timeofevent[i])
                    y_plot_data.append(G[ntail][nhead][k]['thin_flow_overtime'][i])
                    x_plot_data.append(timeofevent[i+1])
                    y_plot_data.append(G[ntail][nhead][k]['thin_flow_overtime'][i])
                plt.plot(x_plot_data[:],y_plot_data[:],label=repr((ntail,nhead,k)))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)

    plt.subplot(413)
    plt.grid()
    plt.title('label in nodes')
    for ntail,nbrs in G.adjacency_iter():
        plt.plot(timeofevent[:],G.node[ntail]['label_overtime'][:],label=repr(ntail))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)


    plt.subplot(414)
    plt.grid()
    plt.title('label_thin_flow in nodes')
    for ntail,nbrs in G.adjacency_iter():
        x_plot_data = []
        y_plot_data = []
        for i in range(len(timeofevent[:])-1):
            x_plot_data.append(timeofevent[i])
            y_plot_data.append(G.node[ntail]['label_thin_flow_overtime'][i])
            x_plot_data.append(timeofevent[i+1])
            y_plot_data.append(G.node[ntail]['label_thin_flow_overtime'][i])
        plt.plot(x_plot_data[:],y_plot_data[:],label=repr(ntail))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)


def postprocess_flows_queues_cumulativeflows(G):
    debug_print= True
    # Compute flows f_e_plus, f_e_minus, F_e_plus, F_e_minus,  on the right interval
    for ntail,nbrs in G.adjacency_iter():
        #G.node[ntail]['shifted_time'] = []
        #for i in range(len(G.node[ntail]['label_overtime'])):
        #    G.node[ntail]['shifted_time'].append( G.node[ntail]['label_overtime'][i])
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                G[ntail][nhead][k]['f_e_plus_overtime'] =[]
                G[ntail][nhead][k]['f_e_minus_overtime'] =[]
                G[ntail][nhead][k]['F_e_plus_overtime'] =[0.0]
                G[ntail][nhead][k]['F_e_minus_overtime'] =[0.0]
                for i in range(len( G[ntail][nhead][k]['thin_flow_overtime'] )):
                    if (G.node[ntail]['label_thin_flow_overtime'][i] >= machine_epsilon):
                        G[ntail][nhead][k]['f_e_plus_overtime'].append(G[ntail][nhead][k]['thin_flow_overtime'][i]/G.node[ntail]['label_thin_flow_overtime'][i])
                    else:
                        G[ntail][nhead][k]['f_e_plus_overtime'].append(0.0)

                    if (G.node[nhead]['label_thin_flow_overtime'][i] >= machine_epsilon):
                        G[ntail][nhead][k]['f_e_minus_overtime'].append(G[ntail][nhead][k]['thin_flow_overtime'][i]/G.node[nhead]['label_thin_flow_overtime'][i])
                    else:
                        G[ntail][nhead][k]['f_e_minus_overtime'].append(0.0)
                        
                for i in range(len( G.node[ntail]['label_overtime'])-1):
                    h= G.node[ntail]['label_overtime'][i+1] -  G.node[ntail]['label_overtime'][i]
                    G[ntail][nhead][k]['F_e_plus_overtime'].append( G[ntail][nhead][k]['f_e_plus_overtime'][i]*h+G[ntail][nhead][k]['F_e_plus_overtime'][i])
                for i in range(len( G.node[nhead]['label_overtime'])-1):
                    h= G.node[nhead]['label_overtime'][i+1] -  G.node[nhead]['label_overtime'][i]
                    G[ntail][nhead][k]['F_e_minus_overtime'].append( G[ntail][nhead][k]['f_e_minus_overtime'][i]*h+G[ntail][nhead][k]['F_e_minus_overtime'][i])

    # Compute queues  on the right interval

    for ntail,nbrs in G.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():

                # Merge the partition of switching times of the F_e_plus and F_e_minus
                switching_times_set=set.union(set(G.node[ntail]['label_overtime']), set(G.node[nhead]['label_overtime']))
                print_debug("switching_times_set = ", switching_times_set)
                switching_times=list(switching_times_set)

                print_debug("compute z_e for edge = ", ntail, nhead)
                print_debug("switching_times = ", switching_times)

                transit_time= G[ntail][nhead][k]['time']

                # Reduce to switching time to the domain of definition of z_e

                switching_times.append(G.node[ntail]['label_overtime'][0])
                switching_times.append(G.node[ntail]['label_overtime'][-1])

                switching_times.append(G.node[ntail]['label_overtime'][0]-transit_time)
                switching_times.append(G.node[ntail]['label_overtime'][-1]-transit_time)

                switching_times.sort()
                if len(switching_times)>0:
                    while (switching_times[-1] > G.node[ntail]['label_overtime'][-1]):
                        switching_times.pop()
                        if len(switching_times) == 0 : break

                if len(switching_times)>0:
                    while (switching_times[-1] > G.node[nhead]['label_overtime'][-1]-transit_time ):
                        switching_times.pop()
                        if len(switching_times) == 0 : break

                switching_times.reverse()

                if len(switching_times)>0:
                    while (switching_times[-1] < G.node[ntail]['label_overtime'][0] ):
                        switching_times.pop()
                        if len(switching_times) == 0 : break
                if len(switching_times)>0:
                    while (switching_times[-1] < G.node[nhead]['label_overtime'][0]-transit_time):
                        switching_times.pop()
                        if len(switching_times) == 0 : break

                switching_times.reverse()
                print_debug("switching_times (after) = ", switching_times)





                G[ntail][nhead][k]['switching_times'] =  switching_times
                # perform the computation of z_e at each switching time
                G[ntail][nhead][k]['z_e_overtime'] =[]

                for i in range(len(switching_times)):

                    time = switching_times[i]
                    print_debug("  --- switching_times[i] =", switching_times[i])

                    value_F_e_plus=0.0
                    value_F_e_minus=0.0


                    if (G.node[ntail]['label_overtime'][0] == time) :
                        value_F_e_plus = G[ntail][nhead][k]['F_e_plus_overtime'][0]
                        print_debug("   F_e_plus(", switching_times[i],")=", value_F_e_plus)

                    for j in range(len( G.node[ntail]['label_overtime'])-1):
                        if (G.node[ntail]['label_overtime'][j+1] == time) :
                            value_F_e_plus = G[ntail][nhead][k]['F_e_plus_overtime'][j+1]
                            print_debug("   F_e_plus(", switching_times[i],")=", value_F_e_plus)

                        print_debug("  interval [a,b]= [",G.node[ntail]['label_overtime'][j], G.node[ntail]['label_overtime'][j+1],"]" )
                        print_debug("  ",(G.node[ntail]['label_overtime'][j] <= time) and (time <(G.node[ntail]['label_overtime'][j+1] ) ))

                        if ((G.node[ntail]['label_overtime'][j] <= time) and (time < (G.node[ntail]['label_overtime'][j+1]) )):
                            h = G.node[ntail]['label_overtime'][j+1] - G.node[ntail]['label_overtime'][j]
                            c = (time - G.node[ntail]['label_overtime'][j]) /h
                            value_F_e_plus =  G[ntail][nhead][k]['F_e_plus_overtime'][j] + c * (G[ntail][nhead][k]['F_e_plus_overtime'][j+1]- G[ntail][nhead][k]['F_e_plus_overtime'][j])
                            print_debug("   F_e_plus(", switching_times[i],")=", value_F_e_plus)

                    time = time + transit_time

                    if (G.node[nhead]['label_overtime'][0] == time) :
                        value_F_e_minus = G[ntail][nhead][k]['F_e_plus_overtime'][0]
                        print_debug("   F_e_minus(", switching_times[i],")=", value_F_e_minus)


                    for j in range(len( G.node[nhead]['label_overtime'])-1):
                        if (G.node[nhead]['label_overtime'][j+1] == time) :
                            value_F_e_minus = G[ntail][nhead][k]['F_e_minus_overtime'][j+1]
                            print_debug("   F_e_minus(", switching_times[i],")=", value_F_e_minus)

                        if ((G.node[nhead]['label_overtime'][j] <= time) and (time < (G.node[nhead]['label_overtime'][j+1]) )):
                            h = G.node[nhead]['label_overtime'][j+1] - G.node[nhead]['label_overtime'][j]
                            c = (time - G.node[nhead]['label_overtime'][j]) /h
                            value_F_e_minus =  G[ntail][nhead][k]['F_e_minus_overtime'][j] + c * (G[ntail][nhead][k]['F_e_minus_overtime'][j+1]- G[ntail][nhead][k]['F_e_minus_overtime'][j])
                            print_debug("   F_e_minus(", switching_times[i]+transit_time,")=",value_F_e_minus)


                    G[ntail][nhead][k]['z_e_overtime'].append(value_F_e_plus-value_F_e_minus)
    debug_print= False

def plot_flows_queues_cumulativeflows(G, edge=None, key=None):


    if edge!=None :
        if G.is_multigraph():
            G_plot=nx.MultiDiGraph()
            G_plot.add_nodes_from(G.nodes(data=True))
            if key==None :
                raise RuntimeError('plot_flows_queues_cumulativeflows(G, edge=None, key=None): FAILED key is needed')
            G_plot.add_edges_from([(edge[0],edge[1],G[edge[0]][edge[1]][key])])
        else:
            G_plot=nx.MultiDiGraph()
            G_plot.add_nodes_from(G.nodes(data=True))
            G_plot.add_edges_from([(edge[0],edge[1],G[edge[0]][edge[1]])])
    else:
        if G.is_multigraph():
            G_plot = G
        else:
            G_plot=nx.MultiDiGraph.copy(G)


    min_x=0.0
    max_x=0.0
    for ntail,nbrs in G_plot.adjacency_iter():
        max_x =max([max_x, max(G_plot.node[ntail]['label_overtime'])])


    plt.subplot(511)
    plt.grid()
    plt.title('f_e_plus in edges')

    for ntail,nbrs in G_plot.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                x_plot_data = []
                y_plot_data = []
                for i in range(len(G_plot.node[ntail]['label_overtime'])-1):
                    x_plot_data.append(G_plot.node[ntail]['label_overtime'][i])
                    y_plot_data.append(G_plot[ntail][nhead][k]['f_e_plus_overtime'][i])
                    x_plot_data.append(G_plot.node[ntail]['label_overtime'][i+1])
                    y_plot_data.append(G_plot[ntail][nhead][k]['f_e_plus_overtime'][i])
                plt.plot(x_plot_data[:],y_plot_data[:],label=repr((ntail,nhead,k)))

    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([min_y-0.1,max_y+0.1])

    plt.subplot(512)
    plt.grid()
    plt.title('f_e_minus in edges')

    for ntail,nbrs in G_plot.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                x_plot_data = []
                y_plot_data = []
                for i in range(len(G_plot.node[nhead]['label_overtime'])-1):
                    x_plot_data.append(G_plot.node[nhead]['label_overtime'][i])
                    y_plot_data.append(G_plot[ntail][nhead][k]['f_e_minus_overtime'][i])
                    x_plot_data.append(G_plot.node[nhead]['label_overtime'][i+1])
                    y_plot_data.append(G_plot[ntail][nhead][k]['f_e_minus_overtime'][i])
                plt.plot(x_plot_data[:],y_plot_data[:],label=repr((ntail,nhead,k)))


    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([min_y-0.1,max_y+0.1])

    plt.subplot(513)
    plt.grid()
    plt.title('F_e_plus in edges')
    for ntail,nbrs in G_plot.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                plt.plot(G_plot.node[ntail]['label_overtime'][:],G_plot[ntail][nhead][k]['F_e_plus_overtime'][:]   ,label=repr((ntail,nhead,k)))
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([min_y-0.1,max_y+0.1])

    plt.subplot(514)
    plt.grid()
    plt.title('F_e_minus in edges')
    for ntail,nbrs in G_plot.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                plt.plot(G_plot.node[nhead]['label_overtime'][:],G_plot[ntail][nhead][k]['F_e_minus_overtime'][:]   ,label=repr((ntail,nhead,k)))
    plt.xlim([min_x,max_x])
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([min_y-0.1,max_y+0.1])

    plt.subplot(515)
    plt.grid()
    plt.title('z_e in edges')
    for ntail,nbrs in G_plot.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                plt.plot(G_plot[ntail][nhead][k]['switching_times'][:],G_plot[ntail][nhead][k]['z_e_overtime'][:]   ,label=repr((ntail,nhead,k)))
    plt.xlim([min_x,max_x])
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([min_y-0.1,max_y+0.1])


def postprocess_flows_queues_cumulativeflows_timestepping(G,timesteps):
    debug_print= True
    # Compute flows f_e_plus, f_e_minus, F_e_plus, F_e_minus,  on the right interval
    for ntail,nbrs in G.adjacency_iter():
        #G.node[ntail]['shifted_time'] = []
        #for i in range(len(G.node[ntail]['label_overtime'])):
        #    G.node[ntail]['shifted_time'].append( G.node[ntail]['label_overtime'][i])
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                G[ntail][nhead][k]['f_e_plus_overtime'] =[]
                G[ntail][nhead][k]['f_e_minus_overtime'] =[]
                G[ntail][nhead][k]['F_e_plus_overtime'] =[0.0]
                G[ntail][nhead][k]['F_e_minus_overtime'] =[0.0]
                for i in range(len( G[ntail][nhead][k]['thin_flow_overtime'] )):
                    if (G.node[ntail]['label_thin_flow_overtime'][i] !=0):
                        G[ntail][nhead][k]['f_e_plus_overtime'].append(G[ntail][nhead][k]['thin_flow_overtime'][i]/G.node[ntail]['label_thin_flow_overtime'][i])
                    else:
                        G[ntail][nhead][k]['f_e_plus_overtime'].append(0.0)
                    if (G.node[nhead]['label_thin_flow_overtime'][i] !=0):
                        G[ntail][nhead][k]['f_e_minus_overtime'].append(G[ntail][nhead][k]['thin_flow_overtime'][i]/G.node[nhead]['label_thin_flow_overtime'][i])
                    else:
                        G[ntail][nhead][k]['f_e_minus_overtime'].append(0.0)

                for i in range(len( G.node[ntail]['label_overtime'])-1):
                    h= G.node[ntail]['label_overtime'][i+1] -  G.node[ntail]['label_overtime'][i]
                    G[ntail][nhead][k]['F_e_plus_overtime'].append( G[ntail][nhead][k]['f_e_plus_overtime'][i]*h+G[ntail][nhead][k]['F_e_plus_overtime'][i])
                for i in range(len( G.node[nhead]['label_overtime'])-1):
                    h= G.node[nhead]['label_overtime'][i+1] -  G.node[nhead]['label_overtime'][i]
                    G[ntail][nhead][k]['F_e_minus_overtime'].append( G[ntail][nhead][k]['f_e_minus_overtime'][i]*h+G[ntail][nhead][k]['F_e_minus_overtime'][i])
    # Compute queues  on the right interval

    for ntail,nbrs in G.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():

                # Merge the partition of switching times of the F_e_plus and F_e_minus
                switching_times_set=set.union(set(G.node[ntail]['label_overtime']), set(G.node[nhead]['label_overtime']))
                print_debug("switching_times_set = ", switching_times_set)
                switching_times=list(switching_times_set)

                print_debug("compute z_e for edge = ", ntail, nhead)
                print_debug("switching_times = ", switching_times)

                transit_time= G[ntail][nhead][k]['time']

                # Reduce to switching time to the domain of definition of z_e


                switching_times.append(G.node[ntail]['label_overtime'][0])
                switching_times.append(G.node[ntail]['label_overtime'][-1])

                switching_times.append(G.node[ntail]['label_overtime'][0]-transit_time)
                switching_times.append(G.node[ntail]['label_overtime'][-1]-transit_time)

                switching_times.sort()

                while (switching_times[-1] > G.node[ntail]['label_overtime'][-1]):
                    switching_times.pop()


                while (switching_times[-1] > G.node[nhead]['label_overtime'][-1]-transit_time):
                    switching_times.pop()

                switching_times.reverse()


                while (switching_times[-1] < G.node[ntail]['label_overtime'][0]):
                    switching_times.pop()

                while (switching_times[-1] < G.node[nhead]['label_overtime'][0]-transit_time):
                    switching_times.pop()

                switching_times.reverse()
                print_debug("switching_times (after) = ", switching_times)





                G[ntail][nhead][k]['switching_times'] =  switching_times
                # perform the computation of z_e at each switching time
                G[ntail][nhead][k]['z_e_overtime'] =[]

                for i in range(len(switching_times)):

                    time = switching_times[i]
                    print_debug("  --- switching_times[i] =", switching_times[i])

                    value_F_e_plus=0.0
                    value_F_e_minus=0.0


                    if (G.node[ntail]['label_overtime'][0] == time) :
                        value_F_e_plus = G[ntail][nhead][k]['F_e_plus_overtime'][0]
                        print_debug("   F_e_plus(", switching_times[i],")=", value_F_e_plus)

                    for j in range(len( G.node[ntail]['label_overtime'])-1):
                        if (G.node[ntail]['label_overtime'][j+1] == time) :
                            value_F_e_plus = G[ntail][nhead][k]['F_e_plus_overtime'][j+1]
                            print_debug("   F_e_plus(", switching_times[i],")=", value_F_e_plus)

                        print_debug("  interval [a,b]= [",G.node[ntail]['label_overtime'][j], G.node[ntail]['label_overtime'][j+1],"]" )
                        print_debug("  ",(G.node[ntail]['label_overtime'][j] <= time) and (time <(G.node[ntail]['label_overtime'][j+1] ) ))

                        if ((G.node[ntail]['label_overtime'][j] <= time) and (time < (G.node[ntail]['label_overtime'][j+1]) )):
                            h = G.node[ntail]['label_overtime'][j+1] - G.node[ntail]['label_overtime'][j]
                            c = (time - G.node[ntail]['label_overtime'][j]) /h
                            value_F_e_plus =  G[ntail][nhead][k]['F_e_plus_overtime'][j] + c * (G[ntail][nhead][k]['F_e_plus_overtime'][j+1]- G[ntail][nhead][k]['F_e_plus_overtime'][j])
                            print_debug("   F_e_plus(", switching_times[i],")=", value_F_e_plus)

                    time = time + transit_time

                    if (G.node[nhead]['label_overtime'][0] == time) :
                        value_F_e_minus = G[ntail][nhead][k]['F_e_plus_overtime'][0]
                        print_debug("   F_e_minus(", switching_times[i],")=", value_F_e_minus)


                    for j in range(len( G.node[nhead]['label_overtime'])-1):
                        if (G.node[nhead]['label_overtime'][j+1] == time) :
                            value_F_e_minus = G[ntail][nhead][k]['F_e_minus_overtime'][j+1]
                            print_debug("   F_e_minus(", switching_times[i],")=", value_F_e_minus)

                        if ((G.node[nhead]['label_overtime'][j] <= time) and (time < (G.node[nhead]['label_overtime'][j+1]) )):
                            h = G.node[nhead]['label_overtime'][j+1] - G.node[nhead]['label_overtime'][j]
                            c = (time - G.node[nhead]['label_overtime'][j]) /h
                            value_F_e_minus =  G[ntail][nhead][k]['F_e_minus_overtime'][j] + c * (G[ntail][nhead][k]['F_e_minus_overtime'][j+1]- G[ntail][nhead][k]['F_e_minus_overtime'][j])
                            print_debug("   F_e_minus(", switching_times[i]+transit_time,")=",value_F_e_minus)


                    G[ntail][nhead][k]['z_e_overtime'].append(value_F_e_plus-value_F_e_minus)


    
def plot_flows_queues_cumulativeflows_timestepping(G, timesteps, edge=None, key=None):


    if edge!=None :
        if G.is_multigraph():
            G_plot=nx.MultiDiGraph()
            G_plot.add_nodes_from(G.nodes(data=True))
            if key==None :
                raise RuntimeError('plot_flows_queues_cumulativeflows(G, edge=None, key=None): FAILED key is needed')
            G_plot.add_edges_from([(edge[0],edge[1],G[edge[0]][edge[1]][key])])
        else:
            G_plot=nx.MultiDiGraph()
            G_plot.add_nodes_from(G.nodes(data=True))
            G_plot.add_edges_from([(edge[0],edge[1],G[edge[0]][edge[1]])])
    else:
        if G.is_multigraph():
            G_plot = G
        else:
            G_plot=nx.MultiDiGraph.copy(G)


    min_x=0.0
    max_x=0.0
    for ntail,nbrs in G_plot.adjacency_iter():
        max_x =max([max_x, max(G_plot.node[ntail]['label_overtime'])])

    offset_y =0.2

    plt.subplot(511)
    plt.grid()
    plt.title('f_e_plus in edges')

    for ntail,nbrs in G_plot.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                x_plot_data = []
                y_plot_data = []
                for i in range(len(timesteps)-1):
                    x_plot_data.append(G_plot.node[ntail]['label_overtime'][i])
                    y_plot_data.append(G_plot[ntail][nhead][k]['f_e_plus_overtime'][i])
                    x_plot_data.append(G_plot.node[ntail]['label_overtime'][i+1])
                    y_plot_data.append(G_plot[ntail][nhead][k]['f_e_plus_overtime'][i])

                print_debug("x_plot_data=",x_plot_data)
                plt.plot(x_plot_data[:],y_plot_data[:],label=repr((ntail,nhead,k)))

    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([min_y-offset_y,max_y+offset_y])

    plt.subplot(512)
    plt.grid()
    plt.title('f_e_minus in edges')

    for ntail,nbrs in G_plot.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                x_plot_data = []
                y_plot_data = []
                for i in range(len(timesteps)-1):
                    x_plot_data.append(G_plot.node[ntail]['label_overtime'][i])
                    y_plot_data.append(G_plot[ntail][nhead][k]['f_e_minus_overtime'][i])
                    x_plot_data.append(G_plot.node[ntail]['label_overtime'][i+1])
                    y_plot_data.append(G_plot[ntail][nhead][k]['f_e_minus_overtime'][i])
                plt.plot(x_plot_data[:],y_plot_data[:],label=repr((ntail,nhead,k)))


    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([min_y-offset_y,max_y+offset_y])

    plt.subplot(513)
    plt.grid()
    plt.title('F_e_plus in edges')
    for ntail,nbrs in G_plot.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                plt.plot(G_plot.node[ntail]['label_overtime'][:],G_plot[ntail][nhead][k]['F_e_plus_overtime'][:]   ,label=repr((ntail,nhead,k)))
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([min_y-offset_y,max_y+offset_y])

    plt.subplot(514)
    plt.grid()
    plt.title('F_e_minus in edges')
    for ntail,nbrs in G_plot.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                plt.plot(G_plot.node[nhead]['label_overtime'][:],G_plot[ntail][nhead][k]['F_e_minus_overtime'][:]   ,label=repr((ntail,nhead,k)))
    plt.xlim([min_x,max_x])
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([min_y-offset_y,max_y+offset_y])

    plt.subplot(515)
    plt.grid()
    plt.title('z_e in edges')
    for ntail,nbrs in G_plot.adjacency_iter():
        for nhead,eattr in nbrs.items():
            for k,keydata in eattr.items():
                plt.plot(G_plot[ntail][nhead][k]['switching_times'][:],G_plot[ntail][nhead][k]['z_e_overtime'][:]   ,label=repr((ntail,nhead,k)))
    plt.xlim([min_x,max_x])
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([min_y-offset_y,max_y+offset_y])


def f_e_minus(G, e, time):
    ntail = e[0]
    nhead = e[1]
    key = e[2]
    if time < G.node[nhead]['label_overtime'][0]:
        return 0.0
    for j in range(len( G.node[nhead]['label_overtime'])-1):
        if ((G.node[nhead]['label_overtime'][j] <= time) and (time <= (G.node[nhead]['label_overtime'][j+1]) )):
            return G[ntail][nhead][key]['f_e_minus_overtime'][j]
    print("Warning: time ='",time, "is out of range of definition of f_e_minus")
    return -1.0

def f_e_plus(G, e, time):
    ntail = e[0]
    nhead = e[1]
    key = e[2]
    if time < G.node[ntail]['label_overtime'][0]:
        return 0.0
    for j in range(len( G.node[ntail]['label_overtime'])-1):
        if ((G.node[ntail]['label_overtime'][j] <= time) and (time <= (G.node[ntail]['label_overtime'][j+1]))):
            return G[ntail][nhead][key]['f_e_plus_overtime'][j]
    print("Warning: time =",time, "is out of range of definition of f_e_plus")

    return 1e+24



def postprocess_extravalues(G, source, sink):

    simpleG = nx.DiGraph()
    simpleG.add_nodes_from(G.nodes())
    for e in G.edges(keys=True):
        if e[2] ==0 :
            simpleG.add_edge(e[0],e[1], capacity=G[e[0]][e[1]][e[2]]['capacity'])
        else :
            simpleG[e[0]][e[1]]['capacity'] = simpleG[e[0]][e[1]]['capacity'] + G[e[0]][e[1]][e[2]]['capacity']


    cut_value, partition = nx.minimum_cut(simpleG, source, sink)
    X, Xbar = partition
    print(cut_value, partition)
    G.name=dict([])
    G.name['max_flow']= cut_value
 
    G.name['X']= X
    G.name['Xbar']= Xbar


    edges_cut =set.intersection(set(G.out_edges(X,keys=True)),set(G.in_edges(Xbar,keys=True)))
    G.name['edges_cut']= edges_cut

    print (edges_cut)

    switch_time_f_e_minus=[]
    Tmax_minus=1e+24
    for e  in edges_cut:
        Tmax_minus=min(Tmax_minus,max(G.node[e[1]]['label_overtime']))

    for e  in edges_cut:
        for titi in G.node[e[1]]['label_overtime']:
            if (titi <= Tmax_minus):
                switch_time_f_e_minus.append(titi)
    switch_time_f_e_minus.sort()
    print("switch_time_f_e_minus",switch_time_f_e_minus)
    G.name['switching_times_f_Xbar_minus']= switch_time_f_e_minus



    Tmax_plus=1e+24
    for e  in edges_cut:
        Tmax_plus=min(Tmax_plus,max(G.node[e[0]]['label_overtime']))

    switch_time_f_e_plus=[]
    for e  in edges_cut:
        for titi in G.node[e[0]]['label_overtime']:
            if (titi <= Tmax_plus):
                switch_time_f_e_plus.append(titi)
    switch_time_f_e_plus.sort()
    print("switch_time_f_e_plus",switch_time_f_e_plus)
    G.name['switching_times_f_Xbar_plus']= switch_time_f_e_plus


    f_Xbar_minus = []
    for t in switch_time_f_e_minus:
        flow =0.0
        for e  in edges_cut:
            flow = flow + f_e_minus(G, e, t)
        f_Xbar_minus.append(flow)
    print('f_Xbar_minus =' , f_Xbar_minus)
    G.name['f_Xbar_minus'] = f_Xbar_minus

    f_Xbar_plus = []
    for t in switch_time_f_e_plus:
        flow =0.0
        for e  in edges_cut:
            flow = flow + f_e_plus(G, e, t)
        f_Xbar_plus.append(flow)
    print('f_Xbar_plus =' , f_Xbar_plus)

    G.name['f_Xbar_plus'] = f_Xbar_plus

    switch_time_f_e_minus_sink=[]
    for e in G.in_edges(sink,keys=True):
        for titi in G.node[e[1]]['label_overtime']:
            switch_time_f_e_minus_sink.append(titi)
    switch_time_f_e_minus_sink.sort()
    print("switch_time_f_e_minus_sink",switch_time_f_e_minus_sink)
    G.name['switching_times_f_sink_minus']= switch_time_f_e_minus_sink
    f_sink_minus=[]
    for t in switch_time_f_e_minus_sink:
        flow =0.0
        for e  in G.in_edges(sink,keys=True):
            flow = flow + f_e_minus(G, e, t)
        f_sink_minus.append(flow)
        
    G.name['f_sink_minus']= f_sink_minus
    
def isF_Xbar_minus_increasing(G,tol):
    current_value =  G.name['f_Xbar_minus'][0]
    tk=0
    for f in G.name['f_Xbar_minus']:
        tk=tk+1
        if (f < current_value-tol):
            return False, tk
        else:
            current_value=f
    return True, tk


def isF_sink_minus_increasing(G,tol):
    current_value =  G.name['f_sink_minus'][0]
    tk=0
    for f in G.name['f_sink_minus']:
        tk=tk+1
        if (f < current_value-tol):
            return False, tk
        else:
            current_value=f
    return True, tk



def plot_extravalues(G):

    print(drepr(G.name))

    min_x=0.0
    max_x=0.0
    for ntail,nbrs in G.adjacency_iter():
        max_x =max([max_x, max(G.node[ntail]['label_overtime'])])


    plt.subplot(511)
    plt.grid()
    plt.title('f_Xbar_minus')
    x_plot_data = []
    y_plot_data = []
    for i in range(len(G.name['switching_times_f_Xbar_minus'])-1):
        x_plot_data.append(G.name['switching_times_f_Xbar_minus'][i])
        y_plot_data.append(G.name['f_Xbar_minus'][i+1])
        x_plot_data.append(G.name['switching_times_f_Xbar_minus'][i+1])
        y_plot_data.append(G.name['f_Xbar_minus'][i+1])
    plt.plot(x_plot_data[:],y_plot_data[:])

    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([-0.1,max_y+0.1])

    plt.subplot(512)
    plt.grid()
    plt.title('f_Xbar_plus')
    x_plot_data = []
    y_plot_data = []
    for i in range(len(G.name['switching_times_f_Xbar_plus'])-1):
        x_plot_data.append(G.name['switching_times_f_Xbar_plus'][i])
        y_plot_data.append(G.name['f_Xbar_plus'][i+1])
        x_plot_data.append(G.name['switching_times_f_Xbar_plus'][i+1])
        y_plot_data.append(G.name['f_Xbar_plus'][i+1])
    plt.plot(x_plot_data[:],y_plot_data[:])

    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.xlim([min_x,max_x])
    min_y,max_y=plt.ylim()
    plt.ylim([-0.1,max_y+0.1])
