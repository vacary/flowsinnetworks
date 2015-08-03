'''

 Inria Chile - Flows In Networks (IV)
 
 Dynamic flow visualization

 * Main visualization code

'''

print '[FlowsInNetworks]'
print 'Loading...'


import sys, os
import networkx as nx
import random

import vtk

from numpy import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from lib.GUI.pyQT_GUI import * 

import lib.req.manage   as req_mn  # software requirements validation methods
import lib.vis.manage   as vis_mn  # visualization manage methods

import lib.vis.styles.geometry      as vstyle_gm
import lib.vis.styles.geometry2     as vstyle_gm2
import lib.vis.styles.networks0     as vstyle_n0
import lib.vis.styles.networks1     as vstyle_n1
import lib.vis.styles.networks2     as vstyle_n2

class Visualization:
 
    def __init__(self,pars):
        
        self.pars                       = pars
        
        self.network_name               = self.pars['NETWORK_NAME']
        self.TYPE                       = self.pars['TYPE']

        self.time_step                  = self.pars['TIME_STEP']
        self.Tmax                       = self.pars['T_MAX_VIS']

        self.globalNumberOfTimeSteps    = int(ceil(self.Tmax/self.time_step))

        self.SIMULATION_DATA_AVAILABLE  = self.pars['SIMULATION_DATA_AVAILABLE']
        self.PRIORITY_GRAPHVIZ_LAYOUT   = self.pars['PRIORITY_GRAPHVIZ_LAYOUT']
        self.fps                        = self.pars['FPS']
        
        self.renderer                   = vtk.vtkRenderer()
        
        self.G                          = None
        self.nw                         = None
        self.arrayOf_f_e_minus          = None
        self.arrayOf_Queues             = None
        
        self.time_id                    = 0
        
        self._initialize()     
  
    def _initialize(self):
        
        # Get network graph
        
        gml_file_path = os.path.join('.','projects',self.network_name,'data',str(self.network_name)+'.gml')
        G = vis_mn.get_graphFromGMLFile(gml_file_path)         
        G = nx.MultiDiGraph(G)   
        
        self.G = G
        
        # Set VTK Elements according to the visualization type
        
        if (self.TYPE == 'geometry'):

            vstyle_gm.setScene(self.G,self.renderer,self.pars)
        
        if (self.TYPE == 'geometry2'):
            
            vstyle_gm2.setScene(self.G,self.renderer,self.pars)
            
        if (self.TYPE in ['n0']):
            
            vstyle_n0.setScene(self.G,self.renderer,self.pars)            
            
        if (self.TYPE in ['n1']):
            
            self.getSimulationData()
            self.nw = vstyle_n1.setScene(self.G,self.renderer,self.pars)
            
        if (self.TYPE in ['n2']):
            
            self.getSimulationData()
            self.nw = vstyle_n2.setScene(self.G,self.renderer,self.pars)
            
    def setInteractorStyle(self,renderWindowInteractor):
        
        if (self.TYPE in ['geometry','geometry2']):
             
            renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleRubberBand3D())
        
        if (self.TYPE in ['n0','n1','n2']):
            
            renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleImage())
        
    def getSimulationData(self):
           
        # f_e_minus_data
        fm = file(os.path.join('.','projects',str(self.network_name),'data',str(self.network_name)+'_f_e_minus.dat'),'rb')
        self.arrayOf_f_e_minus  = load(fm)
        fm.close()
        
    def update(self,time_id):

        if (self.TYPE in ['n1']):
            vstyle_n1.update(time_id,self.G,self.nw,self.arrayOf_f_e_minus,self.pars,self.globalNumberOfTimeSteps)
            self.nw.vtkPolyData.Modified()
            
        if (self.TYPE in ['n2']):
            vstyle_n2.update(time_id,self.G,self.nw,self.arrayOf_f_e_minus,self.pars,self.globalNumberOfTimeSteps)
            self.nw.vtkPolyData.Modified()
                
        #print 'update'


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
        self.repeat                             = False
        self.renderTimeInterval                 = 1000/(1.0*viz.fps)
        self.globalNumberOfTimeSteps            = viz.globalNumberOfTimeSteps
  
        self.timerObj                           = QtCore.QTimer()
        QtCore.QObject.connect(self.timerObj,QtCore.SIGNAL("timeout()"),self.updateForAnimation)
         
        self.ui.slider_11.setRange(0,viz.globalNumberOfTimeSteps)
        QtCore.QObject.connect(self.ui.slider_11,QtCore.SIGNAL('valueChanged(int)'),self.updateFromSlider)
    
        QtCore.QObject.connect(self.ui.btn_play,QtCore.SIGNAL('clicked()'),self.playAnimation)
        QtCore.QObject.connect(self.ui.btn_pause,QtCore.SIGNAL('clicked()'),self.pauseAnimation)
        QtCore.QObject.connect(self.ui.btn_stop,QtCore.SIGNAL('clicked()'),self.stopAnimation)
        QtCore.QObject.connect(self.ui.btn_first,QtCore.SIGNAL('clicked()'),self.firstAnimation)
        QtCore.QObject.connect(self.ui.btn_last,QtCore.SIGNAL('clicked()'),self.lastAnimation)
        QtCore.QObject.connect(self.ui.btn_forward,QtCore.SIGNAL('clicked()'),self.forwardAnimation)
        QtCore.QObject.connect(self.ui.btn_back,QtCore.SIGNAL('clicked()'),self.backwardAnimation)
        QtCore.QObject.connect(self.ui.btn_repeat,QtCore.SIGNAL('clicked()'),self.repeatAnimation)

        ### VTKWidget ###

        self.vl                                 = QtGui.QVBoxLayout()
        self.ui.vtkFrame_4.setLayout(self.vl)
        self.vtkWidget                          = QVTKRenderWindowInteractor(self.ui.vtkFrame_4)
        self.vl.addWidget(self.vtkWidget)
        self.renderer = viz.renderer
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        
        self.renderWindowInteractor = self.vtkWidget.GetRenderWindow().GetInteractor()
        viz.setInteractorStyle(self.renderWindowInteractor)
        
        self.viz = viz
        
        self.show()
        
        self.renderWindowInteractor.Initialize()

    def updateVTKWidget(self,time_id):
        self.viz.update(time_id)
        self.renderWindowInteractor.GetRenderWindow().Render()
    
    def playAnimation(self):
        self.animation  = True
        self.timerObj.start(self.renderTimeInterval)

    def repeatAnimation(self):
        self.animation  = True
        self.repeat     = True
        self.timerObj.start(self.renderTimeInterval)

    def pauseAnimation(self):
        self.animation = False
        self.timerObj.stop()
        self.updateSlider(self.timer)
     
    def stopAnimation(self):
        self.animation = False
        self.timerObj.stop()
        self.updateSlider(0)
     
    def firstAnimation(self):
        self.animation = False
        self.timerObj.stop()
        self.updateSlider(0)

    def lastAnimation(self):
        self.animation = False
        self.timerObj.stop()
        self.updateSlider(self.globalNumberOfTimeSteps)
     
    def forwardAnimation(self):
        self.animation = False
        self.timerObj.stop()
        aux_time = self.timer
        if (self.timer < self.globalNumberOfTimeSteps):
            aux_time = self.timer + 1
        self.updateSlider(aux_time)
                
    def backwardAnimation(self):
        self.animation = False
        self.timerObj.stop()
        aux_time = self.timer
        aux_time = int(max(self.timer - 1,0))
        self.updateSlider(aux_time)
        
    def updateSlider(self,timer):
        self.ui.slider_11.setSliderPosition(timer)
        aux_time = int(timer*self.time_step*10.0)/10.0
        self.ui.textSliderValue_11.setText(str(aux_time))    
        
    def updateFromSlider(self):
        aux_time = self.ui.slider_11.value()
        self.timer = aux_time
        self.updateVTKWidget(aux_time)        
        self.updateSlider(aux_time)
     
    def updateForAnimation(self):
        if (self.animation == True):
            aux_time = self.timer
            self.updateSlider(aux_time)
            self.timer += 1   
            if (self.timer > self.globalNumberOfTimeSteps):
                  
                if (self.repeat == False):
                    self.timer = self.globalNumberOfTimeSteps
                    self.pauseAnimation()
                else:
                    self.timer = 0
                    self.playAnimation()
                    

    def executeAnimation(self):
        self.animation = not self.animation
        
        if (self.animation == True):
            self.playAnimation()      
        else:
            self.pauseAnimation()
            
if __name__ == "__main__":
    
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
            
    
    
                