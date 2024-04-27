import numpy as np
from scipy.integrate import odeint

from .body import Body
from the_n_body_problem.physics import constants

class System:
    def __init__(self, bodies: list[Body]):
        self.bodies = bodies

    def solve(self, time: np.ndarray) -> None:
        # Reshape positions and velocities into a single 1D list for ODE solver
        pos = sum([list(b.pos) for b in self.bodies], [])
        vel = sum([list(b.vel) for b in self.bodies], [])
        pos_vel = pos + vel
        # Create a list of all body masses for solver
        mass = np.array([b.mass for b in self.bodies])

        # Define function to solve
        def newton(y, t, mass):
            # Reshape positions and velocites into a n x 3 array
            pos = np.array(y[0 : int(len(y) / 2)]).reshape((-1, 3))
            vel = np.array(y[int(len(y) / 2) : :]).reshape((-1, 3))
            # Calculate distance from each object to every other object
            dist = [[p2 - p1 for p2 in pos if all(p1 != p2)] for p1 in pos]
            # Calculate acceleration vector on each object
            acc = np.array(
                [
                    [
                        # Sum contributions from every body for each cardinal direction
                        sum(
                            constants.G
                            * m
                            * (dr[i] / np.sqrt(sum(d**2 for d in dr)) ** 3)
                            for dr, m in zip(
                                _dist, [m for m in mass[np.arange(len(mass)) != b]]
                            )
                        )
                        for i in range(3)
                    ]
                    # For every body in the system
                    for b, _dist in enumerate(dist)
                ]
            )
            # Flatten velocity and acceleration arrays and join as one list for output
            out = vel.ravel().tolist() + acc.ravel().tolist()
            return out

        # Solve ODE
        solution = odeint(newton, pos_vel, time, (mass,))
        # Assign solutions for each body to its class
        pos = [
            [solution[i][3 * j : 3 * (j + 1)] for i in range(len(time))]
            for j in range(len(self.bodies))
        ]
        for i, b in enumerate(self.bodies):
            b.path = pos[i]
            b.pos = pos[i][-1]
