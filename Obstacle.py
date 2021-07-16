import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.obstacle_image = pygame.image.load('assets/Car1.png').convert_alpha()
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)
        self.obstacle_body = self.obstacle_image.get_rect()

    def draw(self, win):
        win.blit(self.obstacle_image, (self.x, self.y))