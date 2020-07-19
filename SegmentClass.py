import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class PlayerSegment(pygame.sprite.Sprite):

    def __init__(self, x, y, img, angle1=0, rotate=False, wid=80, hie=80, tl=False, cvt=False):
        super().__init__()
        if not cvt:
            self.image = pygame.image.load(img)
        else:
            self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (wid, hie))
        if rotate:
            self.image = pygame.transform.rotate(self.image, angle1)

        self.image.set_colorkey(WHITE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        if tl:
            self.rect.topleft = [x, y]
        else:
            self.rect.center = [x, y]
        self.width = self.image.get_width()
        self.height = self.image.get_height()