import pygame

from .widget import Widget
import core


class Frame(Widget):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.autoclear = True
        self.container = True

        self.surface = pygame.surface.Surface(size)
        self.color = (0, 0, 0)
        self.bg_color = core.theme["frame-background-color"]
        self.widgets = dict()

    def __setitem__(self, name, widget):
        self.add_widget(name, widget)

    def delete(self):
        for name, widget in list(self.widgets.items()):
            widget.delete()
            del self.widgets[name]
            del widget

    def add_widget(self, name, widget):
        widget.master = self
        self.widgets[name] = widget

    def remove_widget(self, name):
        try:
            return self.widgets.pop(name)
        except Exception as e:
            print(str(e))
            return self

    def draw(self, surface):
        if self.autoclear:
            self.surface.fill(self.bg_color)
        
        for wid in list(self.widgets.values()):
            wid.draw(self.surface)
        surface.blit(self.surface, self.pos)

    def update(self, dt):
        for wid in list(self.widgets.values()):
            wid.update(dt)
