"""

Call to simulation program

"""


import os, sys

if __name__ == "__main__":
    
    NETWORK_NAME = str(sys.argv[1]).replace('.','')
    network_src_path    = os.path.join('.','projects',NETWORK_NAME,'__init__.py')
    valid_name          = os.path.isfile(network_src_path)

    if (valid_name == True):    
        
        try:
            
            os.chdir(os.path.join(".","projects",NETWORK_NAME))
            sys.path.append('.')
            execfile("sim.py")
        
            print '[MSG] Updated "'+NETWORK_NAME+'" network'
        
        except:
            
            print(sys.exc_info())
            print '[MSG] update.py error '       
                
    else:
        
        print '[MSG] Network not found'
    
