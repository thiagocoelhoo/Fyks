import pygame


class Camera:
    def __init__(self, position, size):
        self.area = pygame.Rect([position, size])
        self.position = list(position)
        self.size = size
        self._z = 1
    
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
        self.area.centerx = (self.position[0] + self.size[0]/2) * self.zoom
    
    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, value):
        self.position[1] = value
        self.area.centery = (self.position[1] + self.size[1]/2) * self.zoom
    
    @property
    def zoom(self):
        return self._z
    
    @zoom.setter
    def zoom(self, value):
        self._z = value
        self.area.w = self.size[0] * self._z
        self.area.h = self.size[1] * self._z
        self.area.centerx = (self.position[0] + self.size[0]/2) * self.zoom
        self.area.centery = (self.position[1] + self.size[1]/2) * self.zoom

    def collide(self, obj):
        # area = list(self.area)
        # area[2] /= self.zoom
        # area[3] /= self.zoom
        # return pygame.Rect(area).colliderect(obj.get_rect())
        return self.area.colliderect(obj.get_rect())
