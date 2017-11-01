
#
# Associated functions : u0, fe+, fe-, Fe+, Fe-, ze
#
 

def u0(theta):
    
    z = 0.0
    
    if (0 <= theta) and (theta <= 1):
        z = 2.0
    
    if (1 < theta) and (theta <= 2):
        z = 0.0
        
    if (2 < theta) and (theta <= 4):
        z = 1.0
        
    if (theta > 4):
        z = 0.0
        
    return z 

def fePlus(theta):
    
    z = u0(theta)
    
    return z 

def feMinus(theta):
    
    z = 0.0
    
    if (0 <= theta) and (theta <= 1):
        z = 0.0
        
    if (1 < theta) and (theta <= 5):
        z = 1.0
    
    if (theta > 5):
        z = 0.0
        
    return z 

def FePlus(theta):
    
    z = 0.0
    
    if (0 <= theta) and (theta <= 1):
        z = 2.0*theta
    
    if (1 < theta) and (theta <= 2):
        z = 2.0
        
    if (2 < theta) and (theta <= 4):
        z = 1.0*theta
        
    if (theta > 4):
        z = 4.0
        
    return z     

def FeMinus(theta):
    
    z = 0.0
    
    if (0 <= theta) and (theta <= 1):
        z = 0.0
        
    if (1 < theta) and (theta <= 5):
        z = 1.0*theta - 1.0
    
    if (theta > 5):
        z = 4.0
        
    return z 
    
def ze(theta):
    
    z  = 0.0
    te = 1.0
    
    z = FePlus(theta) - FeMinus(theta + te)
    
    return max(z,1e-6)


