
Flows In Networks Project - Visualization software prototype

Maximiliano Olivares <maximiliano.olivares@inria.cl>

Last update : October 21, 2015
------------------------------------------------------------------

# Description

Software prototype developed for the visualization of dynamic equilibria
from time varying flows over networks.
 
------------------------------------------------------------------

# Requirements

Written in Python, this program needs the following packages:

- numpy			/ '1.8.2'
- vtk			/ '6.0.0'
- networkx		/ '1.9.1'
- PyQT4
- matplotlib	/ '1.3.1'
- pygraphviz 
- lxml 
- Pillow (Python Imaging Library) >= 2.0.0

* Python Version : 2.7.6

------------------------------------------------------------------

# Setup

To install this version is recommended to use the instruction

~ $ python setup.py install --record files.txt

To uninstall this program the files commented in files.txt must
be removed manually.

------------------------------------------------------------------

# Test

To test this version:

- Create a folder examples/:

~ $ mkdir examples

- Create a new project in the examples/ folder with the instruction:

~ projects$ network_viz.py --new Larre

- Update the project:

~ projects$ network_viz.py --update Larre

- Run the visualization:

~ projects$ network_viz.py --start Larre

------------------------------------------------------------------

# Documentation

A quick start guide to use this software and general documentation
will be available in the /docs folder (currently under development).

------------------------------------------------------------------

# About the Flows In Networks Project

The goal of the Flows In Networks Project is to design and develop
software prototypes for the simulation and the visualization of 
dynamic flows in networks.

Project Admin: Vincent Acary <vincent.acary@inria.fr>

------------------------------------------------------------------

# About this software

Icons from "Material design icons" by Google.
More information and license info for the "Material design icons" in /icons/mdi/info folder.

Material-design-icon github website:
https://github.com/google/material-design-icons

