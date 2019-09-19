import math

import pygame
import pygame.gfxdraw

import core
import render_engine
from core.rigidbody import RigidBody, ForceField


class Camera:
    def __init__(self, position, size):
        self.area = pygame.Rect([position, size])
        self.zoom = 1

    def collide(self, obj):
        return pygame.Rect(self.area).colliderect(obj.get_rect())
    
    def draw_grid(self, surface):
        color = core.theme["context-grid"]
        
        cols = self.area.w / 10 / self.zoom / 2
        rows = self.area.h / 10 / self.zoom / 2

        for c in range(-int(cols)//2, int(cols)//2 + 1):
            x1 = int(c * self.area.w / cols - self.area.x) % self.area.w
            y1 = 0
            y2 = self.area.h
            pygame.gfxdraw.vline(surface, x1, y1, y2, color)
        
        for r in range(-int(rows)//2, int(rows)//2 + 1):
            x1 = 0
            x2 = self.area.w
            y1 = int(r * self.area.h / rows - self.area.y) % self.area.h
            pygame.gfxdraw.hline(surface, x1, x2, y1, color)
        
    def draw_axes(self, surface):
        pygame.gfxdraw.line(surface, -self.area.x, 0, -self.area.x, self.area.h, (50, 255, 50))
        pygame.gfxdraw.line(surface, 0, -self.area.y, self.area.w, -self.area.y, (255, 50, 50))
    
    def render(self, surface, obj):
        objx = int(obj.x * self.zoom - self.area.x)
        objy = int(obj.y * self.zoom - self.area.y)

        if type(obj) == RigidBody:
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
            
            for fx, fy in obj.forces:
                x1 = int(obj.x * self.zoom - self.area.x)
                y1 = int(obj.y * self.zoom - self.area.y)

                size = (fx * self.zoom, fy * self.zoom)
                tsize = (fx**2 + fy**2)**0.5
                ang = render_engine.get_ang(size[0], size[1])

                color = (200, 200, 200)
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
            pygame.gfxdraw.rectangle(surface, (objx, objy, obj.w, obj.h), (200, 250, 120, 100))
