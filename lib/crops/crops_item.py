from enum import Enum, auto
from lib.crops.rice import Rice

class CropsItems(Enum):
    RICE = Rice

crops_item_name_list = [item.name for item in CropsItems]
crops_item_name_list_lower = [item.name.lower() for item in CropsItems]