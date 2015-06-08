
import os, sys
lib_path = os.path.abspath(os.path.join('..','..'))
sys.path.append(lib_path)
import lib.vfc as vis

from numpy import *
import random
from pylab import plt
plt.ion()

    
def getPointFrom2DRotation(x,y,angleInRads):
    
    newX = x*cos(angleInRads) - y*sin(angleInRads)
    newY = x*sin(angleInRads) + y*cos(angleInRads)
    
    return array([newX,newY,0])

def getListOfPointsForArc(p0,p1,angle,numberOfDivisions,plusFactor):

    ''' Add points to draw the arc from p0 to p1
    '''
    
    # angle take values in the open interval (0, 180)

    radsAngle   = angle*(pi/180.0)
    step        = radsAngle/(1.0*numberOfDivisions)
    
    # arcCenter
    middlePoint = 0.5*(array(p0) + array(p1))
    distance    = linalg.norm(array(p0) - array(p1))
    kFactor     = 0.5*distance/tan(0.5*radsAngle)
    u           = vis.unitNormal2DVectorToLine(p0,p1,0.0)
    
    arcCenter   = middlePoint + plusFactor*kFactor*u
    
    # listOfPoints
    
    points  = []
    points.append(p0)
    
    c2mp        = middlePoint - arcCenter
    direction   = array(p1) - array(p0)
    xcr         = cross(c2mp,direction)
    
    if (xcr[2] < 0):
        angleSign = -1.0
    else:
        angleSign = 1.0
    
    tp0         = p0 - arcCenter
    
    for k in xrange(1,numberOfDivisions):
        
        subRadsAngle = step*k
        tp = getPointFrom2DRotation(tp0[0],tp0[1],angleSign*subRadsAngle)
        point = tp + arcCenter
        points.append(point)
        
    points.append(p1)
    
    return points
        
# dots

p0 = array([5*random.random(),5*random.random(),0])
p1 = array([5*random.random(),5*random.random(),0])

angle = 120
numberOfDivisions = 10
plt.clf()
plt.axes().set_aspect('equal')

# # # center
# # 
#  
# angle       = angle*pi/180.0 
# mp          = 0.5*(array(p0) + array(p1))
# distance    = linalg.norm(array(p1) - array(p0))
# factor      = 0.5*distance/tan(0.5*angle)
# u           = vis.unitNormal2DVectorToLine(p0,p1,0.0)
#  
# c = mp + factor*u
#  
# c2mp = mp - c
# direction  = array(p1) - array(p0)
# 
# xcr = cross(c2mp,direction)
# 
# if (xcr[2] < 0):
#     angleSign = -1.0
# else:
#     angleSign = 1.0
#     
# # adding points
#  
# p = p0
# q = p0-c
# 
# angle_step = angle/(1.0*numberOfDivisions) 
#  
# for i in xrange(1,numberOfDivisions):
#      
#     subAngle = angle_step*i
#     point =  getPointFrom2DRotation(q[0],q[1],angleSign*subAngle)+c
#  
#     plt.plot(point[0],point[1],'rx')
#  
# plt.plot(mp[0],mp[1],'go')
# plt.plot([mp[0],c[0]],[mp[1],c[1]],'b')
#  
# plt.plot(c[0],c[1],'ro')
#  
# plt.plot(0,0,'bx')
# plt.plot(p0[0],p0[1],'bo')
# plt.plot(p1[0],p1[1],'bo')

points = getListOfPointsForArc(p0,p1,angle,numberOfDivisions,1)
 
for point in points:
     
    plt.plot(point[0],point[1],'ro') 
     
# different arcs
  
points = getListOfPointsForArc(p0,p1,90,numberOfDivisions,1)
for point in points:    
    plt.plot(point[0],point[1],'rx') 
  
points = getListOfPointsForArc(p0,p1,140,numberOfDivisions,1)
for point in points:    
    plt.plot(point[0],point[1],'bo')
     
points = getListOfPointsForArc(p0,p1,175,numberOfDivisions,-1)
for point in points:    
    plt.plot(point[0],point[1],'bx')
      
points = getListOfPointsForArc(p0,p1,175,numberOfDivisions,1)
for point in points:    
    plt.plot(point[0],point[1],'gx')

plt.show()





