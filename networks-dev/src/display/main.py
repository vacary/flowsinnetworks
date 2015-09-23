#
# Visualization GUI

# Standard library imports
import os
import sys
import json

# Non standard library imports
import networkx as nx

import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import vtk
vtk.vtkOutputWindow().GlobalWarningDisplayOff()
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor # VTK Widget
from src.display.GUI.lib.MainWindow import * # Qt Gui Elements
import src.display.GUI.lib.Dialog as Qt_Dialog

from numpy import *

# Custom action modules for GUI
import src.display.GUI.actions.actors as actions_actors
import src.display.GUI.actions.animation as actions_animation
import src.display.GUI.actions.plot as actions_plot

# Visualization Class
from src.display.vis.visualization import *

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
        self.toolbar = NavigationToolbar(self.canvas, self, coordinates=True)
        self.layout.addWidget(self.toolbar)

    def update(self,time):
        
        self.fig.clf()
        edge_dict = {}
        try:                
            f = open(os.path.join('.','temp','data.txt'),"r")
            json_edge_dict = f.readline()
            edge_dict = json.loads(json_edge_dict)
            f.close()
        except:
            print (sys.exc_info())
            pass
        
        if (bool(edge_dict)):
            title = actions_plot.edge_data_plot_update(self.fig, time, edge_dict)
            self.fig.suptitle(title)
            self.fig.subplots_adjust(bottom=0.1, left=0.1, right=0.9, top=0.90, hspace=0.3)
            self.canvas.draw()
            self.show()
        else:
            print '[MSG] No edge selected'
            QtGui.QMessageBox.critical(self,"Error" ,"No edge selected")
        #gc.collect()

