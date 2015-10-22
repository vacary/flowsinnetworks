#
# BUILD VISUALIZATION DATA

# Standard library imports
import sys
import os

try:
 
    sys.argv = ['sim.py', NETWORK_NAME, PROJECT_DIR_PATH]
    execfile(file_path_sim)
 
    try:
 
        sys.argv = ['gen.py', NETWORK_NAME, PROJECT_DIR_PATH]
        execfile(file_path_sampler)
 
        try:
 
            sys.argv = ['set.py', NETWORK_NAME, PROJECT_DIR_PATH]
            execfile(file_path_set)
             
        except:
            pass
     
    except:
        pass
         
except:
    pass
 

