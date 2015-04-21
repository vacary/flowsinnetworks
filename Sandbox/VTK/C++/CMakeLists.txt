cmake_minimum_required(VERSION 2.8)
 
PROJECT(ConnectedComponents)
 
find_package(VTK REQUIRED)
include(${VTK_USE_FILE})
 
add_executable(ConnectedComponents MACOSX_BUNDLE ConnectedComponents)
 
if(VTK_LIBRARIES)
  target_link_libraries(ConnectedComponents ${VTK_LIBRARIES})
else()
  target_link_libraries(ConnectedComponents vtkHybrid vtkWidgets)
endif()

