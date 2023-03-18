import pygame

from lib import save
from lib.plants import plants_list
from lib.items import Items
from lib import runtime_values
from lib import farm
from lib import player
from lib import iteminfo
from lib import sell
from lib import help
from lib import logger
import random


def use():
    x, y = map(int, runtime_values.players[0].get_tile_pos())
    tile = farm.tile_map[x][y]
    logger.log_info("using item")
    logger.log_info(f"at  X:{x} Y:{y}")

    if runtime_values.players[0].handle_item in plants_list.plants_list:
        logger.log_info(
            f"Try to plant:{runtime_values.players[0].handle_item.name}")
        if runtime_values.players[0].plant_plant(runtime_values.screen):
            logger.log_info("success planting")
        else:
            logger.log_info("Fail planting")

    elif (runtime_values.players[0].handle_item == Items.HOE) and (tile == farm.Tiles.DIRT):  # 경작
        farm.tile_map[x][y] = farm.Tiles.FARMLAND
        logger.log_info("Hoe")

    elif (runtime_values.players[0].handle_item == Items.SICKLE):  # 낫
        if isinstance(tile, plants_list.plants_list):  # type: ignore
            runtime_values.players[0].farm_plant()
            logger.log_info(f"Sickle")

    elif (runtime_values.players[0].handle_item == Items.SHOVEL) and ((tile == farm.Tiles.FARMLAND)):  # 삽
        farm.tile_map[x][y] = farm.Tiles.DIRT
        logger.log_info(f"Shovel")
    elif runtime_values.players[0].handle_item == Items.NONE:
        pass

    elif (runtime_values.players[0].handle_item == Items.WATER):  # 물
        if isinstance(tile, plants_list.plants_list):  # type: ignore
            farm.tile_map[x][y].watered = True  # type: ignore
            logger.log_info("Warter")

    elif (runtime_values.players[0].handle_item == Items.VITAMIN):  # 비타민
        logger.log_info("Vitamin")
        if not isinstance(tile, plants_list.plants_list):  # type: ignore
            logger.log_info("Fail to using: tile is not a plant")
        elif not farm.tile_map[x][y].watered:  # type: ignore
            logger.log_info("Fail to using: plant is not watered")
        elif runtime_values.players[0].inventory["VITAMIN"] > 0:
            farm.tile_map[x][y].growCount += random.randint(  # type: ignore
                500, 1000)
            runtime_values.players[0].inventory["VITAMIN"] -= 1
        else:
            logger.log_info("Fail to using: Unhandled")

    else:
        logger.log_info("Fail to using: Unhandled")


def process():
    x, y = map(int, runtime_values.players[0].get_tile_pos())
    for event in pygame.event.get():
        moving(event)
        if event.type == pygame.QUIT:
            runtime_values.running = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_d: use()

                # group: change handle item
                case pygame.K_z:  # 선택 해제
                    runtime_values.players[0].handle_item = Items.NONE
                case pygame.K_r:  # 씨앗 선택
                    if runtime_values.players[0].handle_item in plants_list.plants_list:
                        if runtime_values.players[0].handle_item == plants_list.plants_list[-1]:
                            runtime_values.players[0].handle_item = plants_list.plants_list[0]
                        else:
                            runtime_values.players[0].handle_item = plants_list.next_plant(
                                runtime_values.players[0].handle_item)
                    else:
                        runtime_values.players[0].handle_item = plants_list.plants_list[0]
                case pygame.K_f:  # 괭이 선택
                    runtime_values.players[0].handle_item = Items.HOE
                case pygame.K_s:  # 삽 선택
                    runtime_values.players[0].handle_item = Items.SHOVEL
                case pygame.K_e:  # 낫 선택
                    runtime_values.players[0].handle_item = Items.SICKLE
                case pygame.K_w:  # 낫 선택
                    runtime_values.players[0].handle_item = Items.WATER
                case pygame.K_v:  # 비타민
                    runtime_values.players[0].handle_item = Items.VITAMIN

                case pygame.K_a:  # 판매
                    # type: ignore
                    sell.sell(runtime_values.players[0].handle_item)
                case pygame.K_b:  # 구매
                    # type: ignore
                    sell.buy(runtime_values.players[0].handle_item)

                # case pygame.K_b:  #  TODO:수확물 선택
                #     selectImg[0] = pygame.image.load("assets/img/rice.png")
                #     selectImg[1] = 5

                case pygame.K_SPACE:  # 달리기
                    runtime_values.players[0].speed = 4.5

                case pygame.K_t: save.write_save()
                case pygame.K_y: save.import_save(runtime_values.screen)

                # case pygame.K_0:  # TODO:cheat
                #     if int(input("dev code\n")) == 100000:
                #         playerClass.speed = 3
                #         playerClass.inventory = {
                #             "rice": 100000, "riceSeed": 100000, "gold": 100000}
                #         growCount = 5000

                case pygame.K_g:  # 아이템 정보보기
                    if runtime_values.players[0].handle_item in plants_list.plants_list or runtime_values.players[0].handle_item == Items.VITAMIN:
                        pygame.mouse.set_visible(True)
                        iteminfo.info(
                            runtime_values.players[0].handle_item.name, runtime_values.players[0].inventory[runtime_values.players[0].handle_item.name])
                    pygame.mouse.set_visible(False)
                case pygame.K_ESCAPE:  # 메뉴
                    if runtime_values.players[0].handle_item in plants_list.plants_list:
                        pygame.mouse.set_visible(True)
                        iteminfo.info(
                            runtime_values.players[0].handle_item.name, runtime_values.players[0].inventory[runtime_values.players[0].handle_item.name])
                    pygame.mouse.set_visible(False)
                case pygame.K_h:
                    help.help()
        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_SPACE:
                    runtime_values.players[0].speed = 3


