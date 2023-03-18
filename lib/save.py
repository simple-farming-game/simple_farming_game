import json
import pygame
from typing import Union

from lib import farm
from lib import runtime_values
from lib import logger
from lib.farm import plants_list
from lib.plants import carrots, rice, sunFlower, tomato


def write_save():
    tile_map = [[]]
    players = []
    for x_index, line in enumerate(farm.tile_map):
        for y_index, tile in enumerate(line):
            tile_data: dict[str, Union[str,
                                       dict[str, Union[int, bool, str]]]] = {}
            if tile in farm.Tiles:
                tile_data["type_of_tile"] = "farm"
                tile_data["tile_name"] = tile.name
            elif isinstance(tile, plants_list.plants_list):  # type: ignore
                tile_data["type_of_tile"] = "plant"
                tile_data["plants_data"] = {
                    "name": tile.name,
                    "growCount": tile.growCount,  # type: ignore
                    "age": tile.age,  # type: ignore
                    "watered": tile.watered,  # type: ignore
                    "rotCount": tile.rotCount  # type: ignore
                }

            tile_map[x_index][y_index] = tile_data
    players = []
    for player in runtime_values.players:
        player_data = {
            "pos_x": player.pos.x,
            "pos_y": player.pos.y,
            "inventory": player.inventory
        }
        players.append(player_data)

    with open("save.sfgsave", "w") as save:
        save.write(json.dumps({
            "version": runtime_values.version,
            "tiles": tile_map,
            "player_data": players
        }))
    logger.log_info("저장")


def import_save(screen: pygame.Surface) -> bool:
    # import save
    saveData = {}
    try:
        with open("save.sfgsave", "r") as saveFile:
            saveData = json.load(saveFile)
    except:
        logger.log_info("불러오기 실패: 파일 불러오기 실패.")
        return False

    # check version
    version: runtime_values.version_type
    try:
        version = saveData["version"]
    except KeyError:
        return False  # 1.x 로드 지원 포기합니다.
    if runtime_values.version != version:
        return import_legacy_save(version, saveData)

    # alpha 2.1.5
    for x_index, line in enumerate(saveData["tiles"]):
        for y_index, tile in enumerate(line):
            if tile["type_of_tile"] == "farm":
                if tile["tile_name"] == "DIRT":
                    farm.tile_map[x_index][y_index] = farm.Tiles.DIRT
                elif tile["tile_name"] == "FARMLAND":
                    farm.tile_map[x_index][y_index] = farm.Tiles.FARMLAND
                elif tile["tile_name"] == "WATERED_FARMLAND":
                    farm.tile_map[x_index][y_index] = farm.Tiles.WATERED_FARMLAND
                else:
                    logger.log_critical(
                        f"Uncatched farm tile: {tile['tile_name']}")
                    logger.log_critical(f"locate_at: {x_index}, {y_index}")
                    logger.log_info(
                        "Please make an issue on github with version and save file.")
                    logger.save(runtime_values.start_time)
                    exit()
            elif tile["type_of_tile"] == "plant":
                plant: plants_list.plants_type
                pos = pygame.math.Vector2(
                    tile["plants_data"]["pos_x"],
                    tile["plants_data"]["pos_y"]
                )
                if tile["plants_data"]["name"] == "carrot":
                    plant = carrots.Carrots(pos, screen)
                elif tile["plants_data"]["name"] == "rice":
                    plant = rice.Rice(pos, screen)
                elif tile["plants_data"]["name"] == "sunFlower":
                    plant = sunFlower.SunFlower(pos, screen)
                elif tile["plants_data"]["name"] == "tomato":
                    plant = tomato.Tomato(pos, screen)
                else:
                    logger.log_critical(
                        f"Uncatched plant name: {tile['plants_data']['name']}")
                    logger.save(runtime_values.start_time)
                    exit()
                plant.growCount = tile['plants_data']['growCount']
                plant.age = tile['plants_data']['age']
                plant.watered = tile['plants_data']['watered']
                plant.rotCount = tile['plants_data']['rotCount']
                farm.tile_map[x_index][y_index] = plant
            else:
                logger.log_critical(
                    f"Uncatched tile: {tile['type_of_name']}")
                logger.log_critical(f"locate_at: {x_index}, {y_index}")
                exit()
    return True


def import_legacy_save(version: runtime_values.version_type, saveData) -> bool:
    # TODO: 버전코드 바꿀때 "꼭"!!! 추가할것!!!
    ...
