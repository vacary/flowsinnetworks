cmake_minimum_required(VERSION 2.8)
project(olympics)
find_package(VTK REQUIRED)
include(${VTK_USE_FILE})
add_executable(olympics MACOSX_BUNDLE olympics.cxx)
target_link_libraries(olympics
  vtkIOInfovis
  vtkRenderingOpenGL
  vtkRenderingFreeTypeOpenGL
  vtkRenderingVolumeOpenGL
  vtkViewsInfovis
)
