'''
newkini! - sfg
만들꺼:
언어 변경
ide(?)
'''
import pygame
import webbrowser
import lib.player as player
import lib.sfgchat as sfgchat
import lib.keyinput as keyin
import lib.draw as draw
import lib.fun as fun
import json

# 로딩메시지
var = "alpha 1.1.1/1"
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
|____/ imple |_|  farming  \\____|ame V. {var}
loding...
''',end="")

# 세팅 불러오기
lang={
    "guid":"",
    "fail":{
        "d":"",
        "save":""
    }
}
setting = open("data/setting.json", 'r', encoding='utf8')
setting = json.load(setting)
match setting["lang"]:
    case "ko-kr":
        lang = open("data/lang/ko-kr.json", 'r', encoding='utf8')
        lang=json.load(lang)
sfgchat.runchat()



pygame.init()

# 함수


def stop():
    global running
    running = False


# 변수1
# 1.1.1에서저장만들기 1.2에서 언어변경,클릭 인벤토리,오프닝,처음매뉴,디코접속버튼,모드,(노션db로 계정기능 추가), 농작물 추가
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
# ...
seedList = [3]

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
    playerClass.move()
    growCount = 0
    fun.inVar(riceClass,playerClass,growCount,playerImg,selectImg,selectPos,verTextOutline,verText,posTextOutline,posText,invTextOutline,invText,seedList)
    growCount = keyin.key(selectImg, riceClass, farmRiceImg, screen,playerTilePos, stop, fun.delRice, fun.riceSerci, playerClass,fun.reload)
    draw.draw(fun.reload, riceClass,playerClass,screen,growCount,playerImg,selectImg,selectPos,verTextOutline,verText,posTextOutline,posText,invTextOutline,invText)
    pygame.display.update()  # 화면 업데이트
    playerClass.update(keyin.dir)
    # riceClass.update(playerClass.playerTilePos)
pygame.quit()