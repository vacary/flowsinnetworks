
#
# Associated functions
#

from numpy import * 
from pylab import *

def u0(theta):
    
    z = 4.0
        
    return z 

def lfun(theta):
 
    z = zeros(4)
 
    if ( 0 <= theta and theta <= 1):
 
        z[0] = theta
        z[1] = 1 + 4*theta/3.0
        z[2] = 2 + 2*theta
        z[3] = 3 + 4*theta
 
    if ( 1 <= theta and theta < 2):
 
        z[0] = theta
        z[1] = 4*(theta-1)/3.0 + (1 + 4*1.0/3.0)
        z[2] = 2*(theta-1)/3.0 + (2 + 2*1.0) 
        z[3] = 4*(theta-1)/3.0 + (3 + 4*1.0)
 
    if ( 2 <= theta and theta < 3):
 
        z[0] = theta
        z[1] = 4*(theta-2)/3.0 + 4*(2.0-1)/3.0 + (1 + 4*1.0/3.0)
        z[2] = 4*(theta-2)/3.0 + 2*(2.0-1)/3.0 + (2 + 2*1.0) 
        z[3] = 4*(theta-2)/3.0 + 4*(2.0-1)/3.0 + (3 + 4*1.0)
 
    if ( theta >= 3):
 
        z[0] = theta
        z[1] = (theta-3) + 4*(3.0-1)/3.0 + 4*(2.0-1)/3.0 + (1 + 4*1.0/3.0)
        z[2] = (theta-3) + 4*(3.0-1)/3.0 + 2*(2.0-1)/3.0 + (2 + 2*1.0) 
        z[3] = (theta-3) + 4*(3.0-1)/3.0 + 4*(2.0-1)/3.0 + (3 + 4*1.0)
 
    return z

def fePlus(edge,theta):
 
    z = 0.0
 
    z0 = lfun(0)
    z1 = lfun(1)
    z2 = lfun(2)
    z3 = lfun(3)
 
    if (edge == 'e1'):
         
        if (z0[0] <= theta < z1[0]):
            z = 4.0
        if (z1[0] <= theta < z2[0]):
            z = 4.0
        if (z2[0] <= theta < z3[0]):
            z = 4.0
        if (z3[0] <= theta):
            z = 3.0
 
    if (edge == 'e2'):
 
        if (z0[1] <= theta < z1[1]):
            z = 0.0
        if (z1[1] <= theta < z2[1]):
            z = 2.0
        if (z2[1] <= theta < z3[1]):
            z = 2.0
        if (z3[1] <= theta):
            z = 3.0
             
    if (edge == 'e3'):
 
        if (z0[0] <= theta < z1[0]):
            z = 0.0
        if (z1[0] <= theta < z2[0]):
            z = 0.0
        if (z2[0] <= theta < z3[0]):
            z = 0.0
        if (z3[0] <= theta):
            z = 1.0
 
    if (edge == 'e4'):
 
        if (z0[2] <= theta < z1[2]):
            z = 2.0
        if (z1[2] <= theta < z2[2]):
            z = 2.0
        if (z2[2] <= theta < z3[2]):
            z = 1.0
        if (z3[2] <= theta):
            z = 1.0
 
    if (edge == 'e5'):
 
        if (z0[1] <= theta <= z1[1]):
            z = 3.0
        if (z1[1] <= theta <= z2[1]):
            z = 1.0
        if (z2[1] <= theta <= z3[1]):
            z = 1.0
        if (z3[1] <= theta):
            z = 0.0

    if (edge == 'e6'):
        
        return u0(theta)

    return z
 
def feMinus(edge,theta):
 
    z = 0.0
 
    z0 = lfun(0)
    z1 = lfun(1)
    z2 = lfun(2)
    z3 = lfun(3)
 
    if (edge == 'e1'):
         
        if (z0[1] <= theta < z1[1]):
            z = 3.0
        if (z1[1] <= theta < z2[1]):
            z = 3.0
        if (z2[1] <= theta < z3[1]):
            z = 3.0
        if (z3[1] <= theta):
            z = 3.0
 
    if (edge == 'e2'):
 
        if (z0[3] <= theta < z1[3]):
            z = 0.0
        if (z1[3] <= theta < z2[3]):
            z = 2.0
        if (z2[3] <= theta < z3[3]):
            z = 2.0
        if (z3[3] <= theta):
            z = 3.0
             
    if (edge == 'e3'):
 
        if (z0[2] <= theta < z1[2]):
            z = 0.0
        if (z1[2] <= theta < z2[2]):
            z = 0.0
        if (z2[2] <= theta < z3[2]):
            z = 0.0
        if (z3[2] <= theta):
            z = 1.0
 
    if (edge == 'e4'):
 
        if (z0[3] <= theta < z1[3]):
            z = 1.0
        if (z1[3] <= theta < z2[3]):
            z = 1.0
        if (z2[3] <= theta < z3[3]):
            z = 1.0
        if (z3[3] <= theta):
            z = 1.0
 
    if (edge == 'e5'):
 
        if (z0[2] <= theta <= z1[2]):
            z = 2.0
        if (z1[2] <= theta <= z2[2]):
            z = 2.0
        if (z2[2] <= theta <= z3[2]):
            z = 1.0
        if (z3[2] <= theta):
            z = 0.0

    if (edge == 'e6'):
        
        return u0(theta)
 
    return z


