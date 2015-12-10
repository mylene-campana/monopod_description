#/usr/bin/env python
# Script which goes with monopod_description package.
# Easy way to test parabola-planning algo on SO3 joint + 1 transl DOF.

from hpp.corbaserver.monopod import Robot
from hpp.corbaserver import Client
from hpp.corbaserver import ProblemSolver
from viewer_display_library import normalizeDir, plotCone, plotFrame, plotThetaPlane, shootNormPlot, plotStraightLine, plotConeWaypoints, plotSampleSubPath, contactPosition
from parseLog import parseConfig, parseNodes, parseIntersectionConePlane, parseAlphaAngles
from parabola_plot_tools import parabPlotDoubleProjCones, parabPlotOriginCones
import math
import numpy as np
Pi = math.pi

robot = Robot ('robot')
#robot.setJointBounds('base_joint_xyz', [-6, 6.9, -2.5, 3.2, 0, 8]) # ultimate goal!
#robot.setJointBounds('base_joint_xyz', [1.6, 6.9, -2.2, 1.5, 0, 3]) # first goal
#robot.setJointBounds('base_joint_xyz', [-0.3, 6.9, -2.2, 2.4, 0, 3]) # second goal
#robot.setJointBounds('base_joint_xyz', [-2.6, 6.9, -2.2, 2.4, 0, 3]) # third goal
robot.setJointBounds('base_joint_xyz', [-6, 6.9, -2.8, 3.2, 0, 3]) # start to bottom
#robot.setJointBounds('base_joint_xyz', [-6, -2.2, -2.4, 3, 0, 8]) # bottom to ultimate
#robot.setJointBounds('base_joint_xyz', [-5, -2.2, -0.1, 2.8, 0, 6]) # bottom to middle column
#robot.setJointBounds('base_joint_xyz', [-5, -2.2, -0.1, 2.8, 0, 3]) # bottom to bottom 1
#robot.setJointBounds('base_joint_xyz', [-6, 6.9, -2.5, 3.2, 0, 3]) # first to bottom

ps = ProblemSolver (robot)
cl = robot.client
#cl.obstacle.loadObstacleModel('animals_description','inclined_plane_3d','inclined_plane_3d')

from hpp.gepetto import Viewer, PathPlayer
r = Viewer (ps)
pp = PathPlayer (robot.client, r)
r.loadObstacleModel ("animals_description","scene_jump_harder","scene_jump_harder")

# Configs : [x, y, z, q1, q2, q3, q4, dir.x, dir.y, dir.z, theta]
r([0, 0, 0, 1, 0, 0, 0, -0.1, 0, 0, 1, 0])
q11 = [6.4, 0.5, 0.8, 0, 0, 0, 1, -0.1, 0, 0, 1, 0] # start
#q11 = [-3.5, 1.7, 0.4, 0, 0, 0, 1, 0, 0, 1, Pi] # bottom of column
r(q11)
#q22 = [2.6, -1.4, 0.35, 0, 0, 0, 1, 0, 0, 1, Pi] # first plateform
#q22 = [0.7, 1.55, 0.4, 0, 0, 0, 1, 0, 0, 1, Pi] # second plateform
#q22 = [-1.7, -1.5, 0.4, 0, 0, 0, 1, 0, 0, 1, Pi] # third plateform
q22 = [-3.5, 1.7, 0.4, 0, 0, 0, 1, 0, 0, 1, Pi] # bottom of column
#q22 = [-3.3, 1.5, 3.4, 0, 0, 0, 1, 0, 0, 1, Pi] # in column
#q22 = [-4.2, 0.9, 1.7, 0, 0, 0, 1, 0, 0, 1, Pi] # bottom 1 of column
#q22 = [-4.4, 0.9, 4.1, 0, 0, 0, 1, 0, 0, 1, Pi] # bottom 3 of column
#q22 = [-4.4, -1.8, 6.5, 0, 0, 0, 1, 0, 0, 1, Pi] # ultimate goal!
r(q22)


q1 = cl.robot.projectOnObstacle (q11, 0.001); q2 = cl.robot.projectOnObstacle (q22, 0.001)

ps.setInitialConfig (q1); ps.addGoalConfig (q2)
ps.solve ()

samples = plotSampleSubPath (cl, r, 0, 20, "curvy", [0,0,1,1])

samples2 = plotSampleSubPath (cl, r, 2, 20, "curvy2", [0,0.4,0.7,1])

#ps.saveRoadmap ('/local/mcampana/devel/hpp/data/PARAB_envir3d_with_window.rdm')
r.client.gui.setVisibility('robot/l_bounding_sphere',"OFF")

