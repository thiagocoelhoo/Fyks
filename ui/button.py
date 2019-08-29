import pygame
import pygame.gfxdraw
import numpy as np

from .widget import Widget
from .label import Label
from render_engine import aa_round_rect, _aa_render_region


class Button(Widget):
    def __init__(self, position, size, text='Button', func=None):
        super().__init__(position, size)
        self.pressed_color = (200, 200, 200)
        self.hover_color = (180, 180, 200)
        self.none_color = (180, 180, 180)
        self.border_color = (100, 100, 100)
        self.color = self.none_color
        self.label = Label(text, (position[0] + 6, position[1] + 6))
        self.function = func or (lambda: print('Pressed'))
        self.pressed = False
    
    def update(self, dt):
        mouse_down = pygame.mouse.get_pressed()

        if self.is_hover():
            if mouse_down[0]:
                self.color = self.pressed_color
                if not self.pressed:
                    self.function()
                    self.pressed = True
            else:
                self.color = self.hover_color
                if self.pressed:
                    self.pressed = False
        else:
            self.color = self.none_color

    def draw(self, surface):
        aa_round_rect(
            surface=surface,
            rect=(self.pos, self.size),
            color=self.border_color,
            rad=2,
            border=1,
            inside=self.color
        )
        self.label.draw(surface)
