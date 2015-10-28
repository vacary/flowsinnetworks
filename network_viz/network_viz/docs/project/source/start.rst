Getting started
===============

The network_viz software works in terms of visualization projects which
are stored in a workspace folder created by the user.

How to create a new visualization
---------------------------------

To create and execute a new visualization project is necessary to follow, at least,
the following steps:

- Creation of a visualization workspace.
- Creation of a new visualization.
- Edition of the network visualization settings.
- Update of the visualization project.
- Run the network visualization.

Creating the visualization workspace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before create a network visualization, it is necessary create a workspace folder
which will contains the set of projects defined by the user. This can be done directly
using the instruction::

~$ mkdir myprojects

The network_viz.py script must be used inside this folder, for instance::

~/myprojects$ network_vis.py -h

Creating a new visualization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After create the workspace, a new project can be created using
the network_viz.py script with the option --new with the project name as the respective argument ::

~/myprojects$ network_viz.py --new PROJECT_NAME

This option will create a new folder inside the workspace, called as the respective project name with
a set of folders and files which will contains the information required to run the network visualization,
according to the following description

.. glossary::

  settings.py
    Main file of the visualization project. The user must define in this file the information for the network
    to be studied among some related parameters for the visualization.

  /data
    Folder to store generated data for the network visualization.

  /rsc
    Resources folder for the network visualization. This folder contains, by default, the subfolders: /gviz,
    to store data about the network layout; /map, to store images to be used as background (optional) and /osm, to store
    osm files employed to the generation of networks from OpenStreetMap's data. More subfolder can be added by the user.

Visualization settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Once the visualization project is created is necessary to edit the associated network visualization settings in the file *settings.py*.
There are two general components to be edited by the user: the network visualization *parameters* and *functions*.

Visualization settings: Parameters
"""""""""""""""""""""""""""""""""""
In this file there will be considered the following types for the network visualization parameters:

**Simulation parameters**

- TIME_OF_EVENT (list): List with required dimension >= 2. The ith and (i+1)th component of this list corresponds to the lower and upper bound for a time interval associated to a source node inflow value equals to the ith component of the INPUT_FLOW list.
- INPUT_FLOW (list): List with required dimension equals to the number of TIME_OF_EVENT components minus 1. The ith component of this list, corresponds to the source node inflow value in the time interval with lower bound equals to the ith component of TIME_OF_EVENT and upper bound equals to the (i+1)th of the TIME_OF_EVENT list.

**Sampler and layout parameters**

- TIME_STEP (float): Time step to be used by the databuilder application to generate discretized data for the network visualization from simulation results.
- CUSTOM_LAYOUT (int): Parameter with value 0 or 1. If its value is equal to 1 the application will use the 'network_custom_layout' function to build spatial data for the network visualization. If its value is equal to 0, this function is not considered in the visualization project.

**GUI visualizer parameters**

- T_MAX_VIS (float): Time horizon for the visualization.
- FPS (int): User expected frames per second.

Visualization settings: Functions
"""""""""""""""""""""""""""""""""""
On the other hand, in the settings.py file will be available the following functions:

.. glossary::

  network_graph_data()
    Function which must contain the definition of the network to be studied as a networkx's graph. This function has no arguments and must return the graph G, the source node and the sink node of the network.

  network_custom_layout(G)
    Function which must contain instructions to create spatial data for the network's layout (to be considered only if CUSTOM_LAYOUT==1). This function has a networkx graph has argument with no variables to return.

Once the network visualization parameters and functions are defined, is necessary to *update* the project, process which will create the data to be visualized.

Visualization project update
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A project can be updated using::

~/myprojects$ network_vis.py --update PROJECT_NAME

With the option *--update* the network_viz.py script will execute a list of programs which
will create the data to be visualized according to the following stages:

..glossary::

  Simulation
    The program will run a simulation for the development of the flow over time on the network
    creating data in terms of piecewise functions, which must be sampled to generate discrete
    data to be visualized.

  Simulation data sampling
    The simulation data created in the previous stage is *sampled* according to the TIME_STEP
    value defined in the visualization settings.

  Network layout
    Using the visualization settings, the program uses a set of functions to create
    geometry and topology data for the nodes and edges of the studied network.
    If non particular information is used to set the network layout,
    the software employs the Python interface to the Graphviz
    graph layout and visualization package <www.graphviz.org> to generate a basic
    layout data. Another option corresponds to the use of OpenStreetMap files
    (with extension .osm) to use the spatial data of street / road networks.
    Then, the basic layout information is processed to consider a set of divisions
    for each edge, according to the time step defined for the network visualization
    which lets to display what will be the flow particles position at each time.

This three process are executed under the use of the option *--update*, which corresponds to
a *full update* for the project.
However, under small changes on the visualization parameters, some of the stages of a full update
for the project could take several minutes to be completed
(for instance, the simulation process for a large network).
For this case, currently there are available two additional options
*--update-sample* and *--update-layout* according to particular changes
on the parameters and functions of the visualization settings which are
commented in the following resume for the update options.

..glossary::

  network_viz.py --update PROJECT_NAME
    Full update for the visualization project (simulation, simulation data sampling, network layout data generation).

  network_viz.py --update-sample PROJECT_NAME
    Partial update which
    executes the *simulation data sampling* and *network layout* processes.
    Requires a previous full update for the project.
    This option can be used under changes on the TIME_STEP value.

  network_viz.py --update-layout PROJECT_NAME
    Partial update which
    executes the *network layout* process.
    Requires a previous full update for the project.
    This option can be used under changes on the CUSTOM_LAYOUT visualization
    parameter and / or the network_custom_layout function (applied only if
    CUSTOM_LAYOUT==0).

Run a network visualization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After create the required data files using the update option, you will be
able to run the visualization with the option start of the network_viz.py script::

~/myprojects$ network_viz.py --start PROJECT_NAME

A first visualization project
-----------------------------

Using the commented steps,

Using graphviz to modify the network layout
-------------------------------------------
