import pygame

from .widget import Widget
from .label import Label
from render_engine import aa_round_rect, _aa_render_region
import core


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
        self.label = Label(text, (position[0] + 6, position[1] + 6))
        self.function = func or (lambda: print('Pressed'))
        self.pressed = False

        eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)
        eventhandler.add_handler(pygame.MOUSEBUTTONUP, self.on_mouseup)
    
    def on_mousedown(self, event):
        '''
        if self.is_hover():
            if event.button == 0:
                self.color = self.pressed_color
            self.pressed = True
        '''
        pass
    
    def on_mouseup(self, event):
        '''
        if event.button == 0 and self.pressed:
            self.function()
            self.pressed = False
        '''
        pass

    def update(self, dt):
        mouse_down = mouse.pressed

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
        
        #if not self.pressed:
            #if self.is_hover():
                #self.color = self.hover_color
            #else:
                #self.color = self.none_color
    
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
