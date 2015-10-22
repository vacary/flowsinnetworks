from setuptools import setup

# Provisory setup

def check_required_packages():

    import importlib
    
    print '[ Flows in Networks - network_viz ]'

    print 'Check for required packages...'
        
    # List of required packages / modules
    required_packages = ['numpy', 'networkx', 'PyQt4', 'pygraphviz', 'matplotlib', 'lxml', 'vtk', 'PIL']
    
    available_packages = True
    
    for package in required_packages:
    
        try:
            importlib.import_module(package)
            print ''.join(['[*]', ' ', package])
        
        except ImportError, e:
            available_packages = False
            print ''.join(['[x]', ' ', package, ' : ', str(e)])
    
    return available_packages


if (check_required_packages()):

    setup(version='0.1',
        name='network_viz',
        description='Flowsinnetworks visualization prototype',
        scripts=['./network_viz/scripts/network_viz.py'],
    )
else:
    print 'Error: network_viz.py script was not installed'