'''

 Inria Chile - Flows In Networks (IV)
 
 Dynamic flow visualization

 * Main visualization code

'''

import sys, os
import networkx as nx
import random

import vtk

from numpy import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from lib.GUI.pyQT_GUI import * 

import lib.req.manage   as req_mn  # software requirements validation methods
import lib.vis.manage   as vis_mn  # visualization manage methods

class Visualization:
 
    def __init__(self,pars):
        
        self.network_name               = pars['NETWORK_NAME']
        self.TYPE                       = pars['TYPE']
        
        self.time_step                  = pars['TIME_STEP']
        self.Tmax                       = pars['T_MAX_VIS']

        self.globalNumberOfTimeSteps    = int(floor(self.Tmax/self.time_step))

        self.SIMULATION_DATA_AVAILABLE  = pars['SIMULATION_DATA_AVAILABLE']
        self.PRIORITY_GRAPHVIZ_LAYOUT   = pars['PRIORITY_GRAPHVIZ_LAYOUT']
        self.fps                        = pars['FPS']
        
        self.renderer                   = vtk.vtkRenderer()   
        
        self._initialize(pars)     
  
    def _initialize(self,pars):
        
        # Get network graph
        
        gml_file_path = os.path.join('.','projects',self.network_name,'data',str(self.network_name)+'.gml')
        G = vis_mn.get_graphFromGMLFile(gml_file_path)         
        G = nx.MultiDiGraph(G)   
        
        # Set VTK Elements according to the visualization type
        
        if (self.TYPE == 'geometry'):
            
            import lib.vis.styles.geometry  as vstyle
            vstyle.setScene(G,self.renderer,pars)
        
        if (self.TYPE == 'geometry2'):
            
            import lib.vis.styles.geometry2  as vstyle
            vstyle.setScene(G,self.renderer,pars)
            
        if (self.TYPE in ['n1']):
            
            import lib.vis.styles.networks1  as vstyle
            vstyle.setScene(G,self.renderer,pars)
                
    def setInteractorStyle(self,renderWindowInteractor):
        
        if (self.TYPE in ['geometry','geometry2']):
             
            renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleRubberBand3D())
        
        if (self.TYPE in ['n1']):
            
            renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleImage())
        
    def assignSimDataToEdges(self):
                
        print 'data'
        
    def update(self):
                
        print 'update'


class MainWindow(QtGui.QMainWindow):
 
    def __init__(self,viz,parent=None):

        ### GUI ###
        
        QtGui.QWidget.__init__(self,parent)
        self.ui                 = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('FlowsInNetworks')
 
        # GUI elements for animation
        
        self.timer                              = 0
        self.time_step                          = viz.time_step
        self.animation                          = False
        self.renderTimeInterval                 = 1000/(1.0*viz.fps)
        self.globalNumberOfTimeSteps            = viz.globalNumberOfTimeSteps
  
        self.timerObj                           = QtCore.QTimer()
        QtCore.QObject.connect(self.timerObj,QtCore.SIGNAL("timeout()"),self.updateForAnimation)
         
        self.ui.slider_11.setRange(0,viz.globalNumberOfTimeSteps)
        QtCore.QObject.connect(self.ui.slider_11,QtCore.SIGNAL('valueChanged(int)'),self.updateFromSlider)
    
        QtCore.QObject.connect(self.ui.btn_play,QtCore.SIGNAL('clicked()'),self.executeAnimation)

        ### VTKWidget ###

        self.vl                                 = QtGui.QVBoxLayout()
        self.ui.vtkFrame_4.setLayout(self.vl)
        self.vtkWidget                          = QVTKRenderWindowInteractor(self.ui.vtkFrame_4)
        self.vl.addWidget(self.vtkWidget)
        self.renderer   = viz.renderer
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        
        self.renderWindowInteractor = self.vtkWidget.GetRenderWindow().GetInteractor()
        viz.setInteractorStyle(self.renderWindowInteractor)
        
        self.show()
        
        self.renderWindowInteractor.Initialize()

    def updateVTKWidget(self,id_time):
        self.renderWindowInteractor.GetRenderWindow().Render()
        print 'update visualization'
    
    def playAnimation(self):
        self.timerObj.start(self.renderTimeInterval)
        print 'play'
     
    def stopAnimation(self):
        self.timerObj.stop()
        print 'stop'
     
    def updateSlider(self,timer):
        self.ui.slider_11.setSliderPosition(timer)
        aux_time = int(timer*self.time_step*10.0)/10.0
        self.ui.textSliderValue_11.setText(str(aux_time))    
        print 'updateSlider'
        
    def updateFromSlider(self):
        aux_time = self.ui.slider_11.value()
        self.timer = aux_time
        self.updateVTKWidget(aux_time)        
        self.updateSlider(aux_time)
        print 'updateFromSlider'
     
    def updateForAnimation(self):
        if (self.animation == True):
            aux_time = self.timer
            self.updateSlider(aux_time)
            self.timer += 1   
            if (self.timer > self.globalNumberOfTimeSteps):
                self.timer = 0
        print 'updateForAnimation'
     
    def executeAnimation(self):
        self.animation = not self.animation
         
        if (self.animation == True):
            self.playAnimation()
        else:
            self.stopAnimation()


if __name__ == "__main__":
    
    
    print '[Flows In Networks]'
    print 'Evaluation of required packages / modules...'
    
    pck_list            = ['numpy','vtk','networkx','PyQt4','pygraphviz','matplotlib','lxml']
    msg_list            = ['','','','','','','']
    
    available_modules   = req_mn.check_packages(pck_list,msg_list) 
    
    if (available_modules == True):
        
        print 'Searching network...'
        
        if (len(sys.argv) == 2):
            
            NETWORK_NAME        = str(sys.argv[1]).replace('.','')   
            project_path        = os.path.join('.','projects',NETWORK_NAME,'__init__.py')
            project_exists      = os.path.isfile(project_path)

            graph_path          = os.path.join('.','projects',NETWORK_NAME,'data',NETWORK_NAME+'.gml')
            graph_data_exists   = os.path.isfile(graph_path)
            
            if (project_exists == True):

                if (graph_data_exists == True):
        
                    print '[MSG] Found "'+str(NETWORK_NAME)+'" network data' 
                    print 'Loading GUI...'                           
                    
                    visualization_settings_file_path = os.path.join('.','projects',NETWORK_NAME)
                    pars = vis_mn.get_vparameters(visualization_settings_file_path) # visualization parameters

                    # Run application               

                    app = QtGui.QApplication(sys.argv)
                    viz = Visualization(pars)
                    ex  = MainWindow(viz)
                    
                    ex.show()
                    sys.exit(app.exec_())

                else:
                    print '[MSG] Graph data not found. Build update needed. [~$ python update.py '+NETWORK_NAME+ ' -b ] '
                    
            else:
                
                print '[MSG] Network not found'

        else:

            print '[MSG] Non-valid input data. Required network name.'
            
    
    
                