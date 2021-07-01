import sys
from shapely.geometry import Polygon
import pygame
from pygame.rect import Rect

import Car
import Parking
import Sensors
import neat

import random





class Game():
    def __init__(self):
        self.win_width = 1900
        self.win_heigth = 1000
        self.backround = pygame.image.load("assets/Map.png")
        self.action_time = 0
        self.time = 0
        self.parking = Parking.Parking()


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


    def eval_genomes(self):

        cars = []

        cars.append(Car.Car([255,0,0,255],165,82))
        cars[0].image = pygame.image.load("assets/Car_mini.png")

        pygame.init()
        window = pygame.display.set_mode((self.win_width, self.win_heigth))
        clock = pygame.time.Clock()
        delta = 0.0
        max_tps = 60

        for car in cars:
            car.draw(window)


        parking_block = []
        self.parking.add_parking_block(parking_block)
        parking_place = []
        self.parking.add_parking_slot(parking_place)
        parking_lane = []
        self.parking.add_parking_lane(parking_lane)
        self.parking.add_slot_border(parking_lane)
        for par in parking_block:
            par.update_polygon()
        for par in parking_place:
            par.update_polygon()
        for par in parking_lane:
            par.update_polygon()


        run = True
        while run:
            delta += clock.tick(60)
            while delta > 1 / max_tps:
                delta -= 1 / max_tps
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit(0)
                clock.tick(60)
                window.blit(self.backround,[0,0])
                self.action_time += 1
                self.time += 1


                for car in cars:
                    if self.action_time == 5:
                        self.action_time = 0
                        if self.time < 80:
                            self.control_ai(car,1)
                        else:
                            self.control_ai(car, 3)

                    print(-car.heading)

                    car.uptade_polygon()
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


                    for i in parking_block:
                        if car.polygon.intersects(i.polygon):
                            print('kek')


                    car.update()

                    car.draw(window)
                    #pygame.draw.circle(window, center=[car.center_x, car.center_y], radius=10, color=[255, 0, 0, 255])
                for par in parking_block:
                    par.draw(window)
                for par in parking_place:
                    par.draw(window)
                for par in parking_lane:
                    par.draw(window)
                pygame.display.flip()
                clock.tick(0)

