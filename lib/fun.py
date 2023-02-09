import lib.farm as farm
import pygame
def inVar(riceClass,playerClass,growCount,playerImg,selectImg,selectPos,verTextOutline,verText,posTextOutline,posText,invTextOutline,invText,seedList):
    riceClass = riceClass
    playerClass = playerClass
    growCount = growCount
    playerImg = playerImg
    selectImg = selectImg
    selectPos = selectPos
    verTextOutline = verTextOutline
    verText = verText
    posTextOutline = posTextOutline
    posText = posText
    invTextOutline = invTextOutline
    invText = invText
    seedList = seedList
riceClass =      inVar.riceClass
playerClass =    inVar.playerClass
growCount =      inVar.growCount
playerImg =      inVar.playerImg
selectImg =      inVar.selectImg
selectPos =      inVar.selectPos
verTextOutline = inVar.verTextOutline
verText =        inVar.verText
posTextOutline = inVar.posTextOutline
posText =        inVar.posText
invTextOutline = inVar.invTextOutline
invText =        inVar.invText
seedList =       inVar.seedList
dirtImg = pygame.image.load("assets/img/dirt.png")
farmlandImg = pygame.image.load("assets/img/farmland.png")
def delRice(x, y):  # x,y위치에 있는 쌀을 제거
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

def reload(screen):
    tilePos = [0, 0]
    for line in farm.tileMap:
        for tile in line:
            if tile == 1:
                screen.blit(dirtImg, tilePos)  # 1은 흙
            if (tile == 2) or (tile in seedList):
                screen.blit(farmlandImg, tilePos)  # 2는 경작지
            tilePos[0] += 32
        tilePos[1] += 32
        tilePos[0] = 0