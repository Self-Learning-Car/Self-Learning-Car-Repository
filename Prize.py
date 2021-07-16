import pygame

class Prize():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = 'assets/Parking.png'
        self.parking_image = pygame.image.load(self.sprite).convert_alpha()
        self.parking_mask = pygame.mask.from_surface(self.parking_image)
        self.parking_body = self.parking_image.get_rect()
        self.naparkingu = False

    def draw(self, win):
        win.blit(self.parking_image, (self.x, self.y))