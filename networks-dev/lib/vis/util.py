
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

def get_points_from_string_list(str_list):
    
    str_list = str_list[2:-2].replace(' ','').replace("'",'').split('],[')
    points = []

    pos_x = []
    pos_y = []
    for str_point in str_list:
        aux = str_point.split(',')
        point = [float(aux[0]),float(aux[1]),float(aux[2])]    
        points.append(point)
    
    return points

def get_int_array_from_string_list(str_list):

    str_list = str_list[1:-1]
    
    output = [int(elm) for elm in str_list.split(',')]
    
    return output

def getFloatListFromStrList(str_list):

    str_list = str_list[1:-1]
    
    output = [float(elm) for elm in str_list.split(',')]
    
    return output

def get_array_from_string_list(str_list):

    str_list = str_list[1:-1]
    
    output = [float(elm) for elm in str_list.split(',')]
    
    return output

def infoAnnotations(G,renderer,pars):
    
    listOfAnnotations = []
    
    network_name    =   pars['NETWORK_NAME']
    numberOfNodes   =   G.number_of_nodes()
    numberOfEdges   =   G.number_of_edges()

    msgTxt = '\n'
    msgTxt += '  NETWORK \n\n'
    msgTxt += "  '"+str(network_name)+"' \n\n\n"
    
    msgTxt += '  '+str(numberOfNodes)+' nodes\n'
    msgTxt += '  '+str(numberOfEdges)+' edges\n\n'
    
    annotation_info_nw = vtk.vtkCornerAnnotation() 
    annotation_info_nw.SetText(2,msgTxt)
    annotation_info_nw.SetMaximumFontSize(14)
    #annotation_info_nw.GetTextProperty().SetColor(0.75,0.75,0.75)
    annotation_info_nw.GetTextProperty().SetBold(0)
    annotation_info_nw.GetTextProperty().SetItalic(0)
    annotation_info_nw.GetTextProperty().SetShadow(0)

    renderer.AddViewProp(annotation_info_nw)


    msgTxt = '  Interactor Style:\n\n'
    
    if (pars['TYPE'] in ['geometry']):

        msgTxt += '  [ RubberBand3D ]\n\n'
        msgTxt += '  Controls:\n\n'
        msgTxt += '  Right mouse - Rotate \n'
        msgTxt += '  Shift + Right mouse - Zoom \n'
        msgTxt += '  Middle mouse - Pan \n'
        msgTxt += '  Scroll wheel - Zoom \n'
        #msgTxt += '  \n\n\n\n'

    if (pars['TYPE'] in ['network','interactor']):
    
        msgTxt += '  [ StyleImage ]\n\n'
        msgTxt += '  Controls:\n\n'
        msgTxt += '  Right mouse - Zoom \n'
        msgTxt += '  Control + Left mouse - Rotation (2D) \n'
        msgTxt += '  Middle mouse - Pan \n'
        msgTxt += '  Scroll wheel - Zoom \n'
        #msgTxt += '  \n\n\n\n'
    
    msgTxt = '\n' + msgTxt
    
    annotation_info_iren = vtk.vtkCornerAnnotation()
    annotation_info_iren.SetText(0,''.join(msgTxt))
    annotation_info_iren.SetMaximumFontSize(13)
    annotation_info_iren.GetTextProperty().SetBold(0)
    annotation_info_iren.GetTextProperty().SetItalic(0)
    annotation_info_iren.GetTextProperty().SetShadow(0)
    
    renderer.AddViewProp(annotation_info_iren)
    
    return [annotation_info_nw, annotation_info_iren]

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
    renderer.SetBackground(10/255.0,10/255.0,10/255.0)
    #renderer.SetBackground(0/255.0,0/255.0,0/255.0)
    
    pass
     
    
    
    
    
    
    

    
    
