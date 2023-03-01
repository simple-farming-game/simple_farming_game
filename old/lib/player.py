import math
# 완전 스파게티 코드다.... 하....

class player:
    def __init__(self, pos, screen, hw):
        self.dir = "l"
        self.pos = pos
        self.screen = screen
        self.hw = hw
        self.speed = 1
        self.playerTilePos = []
        self.inventory = {"rice": 0, "riceSeed": 5, "gold": 0}

    def move(self):
        match self.dir:
            case "l":
                self.pos[0] -= self.speed
            case "r":
                self.pos[0] += self.speed
            case "u":
                self.pos[1] -= self.speed
            case "d":
                self.pos[1] += self.speed

        if self.pos[0] >= self.hw[0]-32:
            self.pos[0] = self.hw[0]-33
        if self.pos[0] <= 0:
            self.pos[0] = 1
        if self.pos[1] >= self.hw[1]-32:
            self.pos[1] = self.hw[1]-32
        if self.pos[1] <= 1:
            self.pos[1] = 1

    def draw(self, img):
        self.screen.blit(img, self.pos)

    def update(self, dir):
        self.playerTilePos = [math.trunc(self.pos[0]/32), math.trunc(self.pos[1]/32)]
        self.dir = dir