# DRAFT return contact position:
qConeContact = contactPosition (q22, cl, r)

q0 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, Pi]
r(ps.configAtParam(0,0.001))
ps.pathLength(0)
wp = ps.getWaypoints (0)
cl.problem.generateValidConfig(2)
r.client.gui.setVisibility('robot/l_bounding_sphere',"OFF")

# Get projected random configs CONES and display them
num_log = 7308
qrands = parseConfig(num_log,'INFO:/local/mcampana/devel/hpp/src/hpp-core/src/parabola/parabola-planner.cc:157: q_proj: ')
sphereNamePrefix="qrand_sphere_"
for i in range(0,len(qrands)):
    qrand = qrands[i]
    coneName = sphereNamePrefix+str(i)
    plotCone (qrand, cl, r, coneNameSufffix, "friction_cone2")

r.client.gui.refresh ()


## 3D Plot tools ##
q0 = [0, 0, 5, 0, 0, 0, 1, 0, 0, 1, 0];
r(q0)

plotFrame (r, "frame", [0,0,0], 0.5)

plotCone (q, cl, r, "yep", "friction_cone2")
plotConeWaypoints (cl, 0, r, "wp", "friction_cone2")

plotThetaPlane (q1, q2, r, "ThetaPlane")
r.client.gui.removeFromGroup ("ThetaPlane", r.sceneName)
r.client.gui.removeFromGroup ("ThetaPlanebis", r.sceneName)

#plotCone (q1, cl, r, 0.5, 0.4, "c1"); plotCone (q2, cl, r, 0.5, 0.4, "c2")

index = cl.robot.getConfigSize () - cl.robot.getExtraConfigSize ()
q = q2[::]
plotStraightLine ([q [index],q [index+1],q [index+2]], q, r, "normale2")


## Plot all cone waypoints:
#plotConeWaypoints (cl, 0, r, 0.5, 0.4, "wpcones")
wp = cl.problem.getWaypoints (0)
for i in np.arange(0, len(wp), 1):
    qCone = cl.robot.setOrientation (wp[i])
    coneName = "wp_cone_"+str(i)
    r.loadObstacleModel ("animals_description","friction_cone",coneName)
    r.client.gui.applyConfiguration (coneName, qCone[0:7])
    r.client.gui.refresh ()


## Plot ONE cone-planeTheta intersection:
num_log = 3533
configs, theta_vector, xPlus_vector, xMinus_vector, zPlus_vector, zMinus_vector = parseIntersectionConePlane (num_log,'220: theta: ', '544: q: ', '545: x_plus: ', '546: x_minus: ', '547: z_x_plus: ', '548: z_x_minus: ', 11)
i = 0
plotStraightLine ([xPlus_vector[i], xPlus_vector[i]*math.tan(theta_vector[i]), zPlus_vector[i]], q11, r, "inter1")
plotStraightLine ([xMinus_vector[i], xMinus_vector[i]*math.tan(theta_vector[i]), zMinus_vector[i]], q11, r, "inter2")

i = 1
plotStraightLine ([xPlus_vector[i], xPlus_vector[i]*math.tan(theta_vector[i]), zPlus_vector[i]], q22, r, "inter33")
plotStraightLine ([xMinus_vector[i], xMinus_vector[i]*math.tan(theta_vector[i]), zMinus_vector[i]], q22, r, "inter44")
#r.client.gui.removeFromGroup ("inter2"+"straight", r.sceneName)


## Plot all cone-planeTheta intersections:
num_log = 7308
configs, theta_vector, xPlus_vector, xMinus_vector, zPlus_vector, zMinus_vector = parseIntersectionConePlane (num_log,'222: theta: ', '549: q: ', '550: x_plus: ', '551: x_minus: ', '552: z_x_plus: ', '553: z_x_minus: ', 11)
len(xPlus_vector)
for i in range(0,len(xPlus_vector)/4):
    plotStraightLine ([xPlus_vector[i], xPlus_vector[i]*math.tan(theta_vector[i]), zPlus_vector[i]], configs[i], r, "inter"+str(i))




## 2D Plot tools ##

import matplotlib.pyplot as plt
theta = math.atan2((q2 [1] - q1 [1]) , (q2 [0] - q1 [0]))
index = cl.robot.getConfigSize () - 3
NconeOne = [q1 [index]*math.cos(theta) + q1 [index+1]*math.sin(theta), q1 [index+2]]
pointsConeOne = [q1 [0]*math.cos(theta) + q1 [1]*math.sin(theta), q1 [2], xPlus_vector[0]*math.cos(theta) + xPlus_vector[0]*tanTheta*math.sin(theta), zPlus_vector[0], xMinus_vector[0]*math.cos(theta) + xMinus_vector[0]*tanTheta*math.sin(theta), zMinus_vector[0]]

