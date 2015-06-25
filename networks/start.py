'''

 Inria Chile - Flows In Networks (II)
 
 Dynamic flow visualization

 * Main visualization code

'''

import sys, os
import networkx as nx
import random

import vtk
import lib.vfc as vis
import manage as mn

from numpy import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from lib.pyQT_GUI import * 

## About this modules:
## fvc.py      : classes and functions for the visualization
## pyQT_GUI.py : GUI interface

INTERACTOR_STYLE = '3D'

class mainWindow(QtGui.QMainWindow):

    def __init__(self,pars,parent=None):
        
        
        ''' GUI / VTK and parameters for visualization
        '''
        
        # set parameters
        nList    = pars[0]
        vList    = pars[1]
        
        for par in nList:
    
            c = nList.index(par)        
            
            if (par == 'NETWORK_NAME'):
                self.network_name = str(vList[c]).replace('"','')
            if (par == 'TIME_STEP'):
                self.time_step = float(vList[c])
            if (par == 'T_MAX_VIS'):
                self.Tmax = float(vList[c])
            if (par == 'FPS'):
                self.fps = int(vList[c])
            if (par == 'SIMULATION_DATA_AVAILABLE'):
                self.SIMULATION_DATA_AVAILABLE = int(vList[c])
            if (par == 'PRIORITY_GRAPHVIZ_LAYOUT'):
                self.PRIORITY_GRAPHVIZ_LAYOUT = int(vList[c])
            if (par == 'TYPE'):
                self.TYPE = str(vList[c])
            
            
        self.globalNumberOfTimeSteps    = int(floor(self.Tmax/self.time_step))
        self.renderTimeInterval         = 1000/(1.0*self.fps)

        # variables
        self.time                       = 0.0
        self.timer_count                = 0
        self.animation                  = False

        # GUI
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.info = mn.get_GUI_info(INTERACTOR_STYLE) # call the method with the visualization description
        self.setWindowTitle('FlowsInNetworks')
 
        ## GUI elements for animation
        self.edgesElements = []
       
        self.timerObj = QtCore.QTimer()
        QtCore.QObject.connect(self.timerObj,QtCore.SIGNAL("timeout()"),self.updateForAnimation)
        
        ### slider
        self.ui.slider_11.setRange(0,self.globalNumberOfTimeSteps)
        QtCore.QObject.connect(self.ui.slider_11,QtCore.SIGNAL('valueChanged(int)'),self.updateFromSlider)
        # * automatic visualization update under changes in the slider value
        
        ### button
        self.ui.animationButton_11.setText('Play')
        QtCore.QObject.connect(self.ui.animationButton_11,QtCore.SIGNAL('clicked()'),self.executeAnimation)    
        
        ###########        
        ### vtk
        ###
        self.setVTKWidget() # call the method to set the VTKWidget components

    def setVTKWidget(self):
        
        ''' VTKWidget Components
                
            * Main functions to set the visualization scene 
        '''

        # Widget and GUI
        self.vl = QtGui.QVBoxLayout()
        self.ui.vtkFrame_4.setLayout(self.vl)
        self.vtkWidget = QVTKRenderWindowInteractor(self.ui.vtkFrame_4)
        self.vl.addWidget(self.vtkWidget)
         
        # Add renderer 
        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.renderWindowInteractor = self.vtkWidget.GetRenderWindow().GetInteractor()
                
        ######
        #
        # Call the methods with VTK sources, mappers and actors needed to create the scene
        #
        
        ''' Network data
        '''
        path            = os.path.abspath(os.path.join('temp'))
        self.nxGraph    = mn.get_graphFromGMLFile(self.network_name) # Graph
        
        # VTK Elements     
        self.setVTKElements()
        
        if (self.SIMULATION_DATA_AVAILABLE == 1):
            
            self.getSimulationData()
        
        # Set Camera
        self.renderer.ResetCamera()
        
        self.show()
 
        # Set Interactor
      
        if (INTERACTOR_STYLE == 'StyleImage'):
            self.renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleImage())
        else:
            self.renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleRubberBand3D())
         
        # Render
         
        self.renderWindowInteractor.Initialize()        

    def setVTKElements(self):

        ##
        # Graph and visualization elements
        #
        
        ''' Graph
        '''
        if (self.PRIORITY_GRAPHVIZ_LAYOUT == 1):
            self.nodeRadius = 6.0
            self.opacity = 1.0 
            self.rwidth = 0.3
            self.q_opacity = 1.0
            self.scale = 1.0
            self.lbFontSize = 14
        else:
            self.nodeRadius = 12.0
            self.rwidth = 0.3
            self.opacity = 1.0
            self.q_opacity = 1.0
            self.scale = 1.0
            self.lbFontSize = 14
            
        if (self.TYPE == '"1"'):
            self.nodeRadius = 0.0005
            self.rwidth = 0.00002
            self.opacity = 1.0
            self.q_opacity = 0
            self.scale = 20000.0
            self.lbFontSize = 10
        
        #nodes         
        self.renderer.AddActor(vis.vtkNodesElementGlyph(self.nxGraph,self.nodeRadius,self.opacity,self.lbFontSize).vtkActor)     
        self.renderer.AddActor2D(vis.vtkNodesElementGlyph(self.nxGraph,self.nodeRadius,self.opacity,self.lbFontSize).vtkActor2D) #labels for each node

        #edges
        
        for e in sorted(set(self.nxGraph.edges_iter())):
 
            edges = self.nxGraph.edge[e[0]][e[1]]

            if (len(edges) == 1):
         
                    edgeElement = vis.get_CustomVTKGraphLine(self.nxGraph,edges,e[0],e[1],self.time_step,self.globalNumberOfTimeSteps,self.rwidth,self.scale)
                    #
                    self.renderer.AddActor(edgeElement.vtkElement.vtkActor)
                    self.renderer.AddActor(edgeElement.vtkQueue.vtkActor)
                    self.renderer.AddActor(edgeElement.vtkQBox.vtkActor)
                    #
                    self.edgesElements.append(edgeElement)
 
                    edgeElement.vtkQueue.vtkActor.GetProperty().SetOpacity(self.q_opacity)
                    edgeElement.vtkQBox.vtkActor.GetProperty().SetOpacity(self.q_opacity)
 
            else:

                c = 0
                mult = 0
                while (c < len(edges)):

                    plusFactor = (-1)**(c+1)
                    angleForArc = 18
                    
                    if (c%2 == 0 and c > 0):
                        mult = mult + angleForArc   
                    
                    angleForArc = angleForArc + mult                 
                    
                    edgeElement = vis.get_CustomVTKGraphArc(self.nxGraph,edges,c,e[0],e[1],plusFactor,angleForArc,self.time_step,self.globalNumberOfTimeSteps,self.rwidth,self.scale)
                    #
                    self.renderer.AddActor(edgeElement.vtkElement.vtkActor)
                    self.renderer.AddActor(edgeElement.vtkQueue.vtkActor)
                    self.renderer.AddActor(edgeElement.vtkQBox.vtkActor)
                    #
                    self.edgesElements.append(edgeElement)
                    
                    edgeElement.vtkQueue.vtkActor.GetProperty().SetOpacity(self.q_opacity)
                    edgeElement.vtkQBox.vtkActor.GetProperty().SetOpacity(self.q_opacity)
                                        
                    c = c + 1
    
        ''' Visualization elements
        '''

        #Text elements
              
        annotation1 = vtk.vtkCornerAnnotation() 
        annotation1.SetText(2,self.info)
        annotation1.SetMaximumFontSize(14)
        annotation1.GetTextProperty().SetColor(0.75,0.75,0.75)
        self.renderer.AddViewProp(annotation1)

        numberOfNodes = self.nxGraph.number_of_nodes()
        numberOfEdges = self.nxGraph.number_of_edges()
        
        data_msg = ''
        if (self.SIMULATION_DATA_AVAILABLE == 0):
            data_msg = '\n  * Comment: No simulation data \n'
        
        msg = ['  NETWORK \n\n','  '+str(self.network_name)+'\n\n','  '+str(numberOfNodes),' nodes\n','  '+str(numberOfEdges),' edges\n\n','  time step: ',str(self.time_step)+'\n'+data_msg]     
        annotation2 = vtk.vtkCornerAnnotation() 
        annotation2.SetText(0,''.join(msg))
        annotation2.SetMaximumFontSize(14)
        self.renderer.AddViewProp(annotation2)
        
    def getSimulationData(self):
        
        fm = file(os.path.join('.','projects',str(self.network_name),'data',str(self.network_name)+'_f_e_minus.dat'),'rb')
        q = file(os.path.join('.','projects',str(self.network_name),'data',str(self.network_name)+'_z_e.dat'),'rb')
        
        self.arrayOf_f_e_minus = load(fm)
        self.arrayOfQueues = load(q)
        
        fm.close()
        q.close()
        

        for j in xrange(len(self.edgesElements)):
             
            edge_key = self.edgesElements[j].ID

            if (self.edgesElements[j].nodeStart != 'd'):

                # outflow
  
                for k in xrange(self.edgesElements[j].globalNumberOfTimeDivisions+1):
                    for i in xrange(self.edgesElements[j].numberOfTimeStepsForEdge+1):
                      
                        if (i==0):
 
                            self.edgesElements[j].FlowData[k][i] = self.arrayOf_f_e_minus[k,edge_key]
                                  
                        else:
                            if (i <= self.edgesElements[j].numberOfTimeStepsForEdge):
                                self.edgesElements[j].FlowData[k][i] = self.edgesElements[j].FlowData[k-1][i-1]    
                                
                               

    def updateVisualization(self,id_t):

        ''' Scene update method
        '''

    # Changes in the scene only if simulation data is available

        
        if (self.SIMULATION_DATA_AVAILABLE == 1):
         
            for j in xrange(len(self.edgesElements)):
                   
                for i in xrange(self.edgesElements[j].numberOfTimeStepsForEdge+1):
     
                    # EDGES
               
                    mflowValue = self.edgesElements[j].getData(id_t,i)
                    flowValue = max(mflowValue, 0)
                     
                    if (mflowValue > 0):
                        self.edgesElements[j].vtkElement.setColorById(i,[0,0,int(205 + 50*flowValue/4.0)]) # mod blue
                        self.edgesElements[j].vtkElement.setWidthById(i,flowValue)
                    elif (mflowValue == 0):
                        self.edgesElements[j].vtkElement.setColorById(i,[50,50,50])
                        self.edgesElements[j].vtkElement.setWidthById(i,0.01)
                    else:
                        self.edgesElements[j].vtkElement.setColorById(i,[10,10,10])
                        self.edgesElements[j].vtkElement.setWidthById(i,0.01)
       
                    if (self.edgesElements[j].nodeStart != 'd'):
          
                        # QUEUES
          
                        edge_key = self.edgesElements[j].ID
          
                        mqValue = self.arrayOfQueues[id_t][edge_key]
                        qValue = max(mqValue, 1e-5)
                           
                        if (mqValue != -1):
                            self.edgesElements[j].vtkQBox.vtkActor.GetProperty().SetColor(0.5,0.5,0.5)
                            self.edgesElements[j].vtkQueue.vtkActor.GetProperty().SetColor(0,1.0,0)
                            self.edgesElements[j].vtkQueue.setEndPointFromValue(2*max(qValue,1e-5))
                            if (mqValue <= 1e-5):
                                self.edgesElements[j].vtkQueue.vtkActor.GetProperty().SetOpacity(0)
                            else:
                                if (self.q_opacity != 0):
                                    self.edgesElements[j].vtkQueue.vtkActor.GetProperty().SetOpacity(1)
                        else:
                            self.edgesElements[j].vtkQBox.vtkActor.GetProperty().SetColor(0.1,0.1,0.1)
                            self.edgesElements[j].vtkQueue.vtkActor.GetProperty().SetColor(0.1,0.1,0.1)
                         
       
                self.edgesElements[j].vtkElement.vtkPolyData.Modified()
                self.edgesElements[j].vtkQueue.vtkPolyData.Modified()
                     
            self.renderWindowInteractor.GetRenderWindow().Render()

    def playAnimation(self):
        self.timerObj.start(self.renderTimeInterval)
    
    def stopAnimation(self):
        self.timerObj.stop()
    
    def updateSlider(self,id_t):
        self.ui.slider_11.setSliderPosition(id_t)
        aux = int(id_t*self.time_step*10.0)/10.0
        self.ui.textSliderValue_11.setText(str(aux))        
    
    def updateFromSlider(self):
        id_t = self.ui.slider_11.value()
        self.timer_count = id_t
        self.updateSlider(id_t)
        self.updateVisualization(id_t)
    
    def updateForAnimation(self):
        if (self.animation == True):
            
            id_t = self.timer_count
            self.updateSlider(id_t)
            
            self.timer_count += 1   
             
            if (self.timer_count > self.globalNumberOfTimeSteps):
                
                self.timer_count = 0
    
    def executeAnimation(self):
        self.animation = not self.animation
        
        if (self.animation == True):
            self.ui.animationButton_11.setText('Stop')
            self.playAnimation()
        else:
            self.ui.animationButton_11.setText('Play')
            self.stopAnimation()


