'''

 Inria Chile - Flows In Networks
 
 Dynamic flow visualization

 * Main visualization code

'''

import sys, os

import settings as pars
import manage as run
import lib.vfc as vis
import vtk

import networkx as nx
import random

from numpy import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from lib.pyQT_GUI import * 

import gen

## About this modules:
## fvc.py      : classes and functions for the visualization
## pyQT_GUI.py : GUI interface


''' Global parameters / variables
'''

ADD_DUMMY_NODE              = 0 #run.ADD_DUMMY_NODE # 0 or 1  (disabled option)
PRIORITY_GRAPHVIZ_LAYOUT    = run.PRIORITY_GRAPHVIZ_LAYOUT # 0 or 1
INTERACTOR_STYLE            = run.INTERACTOR_STYLE
SIM_DATA_AVAILABLE          = run.SIM_DATA_AVAILABLE
MAP_DATA_AVAILABLE          = run.MAP_DATA_AVAILABLE

class mainWindow(QtGui.QMainWindow):

    def __init__(self,parent=None):
        
        ''' GUI and VTK
        '''
                
        # parameters
        
        self.Tmax                       = pars.T_MAX
        self.time_step                  = max(pars.TIME_STEP,1E-10)
        self.globalNumberOfTimeSteps    = int(floor(self.Tmax/self.time_step))

        self.fps                        = max(pars.FPS,20)
        self.renderTimeInterval         = 1000/(1.0*self.fps)

        # variables
        
        self.time                       = 0.0
        self.timer_count                = 0
        self.animation                  = False

        # GUI
        
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setGuiInfo() # call the method with the visualization description
        self.setWindowTitle('FlowsInNetworks')
 
        ## GUI elements for animation
        
        self.edgesElements = []
       
        self.timerObj = QtCore.QTimer()
        QtCore.QObject.connect(self.timerObj,QtCore.SIGNAL("timeout()"),self.updateForAnimation)
        
        ### slider
        self.ui.slider_11.setRange(0,self.globalNumberOfTimeSteps)
        QtCore.QObject.connect(self.ui.slider_11,QtCore.SIGNAL('valueChanged(int)'),self.updateFromSlider)
        # * automatic visualization update under changes in the slider value !
        
        ### button
        self.ui.animationButton_11.setText('Play')
        QtCore.QObject.connect(self.ui.animationButton_11,QtCore.SIGNAL('clicked()'),self.executeAnimation)    
        
        ### vtk
        self.setVTKWidget() # call the method to set the VTKWidget components
        
        
    def setGuiInfo(self):
        
        ''' Visualization description
        '''
        
        msgTxt = '\n'
        
        msgTxt += '  VTK / QT \n\n'
        msgTxt += '  Visualization Test 26 \n\n'
        msgTxt += '  Jun 15, 2015 \n\n\n'
        msgTxt += '  Interactor Style:\n\n'
        
        if (INTERACTOR_STYLE == 'StyleImage'):
        
            msgTxt += '  [ StyleImage ]\n\n'
            msgTxt += '  Controls:\n\n'
            msgTxt += '  Right mouse - Zoom \n'
            msgTxt += '  Control + Left mouse - Rotation (2D) \n'
            msgTxt += '  Middle mouse - Pan \n'
            msgTxt += '  Scroll wheel - Zoom \n'
        
        else:

            msgTxt += '  [ RubberBand3D ]\n\n'
            msgTxt += '  Controls:\n\n'
            msgTxt += '  Right mouse - Rotate \n'
            msgTxt += '  Shift + Right mouse - Zoom \n'
            msgTxt += '  Middle mouse - Pan \n'
            msgTxt += '  Scroll wheel - Zoom \n'
        
        self.msgTxt = msgTxt
    
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
                
        # Call the methods with VTK sources, mappers and actors needed to create the scene
        
        ''' Important!  CHOOSING SIMULATION OR MAP DATA SCENE
            [ Work in progress ]
        '''
        
        if (MAP_DATA_AVAILABLE == True):
        
            self.setVTKMapElements()
        
        else:
            
            self.setNetworkData()
            self.setVTKElements()
            
            if (SIM_DATA_AVAILABLE == True):
                self.getSimulationData()
        
        
        
        
        # Show the scene and initialize the interactor
        self.camera = self.renderer.GetActiveCamera()
        
        if (MAP_DATA_AVAILABLE == True):
            coords = [-70.60630360192991, -33.41934159072677, 0.016528925619834704]
            x = coords[0]
            y = coords[1]
            z = coords[2]
            self.camera.SetPosition(x,y,z)
            self.camera.SetFocalPoint(x,y,0.0)
                
        else:    
            self.renderer.ResetCamera()
        
        self.show()
        
        if (INTERACTOR_STYLE == 'StyleImage'):
            self.renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleImage())
        else:
            self.renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleRubberBand3D())
        
        self.renderWindowInteractor.Initialize()

    
    def setVTKMapElements(self):
        
        # waterway
        for k in xrange(1,13):
            
            f = file('./data/maps/tobalaba_test/waterway/'+str(k)+'.dat','rb')
            data = load(f)
            f.close()
            
            if (data[0][0] == data[-1][0] and data[0][1] == data[-1][1]):
                element = vis.vtkLines(data,[0,0,0.5],4,0.0)
            else:
                element = vis.vtkLines(data,[0,0,0.5],1,0.0)
            self.renderer.AddActor(element.vtkActor)

        # landuse
        for k in xrange(1,36):
            
            f = file('./data/maps/tobalaba_test/landuse/'+str(k)+'.dat','rb')
            data = load(f)
            f.close()
            element = vis.vtkLines(data,[0.0,0.1,0.0],2,0.0)
            self.renderer.AddActor(element.vtkActor)

        # building
        for k in xrange(1,184):
            
            f = file('./data/maps/tobalaba_test/building/'+str(k)+'.dat','rb')
            data = load(f)
            f.close()
            element = vis.vtkLines(data,[0.15,0.15,0.15],0.1,0.0)
            self.renderer.AddActor(element.vtkActor)

        # railway
        
        f = file('./data/maps/tobalaba_test/railway/'+str(2)+'.dat','rb')
        data = load(f)
        f.close()
        element = vis.vtkLines(data,[0,0,0.15],9,0.0)
        self.renderer.AddActor(element.vtkActor)        
        
        f = file('./data/maps/tobalaba_test/railway/'+str(1)+'.dat','rb')
        data = load(f)
        f.close()
        element = vis.vtkLines(data,[0.15,0,0],9,0.0)
        self.renderer.AddActor(element.vtkActor)
        
        # highway
        for k in xrange(1,174):
            
            f = file('./data/maps/tobalaba_test/highway/'+str(k)+'.dat','rb')
            data = load(f)
            f.close()
            element = vis.vtkLines(data,[0.15,0.15,0.15],2,0.0)
            self.renderer.AddActor(element.vtkActor)
        
        for k in xrange(1,60):
            
            f = file('./data/maps/tobalaba_test/highway_primary/'+str(k)+'.dat','rb')
            data = load(f)
            f.close()
            color = 0.25
            #element = vis.vtkTubes(data,[color,color,color],0.5/100000.0,0.00015)
            element = vis.vtkLines(data,[color,color,color],2.5,0.0)
            #self.renderer.AddActor(element.vtkActor)
            
            color = 0.175
            for i in xrange(len(data)-1):
                p = [data[i,0],data[i,1]]
                q = [data[i+1,0],data[i+1,1]]
                element = vis.vtkRibbonLine(p,q,[color,color,color],0.000018,0.0)
                self.renderer.AddActor(element.vtkActor)


        # coords
        
        label = 'Inria Chile'
        coords = [-70.600237,-33.418167]
        vtkLabel = vis.label2D(coords[0],coords[1],0.0,label,'l','b')
        self.renderer.AddActor(vtkLabel.actor)
        self.renderer.AddActor2D(vtkLabel.actor2D)
        
        label = 'Tobalaba (M)'
        coords = [-70.6014905,-33.4181976]
        vtkLabel = vis.label2D(coords[0],coords[1],0.0,label,'r','b')
        self.renderer.AddActor(vtkLabel.actor)
        self.renderer.AddActor2D(vtkLabel.actor2D)

        label = 'Los Leones (M)'
        coords = [-70.608600,-33.422146]
        vtkLabel = vis.label2D(coords[0],coords[1],0.0,label,'r','b')
        self.renderer.AddActor(vtkLabel.actor)
        self.renderer.AddActor2D(vtkLabel.actor2D)


        # TEXT ELEMENTS

        annotation1 = vtk.vtkCornerAnnotation() 
        annotation1.SetText(2,self.msgTxt)
        annotation1.SetMaximumFontSize(14)
        annotation1.GetTextProperty().SetColor(0.75,0.75,0.75)
        self.renderer.AddViewProp(annotation1)
        
        data_msg = ''
        if (SIM_DATA_AVAILABLE == False):
            data_msg = '\n  * Comment: No simulation data \n'
        
        msg = ['  NETWORK \n\n','  '+str(run.ns)+'\n\n'+data_msg]     
        annotation2 = vtk.vtkCornerAnnotation() 
        annotation2.SetText(0,''.join(msg))
        annotation2.SetMaximumFontSize(14)
        self.renderer.AddViewProp(annotation2)


    
    def setNetworkData(self):
        
        ''' Network data
        '''
        
        path = os.path.abspath(os.path.join('temp'))
        
        # Graph
        
        self.nxGraph = nx.MultiDiGraph()
        
        if (SIM_DATA_AVAILABLE):
            SG = nx.read_gml(os.path.join(path,'temp.gml')) # source_graph
        else:
            SG = run.G
        
        ###############################
        #
        # Setting multigraph structure 
        #
        
        aux_s = None
        
        c = 0
        for n in SG.nodes_iter():
        
            self.nxGraph.add_node(n)
            self.nxGraph.node[n]['id'] = c
            
            if (SIM_DATA_AVAILABLE):

                self.nxGraph.node[n]['nlabel']  = SG.node[n]['nlabel']
                if (self.nxGraph.node[n]['nlabel']=='s'):
                    aux_s = c

            else:

                self.nxGraph.node[n]['nlabel']  = str(n)
                if (self.nxGraph.node[n]['nlabel']=='s'):
                    aux_s = n
            
            c = c + 1
            
        for u,v,data in SG.edges_iter(data=True):
            
            if (SIM_DATA_AVAILABLE):
                edge_key        = data['edge_key']
                edge_skey       = data['edge_skey']
            else:
                edge_key        = 0
                edge_skey       = 0
            
            time        = data['time']
            capacity    = data['capacity']
            
            self.nxGraph.add_edge(u,v, edge_key = edge_key, edge_skey = edge_skey, time = time, capacity = capacity)        
                
        if (ADD_DUMMY_NODE):
            self.nxGraph.add_node('d') # dummy
            self.nxGraph.node['d']['id'] = SG.number_of_nodes() 
            self.nxGraph.node['d']['nlabel'] = 'd'
            self.nxGraph.add_edge('d',aux_s,edge_key = SG.number_of_edges(),  edge_skey = 0, time = 1.0, capacity=10000., flow=0)
         
        #print self.nxGraph.nodes(data=True)
        #print self.nxGraph.edges(data=True)
        #
        #
        ###############################

        # Set position for each node
        
        package = 'pygraphviz'
        gviz = False
        
        try:
            __import__(package)
            gviz = True
        except ImportError:
            gviz = False
        
        if (gviz == True and PRIORITY_GRAPHVIZ_LAYOUT == 1) :
            pos = nx.graphviz_layout(self.nxGraph, prog='dot')
            self.nodeRadius = 6.0
        else: 
            pos = nx.spring_layout(self.nxGraph)
            self.nodeRadius = 12.0
        
        max_x = 0.0
        max_y = 0.0
        
        for key in pos:
            max_x = max(max_x,pos[key][0])
            max_y = max(max_y,pos[key][1])
                
        if (max_x > 0 and max_y > 0):
            
            max_yVis = 100.0
            max_xVis = max_yVis*(max_x/max_y)

        else:
            
            max_xVis = max_x
            max_yVis = max_y
        
        c           = 0
        radsAngle   = 90*(pi/180.0)
        
        for n in self.nxGraph.nodes_iter():
            
            self.nxGraph.add_node(n,id=int(c))
            cx = float(pos[n][0])*(max_xVis/max_x)
            cy = float(pos[n][1])*(max_yVis/max_y)
            
            point = vis.getPointFrom2DRotation(cx,cy,radsAngle)
            
            self.nxGraph.add_node(n,pos= [point[0],point[1],0.0])
            if ( n != 'd'):
                self.nxGraph.add_node(n,type='r')
            else:
                self.nxGraph.add_node(n,type='d')
            c = c + 1
  
        
    def setVTKElements(self):

        ##
        # Graph and visualization elements
        #
        
        ''' Graph
        '''
        
        #nodes         
        self.renderer.AddActor(vis.vtkNodesElementGlyph(self.nxGraph,self.nodeRadius).vtkActor)     
        self.renderer.AddActor2D(vis.vtkNodesElementGlyph(self.nxGraph,self.nodeRadius).vtkActor2D) #labels for each node

        #edges
        
        for e in sorted(set(self.nxGraph.edges_iter())):
 
            edges = self.nxGraph.edge[e[0]][e[1]]

            if (len(edges) == 1):
         
                    # Pair of nodes connected by one arc
 
                    p0 = self.nxGraph.node[e[0]]['pos']
                    p1 = self.nxGraph.node[e[1]]['pos']
                    
                    numberOfTimeDivisions = int(floor(edges[0]['time']/self.time_step))
                    
                    # DYNAMIC
                    el = vis.vtkFlowRibbonLine(p0,p1,numberOfTimeDivisions)
                    el.vtkFilter.SetWidth(0.3)
                    self.renderer.AddActor(el.vtkActor)

                    rPos        = 0.5*(array(p0)+array(p1))
                    qHeight     = 6
                    qDistance   = 3.25
                    qWidth      = 1.25
                    
                    queue   = vis.vtkQueueRibbonUsingRefPosition(p0,p1,rPos,qHeight,qDistance,qWidth)
                    qbox    = vis.vtkQueueBoxUsingRefPosition(p0,p1,rPos,qHeight,qDistance,qWidth)
                    
                    if (self.nxGraph.node[e[0]]['type'] == 'd'):
                        queue.vtkActor.GetProperty().SetOpacity(0)
                        qbox.vtkActor.GetProperty().SetOpacity(0)
                    
                    self.renderer.AddActor(queue.vtkActor)
                    self.renderer.AddActor(qbox.vtkActor)    
 
                    nodeStart                   = self.nxGraph.node[e[0]]['nlabel']
                    nodeEnd                     = self.nxGraph.node[e[1]]['nlabel']
                    edgeID                      = edges[0]['edge_key']#['id']
                    edgeKey                     = edges[0]['edge_skey']#['key']
                    globalNumberOfTimeDivisions = self.globalNumberOfTimeSteps
                    numberOfTimeStepsForEdge    = numberOfTimeDivisions
                    time_step                   = self.time_step
                    vtkQueue                    = queue
                    vtkElement                  = el
                    
                    edgeElement = vis.EdgeElement(nodeStart,nodeEnd,edgeID,edgeKey,numberOfTimeStepsForEdge,globalNumberOfTimeDivisions,time_step,vtkQueue,vtkElement,qbox)
                    
                    self.edgesElements.append(edgeElement)
 
                    '''
                    # STATIC
                    el = vis.vtkEdgeRibbonLine(p0,p1)
                    self.renderer.AddActor(el.vtkActor)
                    #
                    '''

            else:
                
                # Pair of nodes connected by several arcs
                
                c = 0
                mult = 0
                
                while (c < len(edges)):
                    
                    if (c%2 == 0 and c > 0):
                        mult = mult + 30
 
                    p0 = self.nxGraph.node[e[0]]['pos']
                    p1 = self.nxGraph.node[e[1]]['pos']
                    
                    numberOfTimeDivisions = int(floor(edges[c]['time']/self.time_step))
                                       
                    # DYNAMIC
                    
                    plusFactor = (-1)**(c+1)
                    
                    el = vis.vtkFlowRibbonArc(p0,p1,numberOfTimeDivisions,30+ mult,plusFactor)
                    el.vtkFilter.SetWidth(0.3)
                    self.renderer.AddActor(el.vtkActor)                        

                    nArcPoints = el.vtkPoints.GetNumberOfPoints()
                    
                    if (nArcPoints % 2 == 1):
                        
                        p0      = el.vtkPoints.GetPoint(int(0.5*(nArcPoints-1)))
                        rPos    = array(p0)
                    
                    else:
                        
                        p0      = el.vtkPoints.GetPoint(int(0.5*nArcPoints - 1))
                        p1      = el.vtkPoints.GetPoint(int(0.5*nArcPoints))
                        rPos    = 0.5*(array(p0)+array(p1))                        
                    
                    qHeight     = 6
                    qDistance   = 1.75*(-1*plusFactor)
                    qWidth      = 1.25
                    
                    queue   = vis.vtkQueueRibbonUsingRefPosition(p0,p1,rPos,qHeight,qDistance,qWidth)
                    qbox    = vis.vtkQueueBoxUsingRefPosition(p0,p1,rPos,qHeight,qDistance,qWidth)
                    
                    if (self.nxGraph.node[e[0]]['type'] == 'd'):
                        queue.vtkActor.GetProperty().SetOpacity(0)
                        qbox.vtkActor.GetProperty().SetOpacity(0)
                        
