##
#
# Inria Chile - Flows In Networks
# 
# Dynamic flow visualization
#
# * Messages and data for start.py file
#
#

import os, sys
import settings
import lib.errors as e
import dev.graphs.test as dev

lib_path = os.path.abspath(os.path.join('..','..'))
sys.path.append(lib_path)

import Flows.examples as exa

ns                          = settings.NETWORK_GRAPH
msg                         = 'Graph...'+str(ns)
flag                        = 0

ADD_DUMMY_NODE              = settings.ADD_DUMMY_SOURCE_NODE # 0 or 1
PRIORITY_GRAPHVIZ_LAYOUT    = settings.PRIORITY_GRAPHVIZ_LAYOUT # 0 or 1
INTERACTOR_STYLE            = settings.INTERACTOR_STYLE
SIM_DATA_AVAILABLE          = False
MAP_DATA_AVAILABLE          = False

def check_package(string_name):
    
    package = string_name
    flag = 0
    
    try:
        __import__(package)
        flag = 0
        print '[*] '+str(package)
 
        return flag

    except ImportError:
        print '[x] '+str(package)+'...not found '
        flag = 2
    
        return flag

def check_package_opt(string_name):
    
    package = string_name
    flag = 0
    
    try:
        __import__(package)
        flag = 0
        print '[*] '+str(package)+' (optional) '
 
        return flag
    
    except ImportError:
        print '[x] '+str(package)+'...not found (optional)'
        flag = 2
    
        return flag

# packages

print '[FVS] Flow in Networks - Visualization'
print 'Check function for python modules...'

f1 = check_package('numpy')
f2 = check_package('vtk')
f3 = check_package('networkx')
f4 = check_package('PyQt4')
f5 = check_package_opt('pygraphviz')
f6 = check_package('matplotlib')
  
flag = max(f1,f2,f3,f4,f6)  

# graph call

if (flag == 0):


    # graph 
    
    if (ns == 'example1'):
    
        G = exa.example1()
    
    elif (ns == 'example2'):
    
        G = exa.example2()
    
    elif (ns == 'example3'):
        
        G = exa.example3()
    
    elif (ns == 'example4'):
        
        G = exa.example4()        
    
    elif (ns == 'example5'):
        
        G = exa.example5()
    
    elif (ns == 'example_KochSkutella2011_Fig3_Fig4'):
        
        G = exa.example_KochSkutella2011_Fig3_Fig4()    
    
    elif (ns == 'example_simple1'):
        
        G = exa.example_simple1()
    
    elif (ns == 'example_Fig1_Cominetti'):
        
        G = exa.example_Fig1_Cominetti()
    
    elif (ns == 'example_Fig1_Cominetti_variant1'):
        
        G = exa.example_Fig1_Cominetti_variant1()
    
    elif (ns == 'example_Larre'):
        
        G = exa.example_Larre()
        SIM_DATA_AVAILABLE = True
        
    elif (ns == 'example_Larre_bis'):
        
        G = exa.example_Larre_bis()
    
    elif (ns == 'example_parallelpath'):
        
        G = exa.example_parallelpath()    
    
    elif (ns == 'custom_graph'):
        
        G = dev.custom_graph()
        
    elif (ns == 'example_map_Tobalaba'):
        
        MAP_DATA_AVAILABLE = True
    
    else:
        
        G       = e.empty_MultiDiGraph()
        flag    = 1
        msg     = '[WARNING] Empty graph'
        
        print msg

# messages

if (flag == 0):
    print 'Selected graph... '+ns
    print 'Loading visualization...'
    




