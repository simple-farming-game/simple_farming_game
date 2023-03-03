from enum import Enum, auto
from typing import List, Union

from plants.plants_data import Plants_type


class Tiles(Enum):
    DIRT = auto()
    FARMLAND = auto()


tileMap: List[List[Union[Tiles, Plants_type]]] = [
    [Tiles.DIRT for _ in range(30)] for _ in range(20)]
