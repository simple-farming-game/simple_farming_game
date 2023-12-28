from enum import Enum, auto

class Items(Enum):
    HOE = auto()
    NONE = auto()

item_name_list = [item.name for item in Items]