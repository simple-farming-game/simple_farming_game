class player:
    def __init__(self, pos, screen,hw):
        self.dir=""
        self.pos = pos
        self.screen = screen
        self.hw = hw
        self.speed = 1
    def move(self):
        if self.dir == "l":
            self.pos[0] -= self.speed
        elif self.dir == "r":
            self.pos[0] += self.speed
        elif self.dir == "u":
            self.pos[1] -= self.speed
        elif self.dir == "d":
            self.pos[1] += self.speed
        if self.pos[0] >= self.hw[0]-32:
            print(self.pos)
            self.pos[0] = self.hw[0]-33
        if self.pos[0] <= 0:
            print(self.pos)
            self.pos[0] = 1
        if self.pos[1] >= self.hw[1]-32:
            print(self.pos)
            self.pos[1] = self.hw[1]-32
        if self.pos[1] <= 1:
            print(self.pos)
            self.pos[1] = 1
    def draw(self, img):
        self.screen.blit(img, self.pos)