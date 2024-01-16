from lib import farm
from lib.runtime_values import *
from lib.item import Items
from lib.item import item_name_list
from lib.crops.crops_item import CropsItems
from lib.crops.crops_item import crops_item_name_list
import json

def write_save():
    with open("save.sfgsave", "w") as save:
        data = {
            "tile": [],
            "player":{
                "gold":0,
                "inventory":[],
                "pos":[],
                "hendle_item":Items.NONE
                }
        }
        data["player"]["gold"] = playerc.gold
        row = []
        for item in playerc.inventory:
            if isinstance(item, Items):
                row.append(item.name)
            elif isinstance(item, CropsItems):
                row.append(item.name)
            else:
                logger.error("[인벤토리 저장하기] 알수 없는 아이템 감지됨.")
        data["player"]["inventory"] = row
        data["player"]["hendle_item"] = playerc.hendle_item.name
        data["player"]["pos"] = list(playerc.pos)
        
        for i in farm.tile_map:
            row = []  # Create a new row list for each iteration
            for j in i:
                row.append(j.name)  # Append the name of the Enum member
            data["tile"].append(row)  # Append the row to the "tile" list
        save.write(json.dumps(data))

def import_save():
    try:
        with open("save.sfgsave", "r") as save:
            logger.info("불러오기")
            data = json.loads(save.read())
            farm.tile_map = []
            for i in data["tile"]:
                row = []  # Create a new row list for each iteration
                for j in i:
                    row.append(getattr(farm.Tiles, j))  # Append the name of the Enum member
                    logger.debug(f"타일 불러옴: {j}")
                farm.tile_map.append(row)  # Append the row to the "tile" list   
            playerc.gold = data["player"]["gold"]
            row = []
            for item in data["player"]["inventory"]:
                if item in item_name_list:
                    for member in Items:
                        if member.name == item:
                            row.append(member)
                if item in crops_item_name_list:
                    for member in CropsItems:
                        if member.name == item:
                            row.append(member)
                else:
                    logger.error(f"[인벤토리 불러오기] 알수 없는 아이템 감지됨.: {item} 주의: 이 에러는 믿을수 없음.")
                
            playerc.inventory = row
            playerc.pos = pygame.Vector2(data["player"]["pos"])    
            if data["player"]["hendle_item"] in item_name_list:
                for member in Items:
                    if member.name == data["player"]["hendle_item"]:
                        playerc.hendle_item = member
            else:
                logger.error(f"[핸들 아이템 불러오기] 알수 없는 아이템 감지됨.: {data['player']['hendle_item']}")
                
        return True

    except (json.JSONDecodeError, ValueError) as e:
        # Handle the case when there's an issue decoding JSON, the file is not found, or the data is invalid
        logger.error(f"세이브를 불러오는 과정에서 오류가 발생했습니다!: {e}")
    except FileNotFoundError:return False
        

