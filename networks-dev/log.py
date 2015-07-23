'''

Flows In Networks - List of available networks for visualization

'''

import os, sys

print "[ Flows In Networks ] List of available networks for visualization" 

listOfAvailableNetworks = os.walk('./projects').next()[1]

if (len(listOfAvailableNetworks)  == 0):
    
    print '[MSG] Empty list'

else:

    for network in listOfAvailableNetworks:
        
        print '+ '+network

