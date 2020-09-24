import string

import pyglet
from pyglet.window import key

from ui import Widget, Label
from graphicutils import graphicutils


class Entry(Widget):
    def __init__(self, x, y, w, h, parent=None):
        super().__init__(x, y, w, h, None)
        self.text_label = Label(0, 0, 0, 0)
        self.text_label.text = 'Entry'
        self.text_label.lab.color=(61, 85, 94, 255)
        self.mask = string.printable
        self._padding = 8

        self.border_radius = 6
        self.parent = parent
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, value):
        self._x = value
        self.text_label.x = value
    
    @y.setter
    def y(self, value):
        self._y = value
        self.text_label.y = value

    @property
    def text(self):
        return self.text_label.text

    @text.setter
    def text(self, value):
        self.text_label.text = value
    
    def on_key_press(self, symbol, modifiers):
        if self.pressed:
            k = chr(symbol)
            
            if k in self.mask:
                self.text += k
            elif symbol == key.BACKSPACE:
                self.text = self.text[:-1]
    
    def draw(self, offset_x, offset_y):
        if self.pressed:
            pyglet.gl.glColor4f(0.95, 0.95, 0.95, 1)
        else:
            pyglet.gl.glColor4f(0.8, 0.8, 0.8, 1)
        
        graphicutils.draw_rounded_rect(
            self.x + offset_x, 
            self.y + offset_y,
            self.w,
            self.h,
            self.border_radius,
            pyglet.gl.GL_POLYGON
        )

        pyglet.gl.glColor4f(0.4, 0.4, 0.4, 1)
        graphicutils.draw_rounded_rect(
            self.x + offset_x, 
            self.y + offset_y,
            self.w,
            self.h,
            self.border_radius,
            pyglet.gl.GL_LINE_LOOP
        )
        
        self.text_label.draw(
            offset_x + self.padding,
            offset_y + self.padding
        )