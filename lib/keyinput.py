import pygame

import lib.save
from lib.plants import plants_list
from lib.items import Items
from lib import runtime_values
from lib import farm
from lib import player
from lib import sell
from lib import help
from lib.block import block_list
import random

def use():
    x, y = map(int, runtime_values.players[0].get_tile_pos())
    tile = farm.tileMap[x][y]
    runtime_values.logs.info("using item")
    runtime_values.logs.info(f"at  X:{x} Y:{y}")

    if runtime_values.players[0].handle_item in plants_list.plants_list:
        runtime_values.logs.info(
            f"Try to plant:{runtime_values.players[0].handle_item.name}")
        if runtime_values.players[0].plant_plant(runtime_values.screen):
            runtime_values.logs.info("success planting")
        else:
            runtime_values.logs.info("Fail planting")
    
    if runtime_values.players[0].handle_item in block_list.block_list:
        runtime_values.logs.info(
            f"Try to put:{runtime_values.players[0].handle_item.name}")
        if runtime_values.players[0].put_block(runtime_values.screen):
            runtime_values.logs.info("success put")
        else:
            runtime_values.logs.info("Fail put")
            
    elif (runtime_values.players[0].handle_item == Items.HOE) and (tile == farm.Tiles.DIRT):  # 경작
        farm.tileMap[x][y] = farm.Tiles.FARMLAND
        runtime_values.logs.info("Hoe")

    elif (runtime_values.players[0].handle_item == Items.SICKLE): # 낫
        if isinstance(tile, plants_list.plants_list):  # type: ignore
            runtime_values.players[0].farm_plant()
            runtime_values.logs.info(f"Sickle")

    elif (runtime_values.players[0].handle_item == Items.SHOVEL) and ((tile == farm.Tiles.FARMLAND)):  # 삽
        farm.tileMap[x][y] = farm.Tiles.DIRT
        runtime_values.logs.info(f"Shovel")
    elif runtime_values.players[0].handle_item == Items.NONE:
        pass

    elif (runtime_values.players[0].handle_item == Items.WATER) and (isinstance(tile, plants_list.plants_list)):  # 경작 # type: ignore
        farm.tileMap[x][y].water = True # type: ignore
        runtime_values.logs.info("Warter")

    elif (runtime_values.players[0].handle_item == Items.VITAMIN) and (isinstance(tile, plants_list.plants_list)):  # 경작 # type: ignore
        if farm.tileMap[x][y].water and runtime_values.players[0].inventory["VITAMIN"] > 0: # type: ignore
            farm.tileMap[x][y].growCount += random.randint(500,1000) # type: ignore
            runtime_values.players[0].inventory["VITAMIN"] -= 1
        else:runtime_values.logs.info("Fail to using")
        runtime_values.logs.info("Vitamin")

    else:
        runtime_values.logs.info("Fail to using")

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
                        
                case pygame.K_r:  # 씨앗 선택
                    if runtime_values.players[0].handle_item in plants_list.plants_list:
                        if runtime_values.players[0].handle_item == plants_list.plants_list[-1]:
                            runtime_values.players[0].handle_item = plants_list.plants_list[0]
                        else:
                            runtime_values.players[0].handle_item = plants_list.next_plant(
                                runtime_values.players[0].handle_item)
                    else:
                        runtime_values.players[0].handle_item = plants_list.plants_list[0]
                
                case pygame.K_m:  # 블록 선택
                    if runtime_values.players[0].handle_item in block_list.block_list:
                        if runtime_values.players[0].handle_item == block_list.block_list[-1]:
                            runtime_values.players[0].handle_item = block_list.block_list[0]
                        else:
                            runtime_values.players[0].handle_item = block_list.next_block(
                                runtime_values.players[0].handle_item)
                    else:
<<<<<<< HEAD
                        runtime_values.players[0].handle_item = block_list.block_list[0]
=======
                        runtime_values.players[0].handle_item = plants_list.plants_list[0]
>>>>>>> b5b599b (add key(m))
                
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
                    sell.sell(runtime_values.players[0].handle_item) # type: ignore
                case pygame.K_b:  # 구매
                    sell.buy(runtime_values.players[0].handle_item) # type: ignore

                case pygame.K_SPACE:  # 달리기
                    runtime_values.players[0].speed = 4.5

                case pygame.K_k: lib.save.write_save()
                case pygame.K_l: lib.save.import_save()

                # case pygame.K_0:  # TODO:cheat
                #     if int(input("dev code\n")) == 100000:
                #         playerClass.speed = 3
                #         playerClass.inventory = {
                #             "rice": 100000, "riceSeed": 100000, "gold": 100000}
                #         growCount = 5000
                case pygame.K_ESCAPE:  # 메뉴
                    if runtime_values.players[0].handle_item in plants_list.plants_list:
                        pygame.mouse.set_visible(True)
                    pygame.mouse.set_visible(False)
                case pygame.K_0:
                    runtime_values.logs.debug(farm.tileMap[x][y])
                    runtime_values.logs.debug(farm.tileMap[x][y].water)
                case pygame.K_1:
                    runtime_values.logs.debug(runtime_values.players[0].handle_item)
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
