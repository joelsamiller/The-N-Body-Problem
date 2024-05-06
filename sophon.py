from n_body_sim import Body, System
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sun_1 = Body(
    mass=2e30,
    pos=[-1.357584499428084E+06, 1.863360976396262E+05, 3.010543593011742E+04],
    vel=[-1.058798295143081E-03, -1.575049384459885E-02, 1.469211915537368E-04],
    colour='y',
)

sun_2 = Body(
    mass=2e30,
    pos=[-1.357584499428084E+09, 1.863360976396262E+09, 300.010543593011742E+04],
    vel=[-1.058798295143081E+00, -1.575049384459885E+00, 1.469211915537368E-04],
    colour='orange',
)

sun_3 = Body(
    mass=2e30,
    pos=[1.357584499428084E+09, -1.863360976396262E+09, -3.010543593011742E+04],
    vel=[-1.058798295143081E+00, 1.575049384459885E+00, 1.469211915537368E-04],
    colour='r',
)

santi_system = System([sun_1, sun_2, sun_3])

santi_system.solve(np.linspace(0, 3600*365*24*1000, 3600000))

np.save("santi_1000yrs.npy", santi_system.bodies)

paths=np.array([list(zip(*o.path)) for o in santi_system.bodies])
colours=[o.colour for o in santi_system.bodies]
fig = plt.figure()
for b in range(len(santi_system.bodies)):
    plt.plot(paths[b, 0, :], paths[b, 1, :], c=colours[b])
plt.scatter(paths[:, 0, -1], paths[:, 1, -1], c=colours)
plt.axis('equal')
plt.show()
