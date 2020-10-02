import pyglet
from pyglet import gl
import numpy as np

from ui.widgets.widget import Widget
from app import colors
import graphicutils as gu
from context.context_wrapper import ContextWrapper

wrapper = ContextWrapper(0, 0)

pause_icon = pyglet.image.load('assets/pause_icon.png')
play_icon = pyglet.image.load('assets/play_icon.png')


class Timeline(Widget):
    def __init__(self, parent):
        super().__init__(
            x=60 + 10 + 30,
            y=10,
            w=parent.w - 60 - 20 - 30,
            h=16, 
            parent=parent
        )
        self.value = 0

    def update(self, dt):
        if wrapper._running:
            self.value += 1
            self.value %= 1
    
    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        if self.is_hover:
            f = (x - self.x) / self.value
            frame = int(wrapper._frame * f)
            wrapper.set_frame(frame)
    
    def draw(self, offset_x, offset_y):
        x = self.x + offset_x
        y = self.y + offset_y

        gl.glColor4f(*colors.TIMELINE_BACKGROUND_COLOR)
        gu.draw_rounded_rect(x, y, self.w, self.h, 3, gl.GL_POLYGON)

        gl.glColor4f(0.5,0.8, 1, 0.05)
        gu.draw_rounded_rect(x + 5, y + 5, self.w - 10, 6, 3, gl.GL_POLYGON)

        gl.glColor3f(0.3, 0.5, 0.7)
        gu.draw_rounded_rect(x + 5, y + 5, int(self.value * (self.w - 10)), 6, 3, gl.GL_POLYGON)

        gl.glColor4f(0.5, 0.8, 1, 0.2)
        if wrapper._running:
            pause_icon.blit(self.x - 30, self.y)
        else:
            play_icon.blit(self.x - 30, self.y)
