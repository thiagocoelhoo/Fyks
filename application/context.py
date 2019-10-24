import pygame
import numpy as np

import core
from core.camera import Camera
from core.rigidbody import RigidBody
from render_engine import draw_vector, get_ang


class Context():
    def __init__(self, framesize):
        self.surface = pygame.Surface(framesize)
        self.objects = []
        self.time = 0.0
        self.cam = Camera((-framesize[0]/2, -framesize[1]/2), framesize)
        self.mode = ''
        self.size = framesize

        self.mesh = np.zeros((framesize[0] // 20 + 1, framesize[1] // 20 + 4, 3))
        self.show = False

        self.paths = []
        self.step = 0.2
        self.t = 0

    def add_object(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        self.objects.remove(obj)

    def clear(self):
        self.cam.area.x = -self.cam.area.w/2
        self.cam.area.y = -self.cam.area.h/2
        self.objects.clear()
        self.mode = ''
        self.paths.clear()
        self.time = 0
    
    def draw(self):
        self.surface.fill(core.theme["context-background"])
        self.cam.draw_grid(self.surface)
        self.cam.draw_axes(self.surface)
           
        if self.show:
            for x in range(self.mesh.shape[0]):
                for y in range(self.mesh.shape[1]):
                    pos = (x * 20, y * 20)
                    ang = get_ang(self.mesh[x, y, 0], self.mesh[x, y, 1])
                    i = self.mesh[x, y, 2]
                    if 100 > i > -100:
                        color = (150, 0, 150)
                    elif i > 100:
                        color = (255, 0, 0)
                    else:
                        color = (0, 0, 255)

                    draw_vector(self.surface, pos, 50, ang, color)
        
        for x, y in self.paths:
            pcolor = core.theme["path-color"]
            x_ = int(x * self.cam.zoom - self.cam.area.x)
            y_ = int(y * self.cam.zoom - self.cam.area.y)
            pygame.gfxdraw.filled_circle(self.surface, x_, y_, int(3 * self.cam.zoom), (*pcolor, 100))
            pygame.gfxdraw.aacircle(self.surface, x_, y_, int(3 * self.cam.zoom), pcolor)
        
        for obj in self.objects:
            if self.cam.collide(obj):
                self.cam.render(self.surface, obj)
     
    def update(self, dt):
        self.t += dt

        for obj in self.objects:
            if type(obj) == RigidBody:
                # obj.temp_forces.clear()
                if self.mode == 'interagente':
                    for obj_ in self.objects:
                        if obj != obj_:
                            for f in obj_.forces:
                                obj.temp_forces.append(f * -1)
            
            obj.update(dt)
            if type(obj) == RigidBody and self.t >= self.step:
                pos = (obj.x, obj.y)
                if not pos in self.paths:
                    self.paths.append(pos)
        
        # atualizar malha de mostragem de campo
        if self.show:
            for x in range(self.mesh.shape[0]):
                for y in range(self.mesh.shape[1]):
                    self.mesh[x, y] = (0, 0, 0)
                    for obj in self.objects:
                        px = self.cam.x + x*20
                        py = self.cam.y + y*20
                        dx = px - obj.x
                        dy = py - obj.y
                        d = (dx**2 + dy**2)**0.5
                        try:
                            self.mesh[x, y, 0] += 9e9 * obj.charge * dx / d**3 # k*q/d**2 * dx/d
                            self.mesh[x, y, 1] += 9e9 * obj.charge * dy / d**3
                            self.mesh[x, y, 2] += 9e9 * obj.charge / d**2
                        except:
                            pass
                        # print(self.mesh[x, y])
            
        if self.t >= self.step:
            self.t = 0.0
