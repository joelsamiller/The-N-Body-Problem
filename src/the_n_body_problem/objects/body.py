import numpy as np


class Body:
    def __init__(self, mass: float, pos: list[float], vel: list[float], colour: str):
        self.mass = mass
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.colour = colour
        self.path = []
    
    @classmethod
    def from_dict(cls, data):
        name = [*data][0]
        data = data[name]
        return cls(data["mass"], data["pos"], data["vel"], data["colour"])