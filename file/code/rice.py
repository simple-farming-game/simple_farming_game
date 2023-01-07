import pygame
import random
import file.code.farm as farm
class rice: # 파일 따로 빼자,...
    def __init__(self, img, screen, playerTilePos):
        self.tilePos=[32 * playerTilePos[0], 32 * playerTilePos[1]]
        self.growCount = 0
        self.img = img
        self.age = 0
        self.screen = screen
    def draw(self):
        self.screen.blit(self.img, self.tilePos)
    def grow(self):
        self.growCount += random.randint(0,5)
        if self.growCount == 3000:
            self.img = pygame.image.load("file/asset/img/farm_rice_1.png")
            self.age+=1
        if self.growCount == 6000:
            self.img = pygame.image.load("file/asset/img/farm_rice_2.png")
            self.age+=1