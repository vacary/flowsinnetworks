'''

Methods to check installed packages / modules

'''

import os, sys, re

def check_package(string_name,msg):
    
    package = string_name
    found   = False
    
    try:
        __import__(package)
        found = True
        print '[*] '+str(package)
 
    except ImportError:
        if (msg == ''):
            msg = '[not found]'
        print '[x] '+str(package)+' '+str(msg)
    
    return found

def check_packages(pck_list,msg_list):
    
    eval = True
    c = 0
    for pck in pck_list:
        check = (check_package(pck,msg_list[c]) and eval)
        eval = check
        c = c + 1
    
    return eval

