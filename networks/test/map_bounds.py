
import os, sys
import networkx as nx

lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

import lib.vis.manage as vis_mn


map_coords_path = '../projects/map/map/bounds.txt'
coords = vis_mn.get_map_crop_bounds(map_coords_path)

print coords