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
rec_icon = pyglet.image.load('assets/rec_icon.png')


class Timeline(Widget):
    def __init__(self, x, y, parent):
        super().__init__(x, y, w=parent.w - 104, h=16, parent=parent)
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
        gu.draw_rounded_rect(x + 40, y, self.w - 20, self.h, 3, gl.GL_POLYGON)

        gl.glColor4f(0.5,0.8, 1, 0.05)
        gu.draw_rounded_rect(x + 45, y + 5, self.w - 30, 6, 3, gl.GL_POLYGON)

        gl.glColor3f(0.3, 0.5, 0.7)
        gu.draw_rounded_rect(x + 45, y + 5, int(self.value * (self.w - 30)), 6, 3, gl.GL_POLYGON)

        gl.glColor4f(0.5, 0.8, 1, 0.2)
        if wrapper._running:
            pause_icon.blit(self.x, self.y + 1)
        else:
            play_icon.blit(self.x, self.y + 1)
        
        gl.glColor4f(1, 0.5, 0.8, 0.2)
        rec_icon.blit(self.x + 20, self.y + 1)