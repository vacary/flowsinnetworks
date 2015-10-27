Getting started
===============

The network_viz software works in terms of visualization projects which
are stored in a workspace folder created by the user.

A first visualization project
-------------------------------------

Creating the visualizations workspace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before create a network visualization is necessary to create a folder which
will contains the projects defined by the user. This can be done directly
using the instruction::

~$ mkdir myprojects

Then, the network_viz.py script will be used inside this folder::

~/myprojects$ network_vis.py -h

Creating a new visualization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After create the workspace, a new project can be created using
the option --new  with the project name as the respective argument ::

~/myprojects$ network_viz.py --new PROJECT_NAME

In this section we will consider the creation the project "Larre",
with the instruction::

~/myprojects$ network_viz.py --new Larre

This option will create a new folder inside the workspace, called as the respective project name with
a set of folders and files which will contain the information required to run the network visualization,
according to the following description

.. glossary::

  settings.py
    Main file of the visualization project. The user must define in this file the information for the network
    to be studied among some related parameters for the visualization.

  /data
    Folder to store generated data for the network visualization.

  /rsc
    Resources folder for the network visualization. By default folders: /gviz, to store data about the
    network layout; /map, to store images to be used as background (optional) and /osm, to store
    osm files employed to the generation of networks from OpenStreetMap's data.

Visualization settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Inside the visualization project folder, the user will be able to find the file *settings.py*.
In this file the user will be able to edit the follwing type of parameters:
