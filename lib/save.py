import json
from typing import Tuple

from lib import farm
from lib import draw
from lib import runtime_values



def write_save():
    with open("save.sfgsave", "w") as save:
        data = {
            "version": runtime_values.version,
            "tile": list(),
            "player_pos": [runtime_values.players[0].pos.x, runtime_values.players[0].pos.y]
        }
        data["tile"] = []
        for i in farm.tileMap:
            for j in range(len(i)):
                print(i[j].name)
                data["tile"].append(i[j].name)
        print(data)
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
    print(runtime_values.version != version)
    # alpha 2.0.0
    saveData["tile"] = []
    for i in saveData["tile"]:
        saveData["tile"].append(list(map(lambda x: farm.Tiles[x], saveData["tile"][i])))
    saveData["player_pos"] = json.loads(saveData["player_pos"])
    print(saveData["player_pos"])
    runtime_values.players[0].pos.x = saveData["player_pos"][0]
    runtime_values.players[0].pos.y = saveData["player_pos"][1]
    runtime_values.logs.info("성공!")
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