import math


class Element:
    def __init__(self, x, y, w, h, parent=None):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

        self.parent = parent
        self.min_width = 0
        self.min_height = 0
        self.max_width = math.inf
        self.max_height = math.inf
    
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
    def top(self):
        if self.parent is not None:
            return self.parent.height - self.y - self.height
        
    @top.setter
    def top(self, value):
        if self.parent is not None:
            self.y = self.parent.height - self.height - value

    @property
    def right(self):
        if self.parent is not None:
            return self.parent.width - self.x - self.width

    @right.setter
    def right(self, value):
        if self.parent is not None:
            self.x = self.parent.width - self.width - value

    @property
    def bottom(self):
        return self.y

    @bottom.setter
    def bottom(self, value):
        self.y = value

    @property
    def left(self):
        return self.x
    
    @left.setter
    def left(self, value):
        self.x = value

    @property
    def width(self):
        return int(self._w)
    
    @width.setter
    def width(self, value):
        if value < self.min_width:
            self._w = self.min_width
        elif value > self.max_width:
            self._w = self.max_width
        else:
            self._w = value
    
    @property
    def height(self):
        return int(self._h)

    @height.setter
    def height(self, value):
        if value < self.min_height:
            self._h = self.min_height
        elif value > self.max_height:
            self._h = self.max_height
        else:
            self._h = value

    @property
    def global_position(self):
        x = self.x
        y = self.y
        if self.parent is not None:
            parent_position = self.parent.global_position
            x += parent_position[0]
            y += parent_position[1]
        return (x, y)
    
    def resize(self, width, height):
        self.width = width
        self.height = height
