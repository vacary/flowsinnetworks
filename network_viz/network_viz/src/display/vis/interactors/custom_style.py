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
# Custom interactor style

# Standard library imports
import os
import sys
import json
import unicodedata
import HTMLParser

# Non standard library imports
import vtk

# Comments:
# Requires temp file to store the temporal edge information
temp_file_path =  os.path.join(os.path.dirname(__file__),'..','..','..','..','temp','data.txt')

class CustomInteractorStyle(vtk.vtkInteractorStyleImage):
    
    """ Custom interactor style
    
    Network edge selection using vtk cells. 
    After click an edge, the interactor annotation (with the edge
    name) is displayed on the screen.
    
    """
    
    def __init__(self):
        
        self.AddObserver("LeftButtonPressEvent",self.leftButtonPressEvent)
        
    def leftButtonPressEvent(self,obj,event):
                  
        interactor  = self.GetInteractor()
        renderer    = self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer()
        clickPos    = self.GetInteractor().GetEventPosition()
 
        cellPicker  = vtk.vtkCellPicker()
        cellPicker.SetTolerance(0.0005)
        cellPicker.Pick(clickPos[0],clickPos[1],0,renderer)
         
        actorPicker = vtk.vtkPropPicker()
        actorPicker.Pick(clickPos[0],clickPos[1],0,renderer)
        worldPos    = cellPicker.GetPickPosition()
        
        pickedActor = actorPicker.GetActor()
        
        props = renderer.GetViewProps()
        props.InitTraversal()
        
        interactorAnnotation = None
        
        for i in xrange(props.GetNumberOfItems()):
            
            try: 
                prop = props.GetNextProp()
                auxString = prop.GetInput().split(' ')[0]
                if (auxString == 'Selected'):
                    interactorAnnotation = prop
                    interactorAnnotation.GetProperty().SetOpacity(0)
                    interactor.Render()        
            except:
                pass

        
        if (pickedActor != None):
        
            cellId = cellPicker.GetCellId()
             
            if (cellId >= 0):
             
                try:
                     
                    actorPolyData           = actorPicker.GetActor().GetMapper().GetInput()
                    jsonStringWithEdgeData  = actorPolyData.GetCellData().GetAbstractArray('CellData').GetValue(cellId)
                    
                    aux_dict = json.loads(jsonStringWithEdgeData)
                
                    print '[MSG] Selected edge : %s' %(aux_dict['selected_edge'])

                    # update interactorAnnotation with the edge name
                    
                    if (interactorAnnotation != None):
                        msg = 'Selected edge : %s' %(aux_dict['selected_edge'])
                        if (aux_dict['name'] not in {'',' ','[]'}):
                            name = HTMLParser.HTMLParser().unescape(aux_dict['name'])
                            msg = 'Selected : '+ unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
                        interactorAnnotation.SetInput(msg)
                        interactorAnnotation.SetPosition(clickPos[0], clickPos[1])
                        interactorAnnotation.GetProperty().SetOpacity(1)
                        interactor.Render()        
                    
                    f = open(temp_file_path, "w")
                    f.write(jsonStringWithEdgeData)
                    f.close()
                     
                except:
                    #print (sys.exc_info())
                    pass
             
            else:
             
                try:
                
                    f = open(temp_file_path, "w")
                    f.write(json.dumps({}))
                    f.close()
                
                except:
                    #print (sys.exc_info())
                    pass
        
        else:

            try:
                    
                f = open(temp_file_path, "w")
                f.write(json.dumps({}))
                f.close()
                 
            except:
                #print (sys.exc_info())
                pass
            
        self.OnLeftButtonDown()
        return
