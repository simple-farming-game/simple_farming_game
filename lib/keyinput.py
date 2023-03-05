import lib.save
from lib.plants import plants_list
from lib.items import Items
from lib import window
import lib.farm as farm
import lib.player as player
import pygame

# growCount = random.randint(0, 5)


def use():
    x, y = map(int, window.players[0].get_tile_pos())
    tile = farm.tileMap[x][y]
    if isinstance(window.players[0].handle_item, plants_list.plants_list):  # type: ignore
        window.players[0].plant_plant(window.screen)

    elif (window.players[0].handle_item == Items.HOE) and (tile == 1):  # 경작
        tile = farm.Tiles.FARMLAND
        window.logs.info(f"경작 : X:{y} Y:{x}")

    elif (window.players[0].handle_item == Items.SICKLE):
        if isinstance(tile, plants_list.plants_list):  # type: ignore
            window.players[0].farm_plant()
            window.logs.info(f"캐기 : X:{x} Y:{y}")

    elif (window.players[0].handle_item == Items.SHOVEL) and ((tile == farm.Tiles.FARMLAND)):  # 삽
        farm.tileMap[x][y] = farm.Tiles.DIRT
        window.logs.info(f"삽 : X:{x} Y:{y}")

    else:
        window.logs.info("실패")


dir = player.Direction.STOP


def process():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window.running = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                # group: moves
                case pygame.K_LEFT: dir = player.Direction.LEFT
                case pygame.K_RIGHT: dir = player.Direction.RIGHT
                case pygame.K_UP: dir = player.Direction.UP
                case pygame.K_DOWN: dir = player.Direction.DOWN

                case pygame.K_d: use()

                # group: change handle item
                case pygame.K_z:  # 선택 해제
                    window.players[0].handle_item = Items.NONE
                    # selectImg[0] = pygame.image.load("assets/img/none.png")
                    # selectImg[1] = 0
                case pygame.K_r:  # 씨앗 선택
                    if isinstance(window.players[0].handle_item,
                                  plants_list.plants_list):  # type: ignore

                        window.players[0].handle_item = plants_list.next_plant(
                            window.players[0].handle_item)  # type: ignore
                    else:
                        window.players[0].handle_item = plants_list.plants_list[0]

                    # selectImg[0] = pygame.image.load(
                    #     "assets/img/rice_seed.png")
                    # selectImg[1] = 1
                case pygame.K_f:  # 괭이 선택
                    window.players[0].handle_item = Items.HOE
                    # selectImg[0] = pygame.image.load("assets/img/hoe.png")
                    # selectImg[1] = 2
                case pygame.K_s:  # 삽 선택
                    window.players[0].handle_item = Items.SHOVEL
                    # selectImg[0] = pygame.image.load("assets/img/shovel.png")
                    # selectImg[1] = 3
                case pygame.K_e:  # 낫 선택
                    window.players[0].handle_item = Items.SICKLE
                    # selectImg[0] = pygame.image.load("assets/img/sickle.png")
                    # selectImg[1] = 4

                # case pygame.K_b:  #  TODO:수확물 선택
                #     selectImg[0] = pygame.image.load("assets/img/rice.png")
                #     selectImg[1] = 5

                case pygame.K_SPACE:  # 달리기
                    window.players[0].speed = 2.5
                case pygame.K_t:  lib.save.write_save()
                case pygame.K_y: lib.save.import_save()
                # case pygame.K_0:  # TODO:cheat
                #     if int(input("dev code\n")) == 20121029:
                #         playerClass.speed = 3
                #         playerClass.inventory = {
                #             "rice": 20121029, "riceSeed": 20121029, "gold": 20121029}
                #         growCount = 5000

        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_UP | pygame.K_DOWN | pygame.K_LEFT | pygame.K_RIGHT:
                    dir = player.Direction.STOP
                case pygame.K_SPACE:
                    window.players[0].speed = 1
