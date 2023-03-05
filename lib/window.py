import pygame
import platform
import json
import os
from typing import Tuple, Dict

import lib.player
import lib.keyinput
import lib.draw
import lib.farm
import lib.logger

version_type = Tuple[str, int, int, int]
version: version_type = ("alpha", 2, 0, 0)

comInfo = {
    "core": os.cpu_count(),
    "os": platform.system(),
    "processor": platform.processor(),
    "osvar": platform.version()
}

with open("data/setting.json", 'r', encoding='utf8') as setting_file:
    setting = json.load(setting_file)
with open(f"data/lang/{setting['lang']}.json", 'r', encoding='utf8') as lang_file:
    lang = json.load(lang_file)


pygame.init()
window_size = (960, 640)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

players: list[lib.player.player]

running: bool

logs = lib.logger.logger()


def loop():
    running = True

    print(f'''
                        _    ___       ___
    _ __   _____      _| | _|_ _|_ __ |_ _|
    | '_ \\ / _ \\ \\ /\\ / / |/ /| || '_ \\ | |
    | | | |  __/\\ V  V /|   < | || | | || |
    |_| |_|\\___| \\_/\\_/ |_|\\_\\___|_| |_|___| Games
    ____         _____         ____
    / ___|       |  ___|       / ___|
    \\___ \\       | |_         | |  _
    ___) |      |  _|        | |_| |
    |____/ imple |_|  arming  \\____|ame
    
    V. {version[0]} {version[1]}.{version[2]}.{version[3]}
    최고의 게발섭! mng커뮤니티! https://discord.gg/mng
    
    loding...
    ''', end="")

    players = [
        lib.player.player(
            pygame.image.load("assets/img/player.png"),
            pygame.math.Vector2(900, 100),
            screen, window_size)
    ]
    # colors
    SKYBLUE = pygame.Color(113, 199, 245)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)

    font_renderer = pygame.font.Font("assets/font/Galmuri.ttf", 20)

    pygame.display.set_caption(f"sfg {version}! - by newkini")
    pygame.display.set_icon(pygame.image.load('assets/img/icon.png'))

    # 게임와일
    while running:
        clock.tick(100)
        screen.fill(SKYBLUE)  # 화면 채우기

        lib.draw.draw_text_with_border(
            screen, font_renderer, f"SFG {version}!  {lang['guid']}", WHITE, BLACK, 2, pygame.math.Vector2(10, 10))
        lib.draw.draw_text_with_border(
            screen, font_renderer, str(players[0].get_tile_pos()), WHITE, BLACK, 2, pygame.math.Vector2(850, 35))
        lib.draw.draw_text_with_border(
            screen, font_renderer, str(players[0].inventory), WHITE, BLACK, 2, pygame.math.Vector2(10, 35))
        lib.draw.draw_text_with_border(
            screen, font_renderer, str(players[0].handle_item), WHITE, BLACK, 2, pygame.math.Vector2(10, 70))

        lib.draw.process(screen)
        lib.keyinput.process()

        pygame.display.update()  # 화면 업데이트
    logs.info("quit")
    logs.save()
    pygame.quit()
