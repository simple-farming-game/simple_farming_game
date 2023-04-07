from ..Object import Object
import pygame

class Block(Object):
    name: str  # 영어로 적고 lang 파일에서 참조.

    def __init__(self, pos: pygame.math.Vector2, screen: pygame.Surface) -> None:
<<<<<<< HEAD
        self.image = pygame.image.load(f"assets/img/block/{self.name}.png")
        self.pos = pos
        self.screen = screen
        self.init()
        super().__init__(self.image, pos, screen)
    def returnVar(self):
        return [self.image, self.pos, self.screen]
    def init(self): ...
=======
        image = pygame.image.load(f"assets/img/block/{self.name}.png")
        super().__init__(image, pos, screen)
>>>>>>> d6beeeb (블록 놓기 완성 하지만 오류)
