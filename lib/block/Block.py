from . import block_list
from ..plants import plants_list

class Box:
    # 겟수, 아이템 or 블록 or 식물
    item: dict[int, block_list.block_type or plants_list.plants_type]