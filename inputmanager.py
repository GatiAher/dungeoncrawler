# inputmanager
import pygame
import game
from blocks import Player

class AbstractCommand(object):

    def __init__(self, reciever):
        self.reciever = reciever
        pass

    def execute(self):
        pass



class CloseGameCommand(AbstractCommand):

    def __init__(self):
        super().__init__(None)

    def execute(self):
        pygame.quit()



class DirectionCommand(AbstractCommand):

    def __init__(self):
        self.player = Player()
        super().__init__(self.player)

    def execute(self, event_type):
        pass



class MoveUpCommand(DirectionCommand):

    def __init__(self):
        super().__init__()

    def execute(self, event_type):
        if event_type == pygame.KEYDOWN:
            self.reciever.dy = -1
        else:
            self.reciever.dy = 0



class MoveDownCommand(DirectionCommand):

    def __init__(self):
        super().__init__()

    def execute(self, event_type):
        if event_type == pygame.KEYDOWN:
            self.reciever.dy = 1
        else:
            self.reciever.dy = 0


class MoveRightCommand(DirectionCommand):

    def __init__(self):
        super().__init__()

    def execute(self, event_type):
        if event_type == pygame.KEYDOWN:
            self.reciever.dx = 1
        else:
            self.reciever.dx = 0


class MoveLeftCommand(DirectionCommand):

    def __init__(self):
        super().__init__()

    def execute(self, event_type):
        if event_type == pygame.KEYDOWN:
            self.reciever.dx = -1
        else:
            self.reciever.dx = 0


class AbstractAttackCommand(AbstractCommand):

    def __init__(self):
        super().__init__(None)

    def give_current_room(self, cr):
        self.reciever = cr

    def execute(self, event_type):
        pass


class AttackNorthCommand(AbstractAttackCommand):

    def __init__(self):
        super().__init__()

    def give_current_room(self, cr):
        self.reciever = cr

    def execute(self, event_type):
        pass
        if event_type == pygame.KEYDOWN:
            self.reciever.register_player_bullets("N")


class AttackSouthCommand(AbstractAttackCommand):

    def __init__(self):
        super().__init__()

    def give_current_room(self, cr):
        self.reciever = cr

    def execute(self, event_type):
        pass
        if event_type == pygame.KEYDOWN:
            self.reciever.register_player_bullets("S")


class AttackEastCommand(AbstractAttackCommand):

    def __init__(self):
        super().__init__()

    def give_current_room(self, cr):
        self.reciever = cr

    def execute(self, event_type):
        pass
        if event_type == pygame.KEYDOWN:
            self.reciever.register_player_bullets("E")


class AttackWestCommand(AbstractAttackCommand):

    def __init__(self):
        super().__init__()

    def give_current_room(self, cr):
        self.reciever = cr

    def execute(self, event_type):
        pass
        if event_type == pygame.KEYDOWN:
            self.reciever.register_player_bullets("W")


class InputManager(object):

    command_dict = {
        pygame.QUIT: CloseGameCommand(),
        pygame.K_w: MoveUpCommand(),
        pygame.K_s: MoveDownCommand(),
        pygame.K_d: MoveRightCommand(),
        pygame.K_a: MoveLeftCommand(),
        pygame.K_UP: AttackNorthCommand(),
        pygame.K_DOWN: AttackSouthCommand(),
        pygame.K_LEFT: AttackWestCommand(),
        pygame.K_RIGHT: AttackEastCommand()
    }

    @ classmethod
    def handle_events(cls):
        for event in pygame.event.get():

            if event.type in cls.command_dict:
                cls.command_dict[event.type].execute()

            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
                if event.key in cls.command_dict:
                    cls.command_dict[event.key].execute(event.type)






