import arcade
from map_hitboxes.map_hitbox import MapHitbox
from map_hitboxes.parking_slot_hitbox import ParkingSlotHitbox
from map_hitboxes.parking_line_hitbox import ParkingLineHitbox


class Hitboxes:
    def __init__(self):
        #wysokość miejsca parkingowego
        self.parking_slot_height = 190
        #szerokość miejsca parkingowego
        self.parking_slot_width = 120
        #wysokość linii parkingowej
        self.parking_line_height = 190
        #szerokość linii parkingowel
        self.parking_line_width = 10
        #lista hitboxów
        self.hitboxes_list = []
        #widoczność hitboxów
        self.is_visible = True

        if self.is_visible:
            self.visible = 255
        else:
            self.visible = 0
        self.map_hitbox_color = (255, 0, 0, self.visible)
        self.parking_slot_hitbox_color = (0, 255, 0, self.visible)
        self.parking_line_hitbox_color = (0, 0, 255, self.visible)

    def draw_hitboxes(self):
        self.draw_parking_hitboxes()
        self.draw_parking_slots_hitboxes()
        self.draw_parking_lines_hitboxes()

        for hitbox in self.hitboxes_list:
            hitbox.draw()

    def draw_parking_hitboxes(self):
        top_corner = MapHitbox(0, 1000, 400, 650, self.map_hitbox_color, 3)
        top = MapHitbox(1010, 1000, 1620, 250, self.map_hitbox_color, 3)
        right = MapHitbox(1860, 500, 80, 1000, self.map_hitbox_color, 3)
        bottom = MapHitbox(1010, 70, 1620, 140, self.map_hitbox_color, 3)
        bottom_corner = MapHitbox(0, 50, 400, 500, self.map_hitbox_color, 3)

        #self.hitboxes_list.append({top_corner, top, right, bottom, bottom_corner})
        self.hitboxes_list.append(top_corner)
        self.hitboxes_list.append(top)
        self.hitboxes_list.append(right)
        self.hitboxes_list.append(bottom)
        self.hitboxes_list.append(bottom_corner)

    def draw_parking_slots_hitboxes(self):
        # Top row
        top1 = ParkingSlotHitbox(430, 780, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        top2 = ParkingSlotHitbox(575, 780, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        top3 = ParkingSlotHitbox(715, 780, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        top4 = ParkingSlotHitbox(855, 780, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        top5 = ParkingSlotHitbox(1000, 780, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        top6 = ParkingSlotHitbox(1145, 780, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        top7 = ParkingSlotHitbox(1285, 780, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        top8 = ParkingSlotHitbox(1425, 780, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        top9 = ParkingSlotHitbox(1570, 780, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        # Bottom row
        bottom1 = ParkingSlotHitbox(430, 230, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        bottom2 = ParkingSlotHitbox(575, 230, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        bottom3 = ParkingSlotHitbox(715, 230, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        bottom4 = ParkingSlotHitbox(855, 230, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        bottom5 = ParkingSlotHitbox(1000, 230, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        bottom6 = ParkingSlotHitbox(1145, 230, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        bottom7 = ParkingSlotHitbox(1285, 230, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        bottom8 = ParkingSlotHitbox(1425, 230, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)
        bottom9 = ParkingSlotHitbox(1570, 230, self.parking_slot_width, self.parking_slot_height, self.parking_slot_hitbox_color, 2)

        parking_slots_hitboxes = {top1, top2, top3, top4, top5, top6, top7, top8, top9, bottom1, bottom2, bottom3,
                                  bottom4, bottom5, bottom6, bottom7, bottom8, bottom9}

        for slot in parking_slots_hitboxes:
            self.hitboxes_list.append(slot)

    def draw_parking_lines_hitboxes(self):
        # Top row
        top1 = ParkingLineHitbox(360, 780, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        top2 = ParkingLineHitbox(500, 780, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        top3 = ParkingLineHitbox(640, 780, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        top4 = ParkingLineHitbox(785, 780, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        top5 = ParkingLineHitbox(930, 780, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        top6 = ParkingLineHitbox(1075, 780, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        top7 = ParkingLineHitbox(1215, 780, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        top8 = ParkingLineHitbox(1355, 780, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        top9 = ParkingLineHitbox(1500, 780, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        top10 = ParkingLineHitbox(1645, 780, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)

        # Bottom row
        bottom1 = ParkingLineHitbox(360, 230, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        bottom2 = ParkingLineHitbox(500, 230, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        bottom3 = ParkingLineHitbox(640, 230, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        bottom4 = ParkingLineHitbox(785, 230, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        bottom5 = ParkingLineHitbox(930, 230, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        bottom6 = ParkingLineHitbox(1075, 230, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        bottom7 = ParkingLineHitbox(1215, 230, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        bottom8 = ParkingLineHitbox(1355, 230, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        bottom9 = ParkingLineHitbox(1500, 230, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)
        bottom10 = ParkingLineHitbox(1645, 230, self.parking_line_width, self.parking_line_height, self.parking_line_hitbox_color, 2)

        parking_lines_hitboxes = {top1, top2, top3, top4, top5, top6, top7, top8, top9, top10, bottom1, bottom2,
                                  bottom3, bottom4, bottom5, bottom6, bottom7, bottom8, bottom9, bottom10}

        for line in parking_lines_hitboxes:
            self.hitboxes_list.append(line)