import pygame

from .frame import Frame
from .button import Button
import core

eventhandler = core.get_eventhandler()


class OptionsList(Frame):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.close_after = True
        self.length = 0
        eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)

    def set_options(self, options):
        for i, (k, f) in enumerate(options.items()):
            self.add_widget(k, Button((0, 25 * (i+self.length)), (self.w, 25), k, func=f))
        self.length += len(list(options))

    def on_mousedown(self, event):
        if event.button == 1:
            for b in self.widgets.values():
                if b.is_mouse_over():
                    b.function()
            if self.close_after:
                self.close()

    def close(self):
        for b in self.widgets.copy():
            del self.widgets[b]

        for k in self.master.widgets.copy():
            if self.master.widgets[k] == self:    
                del self.master.widgets[k]
