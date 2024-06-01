def buy(item):
    from lib.runtime_values import playerc
    from lib.runtime_values import logger

    if playerc.gold >= item.value.price:
        playerc.gold -= item.value.price
        playerc.add_item(item)
    else:
        logger.info("돈이 부족합니다.")
