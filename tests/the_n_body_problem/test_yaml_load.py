import os

import numpy as np
import numpy.testing as npt

from the_n_body_problem.objects import Body, System

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

def test_body_from_dict():
    body_data = {
        "Test Body": {
            "mass": 1.0,
            "pos": [1., 2., 3.],
            "vel": [4., 5., 6.],
            "colour": "black",
        }
    }
    body = Body.from_dict(body_data)

    assert isinstance(body, Body)
    assert body.mass == 1.
    npt.assert_array_equal(body.pos, np.array([1., 2., 3.]))
    npt.assert_array_equal(body.vel, np.array([4., 5., 6.]))
    assert body.colour == "black"
    assert body.path == []

def test_system_from_yaml():
    test_system = System.from_yaml(os.path.join(TEST_DIR, "data", "test_system_yaml.yaml"))

    assert isinstance(test_system, System)
    assert all([isinstance(b, Body) for b in test_system.bodies])

    test_body_a = test_system.bodies[0]
    test_body_b = test_system.bodies[1]
    
    assert test_body_a.mass == 1.
    npt.assert_array_equal(test_body_a.pos, np.array([1., 2., 3.]))
    npt.assert_array_equal(test_body_a.vel, np.array([4., 5., 6.]))
    assert test_body_a.colour == "black"

    assert test_body_b.mass == 2.
    npt.assert_array_equal(test_body_b.pos, np.array([2., 3., 4.]))
    npt.assert_array_equal(test_body_b.vel, np.array([5., 6., 7.]))
    assert test_body_b.colour == "white"