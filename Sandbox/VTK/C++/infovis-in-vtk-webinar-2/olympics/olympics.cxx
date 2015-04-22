#include <vtkDelimitedTextReader.h>
#include <vtkGraphLayoutView.h>
#include <vtkGroupLeafVertices.h>
#include <vtkNew.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkTableToTreeFilter.h>
#include <vtkTextProperty.h>
#include <vtkTreeFieldAggregator.h>
#include <vtkTreeMapView.h>
#include <vtkViewTheme.h>

int main()
{
  // Read in the table
  vtkNew<vtkDelimitedTextReader> reader;
  reader->SetFileName("olympics2012.csv");
  reader->SetHaveHeaders(true);
  reader->SetDetectNumericColumns(true);
  reader->SetOutputPedigreeIds(true);

  // Convert to tree
  vtkNew<vtkTableToTreeFilter> tableToTree;
  tableToTree->SetInputConnection(reader->GetOutputPort());

  // Add a level
  vtkNew<vtkGroupLeafVertices> groupLeaves;
  groupLeaves->SetInputConnection(tableToTree->GetOutputPort());
  groupLeaves->SetInputArrayToProcess(0, 0, 0, vtkDataObject::VERTEX, "Event");
  groupLeaves->SetInputArrayToProcess(1, 0, 0, vtkDataObject::VERTEX, "Country_Event");

  // Aggregate a field
  vtkNew<vtkTreeFieldAggregator> agg;
  agg->SetInputConnection(groupLeaves->GetOutputPort());
  agg->SetLeafVertexUnitSize(false);
  agg->SetField("Gold");

  // Treemap view
  vtkNew<vtkTreeMapView> treemapView;
  treemapView->SetRepresentationFromInputConnection(agg->GetOutputPort());
  treemapView->SetLayoutStrategyToSquarify();
  treemapView->SetAreaLabelVisibility(true);
  treemapView->SetAreaLabelArrayName("Country_Event");
  treemapView->SetAreaSizeArrayName("Gold");

  // Standard tree view
  vtkNew<vtkGraphLayoutView> treeView;
  treeView->SetRepresentationFromInputConnection(agg->GetOutputPort());
  treeView->SetLayoutStrategyToTree();
  treeView->SetVertexLabelVisibility(true);
  treeView->SetVertexLabelArrayName("Country_Event");

  // Set up view theme
  vtkNew<vtkViewTheme> theme;
  theme->SetBackgroundColor(1, 1, 1);
  theme->SetBackgroundColor2(1, 1, 1);
  theme->SetPointSaturationRange(0.5, 0.5);
  theme->SetCellColor(0, 0, 0);
  theme->SetCellOpacity(0.5);
  theme->GetPointTextProperty()->SetColor(0, 0, 0);

  // Run tree view
  treeView->ApplyViewTheme(theme.GetPointer());
  treeView->GetRenderWindow()->SetSize(800, 800);
  treeView->GetRenderWindow()->SetLineSmoothing(true);
  treeView->GetRenderWindow()->SetPointSmoothing(true);
  treeView->Update();
  treeView->ResetCamera();
  treeView->Render();

  // Run treemap view
  treemapView->ApplyViewTheme(theme.GetPointer());
  treemapView->GetRenderWindow()->SetSize(800, 800);
  treemapView->Update();
  treemapView->ResetCamera();
  treemapView->Render();

  // Start up interaction
  treemapView->GetInteractor()->Initialize();
  treemapView->GetInteractor()->Start();

  return 0;
}
