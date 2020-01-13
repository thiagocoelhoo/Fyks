import pygame

import core
from .widget import Widget


class Layout(Widget):
    def __init__(self, position):
        super().__init__(position, [230, 0])
        self.position = position
        # self.orientation = 'vertical'
        # self.padding = (0, 0, 0, 0)
        self.spacing = 5
        self.widgets = []
        self.scrollable = True
        self.scroll = 0

        self.eventhandler = core.get_eventhandler()
        self.eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)

    def add(self, widget):
        widget.master = self
        self.widgets.append(widget)
        self.size[1] += widget.size[1] + self.spacing

    def remove(self, widget):
        self.widgets.remove(widget)
        widget.master = None
    
    def pop(self, n):
        return self.widgets.pop(n)

    def on_mousedown(self, event):
        if self.scrollable and self.is_mouse_over():
            if event.button == 4 and self.scroll > 10:
                self.scroll -= 15
                for wid in self.widgets:
                    wid.y += 15
            elif event.button == 5:                
                self.scroll += 15
                for wid in self.widgets:
                    wid.y -= 15
    
    def draw(self, surface):
        p = self.position[1] - self.scroll
        
        for i, widget in enumerate(self.widgets):
            widget.render()
            widget.draw(surface, (0, p))
            p += widget.surface.get_height() + self.spacing
    
    def update(self, dt):
        for widget in self.widgets:
            widget.update(dt)
