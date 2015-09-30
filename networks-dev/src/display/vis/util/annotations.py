#
# Function to add the network and interaction info annotations

import vtk

def infoAnnotations(G,renderer,pars):
    
    """ Function to add the network and interaction info annotations
    
    Args: 
    
        G : Networkx graph
        renderer: Visualization vtk renderer
        pars: Network project settings
    
    """
    
    listOfAnnotations = []
    
    network_name = pars['NETWORK_NAME']
    numberOfNodes = G.number_of_nodes()
    numberOfEdges = G.number_of_edges()

    # Network Corner Annotation
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

    # Interactor Description Corner Annotation
    msgTxt = '  Interactor Style:\n\n'
    if (pars['TYPE'] in ['network']):
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
