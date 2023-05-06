from enum import Enum, auto
from lib.plants import plants_list
from lib.block import block_list


class Items:
    HOE = auto()
    SHOVEL = auto()
    SICKLE = auto()
    VITAMIN = auto()
    WATER = auto()
    NONE = auto()
    
for i in plants_list.plants_list:
    exec(f"Items.{i.name.upper()} = auto()")
for i in block_list.block_list:
    exec(f"Items.{i.name.upper()} = auto()")

print(list(Items.__dict__.keys()))