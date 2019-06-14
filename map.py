import random
import blocks
import rooms


class RoomMap(object):

    map = None
    room_list = []

    ANTIDIRECTIONS = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E"
    }

    @classmethod
    def add_new_room(cls, new_name, room_type="M", start_room=None):

        is_start_room_fixed = False

        if len(cls.room_list) < 1:
            start_room = cls.map[2][2]
            is_start_room_fixed = True
        elif room_type == "E":
            is_start_room_fixed = True

        successful = False
        while not successful:

            if not is_start_room_fixed:
                start_room = random.choice(cls.room_list)

            target = random.choice(list(start_room.directions.keys()))
            if not isinstance(start_room.directions[target], blocks.Portal):

                row_coor = int(start_room.directions[target][0]) + start_room.location[0]
                col_coor = int(start_room.directions[target][1]) + start_room.location[1]

                if row_coor > 0 and row_coor < 5 and col_coor > 0 and col_coor < 5:
                    if not isinstance(cls.map[row_coor][col_coor], rooms.AbstractRoom):
                        if room_type == "E":
                            new_room = rooms.EndRoom(row_coor, col_coor)
                        else:
                            new_room = rooms.MonsterRoom(row_coor, col_coor, new_name)
                            cls.room_list.append(new_room)

                        cls.map[row_coor][col_coor] = new_room
                        start_room.directions[target] = blocks.Portal(target, new_room)
                        new_room.directions[cls.ANTIDIRECTIONS[target]] = blocks.Portal(cls.ANTIDIRECTIONS[target],
                                                                                        start_room)

                        successful = True
                        return new_room

    @classmethod
    def make_map(cls):

        cls.map = [0] * 5
        for i in range(5):
            cls.map[i] = [0] * 5

        cls.room_list = []

        room1 = rooms.HomeRoom(2, 2)
        cls.map[2][2] = room1

        cls.add_new_room("1")
        room2 = cls.add_new_room("2")
        cls.add_new_room("3", "E", room2)
        cls.add_new_room("4")
        cls.add_new_room("5")
        cls.add_new_room("6")
        cls.add_new_room("7")

        cls.print_map()
        cls.configure_rooms()


    @ classmethod
    def configure_rooms(cls):
        for i in range(5):
            for j in range(5):
                if isinstance(cls.map[i][j], rooms.AbstractRoom):
                    cls.map[i][j].assign_portals_floorplan()


    @classmethod
    def print_map(cls):

        for i in range(5):
            print()
            for j in range(5):
                if isinstance(cls.map[i][j], rooms.AbstractRoom):
                    print(" R" + cls.map[i][j].name, end=" ")
                else:
                    print(" 0 ", end=" ")
        print()
        print()

        for room in cls.room_list:
            print("ROOM " + room.name)
            for tar in list(room.directions.keys()):
                if isinstance(room.directions[tar], blocks.Portal):
                    portal = room.directions[tar]
                    print("   PORTAL: " + portal.direction + " --> " + portal.next_room.name)


