import math

import pygame
import pygame.gfxdraw

import core
import render_engine
from core.rigidbody import RigidBody, ForceField


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
    
    def draw_grid(self, surface):
        color = core.theme["context-grid"]
        space = int(20 * self.zoom)
        cols = self.w / space
        rows = self.h / space
        
        for c in range(-int(cols)//2, int(cols)//2 +  1):
            x1 = (c * space - self.area.x) % int(self.w // space * space)
            y1 = 0
            y2 = self.h
            pygame.gfxdraw.vline(surface, x1, y1, y2, color)
        
        for r in range(-int(rows)//2, int(rows)//2 + 1):
            x1 = 0
            x2 = self.w
            y1 = int(r * space - self.area.y) % int(self.h // space * space)
            pygame.gfxdraw.hline(surface, x1, x2, y1, color)

    def draw_axes(self, surface):
        pygame.gfxdraw.line(surface, -self.area.x, 0, -self.area.x, self.h, (50, 255, 50))
        pygame.gfxdraw.line(surface, 0, -self.area.y, self.w, -self.area.y, (255, 50, 50))
    
    def render(self, surface, obj, v=True):
        objx = int(obj.x * self.zoom - self.area.x)
        objy = int(obj.y * self.zoom - self.area.y)

        if type(obj) == RigidBody:
            if v:
                for force in obj.forces:
                    x1 = int(obj.x * self.zoom - self.area.x)
                    y1 = int(obj.y * self.zoom - self.area.y)

                    size = (force.fx * self.zoom, force.fy * self.zoom)
                    tsize = (force.fx**2 + force.fy**2)**0.5
                    ang = render_engine.get_ang(size[0], size[1])
                    
                    if force.selected:
                        color = (69, 161, 255)
                    else:
                        color = (200, 200, 200)
                    render_engine.draw_vector(surface, (x1, y1), tsize, ang, color)

                for force in obj.temp_forces:
                    x1 = int(obj.x * self.zoom - self.area.x)
                    y1 = int(obj.y * self.zoom - self.area.y)

                    size = (force.fx * self.zoom, force.fy * self.zoom)
                    tsize = (force.fx**2 + force.fy**2)**0.5
                    ang = render_engine.get_ang(size[0], size[1])
                    
                    if force.selected:
                        color = (255, 161, 69)
                    else:
                        color = (50, 50, 50)
                    render_engine.draw_vector(surface, (x1, y1), tsize, ang, color)

            if obj.selected:
                pygame.gfxdraw.filled_circle(surface, objx, objy, int(obj.r*self.zoom), (50, 100, 100, 50))
                pygame.gfxdraw.aacircle(surface, objx, objy, int(obj.r*self.zoom), (50, 255, 100))
            else:
                pygame.gfxdraw.filled_circle(surface, objx, objy, int(obj.r*self.zoom), (255, 0, 0, 50))
                pygame.gfxdraw.aacircle(surface, objx, objy, int(obj.r*self.zoom), obj.color)

            if obj.vx or obj.vy:
                x1 = int(obj.x * self.zoom - self.area.x)
                y1 = int(obj.y * self.zoom - self.area.y)

                size = (obj.vx * self.zoom, obj.vy * self.zoom)
                tsize = (obj.vx**2 + obj.vy**2)**0.5
                ang = render_engine.get_ang(size[0], size[1])

                color = (0, 255, 0)
                render_engine.draw_vector(surface, (x1, y1), tsize, ang, color)

            if obj.ax or obj.ay:
                x1 = int(obj.x * self.zoom - self.area.x)
                y1 = int(obj.y * self.zoom - self.area.y) - 30

                size = (obj.ax * self.zoom, obj.ay * self.zoom)
                tsize = (obj.ax**2 + obj.ay**2)**0.5
                ang = render_engine.get_ang(size[0], size[1])

                color = (200, 50, 255)
                render_engine.draw_vector(surface, (x1, y1), tsize, ang, color)
        elif type(obj) == ForceField:
            if obj.selected:
                pygame.gfxdraw.aacircle(surface, objx, objy, int(obj.size * self.zoom), (50, 155, 200, 100))
                pygame.gfxdraw.filled_circle(surface, objx, objy, int(obj.size * self.zoom), (50, 155, 200, 100))

                pygame.gfxdraw.aacircle(surface, objx, objy, 10, (255, 172, 252))
                pygame.gfxdraw.filled_circle(surface, objx, objy, 10, (255, 102, 252, 200))
            else:
                pygame.gfxdraw.aacircle(surface, objx, objy, int(obj.size * self.zoom), (235, 192, 52, 100))
                pygame.gfxdraw.filled_circle(surface, objx, objy, int(obj.size * self.zoom), (235, 192, 52, 80))

                pygame.gfxdraw.aacircle(surface, objx, objy, 10, (255, 72, 22))
                pygame.gfxdraw.filled_circle(surface, objx, objy, 10, (255, 102, 52, 200))
        # pygame.gfxdraw.rectangle(surface, (self.size[0]/4, self.size[1]/4, self.area.w, self.area.h), (0, 255, 100))
