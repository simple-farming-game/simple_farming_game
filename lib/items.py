from enum import Enum, EnumMeta, auto

class Items(Enum):
    HOE = (auto(), "assets/img/items/hoe.png")
    SHOVEL = (auto(), "assets/img/items/shovel.png")
    SICKLE = (auto(), "assets/img/items/sickle.png")
    VITAMIN = (auto(), "assets/img/items/vitamin.png")
    WATER = (auto(), "assets/img/items/water.png")
    NONE = (auto(), "assets/img/items/none.png")

value_list = [[i.value[0] for i in Items],[i.value[1] for i in Items]]
value_name = [i.name for i in Items]
def get_value(name):
    return value_list[1][value_name.index(name)]