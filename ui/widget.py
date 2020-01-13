import weakref

import pygame
import pygame.gfxdraw
import numpy as np


class Widget:
    __instances = set()

    def __init__(self, position, size, draw_rect=True):
        self.master = None
        
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.surface = self.surface.convert_alpha()
        self.pos = np.array(position)
        self.size = size

        self.color = (0, 255, 0)
        self.active = False
        self.container = False
        
        self.__instances.add(weakref.ref(self))

    def delete(self):
        pass
    
    @property
    def x(self):
        return self.pos[0]
    
    @x.setter
    def x(self, value):
        self.pos[0] = value

    @property
    def y(self):
        return self.pos[1]
    
    @y.setter
    def y(self, value):
        self.pos[1] = value
    
    @property
    def w(self):
        return self.size[0]
    
    @w.setter
    def w(self, value):
        self.size = (value, self.size[1])
    
    @property
    def h(self):
        return self.size[1]

    @h.setter
    def h(self, value):
        self.size = (self.size[0], value)
    
    @property
    def global_pos(self):
        if self.master:
            return self.pos + self.master.global_pos
        return self.pos

    def is_mouse_over(self):
        mx, my = pygame.mouse.get_pos()
        return self.is_inside((mx, my))
    
    def is_inside(self, position):
        if self.global_pos[0] <= position[0] <= self.global_pos[0] + self.size[0]:
            if self.global_pos[1] <= position[1] <= self.global_pos[1] + self.size[1]:
                return True
        return False
    
    def update(self, dt):
        pass
    
    def render(self):
        self.surface.fill((0, 0, 0, 0))
        rect = ((0, 0), self.size)
        pygame.gfxdraw.rectangle(self.surface, rect, self.color)

    def draw(self, surface, position=None):
        self.render()
        if position is None:
            position = self.pos
        surface.blit(self.surface, position)
