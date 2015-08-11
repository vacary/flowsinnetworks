
import vtk
import networkx as nx

from numpy import *

def getLabelSize(G):

    N = G.number_of_nodes()
    
    fontSize = 12
    
    if ( 10 <= N and N <= 50):
         
        fontSize = 10
         
    if ( 50 <= N and N <= 250):
         
        fontSize = 10
         
    if ( 250 <= N):
         
        fontSize = 10

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

def getArrayFromStrList(str_list):

    str_list = str_list[1:-1]
    
    output = [float(elm) for elm in str_list.split(',')]
    
    return output

def addInfoAnnotations(G,renderer,pars):
    
    network_name    =   pars['NETWORK_NAME']
    numberOfNodes   =   G.number_of_nodes()
    numberOfEdges   =   G.number_of_edges()

    msgTxt = '\n'
    msgTxt += '  NETWORK \n\n'
    msgTxt += "  '"+str(network_name)+"' \n\n\n"
    
    msgTxt += '  '+str(numberOfNodes)+' nodes\n'
    msgTxt += '  '+str(numberOfEdges)+' edges\n\n'
    
    annotation = vtk.vtkCornerAnnotation() 
    annotation.SetText(2,msgTxt)
    annotation.SetMaximumFontSize(14)
    #annotation.GetTextProperty().SetColor(0.75,0.75,0.75)
    renderer.AddViewProp(annotation)


    msgTxt = '  Interactor Style:\n\n'
    
    if (pars['TYPE'] in ['geometry','geometry2']):

        msgTxt += '  [ RubberBand3D ]\n\n'
        msgTxt += '  Controls:\n\n'
        msgTxt += '  Right mouse - Rotate \n'
        msgTxt += '  Shift + Right mouse - Zoom \n'
        msgTxt += '  Middle mouse - Pan \n'
        msgTxt += '  Scroll wheel - Zoom \n'

    if (pars['TYPE'] in ['n0','n1','n2','network']):
    
        msgTxt += '  [ StyleImage ]\n\n'
        msgTxt += '  Controls:\n\n'
        msgTxt += '  Right mouse - Zoom \n'
        msgTxt += '  Control + Left mouse - Rotation (2D) \n'
        msgTxt += '  Middle mouse - Pan \n'
        msgTxt += '  Scroll wheel - Zoom \n'
    
    msgTxt = '\n' + msgTxt    
    annotation2 = vtk.vtkCornerAnnotation() 
    annotation2.SetText(0,''.join(msgTxt))
    annotation2.SetMaximumFontSize(12)
    renderer.AddViewProp(annotation2)
    
    return msgTxt

def setBackgroundStyle(renderer):

#     renderer.GradientBackgroundOn()
#     renderer.SetBackground(0,0,0)
#     renderer.SetBackground2(0.5,0.5,0.5)
    
    #renderer.SetBackground(70/255.0,80/255.0,90/255.0)
    #renderer.SetBackground(47/255.0,47/255.0,47/255.0)

    #renderer.SetBackground(5/255.0,5/255.0,20/255.0)

    #renderer.SetBackground(70/255.0,80/255.0,90/255.0)

#     renderer.GradientBackgroundOn()
#      
#     #renderer.SetBackground(5/255.0,5/255.0,20/255.0)
#     renderer.SetBackground(5/255.0,20/255.0,20/255.0)
#     renderer.SetBackground2(60/255.0,90/255.0,100/255.0)
#     
#     renderer.SetBackground2(76/255.0,90/255.0,100/255.0)
#     renderer.SetBackground2(70/255.0,80/255.0,90/255.0)

    
    #renderer.SetBackground(35/255.0,35/255.0,35/255.0)
    #renderer.SetBackground(0/255.0,0/255.0,0/255.0)
    
    pass
     
    
    
    
    
    
    

    
    
