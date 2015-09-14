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

import lib.vis.interactor           as interactor
import lib.vis.styles.network       as vstyle_nw


class Visualization:
 
    def __init__(self, pars):
        
        self.pars = pars
        
        self.network_name = self.pars['NETWORK_NAME']
        self.TYPE = self.pars['TYPE']

        self.time_step = self.pars['TIME_STEP']
        self.Tmax = self.pars['T_MAX_VIS']

        self.SIMULATION_DATA_AVAILABLE = self.pars['SIMULATION_DATA_AVAILABLE']
        self.PRIORITY_GRAPHVIZ_LAYOUT = self.pars['PRIORITY_GRAPHVIZ_LAYOUT']
        self.fps = self.pars['FPS']
        
        self.globalNumberOfTimeSteps = int(floor(self.Tmax/self.time_step))
        
        self.renderer = vtk.vtkRenderer()
        self.interactorAnnotation = vtk.vtkTextActor()
        
        self.G = None
        
        self.nw                 = None
        self.nw_nodes           = None
        self.nw_data_times      = None
        self.nw_data_capacities = None
        
        self.annotation_info_nw     = None
        self.annotation_info_iren   = None
        
        self.show_colorbar              = True
        self.show_annotations           = False        
        self.show_nodes_st_labels       = True
        self.show_data_layer_time       = False
        self.show_data_layer_capacity   = False
        self.show_nodes_non_st_labels   = False
              
        self.arrayOf_f_e_minus  = None
        self.arrayOf_Queues     = None
        
        self.interactor = None
        
        self.style_pars = {}
        self.time_id = 0
        
        self._initialize()
  
    def _initialize(self):
        
        # Get network graph
        
        gml_file_path = os.path.join('.','projects',self.network_name,'data',str(self.network_name)+'.gml')
        
        G = vis_mn.get_graphFromGMLFile(gml_file_path)         
        G = nx.MultiDiGraph(G)   

        self.G = G
        
        # Set VTK Elements according to the visualization type
        
        if (self.TYPE in ['network']):
            
            self.setInteractorAnnotation()
            self.getSimulationData()
            vtkElements = vstyle_nw.scene_setup(self.G,self.renderer,self.pars,self.style_pars)
  
            self.nw = vtkElements['nw']
            self.nw_data_times = vtkElements['nw_data_times']
            self.nw_data_capacities = vtkElements['nw_data_capacities']
            self.nw_nodes= vtkElements['nw_nodes']
            self.annotation_info_nw = vtkElements['annotation_info_nw']
            self.annotation_info_iren = vtkElements['annotation_info_iren']            
            
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
        
        if (self.TYPE in ['network']):
        
            renderWindowInteractor.SetInteractorStyle(interactor.CustomInteractorStyle())
        
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
             
            vstyle_nw.update(time_id,self.G,self.nw,self.arrayOf_f_e_minus,self.arrayOf_z_e,self.pars,self.globalNumberOfTimeSteps)
 
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
            
            edge_capacity    = edge_dict['capacity']
            
            max_fe_1 = max(edge_dict['f_e_plus_overtime'] )
            max_fe_2 = max(edge_dict['f_e_minus_overtime'] )
            max_fe_3 = edge_capacity 
            y_lim = 1.05*max(max_fe_1,max_fe_2,max_fe_3)
            
            # z_e_overtime arrays
 
            ax = self.fig.add_subplot(311)
            x_data = edge_dict['switching_times']
            y_data = edge_dict['z_e_overtime']
            ax.plot(x_data,y_data,'b')
            
            ax.axvline(x=time,color='r')
            #ax.plot([time,time],[0,1.05*max(y_data)],'r',linewidth="2")
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
  
            title = "Simulation results for edge "+str(edge_dict['selected_edge'])
            
            if (edge_dict['name'] != ''):
                title = title +" -"+str(edge_dict['name'])
  
            self.fig.suptitle(title)
                        
            self.fig.subplots_adjust(bottom=0.1,left=0.1,right=0.9,top=0.90,hspace=0.3)   
        
            self.canvas.draw()
            
            self.show()
            
        else:
            
            print '[MSG] No edge selected'
            QtGui.QMessageBox.critical(self,"Error" ,"No edge selected")
            
        
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
    
        QtCore.QObject.connect(self.ui.actionPlay,QtCore.SIGNAL('triggered()'),self.playAnimation)
        QtCore.QObject.connect(self.ui.actionPause,QtCore.SIGNAL('triggered()'),self.pauseAnimation)
        QtCore.QObject.connect(self.ui.actionStop,QtCore.SIGNAL('triggered()'),self.stopAnimation)
        QtCore.QObject.connect(self.ui.actionFirst,QtCore.SIGNAL('triggered()'),self.firstAnimation)
        QtCore.QObject.connect(self.ui.actionLast,QtCore.SIGNAL('triggered()'),self.lastAnimation)
        QtCore.QObject.connect(self.ui.actionForward,QtCore.SIGNAL('triggered()'),self.forwardAnimation)
        QtCore.QObject.connect(self.ui.actionBack,QtCore.SIGNAL('triggered()'),self.backwardAnimation)
        QtCore.QObject.connect(self.ui.actionRepeat,QtCore.SIGNAL('triggered()'),self.repeatAnimation)

        QtCore.QObject.connect(self.ui.actionCapacity,QtCore.SIGNAL('triggered()'),self.displayNetworkDataCapacitiesLayer)
        QtCore.QObject.connect(self.ui.actionStart,QtCore.SIGNAL('triggered()'),self.displayNetworkVisualization)
        QtCore.QObject.connect(self.ui.actionTime,QtCore.SIGNAL('triggered()'),self.displayNetworkDataTimesLayer)
        
        QtCore.QObject.connect(self.ui.actionAnnotations,QtCore.SIGNAL('triggered()'),self.show_hide_annotations)
        QtCore.QObject.connect(self.ui.actionScalarBar,QtCore.SIGNAL('triggered()'),self.update_show_hide_colorbar)
        QtCore.QObject.connect(self.ui.actionStLabels,QtCore.SIGNAL('triggered()'),self.show_hide_st_labels)
        QtCore.QObject.connect(self.ui.actionLabels,QtCore.SIGNAL('triggered()'),self.show_hide_non_st_labels)
        
        QtCore.QObject.connect(self.ui.actionPlot,QtCore.SIGNAL('triggered()'),self.showPlotDialog)

        ### VTKWidget ###
        
        self.viz = viz

        self.vl = QtGui.QVBoxLayout()
        self.ui.vtkFrame.setLayout(self.vl)
        self.vtkWidget = QVTKRenderWindowInteractor(self.ui.vtkFrame)
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
        
    def updateVTKWidget(self, time_id):
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
        
        if (self.viz.TYPE in ['network']):
            
            time = self.timer*self.time_step
            self.dialog_plot.update(time)

    def displayNetworkDataTimesLayer(self, update_state=True):
        
        self.remove_extra_scene_props()
        
        if (update_state):
            self.viz.show_data_layer_time = not(self.viz.show_data_layer_time)
        
        if (self.viz.show_data_layer_time):
            
            self.viz.show_data_layer_capacity = False
            
            self.viz.nw_data_times.vtkActor.GetProperty().SetOpacity(0.75)
            if (self.viz.show_colorbar):
                opacity = 1
            else:
                opacity = 0
                
            self.viz.nw_data_times.vtkColorBarActor.GetProperty().SetOpacity(opacity)
            self.viz.nw_data_times.vtkColorBarActor.GetTitleTextProperty().SetOpacity(opacity)
            self.viz.nw_data_times.vtkColorBarActor.GetPositionCoordinate().SetValue(0.92,0.04)
        
        self.renderWindowInteractor.GetRenderWindow().Render()

    def displayNetworkDataCapacitiesLayer(self, update_state=True):
        
        self.remove_extra_scene_props()
        
        if (update_state):
            self.viz.show_data_layer_capacity = not(self.viz.show_data_layer_capacity)
        
        if (self.viz.show_data_layer_capacity):      
            
            self.viz.show_data_layer_time = False
              
            self.viz.nw_data_capacities.vtkActor.GetProperty().SetOpacity(0.75)
            if (self.viz.show_colorbar):
                opacity = 1
            else:
                opacity = 0
                
            self.viz.nw_data_capacities.vtkColorBarActor.GetProperty().SetOpacity(opacity)
            self.viz.nw_data_capacities.vtkColorBarActor.GetTitleTextProperty().SetOpacity(opacity)
            self.viz.nw_data_capacities.vtkColorBarActor.GetPositionCoordinate().SetValue(0.92,0.04)
        
        self.renderWindowInteractor.GetRenderWindow().Render()
        
    def displayNetworkVisualization(self):
        
        self.remove_extra_scene_props()
        
        self.viz.show_data_layer_capacity = False
        self.viz.show_data_layer_time = False
        
        if (self.viz.show_colorbar):
            opacity = 1
        else:
            opacity = 0
            
        self.viz.nw.vtkColorBarActor.GetProperty().SetOpacity(opacity)
        self.viz.nw.vtkColorBarActor.GetTitleTextProperty().SetOpacity(opacity)
        self.viz.nw.vtkColorBarActor.GetPositionCoordinate().SetValue(0.92,0.04)        
        
        self.renderWindowInteractor.GetRenderWindow().Render()
        
    def remove_extra_scene_props(self):
        
        self.viz.nw_data_times.vtkActor.GetProperty().SetOpacity(0)
        self.viz.nw_data_times.vtkColorBarActor.GetProperty().SetOpacity(0)
        self.viz.nw_data_times.vtkColorBarActor.GetTitleTextProperty().SetOpacity(0)
        self.viz.nw_data_times.vtkColorBarActor.GetPositionCoordinate().SetValue(0.0,0.0)
        
        self.viz.nw_data_capacities.vtkActor.GetProperty().SetOpacity(0)
        self.viz.nw_data_capacities.vtkColorBarActor.GetProperty().SetOpacity(0)
        self.viz.nw_data_capacities.vtkColorBarActor.GetTitleTextProperty().SetOpacity(0)
        self.viz.nw_data_capacities.vtkColorBarActor.GetPositionCoordinate().SetValue(0.0,0.0)        

        self.viz.nw.vtkColorBarActor.GetProperty().SetOpacity(0)
        self.viz.nw.vtkColorBarActor.GetTitleTextProperty().SetOpacity(0)
        self.viz.nw.vtkColorBarActor.GetPositionCoordinate().SetValue(0.0,0.0)        
        
    def show_hide_non_st_labels(self):
            
        self.viz.show_nodes_non_st_labels = not(self.viz.show_nodes_non_st_labels)
               
        if (self.viz.show_nodes_non_st_labels):
            opacity = 1
        else:
            opacity = 0

        self.viz.nw_nodes.vtkActor_non_st_labels.GetMapper().GetLabelTextProperty().SetOpacity(opacity)
        self.renderWindowInteractor.GetRenderWindow().Render()
        
    def show_hide_st_labels(self):
            
        self.viz.show_nodes_st_labels = not(self.viz.show_nodes_st_labels)
               
        if (self.viz.show_nodes_st_labels):
            opacity = 1
        else:
            opacity = 0

        self.viz.nw_nodes.vtkActor_st_labels.GetMapper().GetLabelTextProperty().SetOpacity(opacity)
        self.renderWindowInteractor.GetRenderWindow().Render()
        
    def show_hide_annotations(self):
        
        self.viz.show_annotations = not(self.viz.show_annotations)
        
        if (self.viz.show_annotations):
            opacity = 0
        else:
            opacity = 1
        
        self.viz.annotation_info_nw.GetTextProperty().SetOpacity(opacity)
        self.viz.annotation_info_iren.GetTextProperty().SetOpacity(opacity)
        
        self.renderWindowInteractor.GetRenderWindow().Render()
        
    def update_show_hide_colorbar(self):
        
        self.viz.show_colorbar = not(self.viz.show_colorbar)
        
        if (self.viz.show_data_layer_time):
            self.displayNetworkDataTimesLayer(update_state=False)

        elif (self.viz.show_data_layer_capacity):
            self.displayNetworkDataCapacitiesLayer(update_state=False)

        else:
            self.displayNetworkVisualization()

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
            
    
    
                