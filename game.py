# game

import pygame # for quit statement
import display
import rooms
import inputmanager
import map

class Game(object):
    """
    Walks user through series of rooms
    """

    current_room = None

    @ classmethod
    def start(cls):
        display.Display.start()
        map.RoomMap.make_map()
        cls.current_room = map.RoomMap.map[2][2]
        inputmanager.InputManager.command_dict.get(pygame.K_UP).give_current_room(cls.current_room)
        inputmanager.InputManager.command_dict.get(pygame.K_DOWN).give_current_room(cls.current_room)
        inputmanager.InputManager.command_dict.get(pygame.K_RIGHT).give_current_room(cls.current_room)
        inputmanager.InputManager.command_dict.get(pygame.K_LEFT).give_current_room(cls.current_room)
        cls.run()

    @ classmethod
    def change_room(cls, new_room):
        cls.current_room = new_room
        inputmanager.InputManager.command_dict.get(pygame.K_UP).give_current_room(cls.current_room)
        inputmanager.InputManager.command_dict.get(pygame.K_DOWN).give_current_room(cls.current_room)
        inputmanager.InputManager.command_dict.get(pygame.K_RIGHT).give_current_room(cls.current_room)
        inputmanager.InputManager.command_dict.get(pygame.K_LEFT).give_current_room(cls.current_room)
        cls.current_room.start()

    @ classmethod
    def end_game(cls):
        cls.current_room = None

    @ classmethod
    def run(cls):

        cls.current_room.start()

        while isinstance(cls.current_room, rooms.AbstractRoom):
            cls.current_room.play()
        pygame.quit()







