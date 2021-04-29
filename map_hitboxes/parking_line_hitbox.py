import arcade
from map_hitboxes import hitbox


class ParkingLineHitbox(hitbox.Hitbox):

    def draw(self):
        arcade.draw_rectangle_outline(self.center_x,
                                      self.center_y,
                                      self.width,
                                      self.height,
                                      self.color,
                                      self.border_width)
