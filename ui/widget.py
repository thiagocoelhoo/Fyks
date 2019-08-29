import weakref

import pygame
import pygame.gfxdraw
import numpy as np


class Widget:
    __instances = set()

    def __init__(self, position, size, draw_rect=True):
        self.master = None

        self.pos = np.array(position)
        self.size = size
        self.color = (0, 255, 0)
        
        self.__instances.add(weakref.ref(self))
    
    @property
    def x(self):
        return self.pos[0]
    
    @property
    def y(self):
        return self.pos[1]
    
    @property
    def w(self):
        return self.size[0]
    
    @property
    def h(self):
        return self.size[1]
        
    @classmethod
    def all(cls):
        dead = set()
        for ref in cls.__instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls.__instances -= dead

    @property
    def global_pos(self):
        if self.master:
            return self.pos + self.master.global_pos
        return self.pos

    def is_hover(self):
        mx, my = pygame.mouse.get_pos()
        if self.global_pos[0] <= mx <= self.global_pos[0] + self.size[0]:
            if self.global_pos[1] <= my <= self.global_pos[1] + self.size[1]:
                return True
    
    def is_inside(self, position):
        if self.global_pos[0] <= position[0] <= self.global_pos[0] + self.size[0]:
            if self.global_pos[1] <= position[1] <= self.global_pos[1] + self.size[1]:
                return True
        return False
    
    def update(self, dt):
        pass
    
    def draw(self, surface):
        rect = (self.pos, self.size)
        pygame.gfxdraw.rectangle(surface, rect, self.color)

