
# Inria / FlowsInNetworks 

#/////////////////////////////
#
# Description:
#
# Visualization test - N.1
#
# Notes:
#
#/////////////////////////////

# M. Olivares - 05/2015


import sys 
import random
from numpy import *

import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from pyQT_GUI import * # GUI interface from Qt Designer

import flows  # flows.py : functions u0, fe+, fe-, Fe+, Fe-, ze
import vm    # vm.py : methods for visualization 

#from vtk.vtkGraphicsPython import vtkTubeFilter, vtkSplineFilter
#from vtk.vtkCommonPython import vtkFloatArray

class mainWindow(QtGui.QMainWindow):

    def __init__(self,parent=None):
    
        # GUI and Vtk
        
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setGuiInfo()
        
        # variables
        
        self.timer_count    = 0
        self.Tmax           = 7.0
        self.numberOfTimeSteps = 250
        self.time_step      = self.Tmax/(1.0*self.numberOfTimeSteps)
        self.animation      = False
        
        self.fps = 20
        self.msec = 1000/(1.0*self.fps)
        self.timerObj = QtCore.QTimer()
        
        QtCore.QObject.connect(self.timerObj,QtCore.SIGNAL("timeout()"),self.updateForAnimation)
        
        self.setVTKWidget()
        
    def setGuiInfo(self):

        self.setWindowTitle('FlowsInNetworks')
        
        msgTxt = ''
        
        msgTxt = 'VTK / QT \n\n'
        msgTxt += 'Visualization Test 1 \n\n'
        msgTxt += 'May 4, 2015 \n\n\n'
        msgTxt += 'Controls:\n\n'
        msgTxt += 'Left mouse - Select \n'
        msgTxt += 'Right mouse - Zoom \n'
        msgTxt += 'Middle mouse - Pan \n'
        msgTxt += 'Scroll wheel - Zoom \n'
        
        self.ui.msgPanel.setText(msgTxt)
        self.ui.msgPanel.setReadOnly(True)

        self.ui.slider.setRange(0,250)
        
        self.ui.animationButton.setText('Play')
        
        QtCore.QObject.connect(self.ui.slider,QtCore.SIGNAL('valueChanged(int)'),self.updateFromSlider)
        
        QtCore.QObject.connect(self.ui.animationButton,QtCore.SIGNAL('clicked()'),self.executeAnimation)        
        
    def setVTKWidget(self):
        
        self.vl = QtGui.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.ui.vtkFrame)
        self.vl.addWidget(self.vtkWidget)
        
        self.graphLayout = vtk.vtkGraphLayout()
        self.graphLayoutView = vtk.vtkGraphLayoutView()
        self.renderer = self.graphLayoutView.GetRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)
        self.renderWindowInteractor = self.vtkWidget.GetRenderWindow().GetInteractor()
        
        self.graphLayoutView.SetRenderWindow(self.vtkWidget.GetRenderWindow())
        
        self.setVTKElements() # VTK sources, mappers and actors
        
        self.ui.vtkFrame.setLayout(self.vl)
        
        self.graphLayoutView.ResetCamera()
        self.show()
        
        self.renderWindowInteractor.Initialize()
                
    def setVTKElements(self):
        
        #map data
        mapPoints = []    
        mapPoints.append([489,46])
        mapPoints.append([628,93])
        mapPoints.append([706,123])
        mapPoints.append([788,162])
        mapPoints.append([512,150])
        mapPoints.append([620,178])
        mapPoints.append([684,197])
        mapPoints.append([542,263])
        mapPoints.append([613,277.13])
        mapPoints.append([660,286.48])
        mapPoints.append([748,304])
    
        # Graph
        graph       = vtk.vtkMutableDirectedGraph()
        points      = vtk.vtkPoints()
        vertexIDs   = vtk.vtkIntArray()
        vertexIDs.SetNumberOfComponents(len(mapPoints))
        vertexIDs.SetName("VertexIDs")
        for i in range(len(mapPoints)):
            points.InsertPoint(i,mapPoints[i][0],-mapPoints[i][1],0)
            graph.AddVertex()
            vertexIDs.InsertNextValue(i)
        graph.SetPoints(points)
        graph.GetVertexData().AddArray(vertexIDs)
    
        graph.AddGraphEdge(4,0)
        graph.AddGraphEdge(0,1)
        graph.AddGraphEdge(2,1)
        graph.AddGraphEdge(3,2)
        graph.AddGraphEdge(3,10)
        graph.AddGraphEdge(4,5)
        graph.AddGraphEdge(4,7)
        graph.AddGraphEdge(5,6)
        graph.AddGraphEdge(5,1)
        graph.AddGraphEdge(6,2)
        graph.AddGraphEdge(7,8)
        graph.AddGraphEdge(8,5)
        graph.AddGraphEdge(8,9)
        graph.AddGraphEdge(9,6)
        graph.AddGraphEdge(9,10)

        if (vtk.VTK_MAJOR_VERSION <= 5):
            self.graphLayout.SetInput(graph)
        else:
            self.graphLayout.SetInputData(graph)
    
        self.graphLayout.SetLayoutStrategy(vtk.vtkPassThroughLayoutStrategy())

        self.graphLayoutView.SetLayoutStrategyToPassThrough()
        self.graphLayoutView.AddRepresentationFromInputConnection(self.graphLayout.GetOutputPort())
    
        self.graphLayoutView.SetVertexLabelArrayName("VertexIDs")
        self.graphLayoutView.SetVertexLabelVisibility(True)

        # Arrows | source / glyph / mapper / actor
    
        graphToPoly = vtk.vtkGraphToPolyData()
        graphToPoly.SetInputConnection(self.graphLayout.GetOutputPort())
        graphToPoly.EdgeGlyphOutputOn()
        graphToPoly.SetEdgeGlyphPosition(0.5)
    
        arrowSource = vtk.vtkGlyphSource2D()
        arrowSource.SetGlyphTypeToEdgeArrow()
        arrowSource.SetScale(0.75)
        arrowSource.Update()
    
        arrowGlyph = vtk.vtkGlyph3D()
        arrowGlyph.SetInputConnection(0,graphToPoly.GetOutputPort(1))
        arrowGlyph.SetInputConnection(1,arrowSource.GetOutputPort())
    
        arrowMapper = vtk.vtkPolyDataMapper()
        arrowMapper.SetInputConnection(arrowGlyph.GetOutputPort())
    
        arrowActor = vtk.vtkActor()
        arrowActor.SetMapper(arrowMapper)
        arrowActor.GetProperty().SetColor(0.98,0.98,0.98)
        
        self.graphLayoutView.GetRenderer().AddActor(arrowActor)

        #-----------------------------------------------
        # Theme for graphLayoutView
        #-----------------------------------------------
        theme = vtk.vtkViewTheme.CreateMellowTheme()
        theme.SetLineWidth(3)
        theme.SetPointSize(3)
        # Vertices
        theme.SetSelectedPointColor(0, 0.5, 1)
        theme.SetPointColor(0,0,0)
        # Edges
        theme.SetSelectedCellColor(1.0, 0.95, 0.75)
        theme.SetCellColor(0,0,0)
        self.graphLayoutView.ApplyViewTheme(theme)
        theme.FastDelete()
        #-----------------------------------------------
        
        # Visualization Elements
        
        # inflow
        
        p1 = points.GetPoint(0)
        p2 = vm.alphaPoint(points.GetPoint(0),points.GetPoint(1),0.5)
        
        inflow = vm.Tube(p1,p2)
        inflow.setOpacity(1)
        
        self.graphLayoutView.GetRenderer().AddActor(inflow.vtkActor)

        self.inflow = inflow
     
        # outflow
        
        p1 = vm.alphaPoint(points.GetPoint(0),points.GetPoint(1),0.5)
        p2 = points.GetPoint(1)
        
        outflow = vm.Tube(p1,p2)
        outflow.setOpacity(1)
        
        self.graphLayoutView.GetRenderer().AddActor(outflow.vtkActor)

        self.outflow = outflow
        
        # queue
        
        aux = vm.alphaPoint(points.GetPoint(0),points.GetPoint(1),0.5)
        
        p1 = [aux[0],aux[1],0]
        p2 =  [aux[0],aux[1],40.0]
        
        queue = vm.Tube(p1,p2)
        
        self.graphLayoutView.GetRenderer().AddActor(queue.vtkActor)

        self.queue = queue
                       
    def updateVisualization(self,id_t):
        
        vFactor = 2
        
        self.inflow.setRadius(vFactor*flows.fePlus(id_t*self.time_step))
        self.outflow.setRadius(vFactor*flows.feMinus(id_t*self.time_step))
        self.queue.setRadius(8*vFactor*flows.ze(id_t*self.time_step))
        
        self.renderWindowInteractor.GetRenderWindow().Render()
    
    def playAnimation(self):
        self.timerObj.start(self.msec)
    
    def stopAnimation(self):
        self.timerObj.stop()
    
    def updateSlider(self,id_t):
        self.ui.slider.setSliderPosition(id_t)
        aux = int(id_t*self.time_step*10.0)/10.0
        self.ui.textSliderValue.setText(str(aux))        
    
    def updateFromSlider(self):

        id_t = self.ui.slider.value()
        self.timer_count = id_t
        self.updateSlider(id_t)
        self.updateVisualization(id_t)
    
    def updateForAnimation(self):
        
        if (self.animation == True):
        
            id_t = self.timer_count
            self.updateSlider(id_t)
            
            # automatic update :: "slider valueChanged(int)---> self.updateFromSlider" 
            
            self.timer_count += 1    
            if (self.timer_count > self.numberOfTimeSteps):
                self.timer_count = 0
    
    def executeAnimation(self):
        
        self.animation = not self.animation
        
        if (self.animation == True):
        
            self.ui.animationButton.setText('Stop')
            self.playAnimation()
            
        else:
            
            self.ui.animationButton.setText('Play')
            self.stopAnimation()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ex = mainWindow()
    ex.show()
    sys.exit(app.exec_())        
    
    
        
