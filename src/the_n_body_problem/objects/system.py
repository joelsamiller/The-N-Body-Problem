import numpy as np
from scipy.spatial import distance
from scipy.integrate import odeint

from .body import Body
from the_n_body_problem.physics import constants


class System:
    def __init__(self, bodies: list[Body]):
        self.bodies = bodies
        self.n = len(bodies)

    def solve(self, time: np.ndarray) -> None:
        # Create position, velocity and u arrays
        pos = np.stack([b.pos for b in self.bodies])
        vel = np.stack([b.vel for b in self.bodies])
        # Create a list of all body masses for solver
        mass = np.array([b.mass for b in self.bodies])
        dt = int(time[-1] / len(time))

        u = np.zeros((len(time) + 1, 2, self.n, 3))
        u[0] = np.stack([pos, vel])
        for k, _ in enumerate(time):
            # Split positions and velocites into n x 3 arrays
            pos = u[k][0]
            vel = u[k][1]
            
            # Calculate distance from each object to every other object
            norm_dist = distance.cdist(pos, pos)  # ||x_i - x_j||
            vector_dist = pos[:, None, :] - pos  # x_i - x_j
            
            # Calculate accelerations
            inv_r3 = norm_dist**-3
            np.fill_diagonal(inv_r3, 0)  # Set acceleration to 0 for i=j
            Gr_r3 = -constants.G * vector_dist * inv_r3[:, :, None]  # Gr/||r||^3
            # Multiply by mass vector for each direction
            acc = np.array([Gr_r3[:, :, i] @ mass for i in range(3)]).T
            
            # Join velocities and accelerations and return
            vel += dt * acc
            pos += dt * vel
            u[k + 1] = np.stack([pos, vel])

        # Assign solutions for each body to its class
        for i, b in enumerate(self.bodies):
            b.path = u[:, 0, i, :]
            b.pos = u[-1, 0, i, :]
