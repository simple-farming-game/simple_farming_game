from enum import Enum, auto
from lib.blocks.shop import Shop


class BlocksItems(Enum):
    SHOP = Shop


blocks_item_name_list = [item.name for item in BlocksItems]
blocks_item_name_list_lower = [item.name.lower() for item in BlocksItems]
