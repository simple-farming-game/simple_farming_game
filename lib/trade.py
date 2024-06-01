def buy(item):
    from lib.runtime_values import playerc
    from lib.runtime_values import logger

    if playerc.gold >= item.value.price:
        playerc.gold -= item.value.price
        playerc.add_item(item, 1)
    else:
        logger.info("돈이 부족합니다.")


def sell(item):
    from lib.runtime_values import playerc
    from lib.runtime_values import logger

    is_sell_item = playerc.del_item(item)
    if is_sell_item:
        playerc.gold += item.value.price
    else:
        logger.info("아이템이 부족합니다.")
