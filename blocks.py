# blocks

import pygame
import math
import game
import display

class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height, hp, speed, x, y):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hp = hp

        self.dx = 0
        self.dy = 0
        self.speed = speed

    def set_dx(self):
        pass

    def set_dy(self):
        pass

    def move_x(self):
        self.rect.centerx += self.dx * self.speed

    def move_y(self):
        self.rect.centery += self.dy * self.speed

    def action_lr(self, hit_list):
        pass

    def action_tb(self, hit_list):
       pass

    def reaction_lr(self, block):
        pass

    def reaction_tb(self, block):
        pass

    def mass_y(self, block):
        block.dy = -1 * block.dy
        block.move_y()
        block.dy = 0

    def mass_x(self, block):
        block.dx = -1 * block.dx
        block.move_x()
        block.dx = 0



class Bullet(Block):

    def __init__(self, owner, aim_x, aim_y):
        super().__init__((209, 8, 18), 5, 10, 1, 10, owner.rect.centerx, owner.rect.centery)

        self.owner = owner
        self.ori_x = owner.rect.centerx
        self.ori_y = owner.rect.centery
        self.aim_x = aim_x
        self.aim_y = aim_y

        diff_x = self.aim_x - self.ori_x
        diff_y = self.aim_y - self.ori_y
        angle = math.atan2(diff_y, diff_x)

        self.dx = math.cos(angle)
        self.dy = math.sin(angle)


    def action_lr(self, hit_list):
        for block in hit_list:
            block.reaction_lr(self)

    def action_tb(self, hit_list):
        for block in hit_list:
            block.reaction_tb(self)



class Player:

    class __Player(Block):

        def __init__(self):
            super().__init__((255, 255, 255), 15, 20, 20, 5, 0, 0)

    instance = None

    def __init__(self):
        if not Player.instance:
            Player.instance = Player.__Player()

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        setattr(self.instance, key, value)

    def set_player(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def action_lr(self, hit_list):
        for block in hit_list:
            block.reaction_lr(self)

    def action_tb(self, hit_list):
        for block in hit_list:
            block.reaction_tb(self)

    def reaction_lr(self, block):
        if isinstance(block, Monster):
            self.mass_x(block)
            self.hp -= 1
        if isinstance(block, Bullet):
            if isinstance(block.owner, Monster):
                self.hp -= block.hp
                block.kill()

    def reaction_tb(self, block):
        if isinstance(block, Monster):
            self.mass_y(block)
            self.hp -= 1
        if isinstance(block, Bullet):
            if isinstance(block.owner, Monster):
                self.hp -= block.hp
                block.kill()


class Monster(Block):

    def __init__(self, x, y):
        super().__init__((80, 216, 17), 15, 20, 3, 1, x, y)

        self.player = Player()
        self.attack_counter = 60
        self.current_count = 0

    def set_dx(self):
        if self.rect.x < self.player.rect.x:
            self.dx = 1
        else:
            self.dx = -1

    def set_dy(self):
        if self.rect.y < self.player.rect.y:
            self.dy = 1
        else:
            self.dy = -1

    def action_lr(self, hit_list):
        for block in hit_list:
            block.reaction_lr(self)

    def action_tb(self, hit_list):
        for block in hit_list:
            block.reaction_tb(self)

    def reaction_lr(self, block):
        if isinstance(block, Player) or (isinstance(block, Monster) and block is not self):
            self.mass_x(block)
        if isinstance(block, Player):
            block.hp -= 1
        if isinstance(block, Bullet):
            if isinstance(block.owner, Player):
                self.hp -= block.hp
                block.kill()

        if self.hp <= 0:
            self.kill()

    def reaction_tb(self, block):
        if isinstance(block, Player) or (isinstance(block, Monster) and block is not self):
            self.mass_y(block)
        if isinstance(block, Player):
            block.hp -= 1
        if isinstance(block, Bullet):
            if isinstance(block.owner, Player):
                self.hp -= block.hp
                block.kill()

        if self.hp <= 0:
            self.kill()


class Wall(Block):

    def __init__(self, width, height, x, y):
        super().__init__((17, 215, 255), width, height, 0, 0, x, y)

    def reaction_lr(self, block):
        if isinstance(block, Player) or isinstance(block, Monster):
            self.mass_x(block)
        if isinstance(block, Bullet):
            block.kill()

    def reaction_tb(self, block):
        if isinstance(block, Player) or isinstance(block, Monster):
            self.mass_y(block)
        if isinstance(block, Bullet):
            block.kill()

class Crate(Block):

    def __init__(self, x, y):
        super().__init__((240, 255, 168), 15, 20, 2, 0, x, y)

    def reaction_lr(self, block):
        if isinstance(block, Player) or isinstance(block, Monster):
            self.mass_x(block)
        if isinstance(block, Bullet):
            self.hp -= block.hp
            block.kill()

        if self.hp <= 0:
            self.kill()


    def reaction_tb(self, block):
        if isinstance(block, Player) or isinstance(block, Monster):
            self.mass_y(block)
        if isinstance(block, Bullet):
            self.hp -= block.hp
            block.kill()

        if self.hp <= 0:
            self.kill()

class Tile(Block):

    def __init__(self, x, y):
        super().__init__((139, 232, 179), 15, 20, 0, 0, x, y)

    def reaction_lr(self, block):
        if isinstance(block, Player) or isinstance(block, Monster):
            pass

    def reaction_tb(self, block):
        if isinstance(block, Player) or isinstance(block, Monster):
            pass


class Portal(Block):

    ANTIDIRECTIONS = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E"
    }

    def __init__(self, direction, next_room):

        super().__init__((125, 7, 193), 15, 20, 0, 0, 0, 0)

        self.is_active = True
        self.direction = direction
        self.next_room = next_room

    def set_portal(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def reaction_lr(self, block):
        if self.is_active:
            if isinstance(block, Player):
                game.Game.change_room(self.next_room)
                if self.direction == "W":
                    block.rect.right = self.next_room.directions.get("E").rect.left
                    block.rect.top = self.next_room.directions.get("E").rect.top
                if self.direction == "E":
                    block.rect.left = self.next_room.directions.get("W").rect.right
                    block.rect.top = self.next_room.directions.get("W").rect.top
        else:
            if isinstance(block, Player) or isinstance(block, Monster):
                self.mass_x(block)

        if isinstance(block, Bullet):
            block.kill()

    def reaction_tb(self, block):
        if self.is_active:
            if isinstance(block, Player):
                game.Game.change_room(self.next_room)
                if self.direction == "N":
                    block.rect.bottom = self.next_room.directions.get("S").rect.top
                    block.rect.right = self.next_room.directions.get("S").rect.right
                if self.direction == "S":
                    block.rect.top = self.next_room.directions.get("N").rect.bottom
                    block.rect.right = self.next_room.directions.get("N").rect.right
        else:
            if isinstance(block, Player) or isinstance(block, Monster):
                self.mass_y(block)

        if isinstance(block, Bullet):
            block.kill()