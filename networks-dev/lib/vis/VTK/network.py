"""

VISUALIZATION METHODS AND CLASSES

network

"""

import sys, os

import vtk
import networkx as nx
import random

from numpy import *
import math

lib_path = os.path.abspath(os.path.join('..','..','..','lib'))
sys.path.append(lib_path)

import lib.vis.general as gen
import lib.vis.VTK.rsc.colormaps as cmap

class VtkNetworkBck:
     
    def __init__(self,G,style_pars):
     
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkLineCells   = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkFilter      = vtk.vtkRibbonFilter()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        
        self._initialize(G,style_pars)
        
    def _initialize(self,G,style_pars):
    
        inf_point_index = 0
        sup_point_index = 0
      
        edge_log = {}
          
        edge_counter    = 0
        point_id        = 0    
        cell_id         = 0

        for edge in G.edges_iter():

            #print edge
   
            edge_tail = G.node[edge[0]]
            edge_head = G.node[edge[1]]
            
            if edge not in edge_log:
                edge_log[edge] = 0
            else:
                edge_log[edge] = edge_log[edge] + 1
                
            edge_id = edge_log[edge]
                
            str_edge_geometry   = G.edge[edge[0]][edge[1]][edge_id]['geometry']
            str_edge_keys       = G.edge[edge[0]][edge[1]][edge_id]['geometry_keys']
                
            edge_geometry = gen.getPointsFromStrList(str_edge_geometry)
            edge_keys     = gen.getArrayFromStrList(str_edge_keys)
            
            #local geometry
            
            local_point_id  = 0
            
            kc      = 0
            inf_key = int(edge_keys[kc])
            sup_key = int(edge_keys[kc+1])
            
            # for edge points classification 
            localCellPointsIDs = []
            aux_stack = []
            
            edgeCellIDs = []
            edgeCellPointsIDs = []
            
            for point in edge_geometry:
                
                self.vtkPoints.InsertNextPoint(point)
                
                # edge points manager
            
                if (len(aux_stack)> 0):
            
                    localCellPointsIDs.append(aux_stack.pop())
                
                if (local_point_id <= sup_key):
                    
                    localCellPointsIDs.append(point_id)
                    
                    if (local_point_id == sup_key):
                        
                        aux_stack.append(point_id)

                        # create polyline for cell
                        cell_numberOfPoints = len(localCellPointsIDs)
                        polyLine = vtk.vtkPolyLine()
                        polyLine.GetPointIds().SetNumberOfIds(cell_numberOfPoints)
                        for i in xrange(cell_numberOfPoints):
                            polyLine.GetPointIds().SetId(i,localCellPointsIDs[i])
                        self.vtkLineCells.InsertNextCell(polyLine)                        
                        
                        edgeCellPointsIDs.append(localCellPointsIDs)
                        edgeCellIDs.append(cell_id)
                        
                        cell_id = cell_id + 1
                        
                        localCellPointsIDs   = []
                
                        if (sup_key != int(edge_keys[-1])):
                            kc      = kc + 1
                            inf_key = int(edge_keys[kc])
                            sup_key = int(edge_keys[kc+1])
                            
                local_point_id  = local_point_id + 1
                point_id        = point_id + 1
                
            sup_point_index = inf_point_index + len(edge_geometry) - 1
            inf_point_index = sup_point_index + 1
            
            #########
            
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLineCells)
         
        # filter
        
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
                
        self.vtkFilter.UseDefaultNormalOn()        
        self.vtkFilter.SetAngle(0) 
            
        self.vtkFilter.SetWidth(1)
        
        # mapper
        
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        self.vtkActor.SetMapper(self.vtkMapper)
        
        if (G.number_of_nodes() <= 75):
            self.vtkActor.GetProperty().SetColor(0.2,0.2,0.2)
        else:
            self.vtkActor.GetProperty().SetColor(0.1,0.1,0.1)


