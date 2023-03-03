import pygame

import lib.farm as farm
from plants.plants_data import Plants_type


dirtImg = pygame.image.load("assets/img/dirt.png")
farmlandImg = pygame.image.load("assets/img/farmland.png")


def farm_plant(pos: pygame.math.Vector2):
    tile = farm.tileMap[int(pos.x)][int(pos.y)]
    if tile in Plants_type:
        pass  # TODO


def reload(screen):
    tilePos = pygame.math.Vector2(0, 0)
    for line in farm.tileMap:
        for tile in line:
            if tile == farm.Tiles.DIRT:
                screen.blit(dirtImg, tilePos)
            if (tile == farm.Tiles.FARMLAND) or (tile in Plants_type):
                screen.blit(farmlandImg, tilePos)
            tilePos.x += 32
            # 이 32도 하드코딩 하지 말고 어디서 참조하는게 좋습니다...
        tilePos.y += 32
        tilePos.x = 0
