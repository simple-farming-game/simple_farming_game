import json
from typing import Tuple

from lib import farm
from lib import draw
from lib import window


def write_save():
    with open("save.sfgsave", "w") as save:
        save.write(json.dumps({
            "version": window.version,
            "tile": farm.tileMap,
            "player_data": window.players
        }))
    window.logs.info("저장")


def import_save() -> bool:
    # import save
    saveData = {}
    try:
        with open("save.sfgsave", "r") as saveFile:
            saveData = json.load(saveFile)
    except:
        window.logs.info("불러오기 실패: 파일 불러오기 실패.")
        return False

    # check version
    version: window.version_type
    try:
        version = saveData["version"]
    except KeyError:
        return import_legacy_save(("non", 0, 0, 0), saveData)
    if window.version != version:
        return import_legacy_save(version, saveData)

    # alpha 2.0.0
    farm.tileMap = saveData["tile"]
    window.players = saveData["player_data"]
    return True


def import_legacy_save(version: Tuple[str, int, int, int], saveData) -> bool:
    if version == ("non", 0, 0, 0):
        # alpha 1.1.1
        window.players[0].inventory = saveData["inv"]
        farm.tileMap = saveData["tile"]
        window.players[0].pos = saveData["pos"]
        draw.draw_ground(window.screen)
        window.logs.info("불러오기")
        return True
    else:
        return False
