"""

Colormaps using matplotlib

"""

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    rgb_tuple = tuple(int(value[i:i+lv/3],16)/255.0 for i in range(0,lv,lv/3))
    return rgb_tuple

def get_color_map(name, numberOfColors=20):

    import matplotlib.pylab as mp
        
    cmap = mp.cm.get_cmap(name)
    
    cstep = 1.0/(1.0*numberOfColors)
    
    colors = []
    
    for i in xrange(numberOfColors+1):
        
        colors.append(cmap(i*cstep))
        
    return colors