import pygame
from lib.runtime_values import *


def draw_text_with_border(
    screen: pygame.Surface,
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

    screen.blit(border, pygame.math.Vector2(positon.x - border_size, positon.y))
    screen.blit(border, pygame.math.Vector2(positon.x + border_size, positon.y))
    screen.blit(border, pygame.math.Vector2(positon.x, positon.y - border_size))
    screen.blit(border, pygame.math.Vector2(positon.x, positon.y + border_size))
    screen.blit(inside, positon)

    return inside


class Btn:
    def __init__(self, text: str, _def, pos: pygame.Vector2):

        self.btn_var = draw_text_with_border(
            screen,
            font,
            text,
            pygame.Color(255, 255, 255),
            pygame.Color(0, 0, 0),
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
        self.btn_var = draw_text_with_border(
            screen,
            font,
            self.text,
            pygame.Color(255, 255, 255),
            pygame.Color(0, 0, 0),
            2,
            self.pos,
        )
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mus_pos: tuple = pygame.mouse.get_pos()
                if self.btn_rect.collidepoint(self.mus_pos):
                    if pygame.mouse.get_pressed()[0] == 1:

                        self.btn_var = draw_text_with_border(
                            screen,
                            font,
                            self.text,
                            pygame.Color(255, 255, 255),
                            pygame.Color(0, 0, 0),
                            2,
                            self.pos,
                        )
