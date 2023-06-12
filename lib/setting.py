from lib import draw
from lib import runtime_values
from lib import ui
import pygame


def not_musicStart():
    runtime_values.setting["musicStart"] = not runtime_values.setting["musicStart"]


def setting():
    if runtime_values.on_setting == True:
        draw.draw_text_with_border(
            runtime_values.screen,
            runtime_values.font,
            "셋팅",
            runtime_values.WHITE,
            runtime_values.BLACK,
            2,
            pygame.math.Vector2(15 * 32, 3 * 32),
        )
        if runtime_values.setting["musicStart"]:
            music = ui.Btn(
                "음악 : 킴", not_musicStart, pygame.math.Vector2(15 * 32, 5 * 32)
            )
            music.draw()
        else:
            music = ui.Btn(
                "음악 : 끔", not_musicStart, pygame.math.Vector2(15 * 32, 5 * 32)
            )
            music.draw()
