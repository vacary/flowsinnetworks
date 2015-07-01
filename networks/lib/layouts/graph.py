'''

Graph layout functions

'''

import networkx as nx
from numpy import *

def getPointFrom2DRotation(x,y,angleInRads):
    
    newX = x*cos(angleInRads) - y*sin(angleInRads)
    newY = x*sin(angleInRads) + y*cos(angleInRads)
    
    return array([newX,newY,0])

def layout_network_graph(G,PRIORITY_GRAPHVIZ_LAYOUT,layout):
    
    package = 'pygraphviz'
    gviz = False
    
    try:
        __import__(package)
        gviz = True
    except ImportError:
        gviz = False
    
    if (gviz == True and PRIORITY_GRAPHVIZ_LAYOUT == 1) :
        pos = nx.graphviz_layout(G, prog=layout)
    else: 
        pos = nx.spring_layout(G)
    
    max_x = 0.0
    max_y = 0.0
    
    for key in pos:
        max_x = max(max_x,pos[key][0])
        max_y = max(max_y,pos[key][1])
            
    if (max_x > 0 and max_y > 0):
        
        max_yVis = 100.0
        max_xVis = max_yVis*(max_x/max_y)

    else:
        
        max_xVis = max_x
        max_yVis = max_y
    
    c           = 0
    radsAngle   = 90*(pi/180.0)
    
    for n in G.nodes_iter():
        
        G.add_node(n,id=int(c))
        cx = float(pos[n][0])*(max_xVis/max_x)
        cy = float(pos[n][1])*(max_yVis/max_y)
        
        point = getPointFrom2DRotation(cx,cy,radsAngle)
        
        G.add_node(n,pos= [point[0],point[1],0.0])

        G.add_node(n,type='r')
        
        c = c + 1
    
    return None
        
def addNodePositionsToGraph(G,TYPE,PRIORITY_GRAPHVIZ_LAYOUT,layout):
    
    if (TYPE == '0'):
        
        layout_network_graph(G,PRIORITY_GRAPHVIZ_LAYOUT,layout)
                
    return None
    
    
    
        