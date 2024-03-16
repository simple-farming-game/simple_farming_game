from lib import farm
from lib.crops.crops_item import crops_item_name_list_lower
from lib.crops.crops_item import crops_item_name_list
from lib.crops.crops_item import CropsItems
from lib.crops.Crops import Crops
from lib.runtime_values import *
from lib.funcs import *
from lib.item import Items
from lib.item import item_name_list
import json
from pygame import Vector2


def write_save():
    with open("save.sfgsave", "w") as save:
        data = {
            "tile": [],
            "player": {
                "gold": 0,
                "inventory": [],
                "pos": [],
                "handle_item": Items.NONE,
            },
        }

        for line in farm.tile_map:
            row = []
            for tile in line:
                if isinstance(tile, Crops):
                    row.append(to_json(tile))
                else:
                    row.append(tile.name)
            data["tile"].append(row)

        for item in playerc.inventory:
            data["player"]["inventory"].append(item.name)

        data["player"]["handle_item"] = playerc.handle_item.name
        data["player"]["pos"] = list(playerc.pos)
        data["player"]["gold"] = playerc.gold

        save.write(json.dumps(data))


def import_save():
    # tile
    # player(gold, inventory, pos, handle_item)
    try:
        with open("save.sfgsave", "r") as save:
            logger.info("불러오기")
            data = json.loads(save.read())
        farm.tile_map = []
        tile_pos = Vector2(0, 0)
        for line in data["tile"]:
            row = []
            for tile in line:
                if tile in farm.tile_name_list:
                    row.append(getattr(farm.Tiles, tile))
                elif json.loads(tile)["name"] in crops_item_name_list_lower:
                    row.append(
                        getattr(CropsItems, json.loads(tile)["name"].upper()).value(
                            tile_pos,
                            screen,
                            json.loads(tile)["age"],
                            json.loads(tile)["age_count"],
                        )
                    )

                else:
                    logger.error(f"[타일맵] 알수없는 아이템 감지됨.: {tile}")
                tile_pos.y += 1
            farm.tile_map.append(row)
            tile_pos.x += 1
            tile_pos.y = 0

        playerc.gold = data["player"]["gold"]
        playerc.pos = pygame.Vector2(data["player"]["pos"])

        for item in data["player"]["inventory"]:
            if item in crops_item_name_list:
                playerc.handle_item = getattr(CropsItems, item)
            elif item in item_name_list:
                playerc.handle_item = getattr(Items, item)
            else:
                logger.error(f"[인벤토리 불러오기] 알수없는 아이템 감지됨.: {item}")

        if data["player"]["handle_item"] in crops_item_name_list:
            playerc.handle_item = getattr(CropsItems, data["player"]["handle_item"])
        elif data["player"]["handle_item"] in item_name_list:
            playerc.handle_item = getattr(Items, data["player"]["handle_item"])
        else:
            logger.error(
                f"[핸들아이템 불러오기] 알수없는 아이템 감지됨.: {data['player']['handle_item']}"
            )

    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"세이브를 불러오는 과정에서 오류가 발생하였습니다.: {e}")
    except FileNotFoundError:
        return False
