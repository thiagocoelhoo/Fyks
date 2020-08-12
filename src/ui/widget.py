import pyglet


class Widget:
    def __init__(self, x, y, w, h, parent=None):
        self.parent = parent
        self.display = True
        self.activated = False
        
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
            self.activated = True
            return True
        self.activated = False
        return False
    
    def on_mouse_motion(self, x, y, dx, dy):
        pass
    
    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_key_press(self, symbol, modifiers):
        pass
        
    def fill_background(self, color):
        pyglet.gl.glColor4f(*color)
        rect = (
            self.x, self.y,
            self.x + self.w, self.y,
            self.x + self.w, self.y + self.h,
            self.x, self.y + self.h
        )
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', rect)
                             )

    def draw(self, offset_x=0, offset_y=0):
        pass

    def update(self, dt):
        pass
