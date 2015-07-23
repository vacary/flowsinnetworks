"""

Call to simulation program

"""

options_list    = ['-b','-s','-l']

import os, sys

def check_empty_entries(arg_lst):
    
    valid_entries       = True
    entry_filename      = arg_lst[0]
    entry_network_name  = arg_lst[1]
    entry_update_option = arg_lst[2]
    
    if (entry_network_name == ''):
        valid_entries = False
        print '[MSG] Required network name'
    
    if (entry_update_option == ''):
        valid_entries = False
        print '[MSG] Required update option'
    
    return valid_entries
    
if __name__ == "__main__":

    entry_filename      = ''
    entry_network_name  = ''
    entry_update_option = ''

    arg_lst             = [entry_filename,entry_network_name,entry_update_option]
    
    c = 0
    for arg in sys.argv:
        arg_lst[c] = sys.argv[c]
        c = c + 1
        
    valid_entries = check_empty_entries(arg_lst)

    if (valid_entries == True):

        NETWORK_NAME        = str(arg_lst[1]).replace('.','')
        update_option       = str(arg_lst[2]).replace('.','')
        
        network_src_path    = os.path.join('.','projects',NETWORK_NAME,'__init__.py')
        
        valid_name          = os.path.isfile(network_src_path)
        valid_option        = update_option in options_list
        
        if (valid_name == True):    
            
            if (valid_option == True):
                
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
    
            else: 
                
                print '[MSG] Non-valid option'  
                print 'Available options:\n'+'\n'.join([str(opt) for opt in options_list])
                          
        else:
            
            print '[MSG] Network not found'
    