class MainWindow(QtGui.QMainWindow):
 
    def __init__(self,viz,parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dialog_plot = PlotDialog() # dialog for edge simulation data plot
        self.QTimer = QtCore.QTimer() # QT timer for animation
        self.viz = viz # current visualization object
        self.slider_label = self.ui.textSliderValue_11
        self.slider = self.ui.slider_11
        self.slider.setRange(0,self.viz.globalNumberOfTimeSteps)
        self.setVTKWidget()
        self.setWindowTitle('FlowsInNetworks')
        self.setGUIConnections()
        
    def setGUIConnections(self):
        
        # Timer and animation update method 
        QtCore.QObject.connect(self.QTimer,QtCore.SIGNAL("timeout()"),self.updateForAnimation)
        
        # Slider and animation update method
        QtCore.QObject.connect(self.ui.slider_11,QtCore.SIGNAL('valueChanged(int)'),self.updateFromSlider)
        
        # GUI bar actions
        
        # * Animation
        QtCore.QObject.connect(self.ui.actionPlay,QtCore.SIGNAL('triggered()'),self.playAnimation)
        QtCore.QObject.connect(self.ui.actionPause,QtCore.SIGNAL('triggered()'),self.pauseAnimation)
        QtCore.QObject.connect(self.ui.actionStop,QtCore.SIGNAL('triggered()'),self.stopAnimation)
        QtCore.QObject.connect(self.ui.actionFirst,QtCore.SIGNAL('triggered()'),self.firstAnimation)
        QtCore.QObject.connect(self.ui.actionLast,QtCore.SIGNAL('triggered()'),self.lastAnimation)
        QtCore.QObject.connect(self.ui.actionForward,QtCore.SIGNAL('triggered()'),self.forwardAnimation)
        QtCore.QObject.connect(self.ui.actionBack,QtCore.SIGNAL('triggered()'),self.backwardAnimation)
        QtCore.QObject.connect(self.ui.actionRepeat,QtCore.SIGNAL('triggered()'),self.repeatAnimation)
        QtCore.QObject.connect(self.ui.actionStart,QtCore.SIGNAL('triggered()'),self.displayNetworkVisualization)
        
        # * Elements
        QtCore.QObject.connect(self.ui.actionCapacity,QtCore.SIGNAL('triggered()'),self.displayNetworkDataCapacitiesLayer)
        QtCore.QObject.connect(self.ui.actionTime,QtCore.SIGNAL('triggered()'),self.displayNetworkDataTimesLayer)
        QtCore.QObject.connect(self.ui.actionAnnotations,QtCore.SIGNAL('triggered()'),self.show_hide_annotations)
        QtCore.QObject.connect(self.ui.actionScalarBar,QtCore.SIGNAL('triggered()'),self.update_show_hide_colorbar)
        QtCore.QObject.connect(self.ui.actionStLabels,QtCore.SIGNAL('triggered()'),self.show_hide_st_labels)
        QtCore.QObject.connect(self.ui.actionLabels,QtCore.SIGNAL('triggered()'),self.show_hide_non_st_labels)        
        QtCore.QObject.connect(self.ui.actionPlot,QtCore.SIGNAL('triggered()'),self.showPlotDialog)
        
    def setVTKWidget(self):
        
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
        
    def updateForAnimation(self):
        actions_animation.update_for_animation(self, self.viz, self.slider, self.slider_label)
                    
    def updateVTKWidget(self, time_id):
        actions_animation.update_VTKWidget(self.vis, time_id)

    def updateFromSlider(self):        
        actions_animation.update_from_slider(self, self.viz, self.slider, self.slider_label)

    def updateSlider(self,timer):
        actions_animation.update_slider(self.slider, self.slider_label, self.viz)

    def playAnimation(self):
        actions_animation.play(self, self.viz)
    
    def repeatAnimation(self):
        actions_animation.repeat(self, self.viz)
    
    def pauseAnimation(self):
        actions_animation.pause(self, self.viz)
    
    def stopAnimation(self):
        actions_animation.stop(self, self.viz, self.slider, self.slider_label)
    
    def firstAnimation(self):
        actions_animation.first_frame(self, self.viz, self.slider, self.slider_label)
    
    def lastAnimation(self):
        actions_animation.last_frame(self, self.viz, self.slider, self.slider_label)
             
    def forwardAnimation(self):
        actions_animation.next_frame(self, self.viz, self.slider, self.slider_label)
        
    def backwardAnimation(self):
        actions_animation.preceding_frame(self, self.viz, self.slider, self.slider_label)
        
    def showPlotDialog(self):
        # Call to PlotDialog
        actions_plot.call_to_plot_dialog(self, self.viz)
        
    def displayNetworkDataTimesLayer(self):
        actions_actors.display_data_times_layer(self.viz)

    def displayNetworkDataCapacitiesLayer(self):
        actions_actors.display_data_capacities_layer(self.viz)
        
    def displayNetworkVisualization(self):
        actions_actors.display_animation_layer(self.viz)
              
    def show_hide_non_st_labels(self):
        actions_actors.display_nodes_non_st_labels(self.viz)
        
    def show_hide_st_labels(self):
        actions_actors.display_nodes_st_labels(self.viz)
  
    def show_hide_annotations(self):
        actions_actors.display_annotations(self.viz)
        
    def update_show_hide_colorbar(self):
        actions_actors.display_colorbar(self.viz)

    def closeEvent(self,event):
        # Clean temp file with the interactor annotation info
        f = open(os.path.join('.','temp','data.txt'),"w")
        f.write(json.dumps({}))
        f.close()
        self.dialog_plot.close()
        event.accept()
        
if __name__ == "__main__":

    """Run the visualization GUI after get the visualization project data."""

    visualization_settings_dir_path = os.path.join('.','projects',NETWORK_NAME)
    pars = vis_mn.get_vparameters(visualization_settings_dir_path) # visualization settings

    # Run application

    app = QtGui.QApplication(sys.argv)
    viz = Visualization(pars)
    ex  = MainWindow(viz)

    ex.show()
    sys.exit(app.exec_())
