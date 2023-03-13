import pygame

from lib.runtime_values import players
from lib import farm
from lib.plants import plants_list


# image assets for ground tiles
ground_images: dict[farm.Tiles, pygame.Surface] = {
    farm.Tiles.DIRT: pygame.image.load("assets/img/ground/dirt.png"),
    farm.Tiles.FARMLAND: pygame.image.load("assets/img/ground/farmland.png")
}


# draw ground tiles on screen
def draw_ground(screen: pygame.Surface):
    tilePos = pygame.math.Vector2(0, 0)
    for line in farm.tileMap:
        for tile in line:
            if isinstance(tile, plants_list.plants_list):  # check if tile contains plants
                screen.blit(ground_images[farm.Tiles.FARMLAND], tilePos)  # draw farmland tile
            elif tile in farm.Tiles:
                screen.blit(ground_images[tile], tilePos)  # draw tile
            tilePos.y += 32
        tilePos.x += 32
        tilePos.y = 0


# draw plants on the screen
def draw_plants():
    for line in farm.tileMap:
        for tile in line:
            if isinstance(tile, plants_list.plants_list):
                tile.draw()


# draw players on the screen
def draw_players():
    for player in players:
        player.draw()


# draw text with border on screen
def draw_text_with_border(screen: pygame.Surface, font: pygame.font.Font, text: str, inside_color: pygame.Color, border_color: pygame.Color, border_size: float, position: pygame.math.Vector2):
    # render text with specified colors
    inside = font.render(text, True, inside_color)
    border = font.render(text, True, border_color)

    # draw borders around text
    screen.blit(border, pygame.math.Vector2(position.x-border_size, position.y))
    screen.blit(border, pygame.math.Vector2(position.x+border_size, position.y))
    screen.blit(border, pygame.math.Vector2(position.x, position.y-border_size))
    screen.blit(border, pygame.math.Vector2(position.x, position.y+border_size))

    # draw text on top of borders
    screen.blit(inside, position)


# main drawing function to call other drawing functions
def process(screen: pygame.Surface):
    draw_ground(screen)
    draw_plants()
    draw_players()
