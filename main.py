import pygame
import json
import os
import os
import platform

import lib.player
import lib.keyinput
import lib.draw
import lib.farm
from lib.logger import logger
# 로딩메시지
version = ("alpha",2,0,0)

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
|____/ imple |_|  arming  \\____|ame V. {version}
최고의 게발섭! mng커뮤니티! https://discord.gg/mng
loding...
''', end="")
logs = logger()
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


running = True


# 변수1
# 1.1.1에서저장만들기 1.2에서 언어변경,클릭 인벤토리,오프닝,처음매뉴,디코접속버튼,모드,(노션db로 계정기능 추가), 농작물 추가


pygame.init()
window_size = (960, 640)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
# 색변수
SKYBLUE = pygame.Color(113, 199, 245)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
# 글씨
lsFont = pygame.font.Font("assets/font/Galmuri.ttf", 20)

# 세팅
pygame.display.set_caption(f"sfg {version}! - by newkini")
pygame.display.set_icon(pygame.image.load('assets/img/icon.png'))
players: list[lib.player.player] = [
    lib.player.player(
        pygame.image.load("assets/img/player.png"),
        pygame.math.Vector2(900, 100),
        screen, window_size)
]

if __name__ != "__main__":
    running = False
# 게임와일
while running:
    clock.tick(100)

    playerTilePos = players[0].get_tile_pos()
    # verText = lsFont.render(f"SFG {var}!  {lang['guid']}", True, WHITE)
    verTextOutline = lsFont.render(f"SFG {version}!  {lang['guid']}", True, BLACK)
    posText = lsFont.render(f"{playerTilePos}", True, WHITE)
    posTextOutline = lsFont.render(f"{playerTilePos}", True, BLACK)
    invText = lsFont.render(
        f"inventory : {players[0].inventory}", True, WHITE)
    invTextOutline = lsFont.render(
        f"inventory : {players[0].inventory}", True, BLACK)

    screen.fill(SKYBLUE)  # 화면 채우기
    growCount = 0

    # TODO
    lib.keyinput.process()
    lib.draw.process()
    # growCount = keyinput.key(selectImg, riceClass, farmRiceImg, screen, playerTilePos,
    #                          stop, fun.delRice, fun.riceSerci, playerClass, fun.reload, logs)
    # draw.draw(fun.reload, riceClass, playerClass, screen, growCount, playerImg, selectImg,
    #           selectPos, verTextOutline, verText, posTextOutline, posText, invTextOutline, invText)
    pygame.display.update()  # 화면 업데이트
    # riceClass.update(playerClass.playerTilePos)
logs.info("quit")
logs.save()
pygame.quit()
