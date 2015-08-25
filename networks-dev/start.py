'''

 Inria Chile - Flows In Networks
 
 Dynamic flow visualization

 * Main visualization code

'''

print '[FlowsInNetworks]'
print 'Loading...'

import sys, os
import networkx as nx
import random
import json

import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure 
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
from numpy import *
import time

import vtk
output = vtk.vtkFileOutputWindow()
output.SetFileName("log.txt")
vtk.vtkOutputWindow().SetInstance(output)

from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor # QT Gui

from lib.GUI.MainWindow import *
import lib.GUI.Dialog as Qt_Dialog

import lib.req.manage               as req_mn  # software requirements validation methods
import lib.vis.manage               as vis_mn  # visualization manage methods
import lib.vis.interactors          as interactors
import lib.vis.styles.geometry      as vstyle_gm
import lib.vis.styles.network       as vstyle_nw
import lib.vis.styles.interactor    as vstyle_iren

class Visualization:
 
    def __init__(self,pars):
        
        self.pars                       = pars
        
        self.network_name               = self.pars['NETWORK_NAME']
        self.TYPE                       = self.pars['TYPE']

        self.time_step                  = self.pars['TIME_STEP']
        self.Tmax                       = self.pars['T_MAX_VIS']

        self.globalNumberOfTimeSteps    = int(floor(self.Tmax/self.time_step))

        self.SIMULATION_DATA_AVAILABLE  = self.pars['SIMULATION_DATA_AVAILABLE']
        self.PRIORITY_GRAPHVIZ_LAYOUT   = self.pars['PRIORITY_GRAPHVIZ_LAYOUT']
        self.fps                        = self.pars['FPS']
        
        self.renderer                   = vtk.vtkRenderer()
        self.interactor                 = None
        self.interactorAnnotation       = vtk.vtkTextActor()
        
        self.G                          = None
        self.nw                         = None
        self.arrayOf_f_e_minus          = None
        self.arrayOf_Queues             = None
        
        self.style_pars                 = {}
        
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
        
        if (self.TYPE in ['network']):
            
            self.getSimulationData()
            self.nw = vstyle_nw.setScene(self.G,self.renderer,self.pars,self.style_pars)
  
        if (self.TYPE in ['interactor']):
        
            self.setInteractorAnnotation()
            self.getSimulationData()
            self.nw = vstyle_iren.setScene(self.G,self.renderer,self.pars,self.style_pars)      
            
    def setInteractorAnnotation(self):
        
        self.interactorAnnotation.GetTextProperty().SetFontSize(14)
        self.interactorAnnotation.GetTextProperty().SetBold(1)
        self.interactorAnnotation.GetTextProperty().SetItalic(0)
        self.interactorAnnotation.GetTextProperty().SetShadow(0)
        self.interactorAnnotation.SetInput('Selected edge : ')
        self.interactorAnnotation.SetPosition(0,0)
        self.interactorAnnotation.GetProperty().SetOpacity(0)
        
        self.renderer.AddActor(self.interactorAnnotation)
        
    def setInteractor(self,renderWindowInteractor):
        
        self.interactor = renderWindowInteractor 

    def setInteractorStyle(self,renderWindowInteractor):
        
        if (self.TYPE in ['geometry']):
             
            renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleRubberBand3D())
        
        if (self.TYPE in ['network']):
        
            renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleImage())
        
        if (self.TYPE in ['interactor']):

            renderWindowInteractor.SetInteractorStyle(interactors.CustomInteractorStyle())
        
    def getSimulationData(self):
           
        # f_e_minus_data
        fm = file(os.path.join('.','projects',str(self.network_name),'data',str(self.network_name)+'_f_e_minus.dat'),'rb')
        self.arrayOf_f_e_minus  = load(fm)
        fm.close()
        
        self.style_pars['max_f_e_minus'] = self.arrayOf_f_e_minus.max()
        
        # z_e_minus_data
        fm = file(os.path.join('.','projects',str(self.network_name),'data',str(self.network_name)+'_z_e.dat'),'rb')
        self.arrayOf_z_e  = load(fm)
        fm.close()
        
        self.style_pars['max_z_e'] = self.arrayOf_z_e.max()        
        
        
    def update(self,time_id):

        if (self.TYPE in ['network']):
            
            print self.G.nodes()
            
            vstyle_nw.update(time_id,self.G,self.nw,self.arrayOf_f_e_minus,self.arrayOf_z_e,self.pars,self.globalNumberOfTimeSteps)

            self.nw.vtkPolyData.Modified()
            self.nw.vtkQPolyData.Modified()
            self.nw.vtkQBoxesPolyData.Modified()

        if (self.TYPE in ['interactor']):
             
            vstyle_iren.update(time_id,self.G,self.nw,self.arrayOf_f_e_minus,self.arrayOf_z_e,self.pars,self.globalNumberOfTimeSteps)
 
            self.nw.vtkPolyData.Modified()
            self.nw.vtkQPolyData.Modified()
            self.nw.vtkQBoxesPolyData.Modified()
  
  
class PlotDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        
        QtGui.QDialog.__init__(self,parent)
        self.ui = Qt_Dialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Simulation Data')

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.layout = self.ui.verticalLayout
        self.layout.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas,self,coordinates=True)
        self.layout.addWidget(self.toolbar)

    def update(self,time):
            
        self.fig.clf()
                
        edge_dict = {}
        
        try:                
            f               = open(os.path.join('.','temp','data.txt'),"r")
            json_edge_dict  = f.readline()
            edge_dict       = json.loads(json_edge_dict)
            f.close()
        except:
            print (sys.exc_info())
            pass
        
        if (bool(edge_dict)):
            
            max_fe_1 = max(edge_dict['f_e_plus_overtime'] )
            max_fe_2 = max(edge_dict['f_e_minus_overtime'] )
            y_lim = 1.05*max(max_fe_1,max_fe_2)
            
            
            edge_capacity    = edge_dict['capacity']
            
            # z_e_overtime arrays
 
            ax = self.fig.add_subplot(311)
            x_data = edge_dict['switching_times']
            y_data = edge_dict['z_e_overtime']
            ax.plot(x_data,y_data,'b')
            ax.plot([time,time],[0,1.05*max(y_data)],'r',linewidth="2")
            ax.set_title('z_e overtime')
            
            # f_e_plus_overtime
               
            vx = edge_dict['ntail_label_overtime']
            vy = edge_dict['f_e_plus_overtime'] 
               
            x_data = []
            y_data = []
               
            for i in xrange(len(vx)-1):
                x_data.append(vx[i])
                y_data.append(vy[i])
                x_data.append(vx[i+1])
                y_data.append(vy[i])
   
            ax = self.fig.add_subplot(312)
            ax.plot(x_data,y_data,'b')
            ax.plot([time,time],[0,y_lim],'r',linewidth="2")
            ax.plot([0,max(x_data)],[edge_capacity,edge_capacity],'g')
            ax.set_title('f_e_plus_overtime')
            
            # f_e_minus_overtime
               
            vx = edge_dict['nhead_label_overtime']
            vy = edge_dict['f_e_minus_overtime'] 
               
            x_data = []
            y_data = []
               
            for i in xrange(len(vx)-1):
                x_data.append(vx[i])
                y_data.append(vy[i])
                x_data.append(vx[i+1])
                y_data.append(vy[i])
   
            ax = self.fig.add_subplot(313)
            ax.plot(x_data,y_data,'b')
            ax.plot([time,time],[0,y_lim],'r',linewidth="2")
            ax.plot([0,max(x_data)],[edge_capacity,edge_capacity],'g')
            ax.set_title('f_e_minus_overtime')
  
            self.fig.suptitle("Simulation results for edge "+str(edge_dict['selected_edge']))
                        
            self.fig.subplots_adjust(bottom=0.1,left=0.1,right=0.9,top=0.90,hspace=0.3)   
        
            self.canvas.draw()
            
            self.show()
            
        else:
            
            print '[MSG] No edge selected'        
        
        #gc.collect()


