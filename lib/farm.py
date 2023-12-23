from enum import Enum, auto
from typing import List

class Tiles(Enum):
    DIRT = auto()
    FARMLAND = auto()
    WATER_FARMLAND = auto()


tileMap: List[List[Tiles]] = [
    [Tiles.DIRT for _ in range(20)] for _ in range(30)
]