if __name__ == "__main__":
    
    print '[Flows In Networks]'
    print 'Evaluation of required packages / modules...'
    
    pck_list            = ['numpy','vtk','networkx','PyQt4','pygraphviz','matplotlib']
    msg_list            = ['','','','','[optional]','']
    available_modules   = mn.check_packages(pck_list,msg_list) 
    
    if (available_modules == True):
        
        print 'Searching network...'
        
        if (len(sys.argv) == 2):
            
            NETWORK_NAME        = str(sys.argv[1]).replace('.','')   
            project_path        = os.path.join('.','projects',NETWORK_NAME,'__init__.py')
            valid_name          = os.path.isfile(project_path)

            graph_path          = os.path.join('.','projects',NETWORK_NAME,'data',NETWORK_NAME+'.gml')
            graph_data_exists   = os.path.isfile(graph_path)
            
            if (valid_name == True):

                if (graph_data_exists == True):
        
                    print '[MSG] Found "'+str(NETWORK_NAME)+'" network data' 
                    print 'Loading GUI...'                           
                    
                    pars = mn.get_vparameters(NETWORK_NAME) # visualization parameters
    
                    ##
                    # Run application                
                    #
                    app = QtGui.QApplication(sys.argv)
                    ex = mainWindow(pars)
                    ex.show()
                    sys.exit(app.exec_())

                else:
                    print '[MSG] Graph data not found. Update needed. [~$ python update.py '+NETWORK_NAME+ '] '
                    

            else:
                
                print '[MSG] Network not found'

        
        else:

            print '[MSG] Non-valid input data. Required network name.'
        
                
    
    
    
