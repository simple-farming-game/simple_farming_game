import pygame
from lib import runtime_values
from lib import farm

def debug(event: pygame.event.Event):
    x, y = map(int, runtime_values.players[0].get_tile_pos())
    if event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_EQUALS:
                runtime_values.logs.debug(farm.tileMap[x][y])
                try:runtime_values.logs.debug(farm.tileMap[x][y].water) # type: ignore
                except:pass
            case pygame.K_MINUS:
                runtime_values.logs.debug(runtime_values.players[0].handle_item)
            case pygame.K_MINUS:
                runtime_values.logs.debug(runtime_values.players[0].handle_item) 