import random

import pygame

from ui import Widget, Label, Button
from render_engine import aa_round_rect


class Item:
    def __init__(self, name, ref, size=(100, 25)):
        self.surface = pygame.Surface(size)
        self.size = size
        self.name = name
        self.ref = ref
        self.color = (random.randint(150, 255), random.randint(100, 200), random.randint(150, 255))

    def draw(self, surface):
        aa_round_rect(
            surface=self.surface,
            rect=((0,0), self.size),
            color=(50, 50, 50),
            rad=2,
            border=1,
            inside=self.color
        )
    
    def update(self, dt):
        pass


class ItemList(Widget):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.items = []

    def __setitem__(self, name, item):
        self.items.append(Item(item, name, (self.w, 25)))

    def draw(self, surface):
        self.surface.fill((0, 0, 0, 0))
        aa_round_rect(
            surface = self.surface, 
            rect = (0, 0, self.w, self.h),
            color = (10, 10, 10),
            rad = 3,
            border = 0,
            inside = (20, 20, 30)
        )
        
        for n, i in enumerate(self.items):
            i.draw(self.surface)
            self.surface.blit(i.surface, (0, n*25))
        
        surface.blit(self.surface, self.pos)
    
    def on_mousebuttondown(self, event):
        if self.is_mouse_over():
            if event.button == 4:
                self.scroll -= 5
            elif event.button == 5:
                sel.scroll += 5
    def update(self, dt):
        pass