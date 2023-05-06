from enum import Enum, EnumMeta, auto

class Items(Enum):
    HOE = (auto(), "assets/img/items/hoe.png")
    SHOVEL = (auto(), "assets/img/items/shovel.png")
    SICKLE = (auto(), "assets/img/items/sickle.png")
    VITAMIN = (auto(), "assets/img/items/vitamin.png")
    WATER = (auto(), "assets/img/items/water.png")
    NONE = (auto(), "assets/img/items/none.png")

print(Items.HOE.value[1])