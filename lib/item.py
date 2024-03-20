from enum import Enum, auto


class Items(Enum):
    HOE = auto()
    SICKLE = auto()
    NONE = auto()


item_name_list = [item.name for item in Items]
