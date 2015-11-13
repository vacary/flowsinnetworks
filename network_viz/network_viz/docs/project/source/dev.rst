Developers' Guide
===================

[On queue]

Introduction
-------------

... Description about the *databuilder* (in charge of the simulation, data sampling and layout stages) and *display* packages
(in charge of the construction of the different VTK elements and contains the files for the visualization GUI).

Files involved in the different stages:

- Simulation manager: databuilder/sim/sim.py

- Data sampler: databuilder/sampler/gen.py

- Set the network layout: databuilder/layouts/set.py

- To run a full project update: databuilder/build.py

- To create new projects: databuilder/projects/new.py

- To run the visualization GUI: display/main.py

Source code packages
---------------------

.. toctree::
   :maxdepth: 4

   databuilder
   display
