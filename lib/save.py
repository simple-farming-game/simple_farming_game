import json
from typing import Tuple

from lib import farm
from lib import draw
from lib import runtime_values


def write_save():
    with open("save.sfgsave", "w") as save:
        save.write(json.dumps({
            "version": "runtime_values.version",
            "tile": "farm.tileMap",
            "player_data": "runtime_values.players"
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
    try:
        version = saveData["version"]
    except KeyError:
        return import_legacy_save(("non", 0, 0, 0), saveData)
    if runtime_values.version != version:
        return import_legacy_save(version, saveData)

    # alpha 2.0.0
    farm.tileMap = saveData["tile"]
    runtime_values.players = saveData["player_data"]
    return True


def import_legacy_save(version: Tuple[str, int, int, int], saveData) -> bool:
    if version == ("non", 0, 0, 0):
        # alpha 1.1.1
        exec("%s = %d" % (saveData["inv"],saveData["inv"]))
        exec("%s = %d" % (saveData["tile"],saveData["tile"]))
        exec("%s = %d" % (saveData["pos"],saveData["pos"]))
        runtime_values.players[0].inventory = saveData["inv"]
        farm.tileMap = saveData["tile"]
        runtime_values.players[0].pos = saveData["pos"]
        draw.draw_ground(runtime_values.screen)
        runtime_values.logs.info("불러오기")
        return True
    else:
        return False