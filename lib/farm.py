from enum import Enum, auto
from typing import List, Union

import lib.plants.plants_list as plants_list


class Tiles(Enum):
    DIRT = auto()
    FARMLAND = auto()


tileMap: List[List[Union[Tiles, plants_list.plants_type]]] = [
    [Tiles.DIRT for _ in range(20)] for _ in range(30)]
