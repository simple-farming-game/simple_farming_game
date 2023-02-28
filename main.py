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
import lib.log as log
import json
# https://inspireman.tistory.com/16
import os
from tkinter import filedialog 
from tkinter import messagebox
# https://mishuni.tistory.com/55
import os , platform , socket
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
''',end="")
logs = log.log()
comInfo = {
    "core":os.cpu_count(),
    "os":platform.system(),
    "processor":platform.processor(),
    "osvar":platform.version()
}

# https://mishuni.tistory.com/55
logs.custem(f"core : {comInfo['core']}") # cpu 갯수 : 8
logs.custem(f"os : {comInfo['os']}") # os 이름 : Linux
logs.custem(f"processor : {comInfo['processor']}") # processor 종류 : x86_64
logs.custem(f"os var : {comInfo['osvar']}") # 44~18.04.2-Ubuntu SMP Thu Apr 23 14:27:18 UTC 2020

# 세팅 불러오기
logs.info("import setting...")
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
logs.info("import lang")
if setting["musicStart"]==True:
    logs.info("music start...")
    # 음악파일 선택 https://inspireman.tistory.com/16
    musicFile = []
    file = filedialog.askopenfilenames(initialdir="/",\
                    title = "파일을 선택 해 주세요",\
                        filetypes = (("*.mp3","*.mp3"),(".",".")))
    
    if file == '':
        messagebox.showwarning("파일선택 안함", "음악을 재생하지 않습니다.")
        logs.info("music no start")
    else:
        # 음악재생 https://inspireman.tistory.com/16
        music = pygame.mixer.Sound(file[0])
        music.play()
else:logs.info("music no start")
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
webSiteBtnText=lsFont.render("SFG site!", True, WHITE)

# 세팅
pygame.display.set_caption(f"sfg {var}! - by newkini")
pygame.display.set_icon(pygameIcon)
playerClass = player.player(playerPos, screen, hw)
riceClass = []
if __name__ != "__main__":
    running=False
logs.info("loding end!")
if comInfo["os"] == "Windows":
    os.system("cls")
else:
    os.system('clear')
# 게임와일
#webbrowser.open("https://newkini-dev.com/sfg")
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
    fun.classVar(riceClass,playerClass)
    fun.textVar(verTextOutline,verText,posTextOutline,posText,invTextOutline,invText)
    fun.imgVar(playerImg,selectImg)
    fun.etcVar(growCount,selectPos,seedList)
    growCount = keyin.key(selectImg, riceClass, farmRiceImg, screen,playerTilePos, stop, fun.delRice, fun.riceSerci, playerClass,fun.reload,logs)
    draw.draw(fun.reload, riceClass,playerClass,screen,growCount,playerImg,selectImg,selectPos,verTextOutline,verText,posTextOutline,posText,invTextOutline,invText)
    pygame.display.update()  # 화면 업데이트
    playerClass.update(keyin.dir)
    # riceClass.update(playerClass.playerTilePos)
logs.info("quit")
logs.save()
pygame.quit()