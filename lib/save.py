import json
from typing import Tuple

from lib import farm
from lib import draw
from lib import runtime_values


def write_save():
    # Write the game's state to a file named "save.sfgsave".
    # The file is opened in write mode.
    with open("save.sfgsave", "w") as save:
        # Serialize the game state into a JSON string and write it to the file.
        save.write(json.dumps({
            "version": runtime_values.version,
            "tile": farm.tileMap,
            "player_data": runtime_values.players
        }))
    # Log a message indicating that the save operation was successful.
    runtime_values.logs.info("저장")


def import_save() -> bool:
    # Load the game state from the "save.sfgsave" file.
    saveData = {}
    try:
        with open("save.sfgsave", "r") as saveFile:
            saveData = json.load(saveFile)
    except:
        # Log an error message if the file could not be opened.
        runtime_values.logs.info("불러오기 실패: 파일 불러오기 실패.")
        return False

    # Check the version of the saved game data.
    version: runtime_values.version_type
    try:
        version = saveData["version"]
    except KeyError:
        # If the saved game data does not contain a version number, assume that it is from an earlier version of the game.
        # Attempt to import the save data as a legacy save.
        return import_legacy_save(("non", 0, 0, 0), saveData)
    if runtime_values.version != version:
        # If the version of the saved game data is different from the current version of the game,
        # attempt to import the save data as a legacy save.
        return import_legacy_save(version, saveData)

    # Import the game state from the saved game data.
    # This assumes that the saved game data is from the current version of the game (alpha 2.0.0).
    farm.tileMap = saveData["tile"]
    runtime_values.players = saveData["player_data"]
    return True


def import_legacy_save(version: Tuple[str, int, int, int], saveData) -> bool:
    if version == ("non", 0, 0, 0):
        # If the saved game data is from alpha 1.1.1,
        # import the game state from the saved game data and draw the ground.
        runtime_values.players[0].inventory = saveData["inv"]
        farm.tileMap = saveData["tile"]
        runtime_values.players[0].pos = saveData["pos"]
        draw.draw_ground(runtime_values.screen)
        # Log a message indicating that the save data was successfully imported.
        runtime_values.logs.info("불러오기")
        return True
    else:
        # If the saved game data is not from alpha 1.1.1 or the current version of the game,
        # return False to indicate that the save data could not be imported.
        return False
