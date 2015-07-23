"""
BUILD VISUALIZATION DATA

"""

sys.argv = ['sim.py',NETWORK_NAME,'1']
execfile(os.path.join('.','lib','build','sim.py'))

sys.argv = ['set.py',NETWORK_NAME,'1']
execfile(os.path.join('.','lib','layouts','set.py'))