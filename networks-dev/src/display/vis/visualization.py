#
# Visualization Class

# Standard library imports
import os
import sys

# Non standard library imports
import networkx as nx
from numpy import *
import vtk

# Custom library imports
import styles.network as vstyle_nw
import interactors.custom_style as interactor

class Visualization:
 
    def __init__(self, network_name):
        
        self.timer = 0
        self.animation = False
        self.repeat = False
        
        self.pars = self.get_vparameters(network_name)
        self.TYPE = self.pars['TYPE']
        self.fps = self.pars['FPS']
        self.network_name = self.pars['NETWORK_NAME']
        self.time_step = self.pars['TIME_STEP']
        self.Tmax = self.pars['T_MAX_VIS']
        
        self.renderTimeInterval = 1000/(1.0*self.fps)
        self.globalNumberOfTimeSteps = int(floor(self.Tmax/self.time_step))
        
        self.G = self.get_graphFromGMLFile(network_name)
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

        self.setup_scene()

    def setup_scene(self):
        
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
                
    def update(self,time_id):
        
        # Scene update method
        
        if (self.TYPE in ['network']):
             
            vstyle_nw.update(time_id,self.G,self.nw,self.arrayOf_f_e_minus,self.arrayOf_z_e,self.pars,self.globalNumberOfTimeSteps)
 
            self.nw.vtkPolyData.Modified()
            self.nw.vtkQPolyData.Modified()
            self.nw.vtkQBoxesPolyData.Modified()
        
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
        
    def update_actors_display(self):
        
        # network actors
        self.add_or_remove_actor(self.nw_data_times.vtkActor, self.show_data_layer_time)
        self.add_or_remove_actor(self.nw_data_capacities.vtkActor, self.show_data_layer_capacity)
        self.add_or_remove_actor(self.nw.vtkActor, self.show_animation_layer)

        # color bars
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
        print 1/self.renderer.GetLastRenderTimeInSeconds() # Real FPS
        
    def get_vparameters(self, network_name):
        
        visualization_settings_path = os.path.abspath(os.path.join('.','projects',network_name))
        sys.path.append(visualization_settings_path)
        
        import settings as vset
        
        # set parameters    
        
        pars = {}
        pars['NETWORK_NAME']                = vset.NETWORK_NAME
        pars['TIME_STEP']                   = vset.TIME_STEP
        pars['T_MAX_VIS']                   = vset.T_MAX_VIS
        pars['FPS']                         = vset.FPS
        pars['TYPE']                        = vset.TYPE
        
        gdata = vset.network_graph_data()
        
        G = gdata[0]
        
        pars['NODE_SOURCE_LABEL']   = str(gdata[1])
        pars['NODE_SINK_LABEL']     = str(gdata[2])
        
        return pars
    
    def get_graphFromGMLFile(self, network_name):
        
        network_gml_file_path = os.path.abspath(os.path.join('.','projects',network_name,'data',str(network_name)+'.gml'))
        
        G = nx.MultiDiGraph()
        SG = nx.read_gml(network_gml_file_path) #source graph
        
        c = 0
        label_overtime = ""
        for n in SG.nodes_iter():
            
            G.add_node(n)
            G.node[n]['id']     = c
            G.node[n]['nlabel'] = SG.node[n]['nlabel']
            try: 
                G.node[n]['label_overtime'] = SG.node[n]['label_overtime']
            except:
                G.node[n]['label_overtime'] = label_overtime
            str_pos = str(SG.node[n]['pos'])
            aux = str_pos.translate(None,''.join(['[',']'])).split(',')
            pos = [float(aux[0]),float(aux[1]),float(aux[2])] 
            G.node[n]['pos']    = array(pos)
            G.node[n]['type']   = 'r'
            c = c + 1
            
        for u,v,data in SG.edges_iter(data=True):
                    
            time        = data['time']
            capacity    = data['capacity']
    
            edge_key            = -1                
            geometry            = ''
            geometry_keys       = ''
            switching_times     = ''
            z_e_overtime        = ''
            f_e_minus_overtime  = ''
            f_e_plus_overtime   = ''
            name                = ''
            
            try:
                edge_key = data['edge_key']
            except:
                pass
            try:
                geometry = data['geometry']
            except:
                pass
            try:
                geometry_keys = data['geometry_keys']
            except:
                pass
            try:
                switching_times = data['switching_times']
            except:
                pass
            try:
                z_e_overtime = data['z_e_overtime']
            except:
                pass
            try: 
                f_e_minus_overtime = data['f_e_minus_overtime']
            except:
                pass
            try:
                f_e_plus_overtime = data['f_e_plus_overtime']
            except:
                pass
            try: 
                name = data['name']
            except:
                pass
            
            G.add_edge(u,v,edge_key=edge_key,time=time,capacity=capacity,geometry=geometry,geometry_keys=geometry_keys,switching_times=switching_times,z_e_overtime=z_e_overtime,f_e_minus_overtime=f_e_minus_overtime,f_e_plus_overtime=f_e_plus_overtime,name=name)
            
        return G        
            
            
            
