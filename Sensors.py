import arcade
import math

from shapely.geometry import LineString, Polygon

from arcade import create_line_loop
from shapely.geometry import Polygon, LineString
import random

class Sensors():
    def __init__(self, car, parked_car_list, parking_block_list):

        self.object_list = []

        for x in parked_car_list:
            self.object_list.append(x)

        for x in parking_block_list:
            self.object_list.append(x)

        self.lenghts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        lenght = 200
        #lenght_front = 200

        sensor = [[car.center_x + math.cos(math.radians(360 - (-car.angle))) * lenght,
                  car.center_y + math.sin(math.radians(360 - (-car.angle))) * lenght],
                  [car.center_x + math.cos(math.radians(340 - (-car.angle))) * lenght,
                  car.center_y + math.sin(math.radians(340 - (-car.angle))) * lenght],
                  [car.center_x + math.cos(math.radians(300 - (-car.angle))) * lenght,
                  car.center_y + math.sin(math.radians(300 - (-car.angle))) * lenght],
                  [car.center_x + math.cos(math.radians(240 - (-car.angle))) * lenght,
                  car.center_y + math.sin(math.radians(240 - (-car.angle))) * lenght],
                  [car.center_x + math.cos(math.radians(200 - (-car.angle))) * lenght,
                  car.center_y + math.sin(math.radians(200 - (-car.angle))) * lenght],
                  [car.center_x + math.cos(math.radians(180 - (-car.angle))) * lenght,
                  car.center_y + math.sin(math.radians(180 - (-car.angle))) * lenght],
                  [car.center_x + math.cos(math.radians(160 - (-car.angle))) * lenght,
                  car.center_y + math.sin(math.radians(160 - (-car.angle))) * lenght],
                  [car.center_x + math.cos(math.radians(120 - (-car.angle))) * lenght,
                  car.center_y + math.sin(math.radians(120 - (-car.angle))) * lenght],
                  [car.center_x + math.cos(math.radians(60 - (-car.angle))) * lenght,
                  car.center_y + math.sin(math.radians(60 - (-car.angle))) * lenght],
                  [car.center_x + math.cos(math.radians(20 - (-car.angle))) * lenght,
                  car.center_y + math.sin(math.radians(20 - (-car.angle))) * lenght]]

        self.point_angle = [360, 340, 300, 240, 200, 180, 160, 120, 60, 20]

        #wywołanie metody, która rysuje punkt w miejscu przecięcia linii z poligonem
        self.distance_point(sensor, car, parked_car_list)

    #mierzenie odległości metodą odległościową
    #(wyglądowo działa płynnie, ale ma te same problemy co metoda punktowa)
    def distance(self, sensor, car, parked_car_list):
        for n, x in enumerate(sensor):
            arcade.draw_line(car.center_x, car.center_y,
                             x[0], x[1],
                             arcade.color.RED, 2)

        for x, endline in enumerate(sensor):
            self.l = LineString([[car.center_x, car.center_y], [endline[0], endline[1]]])
            for kek in parked_car_list:
                self.p = Polygon(kek.get_adjusted_hit_box())
                self.intersect = self.l.intersection(self.p)
                self.lenghts[x] = self.intersect.length
                print(self.lenghts[x])
                coordinate_x = car.center_x + math.cos(math.radians(self.point_angle[x] - (-car.angle))) * (200 - self.lenghts[x])
                coordinate_y = car.center_y + math.sin(math.radians(self.point_angle[x] - (-car.angle))) * (200 - self.lenghts[x])
                arcade.draw_circle_filled(coordinate_x, coordinate_y, 5, arcade.color.GREEN)




        pass

    #mierzenie odległości metodą punktową
    #(ma dziwne problemy z utrzymaniem punktu w jednym miejscu,
    # zdaża się że punkt przeskakuje z jednego boku poligonu na inny,
    # co psuje pomiar)
    def distance_point(self, sensor, car, parked_car_list):
        #rysowanie linii
        for n, x in enumerate(sensor):
            arcade.draw_line(car.center_x, car.center_y,
                             x[0], x[1],
                             arcade.color.RED, 2)

        for endline in sensor:
            #pojedyncza linia wyznaczona z punktu początkowego i końcowego
            self.l = LineString([[car.center_x, car.center_y], [endline[0], endline[1]]])
            #sprawdzanie czy linia przecina poligon
            for kek in self.object_list:
                self.p = Polygon(kek.get_adjusted_hit_box())
                self.intersect = self.l.intersection(self.p).representative_point()
                list(self.intersect.coords)

                if self.intersect:
                    arcade.draw_circle_filled(self.intersect.x, self.intersect.y, 5, arcade.color.GREEN)
        pass
