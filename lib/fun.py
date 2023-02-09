import lib.farm as farm
import pygame
def classVar(riceClass,playerClass):
    riceClass = riceClass
    playerClass = playerClass
def textVar(verTextOutline,verText,posTextOutline,posText,invTextOutline,invText):
    verTextOutline = verTextOutline
    verText = verText
    posTextOutline = posTextOutline
    posText = posText
    invTextOutline = invTextOutline
    invText = invText
def imgVar(playerImg,selectImg):
    playerImg = playerImg
    selectImg = selectImg
    dirtImg = pygame.image.load("assets/img/dirt.png")
    farmlandImg = pygame.image.load("assets/img/farmland.png")
def etcVar(growCount,selectPos,seedList):
    growCount = growCount
    selectPos = selectPos
    seedList = seedList
def delRice(x, y):  # x,y위치에 있는 쌀을 제거
    for i in range(len(classVar.riceClass)):
        try:
            if (classVar.riceClass[i].tilePos[1]/32 == x) and (classVar.riceClass[i].tilePos[0]/32 == y): # 작동은 잘되는데 out of list오류가 남;;
                classVar.riceClass.pop(i)
        except:pass

def riceSerci(x, y):  # x,y위치에 있는 쌀을 알려드림!
    for i in range(len(classVar.riceClass)):
        if (classVar.riceClass[i].tilePos[1]/32 == x) and (classVar.riceClass[i].tilePos[0]/32 == y):
            return classVar.riceClass[i]

def reload(screen):
    tilePos = [0, 0]
    for line in farm.tileMap:
        for tile in line:
            if tile == 1:
                screen.blit(imgVar.dirtImg, tilePos)  # 1은 흙
            if (tile == 2) or (tile in etcVar.seedList):
                screen.blit(imgVar.farmlandImg, tilePos)  # 2는 경작지
            tilePos[0] += 32
        tilePos[1] += 32
        tilePos[0] = 0