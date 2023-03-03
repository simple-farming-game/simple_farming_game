from lib.types.Image import Image
import pygame
# import webbrowser
import lib.player as player
import lib.keyinput as keyinput
import lib.draw as draw
import lib.fun as fun
import lib.logger as logger
import json
# https://inspireman.tistory.com/16
import os
from tkinter import filedialog
from tkinter import messagebox
# https://mishuni.tistory.com/55
import os
import platform
import socket
# 로딩메시지
var = "alpha 1.1.1/3"

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
|____/ imple |_|  arming  \\____|ame V. {var}
최고의 게발섭! mng커뮤니티! https://discord.gg/mng
loding...
''', end="")
logs = logger.logger()
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


# 함수


running = True


def stop():
    running = False


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
# 플래이어 변수
playerImg = Image(pygame.image.load("assets/img/player.png"))
playerPos = pygame.math.Vector2(900, 100)
# 타일맵
dirtImg = pygame.image.load("assets/img/dirt.png")
farmlandImg = pygame.image.load("assets/img/farmland.png")
farmRiceImg = pygame.image.load("assets/img/farm_rice_0.png")
# 글씨
lsFont = pygame.font.Font("assets/font/Galmuri.ttf", 20)
# 이미지
selectImg = [pygame.image.load("assets/img/rice_seed.png"), 1]
# 좌표
selectPos = [10, 60]
# ...
seedList = [3]
webSiteBtnText = lsFont.render("SFG site!", True, WHITE)

# 세팅
pygame.display.set_caption(f"sfg {var}! - by newkini")
pygame.display.set_icon(pygame.image.load('assets/img/icon.png'))
playerClass = player.player(playerImg, playerPos, screen, window_size)
riceClass = []
if __name__ != "__main__":
    running = False
# 게임와일
while running:
    clock.tick(100)

    playerTilePos = playerClass.get_tile_pos()
    verText = lsFont.render(f"SFG {var}!  {lang['guid']}", True, WHITE)
    verTextOutline = lsFont.render(f"SFG {var}!  {lang['guid']}", True, BLACK)
    posText = lsFont.render(f"{playerTilePos}", True, WHITE)
    posTextOutline = lsFont.render(f"{playerTilePos}", True, BLACK)
    invText = lsFont.render(
        f"inventory : {playerClass.inventory}", True, WHITE)
    invTextOutline = lsFont.render(
        f"inventory : {playerClass.inventory}", True, BLACK)

    screen.fill(SKYBLUE)  # 화면 채우기
    playerClass.move(keyinput.dir)
    growCount = 0

    # TODO
    # growCount = keyinput.key(selectImg, riceClass, farmRiceImg, screen, playerTilePos,
    #                          stop, fun.delRice, fun.riceSerci, playerClass, fun.reload, logs)
    # draw.draw(fun.reload, riceClass, playerClass, screen, growCount, playerImg, selectImg,
    #           selectPos, verTextOutline, verText, posTextOutline, posText, invTextOutline, invText)
    pygame.display.update()  # 화면 업데이트
    # riceClass.update(playerClass.playerTilePos)
logs.info("quit")
logs.save()
pygame.quit()