#                         if (plusFactor > 0):
#                             queue.vtkActor.GetProperty().SetColor(0,0,1)
#                             el.vtkActor.GetProperty().SetOpacity(0)
                    
                    self.renderer.AddActor(queue.vtkActor)
                    self.renderer.AddActor(qbox.vtkActor)    
                    
                    nodeStart                   = self.nxGraph.node[e[0]]['nlabel']
                    nodeEnd                     = self.nxGraph.node[e[1]]['nlabel']
                    edgeID                      = edges[c]['edge_key']#['id']
                    edgeKey                     = edges[c]['edge_skey']#['key']
                    globalNumberOfTimeDivisions = self.globalNumberOfTimeSteps
                    numberOfTimeStepsForEdge    = numberOfTimeDivisions
                    time_step                   = self.time_step
                    vtkQueue                    = queue
                    vtkElement                  = el
                    
                    edgeElement = vis.EdgeElement(nodeStart,nodeEnd,edgeID,edgeKey,numberOfTimeStepsForEdge,globalNumberOfTimeDivisions,time_step,vtkQueue,vtkElement,qbox)
                    
                    self.edgesElements.append(edgeElement)
                    
                    '''
                    # STATIC  
                    el = vis.vtkEdgeRibbonArc(p0,p1,30 + mult,(-1)**(c+1))
                    self.renderer.AddActor(el.vtkActor)
                    #
                    '''
                    
                    c = c + 1
    
        ''' Visualization elements
        '''

        #Text elements
              
        annotation1 = vtk.vtkCornerAnnotation() 
        annotation1.SetText(2,self.msgTxt)
        annotation1.SetMaximumFontSize(14)
        annotation1.GetTextProperty().SetColor(0.75,0.75,0.75)
        self.renderer.AddViewProp(annotation1)
        
        if (ADD_DUMMY_NODE == 1):
            numberOfNodes = self.nxGraph.number_of_nodes() - 1
            numberOfEdges = self.nxGraph.number_of_edges() - 1
        else:
            numberOfNodes = self.nxGraph.number_of_nodes()
            numberOfEdges = self.nxGraph.number_of_edges()
        
        data_msg = ''
        if (SIM_DATA_AVAILABLE == False):
            data_msg = '\n  * Comment: No simulation data \n'
        
        msg = ['  NETWORK \n\n','  '+str(run.ns)+'\n\n','  '+str(numberOfNodes),' nodes\n','  '+str(numberOfEdges),' edges\n\n','  time step: ',str(self.time_step)+'\n'+data_msg]     
        annotation2 = vtk.vtkCornerAnnotation() 
        annotation2.SetText(0,''.join(msg))
        annotation2.SetMaximumFontSize(14)
        self.renderer.AddViewProp(annotation2)
    
    def getSimulationData(self):
        
        
        fm = file('./data/'+run.ns+'_f_e_minus.dat','rb')
        q = file('./data/'+run.ns+'_z_e.dat','rb')
        
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
 
