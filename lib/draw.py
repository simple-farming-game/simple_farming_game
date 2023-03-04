import pygame

from lib import farm

images: dict[farm.Tiles, pygame.Surface] = {
    farm.Tiles.DIRT: pygame.image.load("assets/img/dirt.png"),
    farm.Tiles.FARMLAND: pygame.image.load("assets/img/farmland.png")
}


def draw_ground(screen):
    tilePos = pygame.math.Vector2(0, 0)
    for line in farm.tileMap:
        for tile in line:
            if tile in farm.Plants_type:
                screen.blit(images[farm.Tiles.FARMLAND], tilePos)
            if tile in farm.Tiles:
                screen.blit(images[tile], tilePos)

            # if tile == lib.farm.Tiles.DIRT:
            #     screen.blit(, tilePos)
            # if (tile == lib.farm.Tiles.FARMLAND) or (tile in Plants_type):
            #     screen.blit(farmlandImg, tilePos)
            tilePos.x += 32
        tilePos.y += 32
        tilePos.x = 0
