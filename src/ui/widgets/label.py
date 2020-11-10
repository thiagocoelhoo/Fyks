import pyglet

from ui import widgets


class Label(widgets.Widget):
    def __init__(self, x, y, w, h, parent=None):
        super().__init__(x, y, w, h, parent)
        self.lab = pyglet.text.Label(
            font_name='verdana', 
            color=(80, 80, 80, 240))
        self.font_size = 14

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.lab.x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.lab.y = value
    
    @property
    def text(self):
        return self.lab.text
    
    @text.setter
    def text(self, value):
        self.lab.text = value
    
    @property
    def font_size(self):
        return self.lab.font_size * 4/3

    @font_size.setter
    def font_size(self, value):
        self.lab.font_size = value * 3/4
    
    def draw(self):
        self.lab.draw()
