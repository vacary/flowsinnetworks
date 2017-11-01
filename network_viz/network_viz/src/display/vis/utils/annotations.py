# flowsinnetworks is a program dedicated to modeling and simulation
# of dynamic equilibrium of flows in networks
#
# Copyright 2016 INRIA, INRIA Chile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# contact vincent.acary@inria.fr
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
