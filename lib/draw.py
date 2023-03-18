import pygame

from lib.runtime_values import players
from lib import farm
from lib.plants import plants_list


ground_images: dict[farm.Tiles, pygame.Surface] = {
    farm.Tiles.DIRT: pygame.image.load("assets/img/ground/dirt.png"),
    farm.Tiles.FARMLAND: pygame.image.load("assets/img/ground/farmland.png"),
    farm.Tiles.WATERED_FARMLAND: pygame.image.load(
        "assets/img/ground/water_farmland.png")
}


def draw_ground(screen: pygame.Surface):
    tilePos = pygame.math.Vector2(0, 0)
    for line in farm.tile_map:
        for tile in line:
            if isinstance(tile, plants_list.plants_list):  # type: ignore
                if tile.watered:  # type: ignore
                    screen.blit(
                        ground_images[farm.Tiles.WATERED_FARMLAND], tilePos)
                else:
                    screen.blit(ground_images[farm.Tiles.FARMLAND], tilePos)
            elif tile in farm.Tiles:
                screen.blit(ground_images[tile], tilePos)  # type: ignore
            tilePos.y += 32
        tilePos.x += 32
        tilePos.y = 0


def draw_plants():
    for line in farm.tile_map:
        for tile in line:
            if isinstance(tile, plants_list.plants_list):  # type: ignore
                tile.draw()  # type: ignore
            if isinstance(tile, plants_list.plants_list):  # type: ignore
                tile.draw()  # type: ignore


def draw_players():
    for player in players:
        player.draw()


def draw_text_with_border(screen: pygame.Surface, font: pygame.font.Font, text: str, inside_color: pygame.Color, border_color: pygame.Color, border_size: float, positon: pygame.math.Vector2):
    # logs.debug("twb")
    inside = font.render(text, True, inside_color)
    border = font.render(text, True, border_color)

    screen.blit(border, pygame.math.Vector2(positon.x-border_size, positon.y))
    screen.blit(border, pygame.math.Vector2(positon.x+border_size, positon.y))
    screen.blit(border, pygame.math.Vector2(positon.x, positon.y-border_size))
    screen.blit(border, pygame.math.Vector2(positon.x, positon.y+border_size))
    screen.blit(inside, positon)


def process(screen: pygame.Surface):
    draw_ground(screen)
    draw_plants()
    draw_players()