NconeTwo = [q2 [index]*math.cos(theta) + q2 [index+1]*math.sin(theta), q2 [index+2]]
pointsConeTwo = [q2 [0]*math.cos(theta) + q2 [1]*math.sin(theta), q2 [2], xPlus_vector[1]*math.cos(theta) + xPlus_vector[1]*tanTheta*math.sin(theta), zPlus_vector[1], xMinus_vector[1]*math.cos(theta) + xMinus_vector[1]*tanTheta*math.sin(theta), zMinus_vector[1]]

parabPlotDoubleProjCones (cl, 0, theta, NconeOne, pointsConeOne, NconeTwo, pointsConeTwo, plt)

plt.show()


angles = parseAlphaAngles (num_log, '285: alpha_0_min: ', '286: alpha_0_max: ', '303: alpha_lim_minus: ', '302: alpha_lim_plus: ', '317: alpha_imp_inf: ', '318: alpha_imp_sup: ', '290: alpha_inf4: ')

i = 0
parabPlotOriginCones (cl, 0, theta, NconeOne, pointsConeOne, angles, i, 0.6, plt)
plt.show()

# --------------------------------------------------------------------#

## Add light to scene ##
lightName = "li3"
r.client.gui.addLight (lightName, r.windowId, 0.001, [0.5,0.5,0.5,1])
r.client.gui.addToGroup (lightName, r.sceneName)
#r.client.gui.applyConfiguration (lightName, [6,0,0.5,1,0,0,0])
#r.client.gui.applyConfiguration (lightName, [4.5,-3,1,1,0,0,0])
r.client.gui.applyConfiguration (lightName, [-4,-1,3,1,0,0,0])
r.client.gui.refresh ()
#r.client.gui.removeFromGroup (lightName, r.sceneName)

# --------------------------------------------------------------------#
## Video capture ##
import time
pp.dt = 0.02; r(q1)
r.startCapture ("capture","png")
r(q1); time.sleep(0.2)
#pp(1)
r(q2); time.sleep(1)
r.stopCapture ()

## ffmpeg commands
ffmpeg -r 50 -i capture_0_%d.png -r 25 -vcodec libx264 video.mp4
x=0; for i in *png; do counter=$(printf %04d $x); ln "$i" new"$counter".png; x=$(($x+1)); done
ffmpeg -r 50 -i new%04d.png -r 25 -vcodec libx264 video.mp4
mencoder video.mp4 -channels 6 -ovc xvid -xvidencopts fixed_quant=4 -vf harddup -oac pcm -o video.avi
ffmpeg -i untitled.mp4 -vcodec libx264 -crf 24 video.mp4

# --------------------------------------------------------------------#

## Export to Blender ##
r.client.gui.writeNodeFile(0, 'scene.osg')
# osgconvd -O NoExtras scene.osg scene.dae
from hpp.gepetto.blender.exportmotion import exportStates, exportPath
exportPath(r, cl.robot, cl.problem, 0, 1, 'path2.txt')
exportStates(r, cl.robot, q11, 'configs.txt')
from gepettoimport import loadmotion
loadmotion('/local/mcampana/devel/hpp/videos/path2.txt') # and rename first node manually ...

# --------------------------------------------------------------------#
## DEBUG commands
cl.obstacle.getObstaclePosition('decor_base')
robot.isConfigValid(q1)
robot.setCurrentConfig(q1)
res=robot.distancesToCollision()
r( ps.configAtParam(0,5) )
ps.optimizePath (0)
ps.clearRoadmap ()
ps.resetGoalConfigs ()
from numpy import *
argmin(robot.distancesToCollision()[0])
robot.getJointNames ()
robot.getConfigSize ()
r.client.gui.getNodeList()



# Plot a sphere (dot)
[-4.363806586625437, -1.6379223704051435, 6.388551003534305]
[-4.255931854248047, -1.1548488140106201, 6.0563764572143555]

sphereNamePrefix="sdg2"
sphereName = sphereNamePrefix
r.client.gui.addSphere (sphereName,0.01,[0,0.5,0.5,1]) # grey
r.client.gui.applyConfiguration (sphereName, [-4.1308336459234205, 0.6935200067554956, 3.943446921479487,1,0,0,0])
r.client.gui.addToGroup (sphereName, r.sceneName)
r.client.gui.refresh ()


