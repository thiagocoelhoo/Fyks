from pyglet import gl

from .widget import Widget
from app import colors
import graphicutils as gu


class Slidebar(Widget):
    def __init__(self, x, y, w, h, attribute=None, parent=None):
        super().__init__(x, y, w, h, parent)
        self._value = 0
        self.background_color = (0.2, 0.2, 0.2, 1)
        self.inside_color = (0.2, 0.5, 1, 0.5)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.pressed:
            self.value += dx / self.width
            self.value = min(1, self.value)
            self.value = max(0, self.value)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.pressed:
            self.pressed = False
    
    def draw(self):
        x = self.x 
        y = self.y

        gl.glColor4f(*self.background_color)
        gu.draw_rounded_rect(x, y, self.width, self.height, 3, gl.GL_POLYGON)

        gl.glColor4f(*self.inside_color)
        w = max(6, int(self.value * (self.width - 4)))
        gu.draw_rounded_rect(x + 2, y + 2, w, self.height - 4, 3, gl.GL_POLYGON)