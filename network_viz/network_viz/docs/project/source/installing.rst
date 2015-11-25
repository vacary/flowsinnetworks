Installing network_viz
=======================

The network_viz software can be used after installing the script *network_viz.py*, using the setup.py file available in the project repository.
Before installing this script, it is necessary to verify the installation of some required libraries for its execution.

Requirements
--------------

Before install the network_viz.py script, is necessary to check if the following libraries / packages are available:

- numpy       >= 1.8.2
- vtk         >= 6.0.0
- networkx    >= 1.9.1
- PyQT4
- matplotlib  >= 1.3.1
- pygraphviz
- lxml
- PIL         (From Pillow Fork, Pillow >= 2.0.0)

The program was developed under the Python version 2.7.6.

How to Install
--------------

After download the project folder *flowsinnetworks*, the software can be installed using the available file setup.py
in the subfolder *network_viz*.

The recommended way to install this program is using a local installation, which do not require administrative privileges
with the instruction::

~network_viz$ python setup.py install --user

Optionally, can be used::

~network_viz$ python setup.py install --user --record files.txt

to record the files created from the installation. This information will be usefull to remove the script, if necessary,
which requires to delete the files listed in files.txt manually.

After the setup.py execution, the script *network_viz.py* will be installed in the folder commented in the line::

  Installing network_viz.py script to /path/to/dir

Check that the /path/to/dir is in the $PATH variable. If not, it can be temporarily added from the terminal with::

~$ export PATH=/path/to/dir:$PATH

To confirm that the script was installed properly, after type::

~$ network_viz.py -h

must be displayed the script usage information, at any location.
