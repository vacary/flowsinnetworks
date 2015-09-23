# Standard library imports
import os
import sys

if __name__ == "__main__":
    
    """ Print a list with the available network visualization projects. """

    print '[ Flows In Networks ] List of available network visualization projects' 
    
    listOfAvailableNetworks = os.walk('./projects').next()[1]
    
    if (len(listOfAvailableNetworks)  == 0):
    
        print '[MSG] Empty list'
    
    else:
    
        for network in listOfAvailableNetworks:
            print '+ %s' %( network )