import pygame


class Mouse:
    def __init__(self):
        self.pos = (None, None)
        self.rel = (None, None)
        self.pressed = (None, None, None)
    
    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.rel = pygame.mouse.get_rel()
        self.pressed = pygame.mouse.get_pressed()
