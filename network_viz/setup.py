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
from setuptools import setup
import os

# Provisory setup

def check_required_packages():

    import importlib

    print '[ Flows in Networks - network_viz ]'

    print 'Check for required packages...'

    # List of required packages / modules
    required_packages = ['numpy', 'networkx', 'PyQt4', 'pygraphviz', 'matplotlib', 'lxml', 'vtk', 'PIL']

    available_packages = True

    for package in required_packages:

        try:
            importlib.import_module(package)
            print ''.join(['[*]', ' ', package])

        except ImportError, e:
            available_packages = False
            if (package=='PIL'):
                package = "PIL (from 'Pillow' Fork)"
            print ''.join(['[x]', ' ', package, ' : ', str(e)])

    return available_packages


if (check_required_packages()):

    with open('./network_viz/scripts/network_viz.py', "wt") as fout:
        with open('./network_viz/scripts/network_viz.py.in', "rt") as fin:
            for line in fin:
                fout.write(line.replace('@ROOT_DIR_PATH',  '%s%s%s' %( '\"' , os.path.abspath(os.path.join(os.getcwd(),"..")) , '\"') ))

    setup(version='0.1',
          name='network_viz',
          description='Flowsinnetworks visualization prototype',
          scripts=['./network_viz/scripts/network_viz.py'],
          )
else:
    print 'Error: network_viz.py script was not installed'
