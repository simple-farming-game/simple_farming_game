import pygame

import lib.save
from lib.plants import plants_list
from lib.items import Items
from lib import runtime_values
from lib import farm
from lib import player


def use():
    x, y = map(int, runtime_values.players[0].get_tile_pos())
    tile = farm.tileMap[x][y]
    if runtime_values.players[0].handle_item in plants_list.plants_list:
        runtime_values.logs.info(
            f"심기 : X:{x} Y:{y} 작물:{runtime_values.players[0].handle_item.name}")
        runtime_values.players[0].plant_plant(runtime_values.screen)

    elif (runtime_values.players[0].handle_item == Items.HOE) and (tile == farm.Tiles.DIRT):  # 경작
        farm.tileMap[x][y] = farm.Tiles.FARMLAND
        runtime_values.logs.info(f"경작 : X:{y} Y:{x}")

    elif (runtime_values.players[0].handle_item == Items.SICKLE):
        if isinstance(tile, plants_list.plants_list):  # type: ignore
            runtime_values.players[0].farm_plant()
            runtime_values.logs.info(f"캐기 : X:{x} Y:{y}")

    elif (runtime_values.players[0].handle_item == Items.SHOVEL) and ((tile == farm.Tiles.FARMLAND)):  # 삽
        farm.tileMap[x][y] = farm.Tiles.DIRT
        runtime_values.logs.info(f"삽 : X:{x} Y:{y}")
    elif runtime_values.players[0].handle_item == Items.NONE:
        pass
    else:
        runtime_values.logs.info("사용 실패: 일치하는 아이템이 없습니다.")


def process():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runtime_values.running = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                # group: moves
                case pygame.K_LEFT:
                    runtime_values.my_dir = player.Direction.LEFT
                case pygame.K_RIGHT:
                    runtime_values.my_dir = player.Direction.RIGHT
                case pygame.K_UP:
                    runtime_values.my_dir = player.Direction.UP
                case pygame.K_DOWN:
                    runtime_values.my_dir = player.Direction.DOWN

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
                # case pygame.K_b:  #  TODO:수확물 선택
                #     selectImg[0] = pygame.image.load("assets/img/rice.png")
                #     selectImg[1] = 5

                case pygame.K_SPACE:  # 달리기
                    runtime_values.players[0].speed = 2.5

                # TODO: 저장기능 제대로 구현할것.
                # case pygame.K_t: lib.save.write_save()
                # case pygame.K_y: lib.save.import_save()

                # case pygame.K_0:  # TODO:cheat
                #     if int(input("dev code\n")) == 20121029:
                #         playerClass.speed = 3
                #         playerClass.inventory = {
                #             "rice": 20121029, "riceSeed": 20121029, "gold": 20121029}
                #         growCount = 5000

        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_UP | pygame.K_DOWN | pygame.K_LEFT | pygame.K_RIGHT:
                    runtime_values.my_dir = player.Direction.STOP
                case pygame.K_SPACE:
                    runtime_values.players[0].speed = 1
