import sys
import os
import pygame
import math
import file.asset.tilemap.farm as farm
import file.code.player as player
import file.code.sfgchat as sfgchat

sfgchat.runchat()

print("TESTER : OTTO\nIF MACOS : SYSTEM SETING > KEYBORD > INPUT SOURCE > CAPS LOOK KEY ABC INPUT SOURCE TRANSFORM OFF")

pygame.init()

# 함수

# 변수
var = "alpha 1.1/3"
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
# 좌표
selectPos = [0,50]

class rice:
    def __init__(self):
        self.tilePos=[]
        self.drawList=[]
    def update(self, playerTilePos):
        self.tilePos = [32 * playerTilePos[0], 32 * playerTilePos[1]]
    def addList(self):
        self.drawList.append(self.tilePos)
    def draw(self, img):
        for i in self.drawList:
            screen.blit(img, i)

# 세팅
pygame.display.set_caption(f"sfg {var}! - by newkin")
playerClass = player.player(playerPos, screen, hw)
riceClass = rice() # TODO:리스트화하기, 따로따로 자라게


# 게임와일
while running:
    clock.tick(100)

    playerTilePos = playerClass.playerTilePos
    verText = lsFont.render(f"SFG {var}!  플래이어 왼쪽위가 기준입니다!                                                {playerTilePos}", True, BLACK)
    verTextOutline = lsFont.render(f"SFG {var}!  플래이어 왼쪽위가 기준입니다!                                                {playerTilePos}", True, WHITE)

    screen.fill(SKYBLUE) # 화면 채우기
    
    for event in pygame.event.get():  # 키입력 감지
        # 나가기
        if event.type == pygame.QUIT:  # 나가기 버튼 눌럿을때
            running = False  # 와일문 나가기
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dir = "l"
            elif event.key == pygame.K_RIGHT:
                dir = "r"
            elif event.key == pygame.K_UP:
                dir = "u"
            elif event.key == pygame.K_DOWN:
                dir = "d"
            if event.key == pygame.K_d:
                if (selectImg[1] == 1) and (farm.tileMap[playerTilePos[1]][playerTilePos[0]] == 2):
                    # farm.tileMap[playerTilePos[1]][playerTilePos[0]] = 3
                    riceClass.addList()
                    print(f"심기 : X:{playerTilePos[1]} Y:{playerTilePos[0]}")
                else:
                    print("실패 : 이미 심어져 있음.")
            if event.key == pygame.K_f:
                if (farm.tileMap[playerTilePos[1]][playerTilePos[0]] != 3) and (farm.tileMap[playerTilePos[1]][playerTilePos[0]] != 2):
                    farm.tileMap[playerTilePos[1]][playerTilePos[0]] = 2
                    print(f"경작 : X:{playerTilePos[1]} Y:{playerTilePos[0]}")
                else:
                    print("실패 : 이미 심어져 있거나 경작되어 있음.")
            if event.key == pygame.K_0:
                selectImg[0] = pygame.image.load("file/asset/img/none.png")
                selectImg[1] = 0
            elif event.key == pygame.K_1:
                selectImg[0] = pygame.image.load("file/asset/img/rice_seed.png")
                selectImg[1] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                dir = ""
            elif event.key == pygame.K_DOWN:
                dir = ""
            elif event.key == pygame.K_LEFT:
                dir = ""
            elif event.key == pygame.K_RIGHT:
                dir = ""   
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
            if tile == 3:
                screen.blit(farmRiceImg, tilePos)
            tilePos[0] += 32
        tilePos[1] += 32
        tilePos[0] = 0
    # 식물 자라게
    riceClass.draw(farmRiceImg)
    riceCon += 1
    
    if riceCon == 10000:
        farmRiceImg = pygame.image.load("file/asset/img/farm_rice_1.png")
    if riceCon == 50000:
        farmRiceImg = pygame.image.load("file/asset/img/farm_rice_2.png")

    
    # 이미지 그리기
    playerClass.draw(playerImg)
    screen.blit(selectImg[0], selectPos)
    screen.blit(verTextOutline, (10+2,10))
    screen.blit(verTextOutline, (10-2,10))
    screen.blit(verTextOutline, (10,10+2))
    screen.blit(verTextOutline, (10,10-2))
    screen.blit(verText, (10,10))

    pygame.display.update() # 화면 업데이트
    playerClass.update(dir)
    riceClass.update(playerClass.playerTilePos)

pygame.quit()