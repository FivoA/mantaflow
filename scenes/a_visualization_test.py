from manta import *
import math
import numpy as np
import os

save_path = "/home/fivo/Desktop/mfEvaluation/data"

boundary_condition = "no-slip" # "free-slip" or "no-slip"  // NOT WORKING YET: or "periodic" or "windowing"

res = 256
domain_size = 1.0
gs = vec3(res, res, res)
dim = 3
s = FluidSolver(name='test', gridSize=gs, dim=dim)

flags = s.create(FlagGrid)
vel = s.create(MACGrid)
pressure = s.create(RealGrid)
density  = s.create(RealGrid)

bWidth=1
flags.initDomain( boundaryWidth=bWidth )
flags.fillGrid()
if boundary_condition == "no-slip":
    setObstacleStick(flags=flags) # set the obstacles to be no-slip by setting them to be TypeStick

source = s.create(Cylinder, center=gs*vec3(0.5,0.1,0.5), radius=res*0.14, z=gs*vec3(0, 0.02, 0))

initTGVortex(vel=vel, domainSize=domain_size)


#3d numpy array 
npArray = np.ones( [res,res,res, 3], dtype=np.float32 )
#3d numpy density array
npDensityArray = np.ones( [res, res, res], dtype = np.float32)

if GUI:
    gui = Gui()
    gui.show()

for t in range(10000):
    mantaMsg('\nFrame %i' % (s.frame))

    if t<100:
        source.applyToGrid(grid=density, value=1)
		
    advectSemiLagrange(flags=flags, vel=vel, grid=vel, order=2)
    advectSemiLagrange(flags=flags, vel=vel, grid=density, order=2)    

    setWallBcs(flags=flags, vel=vel) #makes sure the velocity field moves in line with the boundary conditions at the walls
    solvePressure(flags=flags, vel=vel, pressure=pressure)

    setWallBcs(flags=flags, vel=vel) #makes sure the velocity field moves in line with the boundary conditions at the walls

    copyGridToArrayVec3(target=npArray, source=vel)
    copyGridToArrayReal(target=npDensityArray, source=density)

    if t % 100 == 0:
        np.save(os.path.join(save_path, "vel_%04d.npy" % t), npArray)
        np.save(os.path.join(save_path, "den_%04d.npy" % t), npDensityArray)

    s.step()