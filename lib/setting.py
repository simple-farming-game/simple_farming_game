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

        music = ui.Btn(
                "음악 : 켜짐", lambda: print("hello world"), pygame.math.Vector2(15, 5) * 32
            )
        
        music.draw()

        if runtime_values.setting["musicStart"]:
            music.text = "음악 : 켜짐"
        else:
            music.text = "음악 : 꺼짐"
