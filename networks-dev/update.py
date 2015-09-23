# Standard library imports
import os
import sys
    
if __name__ == "__main__":
    
    """ Visualization data generator.
    
    Generate (or update) visualization data according to the following available options:
    
    -b : build the visualization data running the simulation, layout and data programs 
    (equivalent result as running the -s, -l and -data options, in this order)
    -s : generate simulation source data (compute and save the inflow/outflow rates by edge 
    and associated queue levels)
    -l : compute and save the network geometry according to spatial or temporal requirements
    according to a required time step
    -data : generate visualization data from the simulation source data, sampling this information 
    according to a required time step

    Examples
    --------
    >>> python update.py PROJECT_NAME -b
    >>> python update.py PROJECT_NAME -s
    >>> python update.py PROJECT_NAME -l
    >>> python update.py PROJECT_NAME -data
    
    """

    # List of available options

    options_list    = ['-b','-s','-l','-data']

    # Check if sys.argv values are valid entries

    is_valid_entry = True

    try:
        entry_filename = sys.argv[0]
        entry_network_name = sys.argv[1]
        entry_update_option = sys.argv[2]
    except:
        is_valid_entry = False
    
    if (is_valid_entry):

        NETWORK_NAME = entry_network_name.replace('.','')
        update_option = entry_update_option.replace('.','')
        network_src_path = os.path.join('.','projects',NETWORK_NAME,'__init__.py')
        is_valid_name = os.path.isfile(network_src_path)
        is_valid_option = update_option in options_list
        
        if (is_valid_name):    

            print '[FlowsInNetworks]'
            print 'Loading...'
            
            if (is_valid_option):
                if (update_option == '-b'):
                    try:
                        sys.argv = ['build.py',NETWORK_NAME,'1']
                        execfile(os.path.join('.','lib','build','build.py'))
                    except:
                        print(sys.exc_info())
                        print '[MSG] update.py -build error'
                if (update_option == '-s'):
                    try:
                        sys.argv = ['sim.py',NETWORK_NAME,'1']
                        execfile(os.path.join('.','lib','build','sim.py'))
                    except:
                        print(sys.exc_info())
                        print '[MSG] update.py -sim error'
                if (update_option == '-l'):
                    try:
                        sys.argv = ['set.py',NETWORK_NAME,'1']
                        execfile(os.path.join('.','lib','layouts','set.py'))
                    except:
                        print(sys.exc_info())
                        print '[MSG] update.py -layout error'
                if (update_option == '-data'):
                    try:
                        sys.argv = ['gen.py',NETWORK_NAME,'1']
                        execfile(os.path.join('.','lib','build','gen.py'))
                    except:
                        print(sys.exc_info())
                        print '[MSG] gen.py -data generator error'
            else: 
                print '[MSG] Entered option is not valid. Consider one of the following options: \n'
                print '\n'.join([str(opt) for opt in options_list])
                print '\n'
        else:
            print '[MSG] Network not found'
    else:
        if (entry_network_name == ''):
            print '[MSG] Required network name'
        if (entry_update_option == ''):
            print '[MSG] Required update option'
        