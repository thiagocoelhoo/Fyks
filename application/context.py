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
        self.camera = Camera((0, 0), framesize)
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
        for obj in self.objects:
            if not self.paused:
                obj.update(dt)

                if type(obj) == RigidBody and self.timer >= self.path_step:
                    offset = obj.off_x * obj.off_x + obj.off_y * obj.off_y
                    if offset > 100:
                        self.paths.append((obj.x, obj.y))
                        obj.off_x = 0
                        obj.off_y = 0
        
        if not self.paused:
            self.timer += dt