class VtkNodes:
    
    def __init__(self,nxGraph,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label):
        
        self.vtkPoints          = vtk.vtkPoints()
        self.vtkVertices        = vtk.vtkCellArray()
        self.vtkPolyData        = vtk.vtkPolyData()
        self.vtkFilter          = vtk.vtkGlyph3D()
        self.vtkMapper          = vtk.vtkPolyDataMapper()
        
        self.colors             = vtk.vtkUnsignedCharArray()
        
        self.vtkActor           = vtk.vtkActor()    # actor for nodes
        
        self.vtkPoints_st_labels    = vtk.vtkPoints()
        self.st_labels              = vtk.vtkStringArray()
        self.vtkActor_st_labels     = vtk.vtkActor2D()  # actor for labels (nodes in {source,sink})

        self._initialize(nxGraph,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label)

    def _initialize(self,G,nodeRadius,opacity,lbFontSize,node_source_label,node_sink_label):
    
        # Points for st labels
        self.vtkPoints_st_labels.SetNumberOfPoints(2)
    
        # Colors
        self.colors.SetNumberOfComponents(4)
        self.colors.SetName("Colors")
        
        c = 0
                
        for i in G.nodes_iter():
            
            posX = G.node[i]['pos'][0] 
            posY = G.node[i]['pos'][1]
            posZ = G.node[i]['pos'][2] + 0.0005
            
            self.vtkPoints.InsertPoint(G.node[i]['id'],posX,posY,posZ)
            
            if (G.node[i]['nlabel'] == node_source_label):
                
                #color   = [int(1*255),0,0,255]
                color   = [255,0,0,255]
                
                self.vtkPoints_st_labels.SetPoint(0,[posX,posY,posZ])
                
            elif (G.node[i]['nlabel'] == node_sink_label ):
                
                color   = [0,50,255,255]
                
                self.vtkPoints_st_labels.SetPoint(1,[posX,posY,posZ])
                
            else:
                
                color   = [75,75,75,255]
                                
            self.colors.InsertNextTupleValue(color)
            
            self.vtkVertices.InsertNextCell(1)
            self.vtkVertices.InsertCellPoint(c)
            
            c = c + 1
            
        # polydata
            
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkVertices)
        
        ### add arrays 
        self.vtkPolyData.GetPointData().AddArray(self.colors)
        
        # filter for nodes
                    
        source = vtk.vtkRegularPolygonSource()
        source.SetNumberOfSides(50)
        source.SetRadius(nodeRadius)
              
        if (vtk.VTK_MAJOR_VERSION <= 5):
            self.vtkFilter.SetInput(self.vtkPolyData)
            self.vtkFilter.SetSource(source.GetOutput())
        else:
            self.vtkFilter.SetInputData(self.vtkPolyData)
            self.vtkFilter.SetSourceConnection(source.GetOutputPort())
            

#         source = vtk.vtkSphereSource()
#         source.SetRadius(1)
#         source.SetPhiResolution(16)
#         source.SetThetaResolution(40)
#              
#         if (vtk.VTK_MAJOR_VERSION <= 5):   
#             self.vtkFilter.SetInput(self.vtkPolyData)
#             self.vtkFilter.SetSource(source.GetOutput())
#         else:
#             self.vtkFilter.SetInputData(self.vtkPolyData)
#             self.vtkFilter.SetSourceConnection(source.GetOutputPort())
        
        
        # mapper
 
        self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUsePointFieldData()
        self.vtkMapper.SelectColorArray("Colors")
        
        # actor
        
        self.vtkActor.SetMapper(self.vtkMapper)

        self.vtkActor.GetProperty().SetSpecularColor(0,0,0)
        self.vtkActor.GetProperty().SetSpecular(0.1)
        self.vtkActor.GetProperty().SetAmbient(0.05)
        self.vtkActor.GetProperty().SetDiffuse(0.5)
        self.vtkActor.GetProperty().SetOpacity(opacity)

        #### Labels for source and sink node
        
        self.st_labels.SetNumberOfValues(2)
        self.st_labels.SetName("st_labels")
        
        st_verts = vtk.vtkCellArray()
        st_verts.InsertNextCell(1)
        st_verts.InsertCellPoint(0)
        st_verts.InsertNextCell(1)
        st_verts.InsertCellPoint(1)
        
        self.st_labels.SetValue(0,'s')#node_source_label)
        self.st_labels.SetValue(1,'t')#node_sink_label)
        
        st_pointData  = vtk.vtkPolyData()   
        st_pointData.SetPoints(self.vtkPoints_st_labels)          
        st_pointData.SetVerts(st_verts)         
        
        st_pointData.GetPointData().AddArray(self.st_labels)            
         
        st_mapper = vtk.vtkPolyDataMapper()
        
        if (vtk.VTK_MAJOR_VERSION <= 5):
            st_mapper.SetInput(st_pointData)
        else:
            st_mapper.SetInputData(st_pointData)
                        
        st_labelMapper = vtk.vtkLabeledDataMapper()
        st_labelMapper.SetInputData(st_pointData)
        st_labelMapper.SetLabelModeToLabelFieldData()
        tprop = st_labelMapper.GetLabelTextProperty()
        tprop.SetFontSize(lbFontSize)
        tprop.SetBold(1)
        tprop.SetItalic(0)
        
        if ( G.number_of_nodes() <= 25 ):
            tprop.SetShadow(0)
        else:
            tprop.SetShadow(1)
        
        tprop.SetJustificationToCentered()
        tprop.SetVerticalJustificationToCentered()
        
        self.vtkActor_st_labels.SetMapper(st_labelMapper)


