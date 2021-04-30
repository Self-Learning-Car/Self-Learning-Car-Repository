import arcade
import math

class Car(arcade.Sprite):
    def __init__(self,image,scale):

        super().__init__(image,scale, hit_box_algorithm='Detailed', hit_box_detail=4)

        # Maksymalna prędkość pojazdu.
        self.max_speed = 8.0
        # Maksymalna prędkość cofania się.
        self.min_speed = -2.0
        # Obecna prędkość pojazdu.
        self.current_speed = 0.0
        # Wartość przyśpieszenia.
        self.accelerate= 0.1
        # Wartość spowolnienia.
        self.deaccelerate = 0.05
        # Szybkość obracania.
        self.angle_speed = 0.1
        # Wartość przy ktorej samochód się nie porusza.
        self.car_stop = 0.0
        # Szybkość hamowania.
        self.break_speed = -0.5
        # Przyśpieszenie cofania.
        self.back_accelerate = -0.2
        # Czy pojazd jest w trakcie hamowania (używane w Game przy sterowaniu).
        self.is_breaking = False

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
        if self.current_speed == self.car_stop:
            pass
        elif self.current_speed > self.car_stop:
            self.change_angle = -self.angle_speed * self.current_speed
        else:
            self.change_angle = -self.angle_speed * self.current_speed

    def left(self):
        """
        Metoda odpowiedzialna za skręt w lewo.
        """
        if self.current_speed == self.car_stop:
            pass
        elif self.current_speed > self.car_stop:
            self.change_angle = self.angle_speed * self.current_speed
        else:
            self.change_angle = self.angle_speed * self.current_speed

    def stop_angle(self):
        """
        Metoda odpowiedzialna za zatzymanie skręcania się pojazdu.
        """
        self.change_angle = 0

    def update(self):
        """
        Metoda odpowiedzialna za zmianę pozycji pojazdu.
        """
        angle_rad = math.radians(self.angle)
        self.angle += self.change_angle
        if self.current_speed != self.car_stop:
            self.center_x += -self.current_speed * math.sin(angle_rad)
            self.center_y += self.current_speed * math.cos(angle_rad)


