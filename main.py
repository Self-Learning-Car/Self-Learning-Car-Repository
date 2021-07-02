import math

import numpy
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



        self.pozycja = [100,500]
        self.width = 165
        self.height = 65

        self.speed = 0

        self.angle = 0

        self.num = 0


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
        if self.speed < 20:
            self.speed += 3

    def backward(self):
        if self.speed > - 20:
            self.speed -= 3

    def left(self):
        self.angle += 0.4 * self.speed

    def right(self):
        self.angle -= 0.4 * self.speed

    def random_act(self):
        act = random.randrange(0,6)
        if act == 0:
            self.forward()
        elif act == 1:
            self.backward()
        elif act == 2:
            self.right()
        else:
            self.left()

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


    for car in cars:
        car.draw(win)


    for obstacle in obstacles:
        win.blit(obstacle.obstacle_image, (obstacle.x, obstacle.y))


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
    act_time = 0


    clock = pygame.time.Clock()
    run = True
    while run and len(cars) > 0:
        clock.tick(60)

        act_time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        if act_time == 5:
            act_time = 0
            for car in cars:
                car.random_act()



                for obs in obstacles:
                    offset = (int(car.pozycja[0] - obs.x),int(car.pozycja[1] - obs.y))
                    result = obs.obstacle_mask.overlap(car.body_mask, offset)
                    if result:
                        print(car.num)
                        car.num = car.num + 1
        for car in cars:
            car.update()
        screen.blit(map, (0, 0))
        draw_window(screen, cars, obstacles)
        pygame.display.flip()
        clock.tick(0)

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    print('\nBest genome:\n{!s}'.format(winner))

########################################################################################################################
########################################################################################################################
########################################################################################################################

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
