"""
BUILD VISUALIZATION DATA

"""

try:

    sys.argv = ['sim.py',NETWORK_NAME,'1']
    execfile(os.path.join('.','lib','build','sim.py'))

    try:

        sys.argv = ['gen.py',NETWORK_NAME,'1']
        execfile(os.path.join('.','lib','build','gen.py'))

        try:

            sys.argv = ['set.py',NETWORK_NAME,'1']
            execfile(os.path.join('.','lib','layouts','set.py'))
            
        except:
            pass
    
    except:
        pass
        
except:
    pass


