import numpy as np

from .body import Body
from the_n_body_problem.physics import equations


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
        # Get the timestep
        dt = int(time[-1] / len(time))

        u = self.forward_euler(np.stack([pos, vel]), mass, dt, len(time))

        # Assign solutions for each body to its class
        for i, b in enumerate(self.bodies):
            b.path = u[:, 0, i, :]
            b.pos = u[-1, 0, i, :]

    @staticmethod
    def forward_euler(u0: np.ndarray, mass: np.ndarray, dt: int, Nt: int) -> np.ndarray:
        """
        Use the forward Euler method to solve the equations of motion for the system.

        Parameters:
            u0 (np.ndarray): Initial conditions array.
            mass (np.ndarray): 1 x N array containing the mass of each object.
            dt (int): The time step in seconds.
            Nt (int): The total number of time steps.

        Returns:
            np.ndarray: Nt x 2 x N x 3 array containing the positions and velocities of each object
                        at each time step, in the x, y and z directions.
        """
        u = np.zeros((Nt,) + u0.shape)
        u[0] = u0

        for k in range(Nt - 1):
            # Split positions and velocites into n x 3 arrays
            pos = u[k][0]
            vel = u[k][1]

            # Calculate accelerations
            acc = equations.gravitational_acceleration(mass, pos)

            # Update velocities and positions
            vel += dt * acc
            pos += dt * vel
            u[k + 1] = np.stack([pos, vel])

        return u
