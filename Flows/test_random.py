import gen_graph
import test
import sys
def test_random_varyingdn():
    degree = 4
    number_nodes_init=5
    k=0
    while (True and k<20):

        print('############################################################')
        print('#################### Random test',k,'######################')
        print('############################################################')

        #try:
        kk=0
        while(kk < 500):
            number_nodes=number_nodes_init+kk/100
            if degree >= number_nodes :
                number_nodes_init = number_nodes_init+1
                number_nodes=number_nodes_init+kk/100
            if (number_nodes * degree) % 2 != 0:
                gen_graph.generate_graph(degree,number_nodes+1,'G_gen.gml')
            else:
                gen_graph.generate_graph(degree,number_nodes,'G_gen.gml')
            isincreasing, tk = test.test23([],'G_gen.gml')
            if not isincreasing:
                print("the flow trough the cut is not increasing")
                raw_input()
            kk=kk+1
            print('############################################################')
            print('#################### End random test',k, kk, '###############')
            print('############################################################')

        degree=degree+1

        #except:
            #print "Unexpected error:", sys.exc_info()[0]
            #raise
            #raw_input()
        k=k+1
        
def test_random():
    k=0
    degree = 3
    number_nodes = 40
    while (True and k<200):

        print('############################################################')
        print('#################### Random test',k,'######################')
        print('############################################################')

        try:
            gen_graph.generate_graph(degree,number_nodes,'G_gen.gml')
            isincreasing, tk = test.test23([],'G_gen.gml')
            if not isincreasing:
                print("the flow trough the cut is not increasing")
            raw_input()
        except:
            raw_input()
        k=k+1


if __name__ == '__main__':
    test_random()
