from pyglet import gl

from .widget import Widget
from app import colors
import graphicutils as gu


class Slidebar(Widget):
    def __init__(self, x, y, w, h, parent):
        super().__init__(x, y, w, h, parent)
        self.value = 0
        self.background_color = (0.2, 0.2, 0.2, 1)
        self.inside_color = (0.2, 0.5, 1, 0.5)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.pressed:
            self.value += dx / self.w
            self.value = min(1, self.value)
            self.value = max(0, self.value)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.pressed:
            self.pressed = False
    
    def draw(self, offset_x, offset_y):
        x = self.x + offset_x
        y = self.y + offset_y

        gl.glColor4f(*self.background_color)
        gu.draw_rounded_rect(x, y, self.w, self.h, 3, gl.GL_POLYGON)

        gl.glColor4f(*self.inside_color)
        w = max(6, int(self.value * (self.w - 4)))
        gu.draw_rounded_rect(x + 2, y + 2, w, self.h - 4, 3, gl.GL_POLYGON)