k =0
while (True and k<20):

    print('############################################################')
    print('#################### Random test',k,'######################')
    print('############################################################')

    try:
        execfile('gen_graph.py')
        execfile('test.py')
    except:
        raw_input()
    k=k+1
    
