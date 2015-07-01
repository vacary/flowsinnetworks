
Flow in networks - Visualization  
// Workspace

Maximiliano Olivares <maximiliano.olivares@inria.cl>

Last update : June 30, 2015

------------------------------------------------------------------

# Description

Program developed for the visualization of dynamic equilibria 
from time varying flows over networks.

------------------------------------------------------------------

# Requirements

Written in Python, this program needs the following modules
to be executed:

- numpy			/ '1.8.2'
- vtk			/ '6.0.0'
- networkx		/ '1.9.1'
- PyQT4
- matplotlib	/ '1.3.1'
* pygraphviz (optional / under evaluation)

* Python Version : 2.7.6

------------------------------------------------------------------

# Steps to run a visualization

1. Create a new visualization project using the following instructions (for instance, "Larre" example)

1.1. Go to the "projects" folder

~ networks$ cd projects

1.2. Create the new project (in this case, with name "Larre", without the quotation marks)

~ networks/projects$ python new.py Larre

1.3. Go to the project folder and edit the file "network.py" adding the required information.

~ networks/projects$ cd Larre
~ networks/projects/Larre$ nano network.py 		(to edit the file)

''' 
It is important to define the network graph (one network/graph for each visualization project)
in the function "network_graph_data()" that can be found in "network.py". 
For this example, you can add the line

G = exa.example_Larre()

which takes a graph available in /flowsinnetworks/Flows/example.py. 
After define the graph and set the visualization parameters, save the "network.py" file.

'''

2.- Update and run the visualization project

2.1. Go back to the main folder and update the project visualization data with the following instruction

~ networks$ python update.py Larre

Note: This instruction runs the simulation program and could take some minutes to generate the visualization data.

2.2. Finally, run the visualization

~ networks$ python start.py Larre

# Comments

## A list with the available projects will be displayed after run the file "log.py" in the main folder

~ networks$ python log.py
 
## To run an available visualization project (for instance, the "Larre" project) just use the instruction
 
~ networks$ python start.py Larre

## After a change in the visualization parameters for a "network.py" file, update the visualization project
using the previous instructions.  
 
## To delete a visualization project, just delete the associated folder in "networks/projects". 

## If in "networks/projects" exists a folder with the name of a new visualization, the program will not create the files.




	
	
