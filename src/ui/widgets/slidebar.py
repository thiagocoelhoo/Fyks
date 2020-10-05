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
        # if self.pressed:
        self.value += dx / self.w
        self.value = min(1, self.value)
        self.value = max(0, self.value)

    def draw(self, offset_x, offset_y):
        x = self.x + offset_x
        y = self.y + offset_y

        gl.glColor4f(*self.background_color)
        gu.draw_rounded_rect(x, y, self.w, self.h, 3, gl.GL_POLYGON)

        gl.glColor4f(0.5, 0.8, 1, 0.05)
        gu.draw_rounded_rect(x + 5, y + 5, self.w - 10, 6, 3, gl.GL_POLYGON)

        gl.glColor4f(*self.inside_color)
        gu.draw_rounded_rect(x + 5, y + 5, 
            int(self.value * (self.w - 10)), 6, 3, gl.GL_POLYGON)