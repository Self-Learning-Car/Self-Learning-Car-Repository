import pygame
import math

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Car_red_lite.png")
        self.image = pygame.transform.scale(self.image,(120,120))
        self.body_image = self.image.convert_alpha()
        self.body_mask = pygame.mask.from_surface(self.body_image)
        self.body = self.body_image.get_rect()
        self.to_delete = False
        self.pozycja = [100,500]
        self.width = 165
        self.height = 65
        self.speed = 0
        self.angle = 0
        self.num = 0
        self.numver_of_moves = 0
        self.na_parkingu = False
        self.na_lini = False
        self.distance_b = 0
        self.is_parked = 0

    def draw(self, win):
        self.blitRotateCenter(win,self.body_image,self.pozycja,self.angle)


    def update(self):
        self.pozycja[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.pozycja[1] += math.sin(math.radians(360 - self.angle)) * self.speed

    def distance(self,x,y):
        dist = math.sqrt((self.body.centerx - x)**2 + (self.body.centery - y)**2)
        return dist

    def blitRotateCenter(self, surf, image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

        surf.blit(rotated_image, new_rect)

    def forward(self):
        if self.speed < 10:
            self.speed += 1

    def backward(self):
        if self.speed > - 5:
            self.speed -= 1

    def left(self):
        if self.speed != 0:
            self.angle += 15

    def right(self):
        if self.speed != 0:
            self.angle += -15

    def stop(self):
        self.speed = 0