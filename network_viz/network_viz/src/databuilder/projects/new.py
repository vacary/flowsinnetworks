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

# Standard library imports
import os
import sys

def set_vis_content(file, vname):

    content = '''# Visualization network settings

# Standard library imports
import os
import sys

# Non standard library imports
import networkx as nx

#####################################################
# Network settings
#####################################################

NETWORK_NAME = "%s"
TYPE = "network"

# Simulation parameters
TIME_OF_EVENT = [0.0,50.0]
INPUT_FLOW = [4.0]

# Sampler and layout parameters
TIME_STEP = 0.1
CUSTOM_LAYOUT = 0

# GUI visualizer parameters
T_MAX_VIS = 20.0
FPS = 24

#####################################################

project_dir_path = os.path.abspath(os.path.join(os.getcwd(), NETWORK_NAME))

def network_graph_data():

    # Example:

    # Import for examples from the root dir path

    import Flows.examples as exa

    G = nx.MultiDiGraph()

    source = 's'
    sink = 't'

    # { begin graph definition } [ Example: G = exa.example_Larre() ]

    G = exa.example_Larre()

    # { end graph definition }

    return [G, source, sink]

def network_custom_layout (G):

    # Important!: This method is applied only if CUSTOM_LAYOUT = 1

    # Example:

    # Databuilder import

    import databuilder.layouts.utils.gviz as gviz_layouts

    # [ Set graphviz layout parameters ]
    graphviz_prog = 'dot'
    graphviz_args = '-Gnodesep=1.0 -Grankdir=LR -Gsplines=ortho'

    #[ Create file with layout information ]

    gviz_file_path = os.path.join(project_dir_path, 'rsc', 'gviz', ''.join((NETWORK_NAME,'_custom.txt')))

    A = nx.to_agraph(G)
    A.draw(gviz_file_path, format='plain', prog=graphviz_prog, args=graphviz_args)

    # Generate graph image with graphviz (optional)
    # A.draw(gviz_file_path.replace('.','')+'.png', format='png', prog=graphviz_prog, args=graphviz_args)

    # [ Load the file with the layout information ]
    gviz_file_path = os.path.abspath(os.path.join(project_dir_path, 'rsc', 'gviz',''.join((NETWORK_NAME, '_custom.txt'))))
    gviz_layouts.addGeometryFromGVizFile(G, gviz_file_path, splines_degree=3, number_of_points=50) # important!

    return None ''' % ( vname )

    file.write(content)

    return None

def set_map_bounds(file):

    content = '''#
# Map crop bounds

W = 0.0
S = 0.0
E = 0.0
N = 0.0
'''
    file.write(content)

    return None

if __name__ == "__main__":

    """ Files generator for new visualization projects

    Program to create the files for a new visualization environment.
    This program must be executed in the '/projects' folder.

    Example
    --------

    >>> python new.py PROJECT_NAME

    """

    try:
        vname = str(sys.argv[1])

        if (vname == ''):
            print '[MSG] Empty name'
        else:

            new_main_path = os.path.abspath(os.path.join(vname))

            if not os.path.exists(new_main_path):

                # Create files and folders
                os.makedirs(new_main_path)
                os.makedirs(os.path.abspath(os.path.join(vname,'data')))
                os.makedirs(os.path.abspath(os.path.join(vname,'rsc')))
                os.makedirs(os.path.abspath(os.path.join(vname,'rsc','map')))
                os.makedirs(os.path.abspath(os.path.join(vname,'rsc','osm')))
                os.makedirs(os.path.abspath(os.path.join(vname,'rsc','gviz')))
                f = open(os.path.abspath(os.path.join(vname,'rsc','map','bounds.py')),'w')
                set_map_bounds(f)
                f.close()
                f = open(os.path.abspath(os.path.join(vname,'__init__.py')),'w')
                f.close()
                f = open(os.path.abspath(os.path.join(vname,'rsc','__init__.py')),'w')
                f.close()
                f = open(os.path.abspath(os.path.join(vname,'rsc','map','__init__.py')),'w')
                f.close()
                f = open(os.path.abspath(os.path.join(vname,'settings.py')),'w')
                set_vis_content(f,vname)
                f.close()

            else:

                print '[MSG] A folder with this name already exists.'

    except:

        print '[Error] Non-valid visualization name'
