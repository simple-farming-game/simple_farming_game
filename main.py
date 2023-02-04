'''
newkini! - sfg
만들꺼:
언어 변경
ide(?)
'''
import pygame
import webbrowser
import lib.farm as farm
import lib.player as player
import lib.sfgchat as sfgchat
import lib.keyinput as keyin
import json

# 세팅 불러오기
lang=""
setting = open("data/setting.json", 'r', encoding='utf8')
setting = json.load(setting)
match setting["lang"]:
    case "ko-kr":
        lang = open("data/lang/ko-kr.json", 'r', encoding='utf8')
        lang=json.load(lang)
sfgchat.runchat()

print("TESTER : OTTO\nIF MACOS : SYSTEM SETTING > KEYBORD > INPUT SOURCE > CAPS LOOK KEY ABC INPUT SOURCE TRANSFORM OFF")

pygame.init()

# 함수


def stop():
    global running
    running = False


# 변수1
var = "alpha 1.1.1"  # 1.1.1에서저장만들기 1.2에서 언어변경,클릭 인벤토리,오프닝,처음매뉴,디코접속버튼,모드,(노션db로 계정기능 추가), 농작물 추가
hw = (960, 640)
running = True
screen = pygame.display.set_mode(hw)
clock = pygame.time.Clock()
riceCon = 0
# 색변수
SKYBLUE = (113, 199, 245)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# 플래이어 변수
playerImg = pygame.image.load("assets/img/player.png")
playerPos = [900, 100]
# 타일맵
dirtImg = pygame.image.load("assets/img/dirt.png")
farmlandImg = pygame.image.load("assets/img/farmland.png")
farmRiceImg = pygame.image.load("assets/img/farm_rice_0.png")
# 글시
lsFont = pygame.font.Font("assets/font/Galmuri.ttf", 20)
# 이미지
selectImg = [pygame.image.load("assets/img/rice_seed.png"), 1]
pygameIcon = pygame.image.load('assets/img/icon.png')
# 좌표
selectPos = [10, 60]

# 세팅
pygame.display.set_caption(f"sfg {var}! - by newkin")
pygame.display.set_icon(pygameIcon)
playerClass = player.player(playerPos, screen, hw)
riceClass = []
if __name__ != "__main__":
    running=False
# 게임와일
while running:
    clock.tick(100)
    playerTilePos = playerClass.playerTilePos
    verText = lsFont.render(f"SFG {var}!  {lang['guid']}", True, WHITE)
    verTextOutline = lsFont.render(f"SFG {var}!  {lang['guid']}", True, BLACK)
    posText = lsFont.render(f"{playerTilePos}", True, WHITE)
    posTextOutline = lsFont.render(f"{playerTilePos}", True, BLACK)
    invText = lsFont.render(f"inventory : {playerClass.inventory}", True, WHITE)
    invTextOutline = lsFont.render(f"inventory : {playerClass.inventory}", True, BLACK)

    screen.fill(SKYBLUE)  # 화면 채우기

    # 함수
    def delRice(x, y):  # x,y위치에 있는 쌀을 제거
        global riceClass
        for i in range(len(riceClass)):
            try:
                if (riceClass[i].tilePos[1]/32 == x) and (riceClass[i].tilePos[0]/32 == y): # 작동은 잘되는데 out of list오류가 남;;
                    riceClass.pop(i)
            except:pass

    def riceSerci(x, y):  # x,y위치에 있는 쌀을 알려드림!
        global riceClass
        for i in range(len(riceClass)):
            if (riceClass[i].tilePos[1]/32 == x) and (riceClass[i].tilePos[0]/32 == y):
                return riceClass[i]
    
    def reload():
        tilePos = [0, 0]
        for line in farm.tileMap:
            for tile in line:
                if tile == 1:
                    screen.blit(dirtImg, tilePos)  # 1은 흙
                if tile == 2:
                    screen.blit(farmlandImg, tilePos)  # 2는 경작지
                tilePos[0] += 32
            tilePos[1] += 32
            tilePos[0] = 0

    # 플래이어
    # 움직이기
    playerClass.move()
    # 타일맵
    # 자라게

    growCount = keyin.key(selectImg, riceClass, farmRiceImg, screen,playerTilePos, stop, delRice, riceSerci, playerClass,reload)

    # 드로우
    reload()
    # riceClass.draw(farmRiceImg)
    for i in range(len(riceClass)):
        riceClass[i].draw()
        riceClass[i].grow(growCount)

    # 이미지 그리기
    playerClass.draw(playerImg)
    screen.blit(selectImg[0], selectPos)
    screen.blit(verTextOutline, (10+2, 10))
    screen.blit(verTextOutline, (10-2, 10))
    screen.blit(verTextOutline, (10, 10+2))
    screen.blit(verTextOutline, (10, 10-2))
    screen.blit(verText, (10, 10))
    screen.blit(posTextOutline, (850+2, 10))
    screen.blit(posTextOutline, (850-2, 10))
    screen.blit(posTextOutline, (850, 10+2))
    screen.blit(posTextOutline, (850, 10-2))
    screen.blit(posText, (850, 10))
    screen.blit(invTextOutline, (10+2, 35))
    screen.blit(invTextOutline, (10-2, 35))
    screen.blit(invTextOutline, (10, 35+2))
    screen.blit(invTextOutline, (10, 35-2))
    screen.blit(invText, (10, 35))

    pygame.display.update()  # 화면 업데이트
    playerClass.update(keyin.dir)
    # riceClass.update(playerClass.playerTilePos)

pygame.quit()