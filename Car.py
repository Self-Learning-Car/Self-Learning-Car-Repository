import pygame
import math
import numpy
from shapely.geometry import Polygon

class Car():
    def __init__(self, width,height,x,y,image):

#165 82
        self.image = pygame.image.load(image)

        #self.surface = pygame.image.load(asset)
        self.width = width
        self.height = height
        #self.rotate_surface = self.surface
        self.center_x = x
        self.center_y = y
        self.polygon = Polygon([(0,0), (0,0), (0,0), (0,0)])
        self.distance = math.sqrt((1140 - self.center_x)**2 + (230-self.center_y)**2)
        self.bug = 0


        self.pressed_up = False
        self.pressed_down = False
        self.pressed_left = False
        self.pressed_right = False


        # Maksymalna prędkość pojazdu.
        self.max_speed = 8.0
        # Maksymalna prędkość cofania się.
        self.min_speed = -5.0
        # Obecna prędkość pojazdu.
        self.current_speed = 0.0
        # Wartość przyśpieszenia.
        self.accelerate= 0.3
        # Wartość spowolnienia.
        self.deaccelerate = 0.3
        # Szybkość obracania.
        self.angle_speed = 30
        # Wartość przy ktorej samochód się nie porusza.
        self.car_stop = 0.0
        # Szybkość hamowania.
        self.break_speed = -0.5
        # Przyśpieszenie cofania.
        self.back_accelerate = -0.8
        # Czy pojazd jest w trakcie hamowania (używane w Game przy sterowaniu).
        self.is_breaking = False
        # Czy pojazd jest zaparkowany
        self.is_parked = False

        self.heading = 0
        self.car_position = numpy.array([self.center_x, self.center_y])
        self.wheel_base = 165-20
        self.front_wheel = numpy.array([None,None])
        self.back_wheel = numpy.array([None,None])
        self.steer_angle = 0


    def acceleration(self):
        """
        Metoda odpowiadająca za zwiększenie prędkości samochodu "current_speed" o zmienną "accelerate" aż do osiągnięcia
        maksymalnej prędkości "max_speed".
        """
        if self.current_speed < self.max_speed:
            self.current_speed += self.accelerate
        else:
            self.current_speed = self.max_speed

    def deacceleration(self):
        """
        Metoda odpowiadająca za prędkości "current_speed" o zmienną "deaccelerate" aż do zatrzymania się (osiągnięcia
        prędkości "car_stop"), odczuwalną po puszczeniu klawisza odpowiedzialnego za jazdę/cofanie.
        """
        if self.current_speed < self.car_stop:
            if self.current_speed + self.deaccelerate > self.car_stop:
                self.current_speed = self.car_stop
            else:
                self.current_speed += self.deaccelerate
        elif self.current_speed > self.car_stop:
            if self.current_speed - self.deaccelerate < self.car_stop:
                self.current_speed = self.car_stop
            else:
                self.current_speed -= self.deaccelerate

    def car_break(self):
        """
        Metoda odbowiedzialna za hamowanie, w postaci zmniejszenia prędkości "current_speed" o zmienną "break_speed" aż
        do zatrzymania (osiągnięcia prędkości "car_stop").
        """
        self.current_speed += self.break_speed
        if self.current_speed <= self.car_stop:
            self.current_speed = self.car_stop

    def car_back(self):
        """
        Metoda odpowiedzialna za cofanie się, w postaci zmiany prędkości "current_speed" o zmienną "back_accelerate" aż
        do osiągnięcia maksymalnej prędkości cofania "min_speed".
        """
        if self.current_speed > self.min_speed:
            self.current_speed += self.back_accelerate
        else:
            self.current_speed = self.min_speed


    def right(self):
        """
        Metoda odpowiedzialna za skręt w prawo.
        """
        if self.current_speed != 0:
            self.steer_angle = -self.angle_speed

    def left(self):
        """
        Metoda odpowiedzialna za skręt w lewo.
        """
        if self.current_speed != 0:
            self.steer_angle = self.angle_speed

    def stop_angle(self):
        """
        Metoda odpowiedzialna za zatzymanie skręcania się pojazdu.
        """
        self.steer_angle = 0

    def update(self):
        """
        Metoda odpowiedzialna za zmianę pozycji pojazdu.
        """
        if self.current_speed != 0:



            self.front_wheel = self.car_position + self.wheel_base/2 * numpy.array([math.cos(math.radians(self.heading)),math.sin(math.radians(self.heading))])
            self.back_wheel = self.car_position - self.wheel_base/2* numpy.array([math.cos(math.radians(self.heading)),math.sin(math.radians(self.heading))])

            self.back_wheel += self.current_speed * numpy.array([math.cos(math.radians(self.heading)),math.sin(math.radians(self.heading))])
            self.front_wheel += self.current_speed * numpy.array([math.cos(math.radians(self.heading+self.steer_angle)),math.sin(math.radians(self.heading+self.steer_angle))])

            self.car_position = (self.front_wheel + self.back_wheel)/2
            self.heading = math.degrees(math.atan2(self.front_wheel[1]-self.back_wheel[1],self.front_wheel[0]-self.back_wheel[0]))

            self.center_x = self.car_position[0]
            self.center_y = self.car_position[1]


            #self.rotate_surface = self.rot_center(self.surface, -self.heading)

    def draw(self,screen):
        #screen.blit(self.rotate_surface,[self.center_x-82.5,self.center_y-41]) # do zoe
        self.blitRotateCenter(screen,self.image,[self.center_x-self.width/2,self.center_y-self.height/2],-self.heading)

    def blitRotateCenter(self, surf, image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

        surf.blit(rotated_image, new_rect)

    def uptade_polygon(self):
        cordx = self.center_x + math.cos(math.radians(25 - (-self.heading))) * 80
        cordy = self.center_y + math.sin(math.radians(25 - (-self.heading))) * 80
        cord = (cordx, cordy)

        cordx1 = self.center_x + math.cos(math.radians(335 - (-self.heading))) * 80
        cordy1 = self.center_y + math.sin(math.radians(335 - (-self.heading))) * 80
        cord1 = (cordx1, cordy1)

        cordx3 = self.center_x + math.cos(math.radians(205 - (-self.heading))) * 80
        cordy3 = self.center_y + math.sin(math.radians(205 - (-self.heading))) * 80
        cord3 = (cordx3, cordy3)

        cordx2 = self.center_x + math.cos(math.radians(155 - (-self.heading))) * 80
        cordy2 = self.center_y + math.sin(math.radians(155 - (-self.heading))) * 80
        cord2 = (cordx2, cordy2)

        self.polygon = Polygon([cord,cord1,cord3,cord2])

