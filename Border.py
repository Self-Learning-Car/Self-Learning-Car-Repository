import pygame

class Border(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.sprite = sprite
        self.obstacle_image = pygame.image.load(self.sprite).convert_alpha()
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)
        self.obstacle_body = self.obstacle_image.get_rect()

    def draw(self, win):
        win.blit(self.obstacle_image, (self.x, self.y))