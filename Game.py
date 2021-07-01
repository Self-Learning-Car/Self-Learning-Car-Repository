import pygame
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

        print('ruch')

    def eval_genomes(self):

        cars = []

        cars.append(Car.Car())

        pygame.init()
        window = pygame.display.set_mode((self.win_width, self.win_heigth))
        clock = pygame.time.Clock()

        for car in cars:
            car.draw(window)


        run = True
        while run:
            clock.tick(60)
            window.blit(self.backround,[0,0])
            self.action_time += 1
            self.time += 1


            for car in cars:
                if self.action_time == 5:
                    self.action_time = 0
                    if self.time < 80:
                        self.control_ai(car,1)
                    elif self.time > 80 and self.time < 90:
                        self.control_ai(car,2)
                    elif self.time > 90 and self.time < 100:
                        self.control_ai(car,0)
                    else:
                        self.control_ai(car, 6)


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


                car.update()
                car.draw(window)
                #pygame.draw.circle(window, center=[car.center_x, car.center_y], radius=10, color=[255, 0, 0, 255])

            pygame.display.flip()
            clock.tick(0)

