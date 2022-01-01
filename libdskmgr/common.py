from enum import Enum
from typing import NamedTuple

class Location(NamedTuple):
    x: int
    y: int

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
