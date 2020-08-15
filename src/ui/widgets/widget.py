import pyglet

from graphicutils import graphicutils


class Widget:
    def __init__(self, x, y, w, h, parent=None):
        self.parent = parent
        self.display = True
        self.activated = 0
        
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._padding = 0
        self._margin = 0
        self._border_radius = 4
        self._background_color = (0, 0, 0, 1)

        if parent is not None:
            parent.add(self)
        
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        self._h = value

    @property
    def padding(self):
        return self._padding
    
    @padding.setter
    def padding(self, value):
        self._padding = value
    
    @property
    def margin(self):
        return self._margin
    
    @property
    def _top(self):
        return self.y + self.h

    @property
    def _right(self):
        return self.x + self.w

    @property
    def top(self):
        if self.parent:
            height = self.parent.h
            return height - self.y - self.h
    
    @top.setter
    def top(self, value):
        if self.parent:
            height = self.parent.h
            self.y = height - self.h - value
    
    @property
    def right(self):
        if self.parent:
            width = self.parent.w
            return width - self.x - self.w
    
    @right.setter
    def right(self, value):
        if self.parent:
            width = self.parent.w
            self.x = width - value - self.w
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if self.x < x < self._right and self.y < y < self._top:
            self.activated = 1
        else:
            self.activated = 0
    
    def on_mouse_motion(self, x, y, dx, dy):
        pass
    
    def on_mouse_release(self, x, y, button, modifiers):
        pass
    
    def on_key_press(self, symbol, modifiers):
        pass

    
    def draw(self, offset_x=0, offset_y=0):
        pass

    def update(self, dt):
        pass
