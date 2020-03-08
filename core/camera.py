import pygame


class Camera:
    def __init__(self, position, size):
        self.area = pygame.Rect([position, size])
        self.position = list(position)
        self._x, self._y = position
        self._z = 1
        self.size = size
    
    @property
    def w(self):
        return self.size[0]
    
    @property
    def h(self):
        return self.size[1]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.area.centerx = self.position[0] + self.size[0] * self.zoom / 2

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.area.centery = self.position[1] + self.size[1] * self.zoom / 2

    @property
    def centerx(self):
        return self.area.w / 2 - self.x
    
    @property
    def centery(self):
        return self.area.h / 2 - self.y
    
    @property
    def left(self):
        return int(self._x - self.area.w / 2)

    @property
    def top(self):
        return int(self._y - self.area.h / 2)
    
    @property
    def right(self):
        return int(self._x + self.area.w / 2)

    @property
    def bottom(self):
        return int(self._y + self.area.h / 2)

    @property
    def zoom(self):
        return self._z

    @zoom.setter
    def zoom(self, value):
        self._z = value
        self.area.w = self.size[0] * self.zoom
        self.area.h = self.size[1] * self.zoom
        self.area.centerx = self.position[0] + self.size[0] * self.zoom / 2
        self.area.centery = self.position[1] + self.size[1] * self.zoom / 2

    def move(self, x_offset, y_offset):
        self._x += x_offset
        self._y += y_offset
    
    def collide(self, obj):
        # area = list(self.area)
        # area[2] /= self.zoom
        # area[3] /= self.zoom
        # return pygame.Rect(area).colliderect(obj.get_rect())
        # return self.area.colliderect(obj.get_rect()
        return obj.x <= self.right and self.left <= obj.x + obj.r and\
            obj.y <= self.bottom and self.top <= obj.y + obj.r