#             else:
#            [ Work in progress... ]
#                 # dummy
#                  
#                 for k in xrange(self.edgesElements[j].globalNumberOfTimeDivisions+1):
#                     for i in xrange(self.edgesElements[j].numberOfTimeStepsForEdge+1):
#  
#                         self.edgesElements[j].FlowData[k][i] = flows.u0(k*self.time_step)                

            
    def updateVisualization(self,id_t):

        ''' Scene update method
        '''

    # Changes in the scene only if simulation data is available

        if (MAP_DATA_AVAILABLE == True):
            
            print self.camera.GetPosition()
        
        if (SIM_DATA_AVAILABLE == True):
         
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
                        qValue = max(mqValue, 0.00001)
                           
                        if (mqValue != -1):
                            self.edgesElements[j].vtkQBox.vtkActor.GetProperty().SetColor(0.5,0.5,0.5)
                            self.edgesElements[j].vtkQueue.vtkActor.GetProperty().SetColor(0,1.0,0)
                            self.edgesElements[j].vtkQueue.setEndPointFromValue(2*max(qValue,0.00001))
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
    
    if (run.flag == 0):
        
        print 'Loading GUI...'
        
        print 'Running data file generator...'
        
        SIM_DATA_AVAILABLE = gen.data_generator()
        
        app = QtGui.QApplication(sys.argv)
        ex = mainWindow()
        ex.show()
        sys.exit(app.exec_())
        
    else:
        if (run.flag == 1):
            print '[ MSG ] Error in main.py file. Graph not found.'
        if (run.flag == 2):
            print '[ MSG ] Python module / package not found '
        
    
    
    
    