from enum import Enum, auto
from lib.crops.crops_item import CropsItems
from lib.blocks.blocks_item import BlocksItems
import json


class Items(Enum):
    HOE = auto()
    SICKLE = auto()
    NONE = auto()


class Item:
    def __init__(self, item: Items | CropsItems | BlocksItems, count: int) -> None:
        self.item = item
        self.count = count

    def __str__(self) -> str:
        return json.dumps({"name": self.item.name, "count": self.count})


item_name_list = [item.name for item in Items]
