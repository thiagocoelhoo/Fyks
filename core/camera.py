import pygame


class Camera:
    def __init__(self, position, size):
        self.area = pygame.Rect((position, size))
        self.position = list(position)
        self.size = size
        self._z = 1
        self.cursor = [0, 0]

    @property
    def w(self):
        return self.size[0]
    
    @property
    def h(self):
        return self.size[1]

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, value):
        self.position[0] = value
        self.area.centerx = self.centerx

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, value):
        self.position[1] = value
        self.area.centery = self.centery

    @property
    def centerx(self):
        return self.size[0] / 2 - self.x
    
    @property
    def centery(self):
        return self.size[1] / 2 - self.y
    
    @property
    def left(self):
        return int(self.x - self.w / 2)

    @property
    def top(self):
        return int(self.y - self.h / 2)
    
    @property
    def right(self):
        return int(self.x + self.w / 2)

    @property
    def bottom(self):
        return int(self.y + self.h / 2)

    @property
    def zoom(self):
        return self._z

    @zoom.setter
    def zoom(self, value):
        x, y = self.cursor
        self.x += (x - self.centerx) * (value - self.zoom)
        self.y += (y - self.centery) * (value - self.zoom)
        self._z = value
        self.area.w = self.size[0] * self.zoom
        self.area.h = self.size[1] * self.zoom
        

    def move(self, x_offset, y_offset):
        self.x += x_offset
        self.y += y_offset
    
    def collide(self, obj):
        objx = obj.x / self.zoom
        objy = obj.y / self.zoom
        return self.left <= objx <= self.right and self.top <= objy <= self.bottom
