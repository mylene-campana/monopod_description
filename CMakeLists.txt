# Copyright (c) 2015 CNRS
# Author: Mylene Campana
#
# This file is part of monopod_description.
# monopod_description is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# monopod_description is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# monopod_description.  If not, see
# <http://www.gnu.org/licenses/>.

# Requires at least CMake 2.6 to configure the package.
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

INCLUDE(cmake/base.cmake)
INCLUDE(cmake/python.cmake)

SET(PROJECT_NAME monopod_description)
SET(PROJECT_DESCRIPTION "Data specific to monopod robot for hpp-corbaserver")
SET(PROJECT_URL "")

SETUP_PROJECT()

FINDPYTHON()
ADD_REQUIRED_DEPENDENCY ("hpp-corbaserver >= 3")

SET(CATKIN_PACKAGE_SHARE_DESTINATION
  ${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME})


# install all files contained in meshes
install(DIRECTORY meshes/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/meshes)

 # robot URDF
install(FILES
  urdf/monopod.urdf
  urdf/monopod_mesh.urdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/urdf)

 # robot SRDF
install(FILES
  srdf/monopod.srdf
  srdf/monopod_mesh.srdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/srdf)


install (FILES
  src/hpp/corbaserver/monopod/robot.py
  src/hpp/corbaserver/monopod/__init__.py
  DESTINATION ${PYTHON_SITELIB}/hpp/corbaserver/monopod)

install (FILES
  src/hpp/corbaserver/monopod_mesh/robot.py
  src/hpp/corbaserver/monopod_mesh/__init__.py
  DESTINATION ${PYTHON_SITELIB}/hpp/corbaserver/monopod_mesh)

SETUP_PROJECT_FINALIZE()
