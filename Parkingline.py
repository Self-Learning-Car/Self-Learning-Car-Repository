import pygame

class Parkingline(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.img = img
        self.parkline_image = pygame.image.load(self.img).convert_alpha()
        self.parkline_mask = pygame.mask.from_surface(self.parkline_image)
        self.parkline_body = self.parkline_image.get_rect()
        self.nalinii = False