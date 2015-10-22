#!/usr/bin/python

# Standard library imports
import os
import sys

# Paths

## Main paths

home = os.path.expanduser("~") ## Source folder
#-------
root_dir_path = os.path.join(home,'workspace','flowsinnetworks')  #important!
#-------
vroot_dir_path = os.path.join(root_dir_path,'network_viz','network_viz')
src_dir_path = os.path.join(vroot_dir_path,'src')

sys.path.append(root_dir_path)
sys.path.append(vroot_dir_path)
sys.path.append(src_dir_path)

## Auxiliary paths

#---
file_path_new_project   = os.path.join(src_dir_path,'databuilder','projects','new.py') ## Script to create new projects
file_path_sim           = os.path.join(src_dir_path,'databuilder','sim','sim.py') ## Simulation execution and save source data
file_path_sampler       = os.path.join(src_dir_path,'databuilder','sampler','gen.py') ## Data sampler
file_path_set           = os.path.join(src_dir_path,'databuilder','layouts','set.py') ## Set network layout
file_path_build         = os.path.join(src_dir_path,'databuilder','build.py') ## Program to run all the previous instructions
file_path_start         = os.path.join(src_dir_path,'display','main.py') ## Program to run the visualization GUI
#---

if __name__ == "__main__":
    
    # List of available options

    options_list    = ['--start', '--update', '--new']

    # Check if sys.argv values are valid entries

    is_valid_entry = True

    try:
        entry_filename = sys.argv[0]
        entry_option = sys.argv[1]
        entry_network_name = sys.argv[2]
    except:
        is_valid_entry = False
    
    if (is_valid_entry):
        
        NETWORK_NAME = entry_network_name.replace('.','')
        
        CURRENT_DIR_PATH = os.getcwd()
        
        PROJECT_DIR_PATH = os.path.abspath(os.path.join(CURRENT_DIR_PATH, NETWORK_NAME))
        sys.path.append(os.path.abspath(os.path.join('.')))

        is_valid_option = entry_option in options_list

        if (is_valid_option):
            
            if (entry_option == '--new'):
                sys.argv = ['new.py', NETWORK_NAME]
                execfile(file_path_new_project)
                
            if (entry_option == '--update'):
                sys.argv = ['build.py', NETWORK_NAME, PROJECT_DIR_PATH]
                execfile(file_path_build)
                
            if (entry_option == '--start'):
                sys.argv = ['main.py', NETWORK_NAME, PROJECT_DIR_PATH]
                execfile(file_path_start)
                
    else:
        
        print '[MSG] Non valid options'
        
        
        
