import arcade

class Parking:
    def __init__(self):


        # wysokość miejsca parkingowego
        self.parking_slot_height = 190
        # szerokość miejsca parkingowego
        self.parking_slot_width = 120
        # wysokość linii parkingowej
        self.parking_line_height = 190
        # szerokość linii parkingowel
        self.parking_line_width = 10
        # wysokość granicy miejsca parkingowego
        self.slot_border_height = 2
        # centralna pozycja y parkingu
        self.parking_center_position = 500
        # pozycje miejsc parkingowych
        self.parking_slot_position = [(430, 780),(575, 780),(715, 780),(855, 780),(1000, 780),(1145, 780),(1285, 780),
                                      (1425, 780),(1570, 780),(430, 230),(575, 230),(715, 230),(855, 230),(1000, 230),
                                      (1145, 230),(1285, 230),(1425, 230),(1570, 230)]
        # pozycje linii parkingweych
        self.parking_line_position = [(360, 780),(500, 780),(640, 780),(785, 780),(930, 780),(1075, 780),(1215, 780),
                                      (1355, 780),(1500, 780),(1645, 780),(360, 230),(500, 230),(640, 230),(785, 230),
                                      (930, 230),(1075, 230),(1215, 230),(1355, 230),(1500, 230),(1645, 230)]
        # pozycje obszarów niedozwolonych (poza granicami parkingu) oraz ich rozmiary
        self.parking_block_position = [(0, 1000, 400, 650),(1010, 1000, 1620, 250),(1860, 500, 80, 1000),
                                       (1010, 70, 1620, 140),(0, 50, 400, 500)]


    def add_parking_block(self,list):
        """
        Metoda tworząca obszary nie dozwolone (poza granicami parkingu) jako Sprite'y i dodająca je do listy podanej
        jako argument.
        """
        for position in self.parking_block_position:
            parking_block = Parking_block("assets/Empty.png")
            parking_block.center_x = position[0]
            parking_block.center_y = position[1]
            parking_block.width = position[2]
            parking_block.height = position[3]
            list.append(parking_block)

    def add_parking_slot(self,list):
        """
        Metoda tworząca miejsca parkingowe jako Sprite'y i dodająca je do listy podanej jako argument.
        """
        for position in self.parking_slot_position:
            parking_slot = Parking_slot("assets/Empty.png")
            parking_slot.center_x = position[0]
            parking_slot.center_y = position[1]
            parking_slot.width = self.parking_slot_width
            parking_slot.height = self.parking_slot_height
            list.append(parking_slot)


    def add_parking_lane(self,list):
        """
        Metoda tworząca linie parkingowe jako Sprite'y i dodająca je do listy podanej
        jako argument.
        """
        for position in self.parking_line_position:
            parking_line = Parking_line("assets/Empty.png")
            parking_line.center_x = position[0]
            parking_line.center_y = position[1]
            parking_line.width = self.parking_line_width
            parking_line.height = self.parking_line_height
            list.append(parking_line)

    def add_slot_border(self,list):
        """
        Metoda tworząca granice miejsc parkingowych jako Sprite'y i dodająca je do listy podanej jako argument.
        """
        for position in self.parking_slot_position:
            slot_border = Parking_line("assets/Empty.png")
            slot_border.center_x = position[0]
            y_position = position[1]
            if self.parking_center_position < y_position:
                slot_border.center_y = (y_position-(self.parking_line_height/2)-1)
            else:
                slot_border.center_y = (y_position+(self.parking_line_height/2)+1)
            slot_border.width = self.parking_slot_width
            slot_border.height = self.slot_border_height
            list.append(slot_border)

class Parking_slot(arcade.Sprite):
    def __init__(self,image):
        super().__init__(image,hit_box_algorithm='None')

class Parking_line(arcade.Sprite):
    def __init__(self,image):
        super().__init__(image,hit_box_algorithm='None')

class Parking_block(arcade.Sprite):
    def __init__(self,image):
        super().__init__(image,hit_box_algorithm='None')