import arcade
import Car
import Parking
import Sensors


import random



class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.parking = Parking.Parking()


        #widok hitboxów
        self.hitbox_visible = True

        self.action = None
        # Zmienne mówiące o tym czy dany klawisz jest wciśnięty.
        self.pressed_up = False
        self.pressed_down = False
        self.pressed_right = False
        self.pressed_left = False

        # Zmienne dotyczące tworzenia zaparokwanych samochodów.
        self.random_car_placement = False
        self.random_car_number = False
        self.parked_car_number = 15

        # Pozycje zaparkowanych samochodów, pierwsza wartość oznacz miejscie (liczone od lewa do prawa zaczynając od
        # dołu, druga pozycje x, trzecia pozycje y.
        self.spawn_points = [(1,430,230),(2,572,230),(3,714,230),(4,856,230),(5,998,230),(6,1140,230),(7,1282,230),
                             (8,1424,230),(9,1566,230),(10,430,780),(11,572,780),(12,714,780),(13,856,780),(14,998,780),
                             (15,1140,780),(16,1282,780),(17,1424,780),(18,1566,780)]

        arcade.set_background_color(arcade.color.AMAZON)

        self.setup()
        arcade.run()

        # If you have sprite lists, you should create them here,
        # and set them to None

        self.player_car_list = None
        self.car_sprite = None
        self.car_sensors_list = None

        self.parked_car_list = None
        self.parked_car_sprite = None
        self.parking_slot_list = None
        self.parking_line_list = None
        self.parking_block_list = None
        self.parking_slot_border_list = None

		# Pozycje zaparkowanych samochodów, pierwsza wartość oznacz miejscie (liczone od lewa do prawa zaczynając od
        # dołu), druga pozycje x, trzecia pozycje y.
        self.spawn_points = [(1, 430, 230), (2, 572, 230), (3, 714, 230), (4, 856, 230), (5, 998, 230), (6, 1140, 230),
                             (7, 1282, 230), (8, 1424, 230), (9, 1566, 230),
                             (10, 430, 780), (11, 572, 780), (12, 714, 780), (13, 856, 780), (14, 998, 780),
                             (15, 1140, 780), (16, 1282, 780), (17, 1424, 780), (18, 1566, 780)]

    def car_spawn(self):
        """
        Funkcja odpowiadająca za utrzworzenie zaparkowanych samochodów, zależna od: "random_car_placement" mówiące czy
        ustawienie samochodów ma być losowe czy wcześniej z góry ustalone, "random_car_number" mówiąące czy liczba
        samochodów ma być losowa czy z góry ustalona, "parked_car_number" mówiące ile samochodów ma zostać utworzonych.
        """
        if self.random_car_placement:
            if self.random_car_number:
                cars_to_spawn = random.sample(self.spawn_points,random.randrange(0,len(self.spawn_points)-1))
            else:
                cars_to_spawn = random.sample(self.spawn_points,self.parked_car_number)
        else:
            number = 0
            cars_to_spawn = []
            for spawn_point in self.spawn_points:
                if spawn_point[0] in [3]:
                    pass
                else:
                    cars_to_spawn.append(spawn_point)
        for spawn_point in cars_to_spawn:
            if number < 10:
                pass
            else:
                number = 0
            number += 1
            self.parked_car_sprite = Car.Car(f"assets/Car{number}.png", 0.15)
            self.parked_car_sprite.center_x = spawn_point[1]
            self.parked_car_sprite.center_y = spawn_point[2]
            self.parked_car_list.append(self.parked_car_sprite)
            self.car_sprite.draw_hit_box

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        self.player_car_list = arcade.SpriteList()
        self.parked_car_list = arcade.SpriteList()
        self.parking_slot_list = arcade.SpriteList()
        self.parking_line_list = arcade.SpriteList()
        self.parking_block_list = arcade.SpriteList()
        self.parking_slot_border_list = arcade.SpriteList()





        self.background = arcade.load_texture("assets/Map.png")
        self.car_sprite = Car.Car("assets/Car.png", 0.15)
        self.car_sprite.center_x = 100
        self.car_sprite.center_y = 500

        #spawn zaparkowanych samochodów
        self.car_spawn()

        self.player_car_list.append(self.car_sprite)

        self.parking.add_parking_lane(self.parking_line_list)
        self.parking.add_parking_slot_ai(self.parking_slot_list)
        self.parking.add_parking_block(self.parking_block_list)
        self.parking.add_slot_border(self.parking_slot_border_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.

        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0, 1900, 1000, self.background)

        self.player_car_list.draw()
        self.parked_car_list.draw()
        self.parking_line_list.draw()
        self.parking_slot_list.draw()
        self.parking_block_list.draw()
        self.parking_slot_border_list.draw()

        #rysowanie sensorów
        self.sensors = Sensors.Sensors(self.car_sprite, self.parked_car_list, self.parking_block_list)

        #rysuje hitbox pojzadu głównego
        if self.hitbox_visible == True:
            self.car_sprite.draw_hit_box(arcade.color.BLUE, 3)

            for car in self.parked_car_list:
                car.draw_hit_box(arcade.color.RED, 3)

            for slot in self.parking_slot_list:
                slot.draw_hit_box(arcade.color.GREEN,3)

            for line in self.parking_line_list:
                line.draw_hit_box(arcade.color.YELLOW,3)

            for block in self.parking_block_list:
                block.draw_hit_box(arcade.color.RED,3)

            for border in self.parking_slot_border_list:
                border.draw_hit_box(arcade.color.YELLOW,1)

        # Call draw() on all your sprite lists below


    def parking_method(self, car):
        """
        Metoda sprawdzająca czy samochód podany jako argument car jest poprawnie zaparkowany.
        """
        if arcade.check_for_collision_with_list(car, self.parking_slot_list) and not arcade.check_for_collision_with_list(car, self.parking_line_list) and not arcade.check_for_collision_with_list(car, self.parking_slot_border_list) and not car.is_parked:
            car.is_parked = True
            print("Parked succesfully")
            self.setup()

        if arcade.check_for_collision_with_list(car, self.parking_line_list) or arcade.check_for_collision_with_list(car, self.parking_slot_border_list):
            car.is_parked = False

    def collision_method(self, car):

        if arcade.check_for_collision_with_list(car, self.parking_block_list) or arcade.check_for_collision_with_list(car, self.parked_car_list):
            self.setup()
            return True

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.action = random.randrange(1, 7)
        #self.control_ai(self.action)

        # Czynności podejmowane w zależności od wciśniętych klawiszy.
        if self.pressed_up == True and self.pressed_down == False:
            self.car_sprite.acceleration()
        if self.pressed_up == False and self.pressed_down == False:
            self.car_sprite.deacceleration()
        if self.pressed_down == True and self.pressed_up == False and \
                self.car_sprite.current_speed > self.car_sprite.car_stop:
            self.car_sprite.car_break()
            self.car_sprite.is_breaking = True
        if self.pressed_down == False:
            self.car_sprite.is_breaking = False
        if self.pressed_down == True and self.car_sprite.is_breaking == False:
            self.car_sprite.car_back()
        if self.pressed_left == True and self.pressed_right == False:
            self.car_sprite.left()
        if self.pressed_right == True and self.pressed_left == False:
            self.car_sprite.right()
        if (self.pressed_right == False and self.pressed_left == False) or self.car_sprite.is_breaking == True:
            self.car_sprite.stop_angle()

        self.player_car_list.update()

        self.parking_method(self.car_sprite)

        if (self.collision_method(self.car_sprite)):
            print("Działa")

        #anulowanie randomowego wcisniecia klawisza przez ai
        #self.pressed_up = False
        #self.pressed_down = False
        #self.pressed_left = False
        #self.pressed_right = False



    #sterowanie pojazdem
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.pressed_up = True
        if key == arcade.key.DOWN:
            self.pressed_down = True
        if key == arcade.key.RIGHT:
            self.pressed_right = True
        if key == arcade.key.LEFT:
            self.pressed_left = True

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.pressed_up = False
        if key == arcade.key.DOWN:
            self.pressed_down = False
        if key == arcade.key.RIGHT:
            self.pressed_right = False
        if key == arcade.key.LEFT:
            self.pressed_left = False

    #sterowanie AI
    def control_ai(self, action):
        if action == 1:
            self.pressed_up = True
            print('1')
        if action == 2:
            self.pressed_down = True
            print('2')
        if action == 3:
            self.pressed_up = True
            self.pressed_right = True
            print('3')
        if action == 4:
            self.pressed_up = True
            self.pressed_left = True
            print('4')
        if action == 5:
            self.pressed_down = True
            self.pressed_right = True
            print('5')
        if action == 6:
            self.pressed_down = True
            self.pressed_left = True
            print('6')


