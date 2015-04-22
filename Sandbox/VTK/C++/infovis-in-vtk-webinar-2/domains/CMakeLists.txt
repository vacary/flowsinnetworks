cmake_minimum_required(VERSION 2.8)
project(domains)
find_package(VTK REQUIRED)
include(${VTK_USE_FILE})
add_executable(domains MACOSX_BUNDLE domains.cxx)
target_link_libraries(domains
  vtkCommonColor
  vtkIOInfovis
  vtkRenderingOpenGL
  vtkRenderingFreeTypeOpenGL
  vtkRenderingVolumeOpenGL
  vtkViewsContext2D
  vtkViewsInfovis
)
