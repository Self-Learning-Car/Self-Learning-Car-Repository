import arcade
import Car
import Parking


class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.pressed_up = False
        self.pressed_down = False
        self.pressed_right = False
        self.pressed_left = False

        arcade.set_background_color(arcade.color.AMAZON)

        self.setup()
        arcade.run()


        # If you have sprite lists, you should create them here,
        # and set them to None

        self.car_list = None
        self.car_sprite = None



    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        self.car_list = arcade.SpriteList()

        self.background = arcade.load_texture("assets/Map.png")
        self.car_sprite = Car.Car("assets/Car.png", 0.15)
        self.car_sprite.center_x = 100
        self.car_sprite.center_y = 500
        self.car_sprite.angle = -90


        self.car_list.append(self.car_sprite)

        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.

        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0, 1900, 1000, self.background)
        self.car_list.draw()

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





        self.car_list.update()

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
