from pyglet.gl import *

from ui import Widget, Frame, Button
from graphicutils import graphicutils


class Subwindow(Frame):
    def __init__(self, x, y, w, h, parent):
        super().__init__(x, y, w, h + 22, parent)
        self.frame = Frame(0, 0, w, h)
        self.close_bt = Button(
            x=w - 21,
            y=h + 1,
            w=20,
            h=20,
            text='',
            command=self.close
        )
        self.content = [self.frame, self.close_bt]
        self.move = False

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        if self.x < x < self._right and self._top - 30 < y < self._top:
            self.move = True
        else:
            self.move = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        if self.move:
            self.x += dx
            self.y += dy

    def close(self):
        self.display = False

    def draw(self, offset_x=0, offset_y=0):
        x = self.x + offset_x
        y = self.y + offset_y
        bar_height = 22

        # Draw top bar
        glColor4f(0.15, 0.15, 0.2, 1)
        graphicutils.draw_rect(
            x, y + self.h - bar_height,
            self.w, bar_height,
            GL_QUADS
        )
        self.close_bt.draw(offset_x=x, offset_y=y)

        # Draw window content
        self.frame.draw(offset_x=x, offset_y=y)

    def update(self, dt):
        self.frame.update(dt)
