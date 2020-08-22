from pyglet.gl import *

from ui import Frame, Button, Label
from graphicutils import graphicutils


class Subwindow(Frame):
    def __init__(self, x, y, w, h, title, parent):
        self._bar_height = 20
        
        super().__init__(
            x=x, y=y,
            w=w, h=h + 22,
            parent=parent
        )
        
        self.frame = Frame(0, 0, w, h)
        self.close_bt = Button(
            x=w - 18,
            y=h + 4,
            w=16,
            h=16,
            text='',
            command=self.close
        )
        self.children = [self.frame, self.close_bt]
        self.title_label = Label(
            x=4, y=self._top - 16,
            w=self.w-21, h=16)

        self.title_label.font_size = 14
        self.title_label.text = title
        self.title_label.lab.color = (130, 130, 130, 255)

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
        self.is_visible = False
    
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
        self.close_bt.draw(x, y)
        self.title_label.draw(x, y)

        # Draw window children
        self.frame.draw(x, y)
    

    def update(self, dt):
        self.frame.update(dt)