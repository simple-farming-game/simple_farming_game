from lib import farm
from lib.runtime_values import *
import json

def write_save():
    with open("save.sfgsave", "w") as save:
        data = {
            "tile": [],
            "player":{"gold":0,"inventory":[],"pos":[]}
        }
        data["player"]["gold"] = playerc.gold
        data["player"]["inventory"] = playerc.inventory
        data["player"]["pos"] = list(playerc.pos)
        
        for i in farm.tileMap:
            row = []  # Create a new row list for each iteration
            for j in i:
                row.append(j.name)  # Append the name of the Enum member
            data["tile"].append(row)  # Append the row to the "tile" list
        save.write(json.dumps(data))

def import_save():
    try:
        with open("save.sfgsave", "r") as save:
            data = json.loads(save.read())
            farm.tileMap = []
            for i in data["tile"]:
                row = []  # Create a new row list for each iteration
                for j in i:
                    row.append(getattr(farm.Tiles, j))  # Append the name of the Enum member
                farm.tileMap.append(row)  # Append the row to the "tile" list   
            playerc.gold = data["player"]["gold"]
            playerc.inventory = data["player"]["inventory"]
            playerc.pos = pygame.Vector2(data["player"]["pos"])     

    except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
        # Handle the case when there's an issue decoding JSON, the file is not found, or the data is invalid
        print(f"Error importing save: {e}")

