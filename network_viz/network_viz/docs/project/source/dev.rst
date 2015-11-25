Developers' Guide
===================

Introduction
-------------

The structure of the software *network_viz* is established according a number of two 'packages' identified as the *databuilder* and the *display* package. The functions
considered in each package can be consulted at the end of this section.

The *databuilder* package contains all the methods required to generate the data to be displayed with the software GUI (manage of the simulation process, data sampling and layout stages).
On the other hand, the *display* package contains all the necessary components for the visualization (using the VTK software system and the numpy package) and the software GUI (using the PyQT4 package).

To find the methods considered in each of the stages commented in the previous section, you can access to the respective main code in the following files:

- Simulation manager: databuilder/sim/sim.py

- Data sampler: databuilder/sampler/gen.py

- Functions to set the network layout: databuilder/layouts/set.py

- To run a full project update: databuilder/build.py

- To create new projects: databuilder/projects/new.py

- To run the visualization GUI: display/main.py

Source code packages
---------------------

.. toctree::
   :maxdepth: 4

   databuilder
   display
