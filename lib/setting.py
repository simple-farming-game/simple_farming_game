from lib import draw
from lib import runtime_values
import pygame
def setting():
    if runtime_values.on_setting == True:
        draw.draw_text_with_border(runtime_values.screen, runtime_values.font, "셋팅", runtime_values.WHITE, runtime_values.BLACK, 2, pygame.math.Vector2(15*32, 3*32))
        draw.draw_text_with_border(runtime_values.screen, runtime_values.font, "셋팅", runtime_values.WHITE, runtime_values.BLACK, 2, pygame.math.Vector2(15*32, 5*32))