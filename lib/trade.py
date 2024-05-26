from lib.crops.crops_item import CropsItems
from lib.blocks.blocks_item import BlocksItems
from lib.runtime_values import playerc
from lib.runtime_values import logger


def buy(item: CropsItems | BlocksItems):
    if playerc.gold >= item.value.price:
        playerc.gold -= item.value.price
        playerc.add_item(item)
    else:
        logger.info("돈이 부족합니다.")
