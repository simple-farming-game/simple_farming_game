'''
newkini! - sfg
만들꺼:
언어 변경
ide(?)
'''
import pygame
import file.code.farm as farm
import file.code.player as player
import file.code.sfgchat as sfgchat
import file.code.keyinput as keyin
sfgchat.runchat()

print("TESTER : OTTO\nIF MACOS : SYSTEM SETING > KEYBORD > INPUT SOURCE > CAPS LOOK KEY ABC INPUT SOURCE TRANSFORM OFF")

pygame.init()

# 함수
def stop():
    global running
    running = False
# 변수
var = "alpha 1.1/1" # 1.1.1에서 언어변경,클릭 인벤토리 1.2에서 모드추가
hw = (960, 640)
running = True
screen = pygame.display.set_mode(hw)
clock = pygame.time.Clock()
riceCon = 0
# 색변수
SKYBLUE = (113, 199, 245)
BLACK = (255,255,255)
WHITE = (0,0,0)
# 플래이어 변수
playerImg = pygame.image.load("file/asset/img/player.png")
playerPos = [900,100]
# 타일맵
dirtImg = pygame.image.load("file/asset/img/dirt.png")
farmlandImg = pygame.image.load("file/asset/img/farmland.png")
farmRiceImg = pygame.image.load("file/asset/img/farm_rice_0.png")
# 글시
lsFont = pygame.font.Font( "file/asset/font/Galmuri.ttf", 20)
# 이미지
selectImg = [pygame.image.load("file/asset/img/rice_seed.png"), 1]
pygameIcon = pygame.image.load('file/asset/img/icon.png')
# 좌표
selectPos = [10,60]



# 세팅
pygame.display.set_caption(f"sfg {var}! - by newkin")
pygame.display.set_icon(pygameIcon)
playerClass = player.player(playerPos, screen, hw)
riceClass = []


# 게임와일
def run():
    while running:
        clock.tick(100)
        playerTilePos = playerClass.playerTilePos
        verText = lsFont.render(f"SFG {var}!  플래이어 왼쪽위가 기준입니다!", True, BLACK)
        verTextOutline = lsFont.render(f"SFG {var}!  플래이어 왼쪽위가 기준입니다!", True, WHITE)
        posText = lsFont.render(f"{playerTilePos}", True, BLACK)
        posTextOutline = lsFont.render(f"{playerTilePos}", True, WHITE)
        invText = lsFont.render(f"inventory : {playerClass.inventory}", True, BLACK)
        invTextOutline = lsFont.render(f"inventory : {playerClass.inventory}", True, WHITE)

        screen.fill(SKYBLUE) # 화면 채우기
        
        # 함수
        def delRice(x,y):
            global riceClass
            for i in range(len(riceClass)):
                if (riceClass[i].tilePos[1]/32 == x) and (riceClass[i].tilePos[0]/32 == y):
                    riceClass.pop(i)
        def riceSerci(x,y):
            global riceClass
            for i in range(len(riceClass)):
                if (riceClass[i].tilePos[1]/32 == x) and (riceClass[i].tilePos[0]/32 == y):
                    return riceClass[i]
        
        
        # 플래이어
        # 경계
        # 움직이기
        playerClass.move()
        # 타일맵
        tilePos = [0,0]
        for line in farm.tileMap:
            for tile in line:
                if tile == 1:
                    screen.blit(dirtImg, tilePos)
                if tile == 2:
                    screen.blit(farmlandImg, tilePos)
                tilePos[0] += 32
            tilePos[1] += 32
            tilePos[0] = 0
        # 자라게

        keyin.key(selectImg,riceClass,farmRiceImg,screen,playerTilePos,stop,delRice,riceSerci,playerClass)

        # 드로우
        # riceClass.draw(farmRiceImg)
        for i in range(len(riceClass)):
            riceClass[i].draw()
            riceClass[i].grow()

        
        # 이미지 그리기
        playerClass.draw(playerImg)
        screen.blit(selectImg[0], selectPos)
        screen.blit(verTextOutline, (10+2,10))
        screen.blit(verTextOutline, (10-2,10))
        screen.blit(verTextOutline, (10,10+2))
        screen.blit(verTextOutline, (10,10-2))
        screen.blit(verText, (10,10))
        screen.blit(posTextOutline, (850+2,10))
        screen.blit(posTextOutline, (850-2,10))
        screen.blit(posTextOutline, (850,10+2))
        screen.blit(posTextOutline, (850,10-2))
        screen.blit(posText, (850,10))
        screen.blit(invTextOutline, (10+2,35))
        screen.blit(invTextOutline, (10-2,35))
        screen.blit(invTextOutline, (10,35+2))
        screen.blit(invTextOutline, (10,35-2))
        screen.blit(invText, (10,35))

        pygame.display.update() # 화면 업데이트
        playerClass.update(keyin.dir)
        # riceClass.update(playerClass.playerTilePos)

    pygame.quit()