#
# BUILD VISUALIZATION DATA

# Standard library imports
import sys
import os

# Custom library imports
dirs_path = os.path.abspath(os.path.join('..','dirs'))
sys.path.append(dirs_path)
from dirs import *

try:

    sys.argv = ['sim.py',NETWORK_NAME,'1']
    execfile(file_path_sim)

    try:

        sys.argv = ['gen.py',NETWORK_NAME,'1']
        execfile(file_path_sampler)

        try:

            sys.argv = ['set.py',NETWORK_NAME,'1']
            execfile(file_path_set)
            
        except:
            pass
    
    except:
        pass
        
except:
    pass


