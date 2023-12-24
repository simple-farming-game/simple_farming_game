from enum import Enum, auto

class Tiles(Enum):
    DIRT = auto()
    FARMLAND = auto()
    WATER_FARMLAND = auto()


tileMap: list[list[Tiles]] = [
    [Tiles.DIRT for _ in range(20)] for _ in range(30)
]