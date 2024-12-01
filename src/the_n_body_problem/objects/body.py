import textwrap

import numpy as np
from typing import Self


class Body:
    def __init__(self, mass: float, pos: list[float], vel: list[float], colour: str):
        self.mass = float(mass)
        self.pos = np.array(pos).astype(float)
        self.vel = np.array(vel).astype(float)
        self.colour = colour
        self.path = []

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        if not isinstance(data, dict):
            raise TypeError("Argument passed to Body.from_dict() must be of type dict")

        if len(data) > 1:
            raise ValueError(
                textwrap.dedent(
                    """
                    Invalid dict format - dict must be of format,
                    {
                        "Body Name": {
                            "mass": float,
                            "pos": [float, float, float],
                            "vel": [float, float, float],
                            "colour": str,
                        }
                    }
                """
                )
            )

        name = [*data][0]
        data = data[name]

        if (
            missing_properties := {"mass", "pos", "vel", "colour"} - set(data)
        ) != set():
            raise ValueError(
                f"Body '{name}' missing required properties {missing_properties}"
            )

        return cls(data["mass"], data["pos"], data["vel"], data["colour"])
