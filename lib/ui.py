import lib.draw as dw
from lib import runtime_values
import pygame

class Btn:
    def __init__(self, text: str, _def, pos: pygame.Vector2) -> None:
        self.btn_var = dw.draw_text_with_border(runtime_values.screen, runtime_values.font, text, runtime_values.WHITE, runtime_values.BLACK, 2, pos)
        self.btn_rect = self.btn_var.get_rect()
        self._def = _def
        self.text = text
        self.pos = pos

    def draw(self):
        self.btn_var = dw.draw_text_with_border(runtime_values.screen, runtime_values.font, self.text, runtime_values.WHITE, runtime_values.BLACK, 2, self.pos)
        self.musPos: tuple = pygame.mouse.get_pos()
        if self.btn_rect.collidepoint(self.musPos):
            if pygame.mouse.get_pressed()[0] == 1:
                self._def()