from enum import Enum, auto
from typing import List, Union
from lib.crops.Crops import Crops

class Tiles(Enum):
    DIRT = auto()
    FARMLAND = auto()
    WATER_FARMLAND = auto()
tile_name_list = [item.name for item in Tiles]

tile_map: List[List[Union[Tiles, Crops]]] = [
    [Tiles.DIRT for _ in range(20)] for _ in range(30)
]