def moving(event: pygame.event.Event):
    if event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_LEFT:
                if runtime_values.my_dir == player.Direction.STOP:
                    runtime_values.my_dir = player.Direction.LEFT
                if runtime_values.my_dir == player.Direction.UP:
                    runtime_values.my_dir = player.Direction.UP_LEFT
                if runtime_values.my_dir == player.Direction.DOWN:
                    runtime_values.my_dir = player.Direction.DOWN_LEFT
            case pygame.K_RIGHT:
                if runtime_values.my_dir == player.Direction.STOP:
                    runtime_values.my_dir = player.Direction.RIGHT
                if runtime_values.my_dir == player.Direction.UP:
                    runtime_values.my_dir = player.Direction.UP_RIGHT
                if runtime_values.my_dir == player.Direction.DOWN:
                    runtime_values.my_dir = player.Direction.DOWN_RIGHT
            case pygame.K_UP:
                if runtime_values.my_dir == player.Direction.STOP:
                    runtime_values.my_dir = player.Direction.UP
                if runtime_values.my_dir == player.Direction.LEFT:
                    runtime_values.my_dir = player.Direction.UP_LEFT
                if runtime_values.my_dir == player.Direction.RIGHT:
                    runtime_values.my_dir = player.Direction.UP_RIGHT
            case pygame.K_DOWN:
                if runtime_values.my_dir == player.Direction.STOP:
                    runtime_values.my_dir = player.Direction.DOWN
                if runtime_values.my_dir == player.Direction.LEFT:
                    runtime_values.my_dir = player.Direction.DOWN_LEFT
                if runtime_values.my_dir == player.Direction.RIGHT:
                    runtime_values.my_dir = player.Direction.DOWN_RIGHT
    if event.type == pygame.KEYUP:
        match event.key:
            case pygame.K_LEFT:
                if runtime_values.my_dir == player.Direction.LEFT:
                    runtime_values.my_dir = player.Direction.STOP
                if runtime_values.my_dir == player.Direction.UP_LEFT:
                    runtime_values.my_dir = player.Direction.UP
                if runtime_values.my_dir == player.Direction.DOWN_LEFT:
                    runtime_values.my_dir = player.Direction.DOWN
            case pygame.K_RIGHT:
                if runtime_values.my_dir == player.Direction.RIGHT:
                    runtime_values.my_dir = player.Direction.STOP
                if runtime_values.my_dir == player.Direction.UP_RIGHT:
                    runtime_values.my_dir = player.Direction.UP
                if runtime_values.my_dir == player.Direction.DOWN_RIGHT:
                    runtime_values.my_dir = player.Direction.DOWN
            case pygame.K_UP:
                if runtime_values.my_dir == player.Direction.UP:
                    runtime_values.my_dir = player.Direction.STOP
                if runtime_values.my_dir == player.Direction.UP_LEFT:
                    runtime_values.my_dir = player.Direction.LEFT
                if runtime_values.my_dir == player.Direction.UP_RIGHT:
                    runtime_values.my_dir = player.Direction.RIGHT
            case pygame.K_DOWN:
                if runtime_values.my_dir == player.Direction.DOWN:
                    runtime_values.my_dir = player.Direction.STOP
                if runtime_values.my_dir == player.Direction.DOWN_LEFT:
                    runtime_values.my_dir = player.Direction.LEFT
                if runtime_values.my_dir == player.Direction.DOWN_RIGHT:
                    runtime_values.my_dir = player.Direction.RIGHT
