import vtk
#source = vtk.vtkRandomGraphSource()
#source.Update()
#http://www.vtk.org/Wiki/VTK/Examples/Cxx/InfoVis/XGMLReader


# Create a very simple graph
g=vtk.vtkMutableDirectedGraph()
v=[]
v.append(g.AddVertex())
v.append(g.AddVertex())
v.append(g.AddVertex())

e=[]
e.append(g.AddGraphEdge(v[0],v[1]))
e.append(g.AddGraphEdge(v[2],v[1]))
e.append(g.AddGraphEdge(v[2],v[0]))
g.Dump()


# Write the graph into a file
graph_writer=vtk.vtkGraphWriter()
graph_writer.SetFileName('graph1.vtk')
graph_writer.SetInputData(g)
graph_writer.Write()

# Read a graph into a file
graph_reader=vtk.vtkGraphReader()
graph_reader.SetFileName('graph1.vtk')
graph_reader.Update()
f = graph_reader.GetOutput()
f.Dump()



# Create the edge weight array
weights = vtk.vtkDoubleArray()
weights.SetNumberOfComponents(1)
weights.SetName("Weights")
 
# Set the edge weights
weights.InsertNextValue(1.0)
weights.InsertNextValue(1.0)
weights.InsertNextValue(2.0)


# Add the edge weight array to the graph
g.GetEdgeData().AddArray(weights)

# Graph rendering
graphLayoutView = vtk.vtkGraphLayoutView()
graphLayoutView.AddRepresentationFromInput(g)
graphLayoutView.SetLayoutStrategy("Simple 2D")
graphLayoutView.GetLayoutStrategy().SetEdgeWeightField("Weights")
graphLayoutView.GetLayoutStrategy().SetWeightEdges(1)
graphLayoutView.SetEdgeLabelArrayName("Weights")
graphLayoutView.SetEdgeLabelVisibility(1)

graphLayoutView.SetVertexLabelVisibility(1)


graphLayoutView.GetLayoutStrategy().SetRandomSeed(0)

graphLayoutView.ResetCamera()
graphLayoutView.Render()
 
graphLayoutView.GetLayoutStrategy().SetRandomSeed(0)
 
graphLayoutView.GetInteractor().Start()
