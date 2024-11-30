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
        name = [*data][0]
        data = data[name]
        return cls(data["mass"], data["pos"], data["vel"], data["colour"])
