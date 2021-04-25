import arcade
from hitbox import Hitbox


class ParkingSlotHitbox(Hitbox):

    def draw(self):
        arcade.draw_rectangle_outline(self.center_x,
                                      self.center_y,
                                      self.width,
                                      self.height,
                                      self.color,
                                      self.border_width)
