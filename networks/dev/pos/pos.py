
import matplotlib.pyplot as plt
from numpy import *

def unit_dnormal_vector(p,q):
    
    p = array(p)
    q = array(q)
    d = q-p 
    u = d/(linalg.norm(d))
    v = zeros(3)
    
    if (abs(u[0]) > 0.0):
        v[0] = -u[1]/u[0]
        v[1] = 1.0
        v[2] = 0.0
    else:
        v[0] = 1.0
        v[1] = 0.0
        v[2] = 0.0
        
    w = v/(linalg.norm(v))
    z = cross(u,w)
    
    if (z[2]> 0):
        ans = w
    else:
        ans = -w
    
    return ans

def get_doubleLineEdgePoints(p,q,dist):
    
    w = unit_dnormal_vector(p, q)
    
    p = array(p)
    q = array(q)
        
    pw0 = p + dist*w
    qw0 = q + dist*w
    
    pw1 = q - dist*w
    qw1 = p - dist*w    
    
    dp0 = [array(pw0),array(qw0)]
    dp1 = [array(pw1),array(qw1)]

    return [dp0,dp1]


p = array([10*random.random(),10*random.random(),10*random.random()])
q = array([10*random.random(),10*random.random(),10*random.random()])

plt.plot([p[0],q[0]],[p[1],q[1]], 'b')

distance = 0.1*linalg.norm(q-p)
listOfPoints = get_doubleLineEdgePoints(p,q,distance)

for e in listOfPoints:

    print e
    
    p = e[0]
    q = e[1]
 
     
    plt.plot([p[0],q[0]],[p[1],q[1]], 'r')
 
plt.axes().set_aspect('equal')
   
plt.show()

