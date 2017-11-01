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
"""

Colormaps using matplotlib

"""

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    rgb_tuple = tuple(int(value[i:i+lv/3],16)/255.0 for i in range(0,lv,lv/3))
    return rgb_tuple

def get_color_map(name, numberOfColors=20):

    import matplotlib.pylab as mp
        
    cmap = mp.cm.get_cmap(name)
    
    cstep = 1.0/(1.0*numberOfColors)
    
    colors = []
    
    for i in xrange(numberOfColors+1):
        
        colors.append(cmap(i*cstep))
        
    return colors
