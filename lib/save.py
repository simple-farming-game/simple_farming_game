import json
from typing import Tuple

from lib import farm
from lib import draw
from lib import runtime_values


def write_save():
    with open("save.sfgsave", "w") as save:
        save.write(json.dumps({
            "version": f"{runtime_values.version}",
            "tile": f"{farm.tileMap}",
            "player_data": f"{runtime_values.players}"
        }))
    runtime_values.logs.info("저장")


def import_save() -> bool:
    # import save
    saveData = {}
    try:
        with open("save.sfgsave", "r") as saveFile:
            saveData = json.load(saveFile)
            
    except:
        runtime_values.logs.info("불러오기 실패: 파일 불러오기 실패.")
        return False

    # check version
    version: runtime_values.version_type
    version =  tuple(saveData["version"])
    print(runtime_values.version != version)

    # alpha 2.0.0
    farm.tileMap = saveData["tile"]
    runtime_values.players = saveData["player_data"]
    runtime_values.logs.info("성공!")
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