import math

import pygame
import random
import os
import neat

WIN_WIDTH = 1900
WIN_HEIGHT = 1000
WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption("Test")
generation = 0

########################################################################################################################
########################################################################################################################
########################################################################################################################

#klasa Car
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body_image = pygame.image.load('assets/Car.png').convert_alpha()
        self.body_mask = pygame.mask.from_surface(self.body_image)
        self.body = self.body_image.get_rect()
        self.angle = 2

        self.num = 0


########################################################################################################################
########################################################################################################################
########################################################################################################################

#klasa Obstacle, czyli wszystkie przeszkody(również granice parkingu)/zaparkowane samochody na parkingu
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

########################################################################################################################
########################################################################################################################
########################################################################################################################

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

########################################################################################################################
########################################################################################################################
########################################################################################################################

#klasa prize z pustym parkingiem, za który dostaje się nagrodę
class Prize():
    def __init__(self):
        self.x = 1800
        self.y = 0
        self.h = 1000
        self.w = 50
        self.img = pygame.image.load("assets/Empty.png")
        self.img = pygame.transform.scale(self.img, [self.w, self.h])

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

########################################################################################################################
########################################################################################################################
########################################################################################################################

#rysujemy auta itp
def draw_window(win, cars, obstacles):

    #for car in cars:
    car = cars[0]
    mx, my = pygame.mouse.get_pos()
    win.blit(car.body_image, (mx, my))

    for obstacle in obstacles:
        win.blit(obstacle.obstacle_image, (obstacle.x, obstacle.y))
        offset = (mx - obstacle.x, my - obstacle.y)
        result = obstacle.obstacle_mask.overlap(car.body_mask, offset)
        if result:
            print(car.num)
            car.num = car.num + 1

def eval_genomes():

    cars = []
    cars.append(Car())

    parked_car_placement = [[390, 145],
                            [535, 145],
                            [675, 145],
                            [820, 145],
                            [965, 145],
                            [1110, 145],
                            [1250, 145],
                            [1390, 145],
                            [1540, 145],
                            [390, 695],
                            [675, 695],
                            [820, 695],
                            [965, 695],
                            [1110, 695],
                            [1250, 695],
                            [1390, 695],
                            [1540, 695]]

    border_sprites = [['assets/Border1.png'],
                      ['assets/Border2.png'],
                      ['assets/Border3.png'],
                      ['assets/Border4.png'],
                      ['assets/Border5.png'],
                      ['assets/Border6.png']]

    border_placement = [[0, 0],
                        [0, 0],
                        [0, 0],
                        [1804, 0],
                        [0, 868],
                        [0, 706]]

    obstacles = []
    for x in parked_car_placement:
        obstacles.append(Obstacle(x[0], x[1]))

    for n, x in enumerate(border_placement):
        obstacles.append(Border(border_sprites[n][0], x[0], x[1]))

    pygame.init()
    screen = pygame.display.set_mode((1900, 1000))
    map = pygame.image.load('assets/Map.png')

    clock = pygame.time.Clock()
    run = True
    while run and len(cars) > 0:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break



        screen.blit(map, (0, 0))
        draw_window(screen, cars, obstacles)
        pygame.display.flip()
        clock.tick(0)

def run():
    eval_genomes()

########################################################################################################################
########################################################################################################################
########################################################################################################################

if __name__ == '__main__':
    run()