class MainWindow(QtGui.QMainWindow):
 
    def __init__(self,viz,parent=None):

        ### GUI ###
        
        QtGui.QWidget.__init__(self,parent)
        self.ui                 = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.dialog_plot = PlotDialog() #! 

        self.setWindowTitle('FlowsInNetworks')
 
        # GUI elements for animation
        
        self.timer                              = 0
        self.time_step                          = viz.time_step
        self.animation                          = False
        self.repeat                             = False
        self.renderTimeInterval                 = 1000/(1.0*viz.fps)
        self.globalNumberOfTimeSteps            = viz.globalNumberOfTimeSteps
        
        #self.writer                        = vtk.vtkFFMPEGWriter()
  
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

        #QtCore.QObject.connect(self.ui.btn_plot,QtCore.SIGNAL('clicked()'),self.plotSourceData)
        QtCore.QObject.connect(self.ui.btn_plot,QtCore.SIGNAL('clicked()'),self.showPlotDialog)

        ### VTKWidget ###

        self.viz                                = viz

        self.vl                                 = QtGui.QVBoxLayout()
        self.ui.vtkFrame_4.setLayout(self.vl)
        self.vtkWidget                          = QVTKRenderWindowInteractor(self.ui.vtkFrame_4)
        self.vl.addWidget(self.vtkWidget)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.viz.renderer)
        
        self.renderWindow = self.vtkWidget.GetRenderWindow()
        self.renderWindowInteractor = self.renderWindow.GetInteractor()
        self.viz.setInteractor(self.renderWindowInteractor)
        self.viz.setInteractorStyle(self.renderWindowInteractor)
        self.viz.renderer.GetActiveCamera().ParallelProjectionOn()
        self.viz.renderer.ResetCamera()
        
        self.show()
        
        self.renderWindowInteractor.Initialize()
        self.renderWindowInteractor.Start()
           
#         windowToImageFilter = vtk.vtkWindowToImageFilter()
#         windowToImageFilter.SetInput(self.renderWindow)
#         windowToImageFilter.SetInputBufferTypeToRGBA()
#         windowToImageFilter.ReadFrontBufferOff()
#         windowToImageFilter.Update()
        
#         self.writer.SetInputConnection(windowToImageFilter.GetOutputPort())
#         self.writer.SetFileName("test.avi")        
        
    def updateVTKWidget(self,time_id):
        self.viz.update(time_id)
        self.renderWindowInteractor.GetRenderWindow().Render()
        
    def playAnimation(self):
        self.animation  = True
        self.repeat     = False
        self.timerObj.start(self.renderTimeInterval)
#         self.writer.Start()

    def repeatAnimation(self):
        self.animation  = True
        self.repeat     = True
        self.timerObj.start(self.renderTimeInterval)

    def pauseAnimation(self):
        self.animation = False
        self.timerObj.stop()
        self.updateSlider(self.timer)
#         self.writer.End()
        
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
        if (self.timer > 0):
            aux_time = self.timer - 1
        self.updateSlider(aux_time)
        
    def updateSlider(self,timer):
        #self.writer.Write()
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
                    self.repeatAnimation()

    def executeAnimation(self):
        self.animation = not self.animation
        
        if (self.animation == True):
            self.playAnimation()      
        else:
            self.pauseAnimation()

    def showPlotDialog(self):
        
        if (self.viz.TYPE in ['interactor']):

            time = self.timer*self.time_step
            self.dialog_plot.update(time)
            
    def closeEvent(self,event):

        f = open(os.path.join('.','temp','data.txt'),"w")
        f.write(json.dumps({}))
        f.close()
        
        self.dialog_plot.close()
        event.accept()
        
            
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
            
    
    
                
