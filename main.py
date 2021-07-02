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
        self.image = pygame.image.load("assets/Car_red_lite.png")
        self.image = pygame.transform.scale(self.image,(120,120))
        self.body_image = self.image.convert_alpha()
        self.body_mask = pygame.mask.from_surface(self.body_image)
        self.body = self.body_image.get_rect()
        self.rect = self.body_image.get_rect()

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

    def draw(self, win):
        self.blitRotateCenter(win,self.body_image,self.pozycja,self.angle)


    def update(self):
        self.pozycja[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.pozycja[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        #self.rect.move(self.pozycja[0]-self.width/2,self.pozycja[1]-self.height/2)



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

    def random_act(self,act):
        
        if act == 0:
            self.forward()
        elif act == 1:
            self.backward()
        elif act == 2:
            self.right()
        elif act == 3:
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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = 'assets/Parking.png'
        self.parking_image = pygame.image.load(self.sprite).convert_alpha()
        self.parking_mask = pygame.mask.from_surface(self.parking_image)
        self.parking_body = self.parking_image.get_rect()
        self.naparkingu = False

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

########################################################################################################################
########################################################################################################################
########################################################################################################################

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
############################################################################


#rysujemy auta itp
def draw_window(win, cars, obstacles):


    for car in cars:
        car.draw(win)


    for obstacle in obstacles:
        win.blit(obstacle.obstacle_image, (obstacle.x, obstacle.y))


def eval_genomes(genomes, config):
    global generation

    distance = math.sqrt((160 - 856) ** 2 + (560 - 774) ** 2)

    cars = []
    ge = []
    nets = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car())
        ge.append(genome)

    for car in cars:
        car.distance_b = distance


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
                            [535, 695],
                            [675, 695],
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

    parking_lines_sprites = [['assets/parking_line.png'],
                             ['assets/parking_line2.png'],
                             ['assets/parking_line3.png']]

    parking_lines_cords = [[766, 671],
                           [914, 671],
                           [762, 653]]

    parking_lines = []
    for n, x in enumerate(parking_lines_cords):
        parking_lines.append(Parkingline(parking_lines_sprites[n][0], x[0], x[1]))

    obstacles = []
    for x in parked_car_placement:
        obstacles.append(Obstacle(x[0], x[1]))

    for n, x in enumerate(border_placement):
        obstacles.append(Border(border_sprites[n][0], x[0], x[1]))

    parking = Prize(800, 675)

    pygame.init()
    screen = pygame.display.set_mode((1900, 1000))
    screen.blit(parking.parking_image, (parking.x, parking.y))
    map = pygame.image.load('assets/Map.png')
    act_time = 0
    generation += 1

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









        if act_time == 3:
            act_time = 0
            for x, car in enumerate(cars):
                prize = car.distance_b - car.distance(856,774)
                ge[x].fitness += prize * 3
                car.distance_b = car.distance(856,774)
                car.numver_of_moves += 1



                #inputs = [car.speed,car.angle,car.pozycja[0],car.pozycja[1],car.distance(520,700)]

                output = nets[cars.index(car)].activate((car.speed,car.angle,car.pozycja[0],car.pozycja[1],car.distance(856,774),car.distance(710,774),car.distance(1000,774)))
                i = output.index(max(output))


                if i == 0:

                    car.forward()
                elif i == 1:
                    car.backward()
                elif i == 2:
                    car.left()
                elif i ==3 :
                    car.right()

                for parking_line in parking_lines:
                    screen.blit(parking_line.parkline_image, (parking_line.x, parking_line.y))
                    offset = (int(car.pozycja[0]- parking_line.x), int(car.pozycja[1] - parking_line.y))
                    result = parking_line.parkline_mask.overlap(car.body_mask, offset)
                    if result:
                        car.na_lini = True
                    else:
                        car.na_lini = False

                offset = (int(car.pozycja[0] - parking.x), int(car.pozycja[1] - parking.y))
                result = parking.parking_mask.overlap(car.body_mask, offset)
                if result:
                    car.na_parkingu = True
                else:
                    car.na_parkingu= False



                for obs in obstacles:
                    offset = (int(car.pozycja[0] - obs.x),int(car.pozycja[1] - obs.y))
                    result = obs.obstacle_mask.overlap(car.body_mask, offset)
                    if result:
                        car.to_delete = True
                        ge[x].fitness -= -50

                if car.na_parkingu and not car.na_lini:
                    ge[x].fitness += 500



                if car.numver_of_moves > 100:
                    car.to_delete = True
                    ge[x].fitness -= 500

                if car.to_delete:
                    nets.pop(cars.index(car))
                    ge.pop(cars.index(car))
                    cars.pop(cars.index(car))


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
    config_path = os.path.join(local_dir, 'config_feedforward.txt')
    run(config_path)


