import lib.draw as dw
from lib import runtime_values
import pygame

class btn:
    def __init__(self, text: str, _def, pos: pygame.Vector2) -> None:
        dw.draw_text_with_border(runtime_values.screen, runtime_values.font, text, runtime_values.WHITE, runtime_values.BLACK, 2, pos)