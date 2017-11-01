#include <vtkColorSeries.h>
#include <vtkContext2D.h>
#include <vtkContextActor.h>
#include <vtkContextInteractorStyle.h>
#include <vtkContextMouseEvent.h>
#include <vtkContextScene.h>
#include <vtkContextTransform.h>
#include <vtkDataSetAttributes.h>
#include <vtkDelimitedTextReader.h>
#include <vtkFast2DLayoutStrategy.h>
#include <vtkForceDirectedLayoutStrategy.h>
#include <vtkGraphItem.h>
#include <vtkGraphLayout.h>
#include <vtkIncrementalForceLayout.h>
#include <vtkLookupTable.h>
#include <vtkNew.h>
#include <vtkObjectFactory.h>
#include <vtkRandomLayoutStrategy.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkSimple2DLayoutStrategy.h>
#include <vtkTableToGraph.h>
#include <vtkTextProperty.h>
#include <vtkTransform2D.h>

//----------------------------------------------------------------------------
class MyGraphItem : public vtkGraphItem
{
public:
  static MyGraphItem *New();
  vtkTypeMacro(MyGraphItem, vtkGraphItem);

protected:

  vtkIdType focusedVertex;

  // ------------------------------------------------------------------------
  MyGraphItem()
  {
    focusedVertex = -1;
  }

  // ------------------------------------------------------------------------
  virtual vtkColor4ub VertexColor(vtkIdType vertex)
  {
    if (vertex == focusedVertex)
      {
      return vtkColor4ub(255, 0, 0, 255);
      }
    vtkAbstractArray *domain = this->GetGraph()->GetVertexData()->GetAbstractArray("domain");
    if (domain->GetVariantValue(vertex).ToString() == "domain1")
      {
      return vtkColor4ub(128, 128, 175, 128);
      }
    return vtkColor4ub(175, 128, 128, 128);
  }

  // ------------------------------------------------------------------------
  virtual vtkStdString VertexTooltip(vtkIdType vertex)
  {
    vtkAbstractArray *label = this->GetGraph()->GetVertexData()->GetAbstractArray("label");
    return label->GetVariantValue(vertex).ToString();
  }

  // ------------------------------------------------------------------------
  virtual vtkColor4ub EdgeColor(vtkIdType line, vtkIdType point)
  {
    return vtkColor4ub(128, 128, 128, 128);
  }

  // ------------------------------------------------------------------------
  virtual float EdgeWidth(vtkIdType line, vtkIdType point)
  {
    std::cout << "InEdgeWidth "<<  std::endl;
    this->GetGraph()->GetEdgeData()->Print(cout);
    std::cout << "=========" <<this->GetGraph()->GetEdgeData()->GetAbstractArray("Email")->GetVariantValue(line) <<std::endl;
    return 1.0;
  }
  
  virtual float VertexSize	(	vtkIdType 	vertex	)	
  {
    std::cout << "vertex = "<< vertex << std::endl;
    std::cout <<  float(vertex)+1.0<< std::endl;
    std::cout << "degree = "<< this->GetGraph()->GetDegree(vertex) << std::endl;
    this->GetGraph()->GetVertexData()->Print(cout);
    vtkAbstractArray *ids = this->GetGraph()->GetVertexData()->GetAbstractArray("ids");
    ids->Print(cout);
    std::cout <<"ids->GetVariantValue(vertex)"<< ids->GetVariantValue(vertex) << std::endl;
    return this->GetGraph()->GetDegree(vertex) ;
  }
  
  // ------------------------------------------------------------------------
  virtual void PaintBuffers(vtkContext2D *painter)
  {
    // Turn off the tooltip if the superclass turned it on.
    this->PlaceTooltip(-1);

    this->Superclass::PaintBuffers(painter);

    if (focusedVertex >= 0)
      {
      painter->GetTextProp()->SetColor(0, 0, 0);
      painter->GetTextProp()->SetJustificationToCentered();
      painter->GetTextProp()->BoldOff();
      vtkVector2f pos = this->VertexPosition(focusedVertex);
      vtkStdString label = this->VertexTooltip(focusedVertex);
      painter->GetTextProp()->SetFontSize(20);
      painter->DrawString(pos.GetX(), pos.GetY(), label);
      }
  }

  // ------------------------------------------------------------------------
  virtual bool MouseButtonPressEvent(const vtkContextMouseEvent &event)
  {
    this->Superclass::MouseButtonPressEvent(event);
    focusedVertex = this->HitVertex(event.GetPos());
    this->GetGraph()->Modified();
    this->GetScene()->SetDirty(true);
    return true;
  }
};

//----------------------------------------------------------------------------
vtkStandardNewMacro(MyGraphItem);

int main()
{
  // Read in the table
  vtkNew<vtkDelimitedTextReader> reader;
  reader->SetFileName("domains.csv");
  reader->SetHaveHeaders(true);
  reader->SetDetectNumericColumns(true);
  reader->SetOutputPedigreeIds(true);

  vtkNew<vtkTableToGraph> tableToGraph;
  tableToGraph->SetInputConnection(reader->GetOutputPort());
  tableToGraph->AddLinkVertex("Location", "domain1");
  tableToGraph->AddLinkVertex("String", "domain2");
  tableToGraph->AddLinkEdge("Location", "String");
  tableToGraph->SetDirected(true);

  vtkNew<vtkRandomLayoutStrategy> randomStrategy;
  randomStrategy->SetGraphBounds(0, 800, 0, 800, 0, 0);

  vtkNew<vtkSimple2DLayoutStrategy> simple2DStrategy;
  simple2DStrategy->SetIterationsPerLayout(100);

  vtkNew<vtkFast2DLayoutStrategy> fast2DStrategy;
  fast2DStrategy->SetIterationsPerLayout(200);

  vtkNew<vtkGraphLayout> graphLayout;
  graphLayout->SetInputConnection(tableToGraph->GetOutputPort());
  graphLayout->SetLayoutStrategy(randomStrategy.GetPointer());
  graphLayout->Update();

  vtkNew<MyGraphItem> graphItem;
  graphItem->SetGraph(graphLayout->GetOutput());

  vtkNew<vtkContextTransform> trans;
  trans->SetInteractive(true);
  trans->AddItem(graphItem.GetPointer());

  vtkNew<vtkContextActor> actor;
  actor->GetScene()->AddItem(trans.GetPointer());

  vtkNew<vtkRenderer> renderer;
  renderer->SetBackground(1.0, 1.0, 1.0);

  vtkNew<vtkRenderWindow> renderWindow;
  renderWindow->SetSize(800, 800);
  renderWindow->AddRenderer(renderer.GetPointer());
  renderer->AddActor(actor.GetPointer());

  vtkNew<vtkContextInteractorStyle> interactorStyle;
  interactorStyle->SetScene(actor->GetScene());

  vtkNew<vtkRenderWindowInteractor> interactor;
  interactor->SetInteractorStyle(interactorStyle.GetPointer());
  interactor->SetRenderWindow(renderWindow.GetPointer());
  renderWindow->SetLineSmoothing(true);
  renderWindow->Render();
  graphItem->StartLayoutAnimation(interactor.GetPointer());
  interactor->Start();

  return 0;
}
