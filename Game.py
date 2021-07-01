import math
import sys
from shapely.geometry import Polygon
import pygame
from pygame.rect import Rect

import Car
import Parking
import Sensors
import neat

import random

win_width = 1900
win_heigth = 1000
backround = pygame.image.load("assets/Map.png")
WIN = pygame.display.set_mode((win_width,win_heigth))



class Game():
    def __init__(self):
        self.win_width = 1900
        self.win_heigth = 1000
        self.backround = pygame.image.load("assets/Map.png")
        self.action_time = 0
        self.time = 0
        self.parking = Parking.Parking()
        self.spawn_points = [(1, 430, 230), (2, 572, 230), (3, 714, 230), (4, 856, 230), (5, 998, 230), (6, 1140, 230),
                             (7, 1282, 230),
                             (8, 1424, 230), (9, 1566, 230), (10, 430, 780), (11, 572, 780), (12, 714, 780),
                             (13, 856, 780), (14, 998, 780),
                             (15, 1140, 780), (16, 1282, 780), (17, 1424, 780), (18, 1566, 780)]
        self.org_distance = math.sqrt((1140 - 100)**2 + (230-500)**2)


    def action(self,value):
        if value <= -0.72:
            return 0
        elif  -0.72 < value <= -0.44:
            return 1
        elif -0.44 < value <= -0.16:
            return 3
        elif -0.16 < value <= 0.12:
            return 4
        elif 0.12 < value <= 0.4:
            return 2
        elif 0.4 < value <= 0.68:
            return 5
        elif 0.68 < value <= 0.96:
            return 6
        else:
            return 0

    def control_ai(self, car, action):
        moves = [[False, False, False, False],
                 [True, False, False, False],
                 [False, True, False, False],
                 [True, False, True, False],
                 [True, False, False, True],
                 [False, True, True, False],
                 [False, True, False, True]]

        move = moves[action]
        car.pressed_up = move[0]
        car.pressed_down = move[1]
        car.pressed_right = move[2]
        car.pressed_left = move[3]


    def park(self,car,park_place,lanes):
        prize = False
        if car.polygon.intersects(park_place):
            prize = True
            for lane in lanes:
                if car.polygon.intersects(lane):
                    prize = False
        return prize



def eval_genomes(genomes,config):
    global WIN, backround
    game = Game()
    game.time = 0


    nets = []
    cars = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = game.org_distance
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car.Car(165,82,100,500,"assets/Car_mini.png"))
        ge.append(genome)


    print(len(cars))


    pygame.init()
    window = WIN
    window.blit(backround, [0, 0])
    clock = pygame.time.Clock()
    delta = 0.0
    max_tps = 60

    for car in cars:
        car.draw(WIN)


    parking_block = []
    game.parking.add_parking_block(parking_block)
    parking_place = []
    parking_lane = []
    game.parking.add_parking_slot_ai(parking_place,parking_lane,"assets/Empty.png")
    game.parking.add_slot_border(parking_lane)

    for par in parking_block:
        par.update_polygon()
    for par in parking_place:
        par.update_polygon()
    for par in parking_lane:
        par.update_polygon()

    parked_cars = []
    for spawn in game.spawn_points:
        if spawn[0]==6:
            pass
        else:
            new_car = Car.Car(82, 165, spawn[1], spawn[2], "assets/Car1.png")
            new_car.image = pygame.transform.scale(new_car.image,[new_car.width,new_car.height])
            new_car.uptade_polygon()
            parked_cars.append(new_car)



    print("1")
    run = True
    while run and len(cars)>0:
        delta += clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        clock.tick(60)

        game.action_time += 1
        game.time += 1

        for x, car in enumerate(cars):
            ge[x].fitness = game.org_distance - car.distance

            if game.action_time == 5:
                game.action_time = 0

                inp = [random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),car.distance]

                inputs = 0 # do zrobienia
                output = nets[cars.index(car)].activate(inp)

                game.control_ai(car,game.action(output[0]))

            if car.pressed_up == True and car.pressed_down == False:
                car.acceleration()
            if car.pressed_up == False and car.pressed_down == False:
                    car.deacceleration()
            if car.pressed_down == True and car.pressed_up == False and \
                    car.current_speed > car.car_stop:
                car.car_break()
                car.is_breaking = True
            if car.pressed_down == False:
                car.is_breaking = False
            if car.pressed_down == True and car.is_breaking == False:
                car.car_back()
            if car.pressed_left == True and car.pressed_right == False:
                car.left()
            if car.pressed_right == True and car.pressed_left == False:
                car.right()
            if (car.pressed_right == False and car.pressed_left == False) or car.is_breaking == True:
                car.stop_angle()

          #  for x,car in enumerate(cars):
           #     for park in parked_cars:
           #         if car.polygon.intersects(park.polygon):
           #             ge[x].fitness -= 2000
           #             nets.pop(cars.index(car))
           #             ge.pop(cars.index(car))
          #              cars.pop(cars.index(car))


            #for x,car in enumerate(cars):
            #   for block in parking_block:
             #      if car.polygon.intersects(block):
             #           car.bug += 1
             #           if car.bug > 1:
             #               ge[x].fitness -= 2000
             #               nets.pop(cars.index(car))
              #              ge.pop(cars.index(car))
             #               cars.pop(cars.index(car))

        #    for x,car in enumerate(cars):
        #        if game.park(car,parking_place,parking_lane):
         #           ge[x].fitness += 1000
         #           nets.pop(cars.index(car))
         #           ge.pop(cars.index(car))
         #           cars.pop(cars.index(car))


        print(game.time)
        if game.time > 800:
            
            for car in cars:
                nets.pop(cars.index(car))
                ge.pop(cars.index(car))
                cars.pop(cars.index(car))

        car.update()
        car.uptade_polygon()

        car.draw(window)
                    #pygame.draw.circle(window, center=[car.center_x, car.center_y], radius=10, color=[255, 0, 0, 255])
        for par in parking_block:
            par.draw(WIN)
        for par in parking_place:
            par.draw(WIN)
        for par in parking_lane:
            par.draw(WIN)
        for car in parked_cars:
            car.draw(WIN)
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

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 10)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))