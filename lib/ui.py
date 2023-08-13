import lib.draw as dw
from lib import runtime_values
import pygame


class Trigger:
    def __init__(self, fun):
        self.__value = 0
        self.fun = fun

    # getter, 변수값 읽기.
    @property
    def value(self):
        return self.__value

    # setter, 변수에 값 대입하기.
    @value.setter
    def value(self, value):
        if self.__value == 0 and value == 1:
            self.fun()
        # 마지막에 변수값 대입.
        self.__value = value


class Btn:
    def __init__(self, text: str, _def, pos: pygame.Vector2):
        self.trg = Trigger(_def)

        self.btn_var = dw.draw_text_with_border(
            runtime_values.screen,
            runtime_values.font,
            text,
            runtime_values.WHITE,
            runtime_values.BLACK,
            2,
            pos,
        )
        self.btn_rect = self.btn_var.get_rect()
        self._def = _def
        self.text = text
        self.pos = pos
        self.pos_tuple = (int(pos.x), int(pos.y))
        self.btn_rect.center = self.pos_tuple
        self.btn_rect.width = self.btn_rect.width * 2
        self.btn_rect.height = self.btn_rect.height * 2

    def draw(self):
        self.btn_var = dw.draw_text_with_border(
            runtime_values.screen,
            runtime_values.font,
            self.text,
            runtime_values.WHITE,
            runtime_values.BLACK,
            2,
            self.pos,
        )
        self.mus_pos: tuple = pygame.mouse.get_pos()
        if self.btn_rect.collidepoint(self.mus_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.trg.value = 1
                self.btn_var = dw.draw_text_with_border(
                    runtime_values.screen,
                    runtime_values.font,
                    self.text,
                    runtime_values.BLUE,
                    runtime_values.BLACK,
                    2,
                    self.pos,
                )
            else:
                self.trg.value = 0
