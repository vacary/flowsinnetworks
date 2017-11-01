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
#
# GUI actions - Actors
#
# Functions to manage the actors display
#

def display_data_times_layer(vis):
    vis.show_data_layer_time = not(vis.show_data_layer_time)
    vis.show_data_layer_capacity = False
    vis.update_actors_display()

def display_data_capacities_layer(vis):
    vis.show_data_layer_capacity = not(vis.show_data_layer_capacity)
    vis.show_data_layer_time = False
    vis.update_actors_display()

def display_animation_layer(vis):
    vis.show_data_layer_capacity = False
    vis.show_data_layer_time = False    
    vis.update_actors_display()

def display_nodes_non_st_labels(vis):
    vis.show_nodes_non_st_labels = not(vis.show_nodes_non_st_labels)
    vis.update_actors_display()

def display_nodes_st_labels(vis):
    vis.show_nodes_st_labels = not(vis.show_nodes_st_labels)
    vis.update_actors_display()

def display_annotations(vis):
    vis.show_up_left_annotations = not(vis.show_up_left_annotations)
    vis.show_down_left_annotations = not(vis.show_down_left_annotations)
    vis.update_actors_display()

def display_colorbar(vis):
    vis.show_colorbar = not(vis.show_colorbar)
    vis.update_actors_display()