class VtkNetwork:
     
    def __init__(self,G,style_pars):
     
           #network
        self.vtkPoints      = vtk.vtkPoints()
        self.vtkLineCells   = vtk.vtkCellArray()
        self.vtkPolyData    = vtk.vtkPolyData()
        self.vtkFilter      = vtk.vtkRibbonFilter()
        self.vtkMapper      = vtk.vtkPolyDataMapper()
        self.vtkActor       = vtk.vtkActor()
        self.vtkColorBar    = vtk.vtkScalarBarActor()
        
        self.edges_dict     = {}
        self.cells_edges    = vtk.vtkIntArray()
        
        self.cells_colors   = vtk.vtkUnsignedCharArray()
        
        self.lut            = vtk.vtkLookupTable()
        
        #queue boxes
        self.vtkQBoxesPoints      = vtk.vtkPoints()
        self.vtkQBoxesLineCells   = vtk.vtkCellArray()
        self.vtkQBoxesCellsColors = vtk.vtkUnsignedCharArray()
        self.vtkQBoxesPolyData    = vtk.vtkPolyData()
        self.vtkQBoxesMapper      = vtk.vtkPolyDataMapper()
        self.vtkQBoxesActor       = vtk.vtkActor()
    
        #queues
        self.vtkQPoints      = vtk.vtkPoints()
        self.vtkQLineCells   = vtk.vtkCellArray()
        self.vtkQCellsColors = vtk.vtkUnsignedCharArray()
        self.vtkQPolyData    = vtk.vtkPolyData()
        self.vtkQFilter      = vtk.vtkRibbonFilter()
        self.vtkQMapper      = vtk.vtkPolyDataMapper()
        self.vtkQActor       = vtk.vtkActor()        
    
        self._initialize(G,style_pars)
        
    def _initialize(self,G,style_pars):
    
        inf_point_index = 0
        sup_point_index = 0
      
        edge_log = {}
          
        edge_counter    = 0
        point_id        = 0    
        cell_id         = 0
        
        self.cells_edges.SetNumberOfComponents(3)
        self.cells_edges.SetName('CellEdges')

        for edge in G.edges_iter():
            
            edge_tail = G.node[edge[0]]
            edge_head = G.node[edge[1]]
            
            if edge not in edge_log:
                edge_log[edge] = 0
            else:
                edge_log[edge] = edge_log[edge] + 1
                
            edge_id = edge_log[edge]
            
            str_edge_geometry   = G.edge[edge[0]][edge[1]][edge_id]['geometry']
            str_edge_keys       = G.edge[edge[0]][edge[1]][edge_id]['geometry_keys']
                
            edge_geometry = gen.getPointsFromStrList(str_edge_geometry)
            edge_keys     = gen.getArrayFromStrList(str_edge_keys)
            
            #local geometry
            
            
            local_point_id  = 0
            
            kc      = 0
            inf_key = int(edge_keys[kc])
            sup_key = int(edge_keys[kc+1])
            
            # for edge points classification 
            localCellPointsIDs = []
            aux_stack = []
            
            edgeCellIDs = []
            edgeCellPointsIDs = []

            for point in edge_geometry:
                
                self.vtkPoints.InsertNextPoint(point)
                
                # edge points manager
            
                if (len(aux_stack)> 0):
            
                    localCellPointsIDs.append(aux_stack.pop())
                
                if (local_point_id <= sup_key):
                    
                    localCellPointsIDs.append(point_id)
                    
                    if (local_point_id == sup_key):
                        
                        aux_stack.append(point_id)

                        # create polyline for cell
                        cell_numberOfPoints = len(localCellPointsIDs)
                        polyLine = vtk.vtkPolyLine()
                        polyLine.GetPointIds().SetNumberOfIds(cell_numberOfPoints)
                        for i in xrange(cell_numberOfPoints):
                            polyLine.GetPointIds().SetId(i,localCellPointsIDs[i])
                        self.vtkLineCells.InsertNextCell(polyLine)                        
                        
                        edgeCellPointsIDs.append(localCellPointsIDs)
                        edgeCellIDs.append(cell_id)
                        
                        #print str([edge[0],edge[1],edge_id])
                        self.cells_edges.InsertNextTupleValue([edge[0],edge[1],edge_id]) ### data for interactor
                        
                        cell_id = cell_id + 1
                        
                        localCellPointsIDs   = []
                
                        if (sup_key != int(edge_keys[-1])):
                            kc      = kc + 1
                            inf_key = int(edge_keys[kc])
                            sup_key = int(edge_keys[kc+1])
                            
                local_point_id  = local_point_id + 1
                point_id        = point_id + 1
                
            sup_point_index = inf_point_index + len(edge_geometry) - 1
            inf_point_index = sup_point_index + 1
                

            # queues
            
            # ---- qbox ----
            
            qratio = 0.22
            widthFactor = 0.075*0.5
            distanceFactor = 0.0
            h = 1.25*widthFactor

            # reference points
            p = array(edge_geometry[0])
            q = array(edge_geometry[1])
            
            u = (q-p)/linalg.norm(q-p)
            
            v = zeros(3)
            
            if (abs(u[0])> 0):
            
                v[0] = -u[1]/u[0]
                v[1] = 1.0
                v[2] = 0
            else:
                v[0] = 1.0
                v[1] = 0
                v[2] = 0
            
            w = v/linalg.norm(v)
            
            qm = p + u*qratio + distanceFactor*w
            
            qbp = qm + 0.5*widthFactor*w + 0.5*h*u 
            qbm = qm - 0.5*widthFactor*w + 0.5*h*u
            qhp = qbp - h*u
            qhm = qbm - h*u   

            z_aux = 2*1E-5
            qbp[2] = z_aux
            qbm[2] = z_aux
            qhp[2] = z_aux
            qhm[2] = z_aux

            # add points for the box     
            self.vtkQBoxesPoints.InsertNextPoint(qhm)
            self.vtkQBoxesPoints.InsertNextPoint(qbm)
            self.vtkQBoxesPoints.InsertNextPoint(qbp)
            self.vtkQBoxesPoints.InsertNextPoint(qhp)
            
            # create polyline for cell
            q_inf_key = edge_counter*4
            polyLine = vtk.vtkPolyLine()
            polyLine.GetPointIds().SetNumberOfIds(4)
            polyLine.GetPointIds().SetId(0,q_inf_key)
            polyLine.GetPointIds().SetId(1,q_inf_key+1)
            polyLine.GetPointIds().SetId(2,q_inf_key+2)
            polyLine.GetPointIds().SetId(3,q_inf_key+3)
            self.vtkQBoxesLineCells.InsertNextCell(polyLine)
            
            # ---- queue ----
            
            qb = 0.5*(qbp + qbm)
            qh = qb - h*u
            
            qb[2] = z_aux
            qh[2] = z_aux 
            
            #add points for queue element
            self.vtkQPoints.InsertNextPoint(qb)
            self.vtkQPoints.InsertNextPoint(qh)
            
            #create polyline for queue cell.InsertNextTupleValue(nColor)
            q_inf_key = edge_counter*2
            polyLine = vtk.vtkPolyLine()
            polyLine.GetPointIds().SetNumberOfIds(2)
            polyLine.GetPointIds().SetId(0,q_inf_key)
            polyLine.GetPointIds().SetId(1,q_inf_key+1)
            self.vtkQLineCells.InsertNextCell(polyLine)
            
            queuePointsIDs  = [q_inf_key,q_inf_key+1]
            
            queueRefPoints  = [qb,qh]
            queueMaxHeight  = linalg.norm(qh-qb)
            queueRefDirection = (qh-qb)/queueMaxHeight
            queueMaxQValue = style_pars['max_z_e']
            
            queueBoxCellID  = edge_counter
            queueCellID     = edge_counter
            
            edge_counter = edge_counter + 1

            #########
            
            aux = []
            
            aux.append(edgeCellIDs)
            aux.append(edgeCellPointsIDs)
            aux.append(queuePointsIDs)
            aux.append(queueRefPoints)
            aux.append(queueMaxHeight)
            aux.append(queueRefDirection)
            aux.append(queueMaxQValue)
            aux.append(queueBoxCellID)
            aux.append(queueCellID)
            
            self.edges_dict[(edge[0],edge[1],edge_id)] = aux 
            
            
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkLineCells)
        
        # \begin{ qboxes } 
        
        self.vtkQBoxesPolyData.SetPoints(self.vtkQBoxesPoints)
        self.vtkQBoxesPolyData.SetLines(self.vtkQBoxesLineCells)

        if (vtk.VTK_MAJOR_VERSION <= 5):                # check VTK version
            self.vtkQBoxesMapper.SetInput(self.vtkQBoxesPolyData)
        else:
            self.vtkQBoxesMapper.SetInputData(self.vtkQBoxesPolyData)

        self.vtkQBoxesCellsColors.SetNumberOfComponents(4)
        self.vtkQBoxesCellsColors.SetName('QBoxesColors')

        for i in xrange(self.vtkQBoxesLineCells.GetNumberOfCells()):
            nColor = [int(255*0.0),int(255*0.8),int(255*0.0),255]
            #nColor = [int(255*0.15),int(255*0.15),int(255*0.15),int(255*0)]
            self.vtkQBoxesCellsColors.InsertNextTupleValue(nColor)
        self.vtkQBoxesPolyData.GetCellData().AddArray(self.vtkQBoxesCellsColors)

        self.vtkQBoxesMapper.ScalarVisibilityOn()
        self.vtkQBoxesMapper.SetScalarModeToUseCellFieldData()
        self.vtkQBoxesMapper.SelectColorArray('QBoxesColors')

        self.vtkQBoxesActor.SetMapper(self.vtkQBoxesMapper)

        self.vtkQBoxesActor.GetProperty().SetLineWidth(2)
                
        # \end{ qboxes }
        
        # \begin{ queues }

        self.vtkQPolyData.SetPoints(self.vtkQPoints)
        self.vtkQPolyData.SetLines(self.vtkQLineCells)
        
        if (vtk.VTK_MAJOR_VERSION <= 5):   
            self.vtkQFilter.SetInput(self.vtkQPolyData)
        else:
            self.vtkQFilter.SetInputData(self.vtkQPolyData)
                
        self.vtkQFilter.UseDefaultNormalOn()        
        self.vtkQFilter.SetAngle(0) 
        self.vtkQFilter.SetWidth(1.0)
    
        self.vtkQMapper.SetInputConnection(self.vtkQFilter.GetOutputPort())

        self.vtkQCellsColors.SetNumberOfComponents(4)
        self.vtkQCellsColors.SetName('QColors')

        for i in xrange(self.vtkQLineCells.GetNumberOfCells()):
            nColor = [int(255*(random.random())),int(255*(random.random())),int(255*(random.random())),0]
            #nColor = [int(255*0.15),int(255*0.15),int(255*0.15),int(255*0)]
            self.vtkQCellsColors.InsertNextTupleValue(nColor)
        self.vtkQPolyData.GetCellData().AddArray(self.vtkQCellsColors)

        self.vtkQMapper.ScalarVisibilityOn()
        self.vtkQMapper.SetScalarModeToUseCellFieldData()
        self.vtkQMapper.SelectColorArray('QColors')

        self.vtkQActor.SetMapper(self.vtkQMapper)      
        self.vtkQFilter.SetWidth(0.5*widthFactor)       
        
        # \end{ queues }
        
        # colors 
        
        self.cells_colors.SetNumberOfComponents(4)
        self.cells_colors.SetName('Colors')

        for i in xrange(self.vtkLineCells.GetNumberOfCells()):
            #nColor = [int(255*(random.random())),int(255*(random.random())),int(255*(random.random())),200]
            nColor = [int(255*0.15),int(255*0.15),int(255*0.15),int(255*0)]
            self.cells_colors.InsertNextTupleValue(nColor)
        self.vtkPolyData.GetCellData().AddArray(self.cells_colors)
 
        self.vtkPolyData.GetCellData().AddArray(self.cells_edges)

 
        useFilter = True
        
        if (useFilter == True):
 
            # filter
   
            if (vtk.VTK_MAJOR_VERSION <= 5):   
                self.vtkFilter.SetInput(self.vtkPolyData)
            else:
                self.vtkFilter.SetInputData(self.vtkPolyData)
                    
            self.vtkFilter.UseDefaultNormalOn()        
            self.vtkFilter.SetAngle(0) 
                
            self.vtkFilter.SetWidth(1)
            #self.vtkFilter.SetVaryWidth(1)
   
            # mapper
        
            self.vtkMapper.SetInputConnection(self.vtkFilter.GetOutputPort())
        
        else:

            # mapper
            
            if (vtk.VTK_MAJOR_VERSION <= 5):                # check VTK version
                self.vtkMapper.SetInput(self.vtkPolyData)
            else:
                self.vtkMapper.SetInputData(self.vtkPolyData)

        self.vtkMapper.ScalarVisibilityOn()
        self.vtkMapper.SetScalarModeToUseCellFieldData()
        self.vtkMapper.SelectColorArray('Colors')

        self.vtkActor.SetMapper(self.vtkMapper)
        
        # scalarbar
        
        self.vtkColorBar.SetLookupTable(self.vtkMapper.GetLookupTable())
        self.vtkColorBar.SetTitle("Flow rate")
        self.vtkColorBar.SetMaximumWidthInPixels(60)
        self.vtkColorBar.SetMaximumHeightInPixels(500)
        self.vtkColorBar.SetOrientationToVertical()
        self.vtkColorBar.GetTitleTextProperty().SetFontSize(100)
        self.vtkColorBar.GetTitleTextProperty().SetLineOffset(25)
        self.vtkColorBar.SetLabelFormat('%.1f')
        self.vtkColorBar.SetNumberOfLabels(5)
        self.vtkColorBar.UseOpacityOn()

        colorMap = cmap.getColorMap(10)

        self.lut.SetNumberOfTableValues(len(colorMap))
  
        i = 0
        for rgbColor in colorMap:
            c = rgbColor
            self.lut.SetTableValue(i,c[0],c[1],c[2],0.825)
            i = i + 1
    

        self.lut.Build()
                
        self.vtkMapper.SetScalarRange(0,style_pars['max_f_e_minus'])
        self.vtkMapper.SetLookupTable(self.lut)
        self.vtkColorBar.SetLookupTable(self.lut)
                
    def setCellColorByID(self,cell_id,flow_value):
        
        color = [0,0,0]
        self.lut.GetColor(flow_value,color)
        if (flow_value < 1E-8):
            alpha = int(255*0)
            color_tuple = [int(1*255),int(0*255),int(0*255),alpha]
            #color_tuple = [int(0*255),int(0*255),int(0*255),alpha]
            #color_tuple = [int(0.32*255),int(0.32*255),int(0.32*255),alpha]
            #color_tuple = [int(255),int(0*255),int(0*255),alpha]       
            #color_tuple = [int(color[0]*255),int(color[1]*255),int(color[2]*255),alpha]
            
            if (flow_value < 0):
                color_tuple = [int(1*255),int(0*255),int(0*255),255]
            
        else:
            alpha = int(255*0.825)
            color_tuple = [int(color[0]*255),int(color[1]*255),int(color[2]*255),alpha]
        
        self.vtkPolyData.GetCellData().GetArray('Colors').SetTuple(cell_id,color_tuple)
                
    def setQBoxCellColorByID(self,cell_id,queue_value):
        
        color_tuple = [int(255*0.75),int(255*0.0),int(255*0.0),int(255*1)]
        if (queue_value < 1E-10):
            #color_tuple = [int(255*0.25),int(255*0.25),int(255*0.25),255]
            color_tuple = [int(255*0.0),int(255*0.8),int(255*0),int(255)]
        
        if (queue_value < 0):
            color_tuple = [int(255*0.2),int(255*0.2),int(255*0.2),int(255)]
            
        self.vtkQBoxesPolyData.GetCellData().GetArray('QBoxesColors').SetTuple(cell_id,color_tuple)
        
    def setQCellColorByID(self,cell_id,queue_value):

        color_tuple = [int(255*1.0),int(0),int(0),int(255*1)]
        if (queue_value < 1E-10):
            color_tuple = [int(255*0),int(0.5*255),int(0.0),int(255*1)]
            
        if (queue_value < 0):
            color_tuple = [int(255*0.25),int(255*0.25),int(255*0.25),int(255)]
        #color_tuple[3] = int(0*random.random()*255)
        self.vtkQPolyData.GetCellData().GetArray('QColors').SetTuple(cell_id,color_tuple)
        
        
        
        