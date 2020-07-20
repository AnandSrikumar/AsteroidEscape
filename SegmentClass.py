import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class PlayerSegment(pygame.sprite.Sprite):

    def __init__(self, x, y, img, angle1=0, rotate=False, wid=80, hie=80, tl=False, cvt=False):
        super().__init__()
        self.x = x
        self.y = y
        self.img = img
        self.rotate, self.angle1 = rotate, angle1
        self.wid, self.hie, self.tl, self. cvt = wid, hie, tl, cvt
        self.image = pygame.image.load(self.img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.wid, self.hie))
        if self.rotate:
            self.image = pygame.transform.rotate(self.image, self.angle1)
        self.image_copy = self.image.copy()
        self.rect = self.image.get_rect()
        if self.tl:
            self.rect.topleft = [self.x, self.y]
        else:
            self.rect.center = [self.x, self.y]
        self.width = self.image.get_width
        self.height = self.image.get_height

    def get_image(self):
        if self.rotate:
            self.image_copy = pygame.transform.scale(self.image, (self.wid, self.hie))
            self.image_copy = pygame.transform.rotate(self.image_copy, self.angle1)
        self.image_copy.set_colorkey(WHITE)
        self.image_copy.set_colorkey(BLACK)
        self.rect = self.image_copy.get_rect()
        if self.tl:
            self.rect.topleft = [self.x, self.y]
        else:
            self.rect.center = [self.x, self.y]
        self.width = self.image_copy.get_width()
        self.height = self.image_copy.get_height()
