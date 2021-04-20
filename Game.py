import arcade
import Car
import Parking


class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

        self.setup()
        arcade.run()


        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.background = arcade.load_texture("assets/Map.png")
        self.car_sprite = arcade.Sprite("assets/Car.png", 0.15)
        self.car_sprite.center_x = 100
        self.car_sprite.center_y = 500
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.

        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0, 1900, 1000, self.background)
        self.car_sprite.draw()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            print("kekupklik")
        if key == arcade.key.DOWN:
            print("kekdown")
        if key == arcade.key.RIGHT:
            print("kekright")
        if key == arcade.key.LEFT:
            print("kekleft")

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.UP:
            print("kekupunklik")
        if key == arcade.key.DOWN:
            print("kekdownunklik")
        if key == arcade.key.RIGHT:
            print("kekrightunklik")
        if key == arcade.key.LEFT:
            print("kekleftunklik")
