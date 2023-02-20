import lib.farm as farm
import pygame
riceClass = [0,[]]
playerClass = [0]
growCount = [0]
playerImg = [0]
selectImg = [0]
selectPos = [0]
verTextOutline = [0]
verText = [0]
posTextOutline = [0]
posText = [0]
invTextOutline = [0]
invText = [0]
seedList = [0]
dirtImg = pygame.image.load("assets/img/dirt.png")
farmlandImg = pygame.image.load("assets/img/farmland.png")
def classVar(iceClass,layerClass):
    global riceClass
    global playerClass
    riceClass = iceClass
    playerClass = layerClass
def textVar(erTextOutline,erText,osTextOutline,osText,nvTextOutline,nvText):
    global verTextOutline
    global verText
    global posTextOutline
    global posText
    global invTextOutline
    global invText
    verTextOutline = erTextOutline
    verText = erText
    posTextOutline = osTextOutline
    posText = osText
    invTextOutline = nvTextOutline
    invText = nvText
def imgVar(layerImg,electImg):
    global playerImg
    global selectImg
    playerImg = layerImg
    selectImg = electImg
def etcVar(rowCount,electPos,eedList):
    global growCount
    global selectPos
    global seedList
    growCount = rowCount
    selectPos = electPos
    seedList = eedList
def delRice(x, y):  # x,y위치에 있는 쌀을 제거
    for i in range(len(riceClass)):
        try:
            if (riceClass[i].tilePos[1]/32 == x) and (riceClass[i].tilePos[0]/32 == y): # 작동은 잘되는데 out of list오류가 남;;
                riceClass.pop(i)
        except:pass

def riceSerci(x, y):  # x,y위치에 있는 쌀을 알려드림!
    for i in range(len(riceClass)):
        try:
            if (riceClass[i].tilePos[1]/32 == x) and (classVar.riceClass[i].tilePos[0]/32 == y):
                return riceClass[i]
        except:pass

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