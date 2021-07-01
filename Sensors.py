import math
from shapely.geometry import Polygon, LineString

class Sensors():
    def __init__(self, car, parked_car_list, parking_block_list):

        self.object_list = []
        #TABLICA DO PRZEKAZANIA DLA AI
        self.lengths = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
        self.sensor = []
        self.point_angle = [360, 340, 300, 240, 200, 180, 160, 120, 60, 20]
        self.length = 200

        #self.create_sensors_endpoints(car)
        self.add_obstacles(parked_car_list, parking_block_list)
        #self.draw_sensors(car)
        #wywołanie metody, która rysuje punkt w miejscu przecięcia linii z poligonem
        #self.distance_point(car)

    def add_obstacles(self, parked_car_list, parking_block_list):
        for x in parked_car_list:
            self.object_list.append(x)

        for x in parking_block_list:
            self.object_list.append(x)

    def create_sensors_endpoints(self, car):
        for x in self.point_angle:
            tabx = car.center_x + math.cos(math.radians(x - (-car.angle))) * self.length
            taby = car.center_y + math.sin(math.radians(x - (-car.angle))) * self.length
            tab = [tabx, taby]
            self.sensor.append(tab)

    def draw_sensors(self, car):
        self.create_sensors_endpoints(car)
        #rysowanie linii
        for n, x in enumerate(self.sensor):
            arcade.draw_line(car.center_x, car.center_y,
                             x[0], x[1],
                             arcade.color.RED, 2)

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
                self.lengths[x] = self.intersect.length
                print(self.lengths[x])
                coordinate_x = car.center_x + math.cos(math.radians(self.point_angle[x] - (-car.angle))) * (200 - self.lengths[x])
                coordinate_y = car.center_y + math.sin(math.radians(self.point_angle[x] - (-car.angle))) * (200 - self.lengths[x])
                arcade.draw_circle_filled(coordinate_x, coordinate_y, 5, arcade.color.GREEN)

    #mierzenie odległości metodą punktową
    #(ma dziwne problemy z utrzymaniem punktu w jednym miejscu,
    # zdaża się że punkt przeskakuje z jednego boku poligonu na inny,
    # co psuje pomiar)
    def distance_point(self, car):
        for n, endline in enumerate(self.sensor):
            #pojedyncza linia wyznaczona z punktu początkowego i końcowego
            self.l = LineString([[car.center_x, car.center_y], [endline[0], endline[1]]])
            #sprawdzanie czy linia przecina poligon
            for kek in self.object_list:
                self.p = Polygon(kek.get_adjusted_hit_box())
                self.intersect = self.l.intersection(self.p).representative_point()

                if self.intersect:
                    arcade.draw_circle_filled(self.intersect.x, self.intersect.y, 5, arcade.color.GREEN)

                    car_center = [car.center_x, car.center_y]
                    center = [self.intersect.x, self.intersect.y]

                    #self.lengths[n] = math.dist(car_center, center)
