import pyglet
from pyglet import gl

import graphicutils as gu
from .button import Button
from .widget import Widget


class Iconbutton(Button):
    def __init__(self, x, y, w, h, image, parent=None, command=None):
        Widget.__init__(self, x, y, w, h, parent)
        self.image = image
        self.command = command or (lambda: print('Pressed'))
        self.pressed = False

        self.null_color = (1, 1, 1, 0.5)
        self.pressed_color = (0, 0, 0, 0)
        self.border_color = (0, 0, 0, 0)
        self.color = self.null_color

    def draw(self, offset_x=0, offset_y=0):
        gl.glColor4f(*self.color)
        self.image.blit(self.x + offset_x, self.y + offset_y)
