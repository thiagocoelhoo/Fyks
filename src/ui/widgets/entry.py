import string

from pyglet import gl
from pyglet.window import key

from ui import widgets, elements
import graphicutils as gu


class Entry(widgets.Widget):
    def __init__(self, x, y, w, h, parent=None):
        super().__init__(x, y, w, h, parent)
        self.text_label = widgets.Label(8, 6, 0, 0)
        self.text_label.text = 'Entry'
        self.text_label.lab.color = (61, 85, 94, 255)
        self.mask = string.printable

        self.border_radius = 6
    
    @elements.Element.x.setter
    def x(self, value):
        self._x = value
    
    @elements.Element.y.setter
    def y(self, value):
        self._y = value

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
            gl.glColor4f(0.95, 0.95, 0.95, 1)
        else:
            gl.glColor4f(0.8, 0.8, 0.8, 1)
        
        x = self.x + offset_x
        y = self.y + offset_y
    
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
        
        self.text_label.draw(x, y)