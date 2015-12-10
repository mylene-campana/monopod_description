# monopod_description

This package containts the description of a monopod robot.

The purpose of this package is to test parabola-type of steering method with a jumping robot.

The package contains:

  - URDF/SRDF/calss files describing the objects,
 
  - Some Python scripts going along with HPP software (github.com/humanoid-path-planner) for motion planning,

The problem can be vizualised with HPP-gepetto-viewer (github.com/humanoid-path-planner) 
or with RViz (must create .launch files).

To install the package with cmake, simply:

  - Create a 'build' directory in the source package,
  
  - in the created /build, configure the package - particularly the 'install path variable' - and install it 
  with 'ccmake ..' and 'make install'.
