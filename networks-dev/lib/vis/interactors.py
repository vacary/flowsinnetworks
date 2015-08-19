
import vtk

def getArrayFromStrList(str_list):

    str_list    = str_list[1:-1]
    output      = [float(elm) for elm in str_list.split(',')]
    
    return output

class CustomInteractorStyle(vtk.vtkInteractorStyleImage):
    
    def __init__(self,renderer,G,parent=None):
        
        self.G = G
        
        self.annotation = vtk.vtkTextActor()
        self.setAnnotation(renderer)
        
        self.AddObserver("LeftButtonPressEvent",self.leftButtonPressEvent)
        
    def setAnnotation(self,renderer):
        
        self.annotation.GetTextProperty().SetFontSize(14)
        self.annotation.GetTextProperty().SetBold(1)
        self.annotation.GetTextProperty().SetItalic(0)
        self.annotation.GetTextProperty().SetShadow(0)
        self.annotation.SetPosition(0,0)
        self.annotation.SetInput(" ")
        
        renderer.AddActor(self.annotation)
        
    def leftButtonPressEvent(self,obj,event):
        
        interactor  = self.GetInteractor()
        renderer    = self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer()
        pos         = self.GetInteractor().GetEventPosition()

        picker  = vtk.vtkCellPicker()
        picker.SetTolerance(0.0005)
        picker.Pick(pos[0],pos[1],0,renderer)
        
        worldPos    = picker.GetPickPosition()
        
        pickerActor = vtk.vtkPropPicker()
        pickerActor.Pick(pos[0],pos[1],0,renderer)
     
        #print "Cell id is: %i" %(picker.GetCellId())

        cellID = picker.GetCellId()
        
        if (cellID >= 0):
            
            try:
                actorPolyData = pickerActor.GetActor().GetMapper().GetInput()
                
                try:
                    edge_aux = actorPolyData.GetCellData().GetArray("CellEdges").GetTuple(cellID)
                    
                    edge = [int(edge_aux[0]),int(edge_aux[1]),int(edge_aux[2])]
                    
                    ntail   = edge[0]
                    nhead   = edge[1]
                    k       = edge[2]
                    
                    #print "Selected edge: %s" %(edge)
                    
                    ntail_label_overtime    = getArrayFromStrList(self.G.node[ntail]['label_overtime'])
                    nhead_label_overtime    = getArrayFromStrList(self.G.node[nhead]['label_overtime'])
                    f_e_plus_overtime       = getArrayFromStrList(self.G.edge[ntail][nhead][k]['f_e_plus_overtime'])
                    f_e_minus_overtime      = getArrayFromStrList(self.G.edge[ntail][nhead][k]['f_e_minus_overtime'])
                    switching_times         = getArrayFromStrList(self.G.edge[ntail][nhead][k]['switching_times'])
                    z_e_overtime            = getArrayFromStrList(self.G.edge[ntail][nhead][k]['z_e_overtime'])
                    
                    
                    msg = 'Selected edge: (%i, %i) "%i" \n' %(edge[0],edge[1],edge[2])
                    self.annotation.SetPosition(pos[0],pos[1])
                    self.annotation.SetInput(msg)
                    interactor.Render()
                    #print z_e_overtime
                    
                except:
                    
                    self.annotation.SetInput(" ")
                    
                    pass
            except:
                
                pass
        
        else:
            
            self.annotation.SetInput(" ")
        
        #print "Left Button pressed"
        self.OnLeftButtonDown()
        return