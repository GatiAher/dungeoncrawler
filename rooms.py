# room
import pygame
import random
import blocks
import inputmanager
import display
import game

class AbstractRoom(object):

    def __init__(self, row, col, name):

        self.directions = {
            "N": [-1, 0],
            "S": [1, 0],
            "E": [0, 1],
            "W": [0, -1]
        }

        self.name = name

        self.location = [row, col]

        self.player = None
        self.room_cleared = True
        self.created_floorplan = False

        self.all_sprites = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()

        self.room_no_row = 9
        self.room_no_col = 9

        # create floorplan
        self.floorplan = [0] * self.room_no_row
        for i in range(self.room_no_row):
            self.floorplan[i] = [0] * self.room_no_col

        # allot walls in floorplan
        for i in range(self.room_no_row):
            for j in range(self.room_no_col):
                if i == 0 or j == 0 or i == self.room_no_row - 1 or j == self.room_no_col - 1:
                    self.floorplan[i][j] = 1

        self.room_width = 500
        self.room_height = 500

        self.cell_width = self.room_width / self.room_no_col
        self.cell_height = self.room_height / self.room_no_row


    def assign_portals_floorplan(self):
        # make floorplan

        # allot portals
        if isinstance(self.directions.get("N"), blocks.Portal):
            self.floorplan[0][int(self.room_no_col / 2)] = "N"
        if isinstance(self.directions.get("S"), blocks.Portal):
            self.floorplan[self.room_no_row - 1][int(self.room_no_col / 2)] = "S"
        if isinstance(self.directions.get("W"), blocks.Portal):
            self.floorplan[int(self.room_no_row / 2)][0] = "W"
        if isinstance(self.directions.get("E"), blocks.Portal):
            self.floorplan[int(self.room_no_row / 2)][self.room_no_col - 1] = "E"


    # def print_floorplan(self):
    #     for i in range(self.room_no_row):
    #         print()
    #         for j in range(self.room_no_col):
    #             print(str(self.floorplan[i][j]),  end=" ")
    #
    #     print()
    #     print()
    #     print()


    def create_floorplan(self):
        self.create_walls_and_portals()
        self.assign_room_specific_elements()
        self.create_room_specific_elements()


    def create_walls_and_portals(self):
        # actually create floorplan elements

        self.created_floorplan = True

        for i in range(self.room_no_row):
            for j in range(self.room_no_col):
                cell = self.floorplan[i][j]
                if cell == 1:
                    wall = blocks.Wall(self.cell_width, self.cell_height, j * self.cell_width, i * self.cell_height)
                    self.all_sprites.add(wall)
                if cell == "N" or cell == "S" or cell == "W" or cell == "E":
                    portal = self.directions.get(cell)
                    portal.set_portal(j * self.cell_width, i * self.cell_height)
                    self.all_sprites.add(portal)
                    self.portals.add(portal)

    def assign_room_specific_elements(self):
        pass

    def create_room_specific_elements(self):
        pass


    def start(self):
        if not self.created_floorplan:
            self.create_floorplan() # TODO
        self.player = blocks.Player()
        self.player.rect.x = 100
        self.player.rect.y = 100
        self.all_sprites.add(self.player)
        self.play()

    def play(self):
        inputmanager.InputManager.handle_events()
        self.room_logic()
        display.Display.render(self.all_sprites)

        # open doors and initialize new avalible rooms
        # game.goto other room


    def room_logic(self):
        pass


    @classmethod
    def turn(cls, character, list, do_kill = False):

        character.set_dx()
        character.move_x()

        hit_list = pygame.sprite.spritecollide(character, list, do_kill)

        character.action_lr(hit_list)

        character.set_dy()
        character.move_y()

        hit_list = pygame.sprite.spritecollide(character, list, do_kill)

        character.action_tb(hit_list)


class MonsterRoom(AbstractRoom):
    """
    Manages logic of this specific room
    """

    def __init__(self, row, col, name):

        super().__init__(row, col, name)

        self.bullets = pygame.sprite.Group()

        self.monsters = pygame.sprite.Group()
        self.num_monsters = random.randint(3, 7)
        self.num_crates = random.randint(5, 20)
        self.num_tiles = random.randint(5, 20)

        self.room_cleared = False

    def new_player_attack(self, aim_x, aim_y):
        bullet = blocks.Bullet(self.player, aim_x, aim_y)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

    def new_monster_attack(self, monster):
        bullet = blocks.Bullet(monster, self.player.rect.x, self.player.rect.y)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

    def assign_room_specific_elements(self):

        # deactivate portals
        for portal in self.portals:
            portal.is_active = False

        # create crates
        for i in range(self.num_crates):
            successful = False
            while not successful:
                coor_x = random.randint(0, self.room_no_col - 1)
                coor_y = random.randint(0, self.room_no_row - 1)
                if self.floorplan[coor_x][coor_y] == 0:
                    self.floorplan[coor_x][coor_y] = 3
                    crate = blocks.Crate(coor_x * self.cell_width, coor_y * self.cell_height)
                    self.all_sprites.add(crate)
                    successful = True

        # create tiles
        for i in range(self.num_tiles):
            successful = False
            while not successful:
                coor_x = random.randint(0, self.room_no_col - 1)
                coor_y = random.randint(0, self.room_no_row - 1)
                if self.floorplan[coor_x][coor_y] == 0:
                    self.floorplan[coor_x][coor_y] = 4
                    tile = blocks.Tile(coor_x * self.cell_width, coor_y * self.cell_height)
                    self.all_sprites.add(tile)
                    successful = True

        # create monsters
        for i in range(self.num_monsters):
            successful = False
            while not successful:
                coor_x = random.randint(0, self.room_no_col - 1)
                coor_y = random.randint(0, self.room_no_row - 1)
                if self.floorplan[coor_x][coor_y] == 0:
                    self.floorplan[coor_x][coor_y] = 5
                    monster = blocks.Monster(coor_x * self.cell_width, coor_y * self.cell_height)
                    self.all_sprites.add(monster)
                    self.monsters.add(monster)
                    successful = True


    def room_logic(self):

        self.turn(self.player, self.all_sprites)

        if len(self.monsters) == 0:
            self.room_cleared = True
            for portal in self.portals:
                portal.is_active = True

        else:
            for monster in self.monsters:
                self.turn(monster, self.all_sprites)
                monster.current_count += 1
                if monster.current_count % monster.attack_counter == 0:
                    self.new_monster_attack(monster)

        for bullet in self.bullets:
            self.turn(bullet, self.all_sprites)

        print(self.player.hp)

        if self.player.hp <= 0:
            game.Game.end_game()



























class EndRoom(AbstractRoom):
    """
    Manages logic of this specific room
    """

    def __init__(self, row, col):
        super().__init__(row, col, "E")


    def room_logic(self):
        self.turn(self.player, self.all_sprites)


class HomeRoom(AbstractRoom):
    """
    Manages logic of this specific room
    """

    def __init__(self, row, col):
        super().__init__(row, col, "H")


    def room_logic(self):
        self.turn(self.player, self.all_sprites)