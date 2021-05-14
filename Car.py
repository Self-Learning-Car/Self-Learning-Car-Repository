import arcade
import math
import numpy


class Car(arcade.Sprite):
    def __init__(self, image, scale):

        super().__init__(image, scale, hit_box_algorithm='Detailed', hit_box_detail=4)

        # Maksymalna prędkość pojazdu.
        self.max_speed = 8.0
        # Maksymalna prędkość cofania się.
        self.min_speed = -2.0
        # Obecna prędkość pojazdu.
        self.current_speed = 0.0
        # Wartość przyśpieszenia.
        self.accelerate = 0.1
        # Wartość spowolnienia.
        self.deaccelerate = 0.05
        # Wartość przy ktorej samochód się nie porusza.
        self.car_stop = 0.0
        # Szybkość hamowania.
        self.break_speed = -0.5
        # Przyśpieszenie cofania.
        self.back_accelerate = -0.2
        # Czy pojazd jest w trakcie hamowania (używane w Game przy sterowaniu).
        self.is_breaking = False
        # Czy pojazd jest zaparkowany.
        self.is_parked = False
        # Kierunek w który jest odwrócony samochód (użyte przy symulacji kół, wartości ustalane w metodzie
        # update_wheels()).
        self.heading = None
        # Pozycja samochodu jako wektor numpy (użyte przy symulacji kół, wartości ustalane w metodzie uptade_wheels()).
        self.car_position = numpy.array([None, None])
        # Odleglosc między kołami.
        self.wheel_base = self.width - 20
        # Pozyjca przednich koł jako wektor (wartości ustalone są w metodzie update()).
        self.front_wheel = numpy.array([None, None])
        # Pozycja tylnych kół jako wektor (wartości ustalone są w metodzie update()).
        self.back_wheel = numpy.array([None, None])
        # Kąt obrócenia przednich kół.
        self.steer_angle = 0
        # Liczba o jaką mogą obrócić się koła.
        self.steer_angle_range = 15

    def update_wheels(self):
        """
        Metoda służąca do zaktualizowania wektoru pozycji oraz kierunku samochodu
        """
        self.car_position[0] = self.center_x
        self.car_position[1] = self.center_y
        self.heading = self.angle

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
        Metoda odpowiedzialna za skręt kół w prawo.
        """
        self.steer_angle = -self.steer_angle_range

    def left(self):
        """
        Metoda odpowiedzialna za skręt kół w lewo.
        """
        self.steer_angle = self.steer_angle_range

    def stop_angle(self):
        """
        Metoda odpowiedzialna za zatrzymanie skręcania kół.
        """
        self.steer_angle = 0

    def update(self):
        """
        Metoda odpowiedzialna za zmianę pozycji pojazdu.
        """
        if self.current_speed != 0:
            self.front_wheel = self.car_position + self.wheel_base / 2 * \
                               numpy.array([math.cos(math.radians(self.heading)), math.sin(math.radians(self.heading))])
            self.back_wheel = self.car_position - self.wheel_base / 2 * \
                              numpy.array([math.cos(math.radians(self.heading)), math.sin(math.radians(self.heading))])
            self.back_wheel += self.current_speed * \
                               numpy.array([math.cos(math.radians(self.heading)), math.sin(math.radians(self.heading))])
            self.front_wheel += self.current_speed * numpy.array(
                [math.cos(math.radians(self.heading + self.steer_angle)),
                 math.sin(math.radians(self.heading + self.steer_angle))])
            self.car_position = (self.front_wheel + self.back_wheel) / 2
            self.heading = math.degrees(
                math.atan2(self.front_wheel[1] - self.back_wheel[1], self.front_wheel[0] - self.back_wheel[0]))
            self.center_x = self.car_position[0]
            self.center_y = self.car_position[1]
            self.angle = self.heading
