import unittest
import networkx as nx

import numpy as np

try:
    reload(flows)
except:
    import flows

try:
    reload(examples)
except:
    import examples




class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_congestion_labels(self):
        G=examples.example2()
        flows.congestion_labels(G,'s')
        self.assertEqual(G.node['s']['congestion_label'], 0.0)
        self.assertEqual(G.node['t']['congestion_label'], 5.0)
        self.assertEqual(G.node['w']['congestion_label'], 10.0)
        self.assertEqual(G.node['v']['congestion_label'], 5.0)


    def test_congestion_pathmethod(self):
        G=examples.example2()
        flows.congestion_labels_pathmethod(G,'s')

        self.assertEqual(G.node['s']['congestion_label'], 0.0)
        self.assertEqual(G.node['t']['congestion_label'], 5.0)
        self.assertEqual(G.node['w']['congestion_label'], 10.0)
        self.assertEqual(G.node['v']['congestion_label'], 5.0)



    def test_sparsest_cut(self):

        G=examples.example3()
        b= {} # dictionary of flows in nodes
        b['s'] = 9
        b['v'] = 0
        b['w'] = 0
        b['t'] = -9

        congestion,cut,comp_cut = flows.sparsest_cut(G,b,'s')
        print  congestion,cut,comp_cut
        self.assertEqual(congestion, 3.0)
        self.assertEqual(cut, ['s','w','v'])
        self.assertEqual(comp_cut, ['t'])

    def test_sparsest_cut1(self):
        G=examples.example_simple1()
        #display_graph(G)

        b= {} # dictionary of flows in nodes
        b['s'] = 1.0
        b['v'] = 0
        b['t'] = -1.0
        # add a dummy source node
        G.add_node('s0')
        G.add_edge('s0','s',  flow = 0, capacity = 1.0)

        b['s0']= b['s']
        b['s'] = 0

        congestion,cut,comp_cut = flows.sparsest_cut(G,b,'s0')
        print  congestion,cut,comp_cut
        self.assertEqual(congestion, 1.0)
        self.assertEqual(cut, ['s0'])
        self.assertEqual(comp_cut, ['s','t','v'])


    def test_current_shortest_path_graph(self):
        G=examples.example2()
        E,Estar,E_comp=flows.current_shortest_path_graph(G)


        self.assertEqual(set(E.edges()),set( [('s','v'),('s','w'), ('w','t'), ('v','t'), ('v','w')]))
        self.assertEqual(set(E_comp.edges()),set( []))
        self.assertEqual(set(Estar.edges()),set( [('s','v'),('v','w')] ))



    def test_compute_thin_flow_without_resetting(self):
        G=examples.example_KochSkutella2011_Fig3_Fig4()

        b= {} # dictionary of flows in nodes
        b['s'] = 3.0
        b['v'] = 0
        b['w'] = 0
        b['t'] = -3.0
        flows.compute_thin_flow_without_resetting(G,'s',b)

        self.assertEqual(G.node['s']['label_thin_flow'], 0.0)
        self.assertEqual(G.node['v']['label_thin_flow'], 1.0)
        self.assertEqual(G.node['w']['label_thin_flow'], 1.0)
        self.assertEqual(G.node['t']['label_thin_flow'], 1.0)

        self.assertEqual(G['s']['w'][0]['thin_flow'], 1.0)
        self.assertEqual(G['v']['t'][0]['thin_flow'], 2.0)
        self.assertEqual(G['w']['t'][0]['thin_flow'], 1.0)
        self.assertEqual(G['s']['v'][0]['thin_flow'], 2.0)
        self.assertEqual(G['v']['w'][0]['thin_flow'], 0.0)


    def test_compute_thin_flow_without_resetting_withnonzerodemand(self):
        G=examples.example_simple1()
        #display_graph(G)

        b= {} # dictionary of flows in nodes
        b['s'] = 1.0
        b['v'] = 0
        b['t'] = -1.0

        for e in G.edges(keys=True):
            G[e[0]][e[1]][e[2]]['thin_flow'] = -1.0
        for n in G.nodes():
            G.node[n]['label']=-1.0

        demand = 1

        flows.compute_thin_flow_without_resetting(G,'s',b,demand)

        self.assertEqual(G.node['s']['label_thin_flow'], 1.0)
        self.assertEqual(G.node['v']['label_thin_flow'], 1.0)
        self.assertEqual(G.node['t']['label_thin_flow'], 1.0)
        self.assertEqual(G['s']['v'][0]['thin_flow'], 1.0)
        self.assertEqual(G['v']['t'][0]['thin_flow'], 1.0)


    def test_compute_thin_flow(self):
        G=examples.example_simple1()
        b= {} # dictionary of flows in nodes
        b['s'] = 1.0
        b['v'] = 0
        b['t'] = -1.0

        E1 = nx.MultiDiGraph()
        E1.add_edge('v','t')

        for e in G.edges(keys=True):
            G[e[0]][e[1]][e[2]]['thin_flow'] = -1.0
        for n in G.nodes():
            G.node[n]['label']=-1.0

        demand=1

        flows.compute_thin_flow(G,'s',b,E1,demand)
        flows.congestion_labels(G,'s',flow='thin_flow')


        self.assertEqual(G.node['s']['label_thin_flow'], 1.0)
        self.assertEqual(G.node['v']['label_thin_flow'], 1.0)
        self.assertEqual(G.node['t']['label_thin_flow'], 0.5)
        self.assertEqual(G['s']['v'][0]['thin_flow'], 1.0)
        self.assertEqual(G['v']['t'][0]['thin_flow'], 1.0)


    def test_compute_thin_flow_withnonzerodemand2(self):
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

        flows.compute_thin_flow(G,'s',b,E1,demand,param=param)

        tol=param.tol_thin_flow

        self.assertTrue(abs(G.node['s']['label_thin_flow']- 1.0) <= tol )
        self.assertTrue(abs(G.node['v']['label_thin_flow']- 4/3.0) <= tol )
        self.assertTrue(abs(G.node['w']['label_thin_flow']- 1.0) <= tol )
        self.assertTrue(abs(G.node['t']['label_thin_flow']- 4/3.0) <= tol )

        self.assertTrue(abs(G['s']['v'][0]['thin_flow']-8/3.0 ) <= tol )
        self.assertTrue(abs(G['s']['w'][0]['thin_flow']-1/3.0 ) <= tol )
        self.assertTrue(abs(G['v']['t'][0]['thin_flow']-5/3.0) <= tol )
        self.assertTrue(abs(G['v']['w'][0]['thin_flow']-1.0) <= tol )
        self.assertTrue(abs(G['w']['t'][0]['thin_flow']-4/3.0) <= tol )

        flows.assert_thin_flow(G,'s',b,E1,3,param)

    def test_compute_dynamic_equilibrium_for_pwconstant_inputflow(self):
        G=examples.example_Fig1_Cominetti()
        source = 's'
        sink= 't'
        timeofevent=[0.0,1.0,2.0,10.0]
        inputflow=[2.0,0.0,1.0]
        flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow)

        # check current values
        self.assertEqual(G.node['s']['label_thin_flow'], 1.0)
        self.assertEqual(G.node['s']['label'], 10.0)
        self.assertEqual(G.node['r']['label_thin_flow'], 1.0)
        self.assertEqual(G.node['r']['label'], 11.0)
        self.assertEqual(G.node['t']['label_thin_flow'], 1.0)
        self.assertEqual(G.node['t']['label'], 12.0)

        self.assertEqual(G['s']['r'][0]['thin_flow'], 1.0)
        self.assertEqual(G['s']['r'][0]['x'], 10.0)
        self.assertEqual(G['s']['r'][0]['thin_flow_overtime'], [2.0, 0.0, 1.0])
        self.assertEqual(G['s']['r'][0]['x_overtime'], [0.0, 2.0, 2.0, 10.0])

        self.assertEqual(G['r']['t'][0]['thin_flow'], 0.0)
        self.assertEqual(G['r']['t'][0]['x'], 0.0)
        self.assertEqual(G['r']['t'][0]['thin_flow_overtime'], [0.0, 0.0, 0.0] )
        self.assertEqual(G['r']['t'][0]['x_overtime'], [0.0, 0.0, 0.0, 0.0] )

        self.assertEqual(G['r']['t'][1]['thin_flow'], 1.0)
        self.assertEqual(G['r']['t'][1]['x'], 10.0)
        self.assertEqual(G['r']['t'][1]['thin_flow_overtime'], [2.0, 0.0, 1.0])
        self.assertEqual(G['r']['t'][1]['x_overtime'], [0.0, 2.0, 2.0, 10.0])



    def test_compute_dynamic_equilibrium_for_pwconstant_inputflow2(self):
        G=examples.example_KochSkutella2011_Fig3_Fig4()
        source = 's'
        sink ='t'
        timeofevent=[0.0,20.0]
        inputflow=[3.0,3.0,3.0]


        param=flows.parameters()
        param.tol_thin_flow=1e-10
        param.tol_lp=1e-12
        param.tol_cut=1e-12


        flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param=param)

        tol =  param.tol_thin_flow*10



        print("******************************************************************",abs(G.node['v']['label']- 16.0))
        self.assertTrue(abs(G.node['s']['label_thin_flow']- 1.0) <= tol )
        self.assertTrue(abs(G.node['v']['label_thin_flow']- 1.0) <= tol )
        self.assertTrue(abs(G.node['w']['label_thin_flow']- 1.0) <= tol )
        self.assertTrue(abs(G.node['t']['label_thin_flow']- 1.0) <= tol )

        self.assertTrue(abs(G.node['s']['label']- 20.0) <= tol )
        self.assertTrue(abs(G.node['v']['label']- 25.0) <= tol )
        self.assertTrue(abs(G.node['w']['label']- 26.0) <= tol )
        self.assertTrue(abs(G.node['t']['label']- 30.0) <= tol )


        self.assertTrue(np.linalg.norm(np.array(G['s']['w'][0]['thin_flow_overtime']) - np.array([0.0, 1/3.0, 1.0])) <= tol )
        self.assertTrue(np.linalg.norm(np.array(G['s']['v'][0]['thin_flow_overtime']) - np.array([3.0, 8/3.0, 2.0])) <= tol )
        self.assertTrue(np.linalg.norm(np.array(G['w']['t'][0]['thin_flow_overtime']) - np.array([3.0, 4/3.0, 1.0])) <= tol )
        self.assertTrue(np.linalg.norm(np.array(G['v']['t'][0]['thin_flow_overtime']) - np.array([0.0, 5/3.0, 2.0])) <= tol )
        self.assertTrue(np.linalg.norm(np.array(G['v']['w'][0]['thin_flow_overtime']) - np.array([3.0, 1.0, 0.0])) <= tol )

        
    def test_compute_dynamic_equilibrium_for_pwconstant_inputflow3(self):
        
        G=examples.example_Larre()
        source = 's'
        sink ='t'
        timeofevent=[0.0,6.0]
        inputflow=[4.0, 4.0]
        
        
        param=flows.parameters()
        param.tol_thin_flow=1e-10
        param.tol_lp=1e-12
        param.tol_cut=1e-12

        tol =  param.tol_thin_flow*10


        flows.compute_dynamic_equilibrium_for_pwconstant_inputflow(G, source, sink, timeofevent, inputflow,param)

        print("******************************************************************",abs(G.node['v1']['label']- 16.0))
        self.assertTrue(abs(G.node['s']['label_thin_flow']- 1.0) <= tol )
        self.assertTrue(abs(G.node['v1']['label_thin_flow']- 1.0) <= tol )
        self.assertTrue(abs(G.node['v2']['label_thin_flow']- 1.0) <= tol )
        self.assertTrue(abs(G.node['t']['label_thin_flow']- 1.0) <= tol )

        self.assertTrue(abs(G.node['s']['label']- 6.0) <= tol )
        self.assertTrue(abs(G.node['v1']['label']- 8.0) <= tol )
        self.assertTrue(abs(G.node['v2']['label']- 9.0) <= tol )
        self.assertTrue(abs(G.node['t']['label']- 38.0/3.0) <= tol )

        self.assertTrue(np.linalg.norm(np.array(G['s']['v1'][0]['thin_flow_overtime']) - np.array([4.0, 4.0, 4.0, 3.0])) <= tol )
        self.assertTrue(np.linalg.norm(np.array(G['s']['v2'][0]['thin_flow_overtime']) - np.array([0.0, 0.0, 0.0, 1.0])) <= tol )
        self.assertTrue(np.linalg.norm(np.array(G['v2']['t'][0]['thin_flow_overtime']) - np.array([4.0, 4/3.0, 4/3.0, 1.0])) <= tol )
        self.assertTrue(np.linalg.norm(np.array(G['v1']['t'][0]['thin_flow_overtime']) - np.array([0.0, 8/3.0, 8/3.0, 3.0])) <= tol )
        self.assertTrue(np.linalg.norm(np.array(G['v1']['v2'][0]['thin_flow_overtime']) - np.array([4.0, 4.0/3.0, 4.0/3.0, 0.0])) <= tol )

        


#if __name__ == '__main__':
#    unittest.main()
suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
