from manta import *

res = 64
s = Solver(name='main', gridSize=vec3(res, res, 1), dim=2)

flags = s.create(FlagGrid)
vel = s.create(MACGrid)
pressure = s.create(RealGrid)

flags.initDomain()
flags.fillGrid()

if GUI:
     gui = Gui()
     gui.show()

for t in range(200):
    mantaMsg('\nFrame %i' % (s.frame))

    setWallBcs(flags=flags, vel=vel)
    solvePressure(flags=flags, vel=vel, pressure=pressure)
    s.step()
    solvePressure(flags=flags, vel=vel, pressure=pressure)

#my_vorticity = s.create(RealGrid)
#compute_my_vorticity( vel=vel, vorticity=my_vorticity)