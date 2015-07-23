
import vtk

import networkx as nx
from numpy import *


def getLabelSize(G):

    N = G.number_of_nodes()
    
    fontSize = 12
    
    if ( 10 <= N and N <= 50):
         
        fontSize = 8
         
    if ( 50 <= N and N <= 250):
         
        fontSize = 8
         
    if ( 250 <= N):
         
        fontSize = 8

    
    return fontSize

def getPointsFromStrList(str_list):
    
    str_list = str_list[2:-2].replace(' ','').replace("'",'').split('],[')
    points = []

    pos_x = []
    pos_y = []
    for str_point in str_list:
        aux = str_point.split(',')
        point = [float(aux[0]),float(aux[1]),float(aux[2])]    
        points.append(point)
    
    return points

def addInfoAnnotations(G,renderer,pars):
    
    msgTxt = '  Flows In Networks \n\n'
    msgTxt += '  July 22, 2015 \n\n\n'
    
    msgTxt += '  Interactor Style:\n\n'
    
    if (pars['TYPE'] in ['geometry','geometry2']):

        msgTxt += '  [ RubberBand3D ]\n\n'
        msgTxt += '  Controls:\n\n'
        msgTxt += '  Right mouse - Rotate \n'
        msgTxt += '  Shift + Right mouse - Zoom \n'
        msgTxt += '  Middle mouse - Pan \n'
        msgTxt += '  Scroll wheel - Zoom \n'

    if (pars['TYPE'] in ['n1']):
    
        msgTxt += '  [ StyleImage ]\n\n'
        msgTxt += '  Controls:\n\n'
        msgTxt += '  Right mouse - Zoom \n'
        msgTxt += '  Control + Left mouse - Rotation (2D) \n'
        msgTxt += '  Middle mouse - Pan \n'
        msgTxt += '  Scroll wheel - Zoom \n'
    
    msgTxt = '\n' + msgTxt

    annotation = vtk.vtkCornerAnnotation() 
    annotation.SetText(2,msgTxt)
    annotation.SetMaximumFontSize(14)
    #annotation.GetTextProperty().SetColor(0.75,0.75,0.75)
    renderer.AddViewProp(annotation)

    numberOfNodes = G.number_of_nodes()
    numberOfEdges = G.number_of_edges()
    
    msg = ['  NETWORK \n\n','  '+str(pars['NETWORK_NAME'])+'\n\n','  '+str(numberOfNodes),' nodes\n','  '+str(numberOfEdges),' edges\n\n']     
    annotation2 = vtk.vtkCornerAnnotation() 
    annotation2.SetText(0,''.join(msg))
    annotation2.SetMaximumFontSize(14)
    renderer.AddViewProp(annotation2)
    
    return msgTxt

def setBackgroundStyle(renderer):
    
    renderer.GradientBackgroundOn()
    renderer.SetBackground(0.1,0.1,0.1)
    renderer.SetBackground2(0.2,0.2,0.2)
    
    
    
    
    
    
    
    

    
    
