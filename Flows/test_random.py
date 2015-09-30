import gen_graph
import test
import sys
def test_random_varyingdn():
    degree = 5
    number_nodes_init=50
    k=0
    while (True and k<20):

        print('############################################################')
        print('#################### Random test',k,'######################')
        print('############################################################')

        #try:
        kk=0
        while(kk < 50):
            number_nodes=number_nodes_init+kk/10
            if degree >= number_nodes :
                number_nodes_init = number_nodes_init+1
                number_nodes=number_nodes_init+kk/100
            filename = './gen/G_gen'+str(k)+str(kk).zfill(5)+'.gml'
            if (number_nodes * degree) % 2 != 0:
                gen_graph.generate_graph(degree,number_nodes+1,filename)
            else:
                gen_graph.generate_graph(degree,number_nodes,filename)
            G= test.test_file([],filename,timeofevent=[0.0,100.0], inputflow=[20.0])
            # if (not G.name['isF_Xbar_minus_increasing'][0]) and\
            #    (not G.name['isF_sink_minus_increasing'][0]):
            #     print(filename, ": the flow trough the cut and the sink is not increasing")
            #     raw_input()
            #if (not G.name['isF_Xbar_minus_inE_increasing'][0]):
            #    print(filename, ": the flow trough the cut and the sink is not increasing")
            #    raw_input()
            # if not G.name['isF_Xbar_minus_increasing'][0]:
            #     print(filename, ": the flow trough the cut is not increasing")
            #     #raw_input()
            # if not G.name['isF_sink_minus_increasing'][0]:
            #     print(filename, ":the flow at sink is not increasing")
            #     raw_input()
            if not G.name['isTotalTravelTime_increasing'][0]:
                  print(filename, ": the total travel time is not increasing")
                  raw_input()
            if not G.name['isDerTotalTravelTime_decreasing'][0]:
                print(filename, ": the total travel time is not increasing")
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
