
#
# Visualization methods
#

import vtk
from numpy import *

def alphaPoint(p1,p2,alpha):
    
    r = zeros(3)
    
    d = array(p2) - array(p1)
    
    r = array(p1) + alpha*d
    
    return r


class Tube:
    
    def __init__(self,p1,p2):
       
        self.p1 = p1
        self.p2 = p2
        
        self.vtkPoints = vtk.vtkPoints()
        self.vtkPoints.SetNumberOfPoints(2)
        self.vtkPoints.SetPoint(0, self.p1)
        self.vtkPoints.SetPoint(1, self.p2)
        
        self.vtkCellArray  = vtk.vtkCellArray()
        self.vtkCellArray.InsertNextCell(2)
        self.vtkCellArray.InsertCellPoint(0)
        self.vtkCellArray.InsertCellPoint(1)
        
        self.vtkFloatArray = vtk.vtkFloatArray()
        self.vtkFloatArray.SetNumberOfValues(2)
        self.vtkFloatArray.SetValue(0, 1.0)
        self.vtkFloatArray.SetValue(1, 1.0)
        
        self.vtkPolyData = vtk.vtkPolyData()
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetLines(self.vtkCellArray)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkFloatArray)
        
        self.vtkSplineFilter = vtk.vtkSplineFilter()
        if (vtk.VTK_MAJOR_VERSION <= 5):
            self.vtkSplineFilter.SetInput(self.vtkPolyData)
        else:
            self.vtkSplineFilter.SetInputData(self.vtkPolyData)
        self.vtkSplineFilter.SetNumberOfSubdivisions(10*2)
        self.vtkSplineFilter.Update()
        
        self.vtkTubeFilter = vtk.vtkTubeFilter()
        self.vtkTubeFilter.SetInputConnection(self.vtkSplineFilter.GetOutputPort())
        self.vtkTubeFilter.SetRadius(0)
        self.vtkTubeFilter.SetNumberOfSides(20)
        self.vtkTubeFilter.CappingOn()
        
        self.vtkPolyDataMapper = vtk.vtkPolyDataMapper()
        self.vtkPolyDataMapper.SetInputConnection(self.vtkTubeFilter.GetOutputPort())
        
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(self.vtkPolyDataMapper)       

         
    def setRadius(self,r):
        self.vtkTubeFilter.SetRadius(r) 

    def setOpacity(self,opacity):
        self.vtkActor.GetProperty().SetOpacity(opacity)
         


