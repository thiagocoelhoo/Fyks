import pygame

import core
from ui.widget import Widget
from ui.label import Label
from render_engine import aa_round_rect, _aa_render_region

mouse = core.get_mouse()
eventhandler = core.get_eventhandler()


class Button(Widget):
    def __init__(self, position, size, text='Button', func=None):
        super().__init__(position, size)
        self.pressed_color = core.theme["button-pressed-color"]
        self.hover_color = core.theme["button-hover-color"]
        self.none_color = core.theme["button-color"]
        self.border_color = core.theme["button-border-color"]
        self.color = self.none_color

        self.label = Label(text, (6, 6))
        self.function = func or (lambda: print('Pressed'))
        self.pressed = False

        eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)
        eventhandler.add_handler(pygame.MOUSEBUTTONUP, self.on_mouseup)

    def on_mousedown(self, event):
        if self.is_mouse_over() and not self.pressed and event.button == 1:
            self.color = self.pressed_color
            self.pressed = True
            print("pressed")
    
    def on_mouseup(self, event):
        if self.pressed and event.button == 1:
            self.function()
            self.pressed = False
        
    def update(self, dt):        
        if not self.pressed:
            if self.is_mouse_over():
                self.color = self.hover_color
            else:
                self.color = self.none_color
    
    def draw(self, surface):
        aa_round_rect(
            surface=self.surface,
            rect=((0, 0), self.size),
            color=self.border_color,
            rad=2,
            border=1,
            inside=self.color
        )
        self.label.draw(self.surface)
        surface.blit(self.surface, self.pos)