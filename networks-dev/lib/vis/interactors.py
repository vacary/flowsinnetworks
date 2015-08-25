
import sys, os
import vtk
import json

class CustomInteractorStyle(vtk.vtkInteractorStyleRubberBand3D):#(vtk.vtkInteractorStyleImage):
    
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

                    # update interactorAnnotation
                    
                    if (interactorAnnotation != None):
                        msg = 'Selected edge : %s' %(aux_dict['selected_edge'])
                        interactorAnnotation.SetInput(msg)
                        interactorAnnotation.SetPosition(clickPos[0],clickPos[1])
                        interactorAnnotation.GetProperty().SetOpacity(1)
                        interactor.Render()        
                    
                    f = open(os.path.join('.','temp','data.txt'),"w")
                    f.write(jsonStringWithEdgeData)
                    f.close()
                     
                except:
                    print (sys.exc_info())
                    pass
             
            else:
             
                try:
                
                    f = open(os.path.join('.','temp','data.txt'),"w")
                    f.write(json.dumps({}))
                    f.close()
                     
                except:
                    print (sys.exc_info())
                    pass
        

        self.OnLeftButtonDown()
        return
    
    