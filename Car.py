import arcade
import math
"""
car.acceleration()
car.break()
car.right()
car.left()
car.deacceleration()
"""

class Car(arcade.Sprite):
    def __init__(self,image,scale):

        super().__init__(image,scale)

        self.max_speed = 8.0
        self.min_speed = -2.0
        self.current_speed = 0.0
        self.accelerate= 0.1
        self.friction = 0.05
        self.angle_speed = 0.1
        self.car_stop = 0.0
        self.break_speed = -1.0
        self.back_accelerate = -0.2

    def acceleration(self):
        if self.current_speed < self.max_speed:
            self.current_speed += self.accelerate
        else:
            self.current_speed = self.max_speed

    def deacceleration(self):
            if self.current_speed < self.car_stop:
                if self.current_speed + self.friction > self.car_stop:
                    self.current_speed = self.car_stop
                else:
                    self.current_speed += self.friction
            elif self.current_speed > self.car_stop:
                if self.current_speed - self.friction < self.car_stop:
                    self.current_speed = self.car_stop
                else:
                    self.current_speed -= self.friction

    def car_break_back(self):
        if self.current_speed > self.car_stop:
            self.current_speed += self.break_speed
        else:
            if self.current_speed > self.min_speed:
                self.current_speed += self.back_accelerate
            else:
                self.current_speed = self.min_speed

    def right(self):
        if self.current_speed == self.car_stop:
            pass
        elif self.current_speed > self.car_stop:
            self.change_angle = -self.angle_speed * self.current_speed
        else:
            self.change_angle = self.angle_speed * self.current_speed

    def left(self):
        if self.current_speed == self.car_stop:
            pass
        elif self.current_speed > self.car_stop:
            self.change_angle = self.angle_speed * self.current_speed
        else:
            self.change_angle = -self.angle_speed * self.current_speed

    def stop_angle(self):
        self.change_angle = 0

    def update(self):
        angle_rad = math.radians(self.angle)
        self.angle += self.change_angle
        if self.current_speed != self.car_stop:
            self.center_x += -self.current_speed * math.sin(angle_rad)
            self.center_y += self.current_speed * math.cos(angle_rad)


