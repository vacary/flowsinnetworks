

Flow in networks - Visualization  
// Workspace

Maximiliano Olivares <maximiliano.olivares@inria.cl>

Last update : June 8, 2015

------------------------------------------------------------------

# Description

Program developed for the visualization of dynamic equilibria 
from time varying flows over networks.

------------------------------------------------------------------

# Requirements

Written in Python, this program needs the following modules
to be executed:

- numpy		/ '1.8.2'
- vtk		/ '6.0.0'
- networkx	/ '1.9.1'
- PyQT4
* pygraphviz (optional / under evaluation)

* Python Version : 2.7.6

------------------------------------------------------------------

# How to use this program ?

The user can edit the file "settings.py" to set the following elements for
the visualization:

- Network graph	: name of a graph defined, for instance, in ./sim/examples.py
- Tmax		: time horizon for the visualization
- time_step	: visualization time step
- FPS		: frames per second 

After set this requirements, the visualization can be executed
from a terminal with:

~$ python start.py
	
------------------------------------------------------------------
	
	
	
