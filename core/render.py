import math

import pygame
import pygame.gfxdraw

import core
import render_engine
from core.rigidbody import RigidBody, ForceField


def rot(x, y, ang):
    return (x*math.cos(ang) - y*math.sin(ang), y*math.cos(ang) + x*math.sin(ang))


def get_ang(w, h):
    if not w:
        ang = math.pi / 2 if h > 0 else 3 * math.pi / 2
    else:
        hip = (w**2 + h**2)**0.5
        cos = w / hip
        sin = h / hip
        
        arccos = math.acos(cos)
        arcsin = math.asin(sin)

        if arcsin > 0:
            ang = arccos
        else:
            if arccos < 0:
                ang = arcsin
            else:
                ang = math.pi*2 - arccos
    
    return ang


def draw_vector(surface, pos, size, ang, color):
    local_pos = rot(size, 0, ang)
    end_pos = local_pos[0] + pos[0], local_pos[1] + pos[1]
    
    local_l_line = rot(size - 10, -5, ang)
    l_line = local_l_line[0] + pos[0], local_l_line[1] + pos[1]

    local_r_line = rot(size - 10, 5, ang)
    r_line = local_r_line[0] + pos[0], local_r_line[1] + pos[1]
    
    pygame.draw.aaline(surface, color, pos, end_pos)
    pygame.draw.aaline(surface, color, end_pos, l_line)
    pygame.draw.aaline(surface, color, end_pos, r_line)


class Render:
    def __init__(self, camera):
        self.camera = camera
        self.show_vector_mesh = False
    
    def draw_grid(self, surface):
        color = core.theme["context-grid"]
        space = int(20 * self.camera.zoom)
        cols = self.camera.w / space
        rows = self.camera.h / space
        
        for c in range(-int(cols)//2, int(cols)//2 +  1):
            x1 = (c * space - self.camera.area.x) % int(self.camera.w // space * space)
            y1 = 0
            y2 = self.camera.h
            pygame.gfxdraw.vline(surface, x1, y1, y2, color)
        
        for r in range(-int(rows)//2, int(rows)//2 + 1):
            x1 = 0
            x2 = self.camera.w
            y1 = int(r * space - self.camera.area.y) % int(self.camera.h // space * space)
            pygame.gfxdraw.hline(surface, x1, x2, y1, color)
    
    def draw_axes(self, surface):
        pygame.gfxdraw.line(surface, -self.camera.area.x, 0, -self.camera.area.x, self.camera.h, (50, 255, 50))
        pygame.gfxdraw.line(surface, 0, -self.camera.area.y, self.camera.w, -self.camera.area.y, (255, 50, 50))

    def draw_vector_mesh(self, surface, mesh):
        if self.show_vector_mesh:
            for x in range(mesh.shape[0]):
                    for y in range(mesh.shape[1]):
                        pos = (x * 40, y * 40)
                        ang = get_ang(mesh[x, y, 0], mesh[x, y, 1])
                        i = mesh[x, y, 2]

                        if 100 > i > -100:
                            color = (150, 150, 150)
                        elif i > 100:
                            color = (250, 0, 0)
                        else:
                            color = (0, 0, 255)

                        draw_vector(surface, pos, 50, ang, color)

    def draw_paths(self, surface, paths):
        for x, y in paths:
            pcolor = core.theme["path-color"]
            x_ = int(x * self.camera.zoom - self.camera.area.x)
            y_ = int(y * self.camera.zoom - self.camera.area.y)
            pygame.gfxdraw.filled_circle(surface, x_, y_, int(3 * self.camera.zoom), (*pcolor, 100))
            pygame.gfxdraw.aacircle(surface, x_, y_, int(3 * self.camera.zoom), pcolor)

    def render(self, surface, obj, vectors=True):
        objx = int(obj.x * self.camera.zoom - self.camera.area.x)
        objy = int(obj.y * self.camera.zoom - self.camera.area.y)
        
        '''
        if vectors:
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
                y1 = int(obj.y * self.zoom - self.area.y)

                size = (obj.ax * self.zoom, obj.ay * self.zoom)
                tsize = (obj.ax**2 + obj.ay**2)**0.5
                ang = render_engine.get_ang(size[0], size[1])

                color = (200, 50, 255)
                render_engine.draw_vector(surface, (x1, y1), tsize, ang, color)
        '''
        
        if obj.selected:
            pygame.gfxdraw.filled_circle(surface, objx, objy, int(obj.r*self.camera.zoom), (50, 100, 100, 50))
            pygame.gfxdraw.aacircle(surface, objx, objy, int(obj.r*self.camera.zoom), (50, 255, 100))
        else:
            pygame.gfxdraw.filled_circle(surface, objx, objy, int(obj.r*self.camera.zoom), (255, 0, 0, 50))
            pygame.gfxdraw.aacircle(surface, objx, objy, int(obj.r*self.camera.zoom), obj.color)


        # pygame.gfxdraw.rectangle(surface, (self.size[0]/4, self.size[1]/4, self.area.w, self.area.h), (0, 255, 100))
