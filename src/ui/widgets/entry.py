import string

from pyglet import gl
from pyglet.window import key

from ui import widgets, elements
import graphicutils as gu


class Entry(widgets.Widget):
    def __init__(self, x, y, w, h, parent=None):
        super().__init__(0, 0, w, h, parent)
        self.text_label = widgets.Label(0, 0, 0, 0)
        self.text_label.text = 'Entry'
        self.text_label.lab.color = (61, 85, 94, 255)
        self.mask = string.printable
        self.padding = 8
        self.border_radius = 6
        
        self.x = x
        self.y = y
    
    @elements.Element.x.setter
    def x(self, value):
        self._x = value
        self.text_label.x = value + self.padding

    @elements.Element.y.setter
    def y(self, value):
        self._y = value
        self.text_label.y = value + self.padding

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
    
    def draw(self):
        if self.pressed:
            gl.glColor4f(0.95, 0.95, 0.95, 1)
        else:
            gl.glColor4f(0.8, 0.8, 0.8, 1)
        
        x = self.x
        y = self.y
    
        gu.draw_rounded_rect(
            x, y,
            self.width,
            self.height,
            self.border_radius,
            gl.GL_POLYGON
        )
        gl.glColor4f(0.4, 0.4, 0.4, 0.8)
        gu.draw_rounded_rect(
            x, y,
            self.width,
            self.height,
            self.border_radius,
            gl.GL_LINE_LOOP
        )
        
        self.text_label.draw()