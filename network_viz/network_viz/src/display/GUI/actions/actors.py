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