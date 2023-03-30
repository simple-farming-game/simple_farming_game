import json
from typing import Tuple
import pygame

from lib import farm
from lib import draw
from lib import runtime_values
from lib.plants import plants_list



def write_save():
    with open("save.sfgsave", "w") as save:
        data = {
            "version": runtime_values.version,
            "tile": list(),
            "player_pos_x": runtime_values.players[0].pos.x,
            "player_pos_y": runtime_values.players[0].pos.y
        }
        data["tile"] = []
        count = 0
        for i in farm.tileMap:
            data["tile"].append(list())
            for j in range(len(i)):
                print(i[j].name)
                data["tile"][count].append(i[j].name)
            count += 1
        save.write(json.dumps(data))
    runtime_values.logs.info("저장")


def import_save() -> bool:
    # import save
    saveData = {}
    try:
        saveFile = open("save.sfgsave", "r", encoding='utf-8-sig')
        saveData = json.load(saveFile)
        saveFile.close()
        del saveFile
            
    except:
        runtime_values.logs.info("불러오기 실패: 파일 불러오기 실패.")
        return False

    # check version
    version: runtime_values.version_type
    version =  tuple(saveData["version"])
    # alpha 2.0.0
    farm.tileMap = []
    count = 0
    tempPos = [0,0]
    for i in saveData["tile"]:
        farm.tileMap.append(list())
        for j in i:
            try:
                #runtime_values.logs.info(f"import Tile : {j}")
                farm.tileMap[count].append(getattr(farm.Tiles, j))
            except:
                for pl in plants_list.plants_list:
                    if pl.name == j:
                        farm.tileMap[count].append(pl)
                        farm.tileMap[count][-1] = pl(pygame.math.Vector2(tempPos[0]*32,tempPos[1]*32), runtime_values.screen) # type: ignore
                        print(tempPos)
            tempPos[1]+=1
        count += 1           
        tempPos[1]=0
        tempPos[0]+=1
        
            
    runtime_values.players[0].pos.x = int(saveData["player_pos_x"])
    runtime_values.players[0].pos.y = int(saveData["player_pos_y"])
    runtime_values.logs.info("불러오기")
    del saveData
    return True


def import_legacy_save(version: Tuple[str, int, int, int], saveData) -> bool:
    if version == ("non", 0, 0, 0):
        # alpha 1.1.1
        runtime_values.players[0].inventory = saveData["inv"]
        farm.tileMap = saveData["tile"]
        runtime_values.players[0].pos = saveData["pos"]
        draw.draw_ground(runtime_values.screen)
        runtime_values.logs.info("불러오기")
        return True
    else:
        return False