import pygame

from .widget import Widget


class Frame(Widget):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.color = (0, 0, 0)
        self.bg_color = (10, 10, 10)
        self.surface = pygame.surface.Surface(size)
        self.widgets = dict()
        self.autoclear = True
    
    def __setitem__(self, name, widget):
        self.add_widget(name, widget)
    
    def add_widget(self, name, widget):
        widget.master = self
        self.widgets[name] = widget

    def remove_widget(self, name):
        return self.widgets.pop(name)
    
    def draw(self, surface):
        if self.autoclear:
            self.surface.fill(self.bg_color)
        
        for wid in list(self.widgets.values()):
            wid.draw(self.surface)
        surface.blit(self.surface, self.pos)
        super().draw(surface)

    def update(self, dt):
        for wid in list(self.widgets.values()):
            wid.update(dt)
