import arcade
import Car
import Parking
import random

class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.pressed_up = False
        self.pressed_down = False
        self.pressed_right = False
        self.pressed_left = False

        # Car spawn

        self.random_car_placement = True
        self.random_car_number = False
        self.parked_car_number = 15

        self.spawn_points = [(1,430,230),(2,572,230),(3,714,230),(4,856,230),(5,998,230),(6,1140,230),(7,1282,230),(8,1424,230),(9,1566,230),
                             (10,430,780),(11,572,780),(12,714,780),(13,856,780),(14,998,780),(15,1140,780),(16,1282,780),(17,1424,780),(18,1566,780)]

        # Car spawn

        arcade.set_background_color(arcade.color.AMAZON)

        self.setup()
        arcade.run()


        # If you have sprite lists, you should create them here,
        # and set them to None

        self.player_car_list = None
        self.car_sprite = None

        self.parked_car_list = None
        self.parked_car_sprite = None


    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        self.player_car_list = arcade.SpriteList()
        self.parked_car_list = arcade.SpriteList()

        self.background = arcade.load_texture("assets/Map.png")
        self.car_sprite = Car.Car("assets/Car.png", 0.15)
        self.car_sprite.center_x = 100
        self.car_sprite.center_y = 500
        self.car_sprite.angle = -90

        # Car spawn

        if self.random_car_placement:
            if self.random_car_number:
                cars_to_spawn = random.sample(self.spawn_points,random.randrange(0,len(self.spawn_points)-1))
            else:
                cars_to_spawn = random.sample(self.spawn_points,self.parked_car_number)

        else:
            cars_to_spawn = []
            for spawn_point in self.spawn_points:
                if spawn_point[0] in [3,9,11,16]:
                    pass
                else:
                    cars_to_spawn.append(spawn_point)

        for spawn_point in cars_to_spawn:
            number = random.randrange(1, 10)
            self.parked_car_sprite = Car.Car(f"assets/Car{number}.png", 0.15)
            self.parked_car_sprite.center_x = spawn_point[1]
            self.parked_car_sprite.center_y = spawn_point[2]
            self.parked_car_list.append(self.parked_car_sprite)

        # Car spawn

        self.player_car_list.append(self.car_sprite)


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

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.pressed_up==True and self.pressed_down==False:
            self.car_sprite.acceleration()
        if self.pressed_up==False and self.pressed_down==False:
            self.car_sprite.deacceleration()
        if self.pressed_down==True and self.pressed_up==False:
            self.car_sprite.car_break_back()
        if self.pressed_left==True and self.pressed_right==False:
            self.car_sprite.left()
        if self.pressed_right==True and self.pressed_left==False:
            self.car_sprite.right()
        if self.pressed_right==False and self.pressed_left==False:
            self.car_sprite.stop_angle()





        self.player_car_list.update()

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
