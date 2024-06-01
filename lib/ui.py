import pygame
from lib.runtime_values import *


def draw_text_with_border(
    in_screen: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    inside_color: pygame.Color,
    border_color: pygame.Color,
    border_size: float,
    positon: pygame.math.Vector2,
):
    # new_text = text
    # for i in emoji_list:
    #     for _ in range(text.count(f"<{i}>")):
    #         smile_msg_pos = text.find(f"<{i}>")
    #         new_text = text.replace(f"<{i}>", "  ")
    #
    #         no_smile_one = font.render(text.split(f"<{i}>")[0], True, inside_color)
    #
    #         smile_pos = positon.x + no_smile_one.get_width()
    #
    #         if smile_msg_pos != -1
    #             screen.blit(imgs.emojis[f"{i}"], [smile_pos, positon.y])

    inside = font.render(text, True, inside_color)
    border = font.render(text, True, border_color)

    in_screen.blit(border, pygame.math.Vector2(positon.x - border_size, positon.y))
    in_screen.blit(border, pygame.math.Vector2(positon.x + border_size, positon.y))
    in_screen.blit(border, pygame.math.Vector2(positon.x, positon.y - border_size))
    in_screen.blit(border, pygame.math.Vector2(positon.x, positon.y + border_size))
    in_screen.blit(inside, positon)

    return inside


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
    def __init__(self, text: str, _def, pos: pygame.Vector2, in_screen, in_font):
        self.trg = Trigger(_def)
        self.screen = in_screen
        self.font = in_font
        self._def = _def
        self.text = text
        self.pos = pos

        self.btn_var = draw_text_with_border(
            self.screen,
            self.font,
            self.text,
            pygame.Color(255, 255, 255),
            pygame.Color(0, 0, 0),
            2,
            self.pos,
        )
        self.btn_rect = self.btn_var.get_rect()
        self.pos_tuple = (int(pos.x), int(pos.y))
        self.btn_rect.center = self.pos_tuple
        self.btn_rect.width = self.btn_rect.width * 2
        self.btn_rect.height = self.btn_rect.height * 2

    def draw(self):
        self.btn_var = draw_text_with_border(
            self.screen,
            self.font,
            self.text,
            pygame.Color(255, 255, 255),
            pygame.Color(0, 0, 0),
            2,
            self.pos,
        )
        self.mus_pos: tuple = pygame.mouse.get_pos()
        if self.btn_rect.collidepoint(self.mus_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.trg.value = 1
                self.btn_var = draw_text_with_border(
                    self.screen,
                    self.font,
                    self.text,
                    pygame.Color(155, 155, 255),
                    pygame.Color(0, 0, 0),
                    2,
                    self.pos,
                )
            else:
                self.trg.value = 0
