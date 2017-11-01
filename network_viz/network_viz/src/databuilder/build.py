# flowsinnetworks is a program dedicated to modeling and simulation
# of dynamic equilibrium of flows in networks
#
# Copyright 2016 INRIA, INRIA Chile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# contact vincent.acary@inria.fr
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
 

