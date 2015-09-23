#
# Flows in Networks Project
#
# Dynamic flow visualization
# Inria Chile, 2015

# Standard library imports
import os
import sys
import importlib

if __name__ == "__main__":

    """ Start the network visualization GUI.
    
    Open the software GUI with the selected visualization project.
    This program execute an evaluation of the required modules before running the visualization GUI.
    
    Example
    -------
    
    >>> python start.py PROJECT_NAME
    
    """

    # Check if required modules are available

    print '[FlowsInNetworks]'
    print 'Loading...'

    # List of required packages / modules
    
    required_packages = ['numpy','networkx','PyQt4','pygraphviz','matplotlib','lxml','vtk']
    
    global_check = True
    
    for package in required_packages:
        
        try:
            
            importlib.import_module(package)
            print ''.join(['[*]',' ',package])
            
        except ImportError, e:
            
            global_check = False
            print ''.join(['[x]',' ',package,' : ',str(e)])

    # Check if all the packages / modules are available

    if (global_check):
        
        # Check the sys.argv length according to the instruction
        #
        # python start.py NETWORK_NAME
        #
        # then, the program will search the project folder and get the associated network data 
        # (stored using a networkx graph) to run the main visualization program.
        
        if (len(sys.argv) == 2):
            
            NETWORK_NAME        = str(sys.argv[1]).replace('.','')
            
            project_path        = os.path.join('.','projects',NETWORK_NAME,'__init__.py')
            project_exists      = os.path.isfile(project_path)

            graph_path          = os.path.join('.','projects',NETWORK_NAME,'data',NETWORK_NAME+'.gml')
            graph_data_exists   = os.path.isfile(graph_path)
            
            if (project_exists):

                if (graph_data_exists):
                    
                    # Open the software GUI to display the visualization
                    
                    print '[MSG] Found %s network data' %( NETWORK_NAME )
                    print 'Loading GUI...'                        
                    
                    sys.argv = ['main.py',NETWORK_NAME]
                    execfile(os.path.join('.','src','display','main.py'))
                    
                else:

                    print '[MSG] Graph data not found. Project update needed. [~$ python update.py %s -b]' %( NETWORK_NAME )
                    
            else:
                
                print '[MSG] Network not found'

        else:

            print '[MSG] Non-valid input data. Required network name.'
            