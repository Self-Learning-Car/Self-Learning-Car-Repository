class Hitbox:
    """ Generic base hitbox class """
    def __init__(self, center_x, center_y, width, height, color, border_width):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.color = color
        self.border_width = border_width
