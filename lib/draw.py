import pygame

from lib import farm
from lib.plants import plants_list
from .. import main

images: dict[farm.Tiles, pygame.Surface] = {
    farm.Tiles.DIRT: pygame.image.load("assets/img/dirt.png"),
    farm.Tiles.FARMLAND: pygame.image.load("assets/img/farmland.png")
}


def draw_ground(screen: pygame.Surface):
    tilePos = pygame.math.Vector2(0, 0)
    for line in farm.tileMap:
        for tile in line:
            if isinstance(tile, plants_list.plants_list):  # type: ignore
                screen.blit(images[farm.Tiles.FARMLAND], tilePos)
            elif tile in farm.Tiles:
                screen.blit(images[tile], tilePos)  # type: ignore
            tilePos.x += 32
        tilePos.y += 32
        tilePos.x = 0


def draw_plants():
    for line in farm.tileMap:
        for tile in line:
            if isinstance(tile, plants_list.plants_list):  # type: ignore
                tile.draw()  # type: ignore


def draw_players():
    for player in main.players:
        player.draw()


def draw_text_with_border(screen: pygame.Surface, font: pygame.font.Font, text: str, inside_color: pygame.Color, border_color: pygame.Color, border_size: float, positon: pygame.math.Vector2):
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
