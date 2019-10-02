import pygame

import core
from core.camera import Camera


class Context():
    def __init__(self, framesize):
        self.surface = pygame.Surface(framesize)
        self.objects = []
        self.time = 0.0
        self.cam = Camera((-framesize[0]/2, -framesize[1]/2), framesize)
        self.mode = ''
        
        self.time  = 0

    def add_object(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        self.objects.remove(obj)
    
    def draw(self):
        self.surface.fill(core.theme["context-background"])
        self.cam.draw_grid(self.surface)
        self.cam.draw_axes(self.surface)
        for obj in self.objects:
            if self.cam.collide(obj):
                self.cam.render(self.surface, obj)

    def update(self, dt):
        
        for obj in self.objects:
            if self.mode == 'interagente':
                for obj_ in self.objects:
                    if obj != obj_:
                        for f in obj_.forces:
                            obj.temp_forces.append(f * -1)
            obj.update(dt)
