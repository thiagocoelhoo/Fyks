import pyglet
from pyglet.gl import *
import math

from core.camera import Camera
from core.render import Render, draw_circle
from graphicutils import graphicutils
from ui import Widget


class Context(Widget):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.camera = Camera(0, 0, w, h)
        self.context_render = Render(self.camera)
        self.objects = []
        self.selection = None
        self.selected = []
    
    def select(self):
        if self.selection:
            self.selected.clear()
            x1, y1, x2, y2 = self.selection
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))
            zoom = self.camera.zoom
            for obj in self.objects:
                x = obj.x * zoom + self.camera.centerx
                y = obj.y * zoom + self.camera.centery
                if x1 < x < x2 and y1 < y < y2:
                    self.selected.append(obj)
    
    def select_closer(self, x, y):
        point_x = (x - self.camera.centerx) / self.camera.zoom
        point_y = (y - self.camera.centery) / self.camera.zoom
        min_dist = 25 * self.camera.zoom
        closer = None
        
        for obj in self.objects:
            dist = math.hypot(point_x - obj.x, point_y - obj.y)
            if dist < min_dist:
                min_dist = dist
                closer = obj
        
        self.selected.clear()
        if closer is not None:
            self.selected = [closer]

    def delete_selected(self):
        while self.selected:
            obj = self.selected.pop()
            self.objects.remove(obj)
    
    def draw_overlayer(self):
        zoom = self.camera.zoom
        for obj in self.selected:
            if self.camera.collide(obj):
                objx = int(obj.x * zoom + self.camera.centerx)
                objy = int(obj.y * zoom + self.camera.centery)
                draw_circle(
                    objx,
                    objy, 
                    25 * self.camera.zoom,
                    (1, 0.2, 0.2, 0.3),
                    mode=GL_POLYGON
                )
                draw_circle(
                    objx,
                    objy, 
                    25 * self.camera.zoom,
                    (1, 0.2, 0.2, 0.5),
                )
        
        if self.selection is not None:
            x1, y1, x2, y2 = self.selection
            glColor4f(0.1, 0.1, 0.3, 0.2)
            rect = (x1, y1, x2, y1, x2, y2, x1, y2)
            pyglet.graphics.draw(
                4, GL_QUADS,
                ('v2f', rect)
            )
            glColor4f(0.3, 0.3, 0.8, 0.5)
            pyglet.graphics.draw(
                4, GL_LINE_LOOP,
                ('v2f', rect)
            )

    def draw(self, offset_x=0, offset_y=0):
        glColor4f(0.2, 0.2, 0.2, 1)
        graphicutils.draw_rect(
            self.x + offset_x,
            self.y + offset_y,
            self.w, self.h,
            GL_QUADS
        )
        self.context_render.draw_grid()
        self.context_render.draw_axes()
        
        for obj in self.objects:
            if self.camera.collide(obj):
                self.context_render.render(obj)
        
        self.draw_overlayer()

    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)
