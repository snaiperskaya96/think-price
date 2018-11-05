from enum import Enum

class ComponentType(Enum):
    SMD = 1
    THROUGH_HOLE = 2

class MountingSide(Enum):
    TOP = 1
    BOTTOM = 2

class BoardComponent:
    def __init__(self, name, type, side, pins):
        self.name = name
        self.type = type
        self.side = side
        self.end_of_pins = pins