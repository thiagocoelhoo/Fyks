from pyglet import gl

from ui.widgets.widget import Widget
from graphicutils import graphicutils as gu
from app import colors


class Timeline(Widget):
    def __init__(self, parent):
        super().__init__(
            x=60 + 10,
            y=10,
            w=parent.w - 60 - 20,
            h=16, 
            parent=parent
        )
    
    def update(self, dt):
        pass

    def draw(self, offset_x, offset_y):
        x = self.x + offset_x
        y = self.y + offset_y
        gl.glColor4f(*colors.TIMELINE_BACKGROUND_COLOR)
        gu.draw_rounded_rect(x, y, self.w, self.h, 3, gl.GL_POLYGON)
        gl.glColor3f(0.3, 0.5, 0.7)
        gu.draw_rounded_rect(x + 5, y + 5, self.w - 10, 6, 3, gl.GL_POLYGON)