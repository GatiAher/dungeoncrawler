# display

import pygame

class Display(object):

    clock = None
    screen = None

    @ classmethod
    def start(cls):
        pygame.init()
        cls.clock = pygame.time.Clock()
        pygame.display.set_caption("dungeon crawler")
        cls.screen = pygame.display.set_mode([600, 600])

    @ classmethod
    def render(cls, list_of_sprites):
        cls.screen.fill((0, 0, 0))
        list_of_sprites.draw(cls.screen)
        pygame.display.flip()
        cls.clock.tick(20)

    # @ classmethod
    # def draw_line(cls, x1, y1, x2, y2):
    #     pygame.draw.line(cls.screen, (50, 50, 50), (x1, y1), (x2, y2), 5)

