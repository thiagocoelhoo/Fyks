from pyglet import gl

from widgets.widget import Widget
from graphicutils import graphicutils as gu


class Timeline(Widget):
    def __init__(self, x, y, w, h, parent):
        super().__init__(x, y, w, h, parent)
    
    def update(self, dt):
        pass

    def draw(self, offset_x, offset_y):
        x = self.x + offset_x
        y = self.y + offset_y
        gu.draw_rounded_rect(x, y, self.w, self.h, 6, gl.GL_LINE_LOOP)
        