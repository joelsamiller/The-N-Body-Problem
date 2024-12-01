import numpy as np
from scipy.spatial import distance

from the_n_body_problem.physics import constants


def gravitational_acceleration(mass: np.ndarray, position: np.ndarray) -> np.ndarray:
    """
    For N objects, calculate the acceleration due to gravity on each object caused by every other object.

    Parameters:
        mass (np.ndarray): 1 x N array (vector) containing the masses of each object.
        position (np.ndarray): 3 x N array (matirx) containing the x, y and z coordinates of each object.
    Returns:
        np.ndarray: 3 x N array with the accelerations in the x, y and z direction for each object.
    """
    # Calculate distance from each object to every other object
    norm_dist = distance.cdist(position, position)  # ||x_i - x_j||
    vector_dist = position[:, None, :] - position  # x_i - x_j

    # Calculate accelerations
    inv_r3 = norm_dist**-3
    np.fill_diagonal(inv_r3, 0)  # Set acceleration to 0 for i=j
    Gr_r3 = -constants.G * vector_dist * inv_r3[:, :, None]  # Gr/||r||^3
    # Multiply by mass vector for each direction
    acceleration = np.array([Gr_r3[:, :, i] @ mass for i in range(3)]).T

    return acceleration
