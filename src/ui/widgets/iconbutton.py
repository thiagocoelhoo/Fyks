from pyglet import gl

from .button import Button
from .widget import Widget


class Iconbutton(Button):
    def __init__(self, x, y, w, h, image, parent=None, command=None):
        Widget.__init__(self, x, y, w, h, parent)
        self.image = image
        self.command = command or (lambda: print('Pressed'))
        self.pressed = False

        self.null_color = (1, 1, 1, 0.5)
        self.pressed_color = (0, 0, 0, 0.3)
        self.color = self.null_color

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
    
    def draw(self):
        gl.glColor4f(*self.color)
        self.image.blit(self.x, self.y)