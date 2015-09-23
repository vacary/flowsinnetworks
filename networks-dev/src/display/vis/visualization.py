#
# Visualization Class
#

# Standard library imports
import os
import sys

# Non standard library imports
import networkx as nx
from numpy import *
import vtk

import manage as vis_mn
import styles.network as vstyle_nw
import interactors.base as interactor

class Visualization:
 
    def __init__(self, pars):
        
        self.timer = 0
        self.animation = False
        self.repeat = False
        
        self.pars = pars
        self.TYPE = self.pars['TYPE']
        self.fps = self.pars['FPS']
        self.network_name = self.pars['NETWORK_NAME']
        self.time_step = self.pars['TIME_STEP']
        self.Tmax = self.pars['T_MAX_VIS']
        self.SIMULATION_DATA_AVAILABLE = self.pars['SIMULATION_DATA_AVAILABLE']
        self.PRIORITY_GRAPHVIZ_LAYOUT = self.pars['PRIORITY_GRAPHVIZ_LAYOUT']
        
        self.renderTimeInterval = 1000/(1.0*self.fps)
        self.globalNumberOfTimeSteps = int(floor(self.Tmax/self.time_step))
        
        self.G = None
        
        self.renderer = vtk.vtkRenderer()
        self.interactor = None
        self.interactorAnnotation = vtk.vtkTextActor()

        self.style_pars = {}
        self.time_id = 0
        
        self.nw = None
        self.nw_data_times = None
        self.nw_data_capacities = None
        
        self.nw_nodes = None
        
        self.annotation_info_nw = None
        self.annotation_info_iren = None

        self.arrayOf_f_e_minus = None
        self.arrayOf_Queues = None

        self.show_colorbar = True
        self.show_nodes_st_labels = True
        self.show_nodes_non_st_labels = False
        self.show_up_left_annotations = True
        self.show_down_left_annotations = True
        self.show_animation_layer = True
        self.show_data_layer_time = False
        self.show_data_layer_capacity = False
        
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
            
    def setInteractor(self,renderWindowInteractor):
        
        self.interactor = renderWindowInteractor 

    def setInteractorStyle(self,renderWindowInteractor):
        
        if (self.TYPE in ['network']):
        
            renderWindowInteractor.SetInteractorStyle(interactor.CustomInteractorStyle())

    def setInteractorAnnotation(self):
        
        self.interactorAnnotation.GetTextProperty().SetFontSize(14)
        self.interactorAnnotation.GetTextProperty().SetBold(1)
        self.interactorAnnotation.GetTextProperty().SetItalic(0)
        self.interactorAnnotation.GetTextProperty().SetShadow(0)
        self.interactorAnnotation.SetInput('Selected edge : ')
        self.interactorAnnotation.SetPosition(0,0)
        self.interactorAnnotation.GetProperty().SetOpacity(0)
        
        self.renderer.AddActor(self.interactorAnnotation)
                
    def update(self,time_id):

        if (self.TYPE in ['network']):
             
            vstyle_nw.update(time_id,self.G,self.nw,self.arrayOf_f_e_minus,self.arrayOf_z_e,self.pars,self.globalNumberOfTimeSteps)
 
            self.nw.vtkPolyData.Modified()
            self.nw.vtkQPolyData.Modified()
            self.nw.vtkQBoxesPolyData.Modified()
            
    def update_actors_display(self):
        
        # network actors
        self.add_or_remove_actor(self.nw_data_times.vtkActor, self.show_data_layer_time)
        self.add_or_remove_actor(self.nw_data_capacities.vtkActor, self.show_data_layer_capacity)
        self.add_or_remove_actor(self.nw.vtkActor, self.show_animation_layer)

        # colorbars
        if (self.show_animation_layer):
            self.add_or_remove_actor(self.nw.vtkColorBarActor, self.show_colorbar, type='2D')
            self.add_or_remove_actor(self.nw_data_times.vtkColorBarActor, False, type='2D')
            self.add_or_remove_actor(self.nw_data_capacities.vtkColorBarActor, False, type='2D')
            
        if (self.show_data_layer_time):
            self.add_or_remove_actor(self.nw.vtkColorBarActor, False, type='2D')
            self.add_or_remove_actor(self.nw_data_times.vtkColorBarActor, self.show_colorbar, type='2D')
            self.add_or_remove_actor(self.nw_data_capacities.vtkColorBarActor, False, type='2D')
        
        if (self.show_data_layer_capacity):
            self.add_or_remove_actor(self.nw.vtkColorBarActor, False, type='2D')
            self.add_or_remove_actor(self.nw_data_times.vtkColorBarActor, False, type='2D')
            self.add_or_remove_actor(self.nw_data_capacities.vtkColorBarActor, self.show_colorbar, type='2D')

        # labels
        self.add_or_remove_actor(self.nw_nodes.vtkActor_st_labels, self.show_nodes_st_labels)
        self.add_or_remove_actor(self.nw_nodes.vtkActor_non_st_labels, self.show_nodes_non_st_labels)
        
        # annotations
        self.add_or_remove_actor(self.annotation_info_nw, self.show_up_left_annotations, type='2D')
        self.add_or_remove_actor(self.annotation_info_iren, self.show_down_left_annotations, type='2D')
    
        self.Render()
        
    def add_or_remove_actor(self, actor, show, type='3D'):
        
        if (show):
            if (type=='2D'):
                self.renderer.AddActor2D(actor)
            else:
                self.renderer.AddActor(actor)
        else:
            try:
                self.renderer.RemoveActor(actor)
            except:
                pass
            
    def Render(self):
        
        self.interactor.GetRenderWindow().Render()

