import pygame

import core
from core.camera import Camera
from core.rigidbody import RigidBody


class Context():
    def __init__(self, framesize):
        self.surface = pygame.Surface(framesize)
        self.objects = []
        self.time = 0.0
        self.cam = Camera((-framesize[0]/2, -framesize[1]/2), framesize)
        self.mode = ''
        
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

        for x, y in self.paths:
            pcolor = core.theme["path-color"]
            pygame.gfxdraw.filled_circle(self.surface, int(x - self.cam.area.x), int(y - self.cam.area.y), 3, (*pcolor, 100))
            pygame.gfxdraw.aacircle(self.surface, int(x - self.cam.area.x), int(y - self.cam.area.y), 3, pcolor)
        
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
        
        if self.t >= self.step:
            self.t = 0.0