import pygame
import numpy as np

import core
from core.camera import Camera
from core.render import Render
from core.rigidbody import RigidBody
from ui import Frame


class Context(Frame):
    def __init__(self, framesize):
        super().__init__((0, 0), framesize)
        self.size = framesize
        self.camera = Camera((-framesize[0]/2, -framesize[1]/2), framesize)
        self.render = Render(self.camera)
        
        self.mesh = np.zeros((framesize[0] // 40 + 1, framesize[1] // 40 + 4, 3))

        self.paths = []
        self.path_step = 0.2

        self.timer = 0
        self.paused = False
        self.objects = []

        self.mode = ''

    def pause(self):
        self.paused = not self.paused
    
    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
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
        self.render.draw_grid(self.surface)
        self.render.draw_axes(self.surface)
        self.render.draw_vector_mesh(self.surface, self.mesh)
        self.render.draw_paths(self.surface, self.paths)
        
        for obj in self.objects:
            if self.camera.collide(obj):
                self.render.render(self.surface, obj)
    
    def update(self, dt):
        # self.mesh = np.zeros(self.mesh.shape)

        for obj in self.objects:
            if not self.paused:
                obj.update(dt)

                if type(obj) == RigidBody and self.timer >= self.path_step:
                    obj_position = (obj.x, obj.y)
                    if not obj_position in self.paths:
                        self.paths.append(obj_position)

            '''
            # atualizar malha de mostragem de campo
            if self.show:
                for x in range(self.mesh.shape[0]):
                    for y in range(self.mesh.shape[1]):
                        px = self.cam.x + x * 40
                        py = self.cam.y + y * 40
                        dx = px - obj.x
                        dy = py - obj.y
                        d = (dx**2 + dy**2)**0.5
                        try:
                            self.mesh[x, y, 0] += 9e9 * obj.charge * dx / d**3 # k*q/d**2 * dx/d
                            self.mesh[x, y, 1] += 9e9 * obj.charge * dy / d**3
                            self.mesh[x, y, 2] += 9e9 * obj.charge / d**2
                        except:
                            pass
            '''
        
        if not self.paused:
            self.timer += dt
