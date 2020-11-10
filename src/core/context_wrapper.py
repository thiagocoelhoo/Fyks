import pyglet
import pyglet.gl as gl
from pyglet.window import mouse, key
import numpy as np

from core.camera import Camera
from core.render import Render, draw_circle
from .context import Context
from core.rigidbody import RigidBody
from constants import *


class ContextWrapper(Context):
    def __init__(self, w, h):
        super().__init__()
        self._camera = Camera(0, 0, w, h)
        self._render = Render(self._camera)
        self._running = False
        self._selection = []
        self._selected = []
        self._mode = None
        self._frames = []

        self.mode = SELECT_MODE
    
    @property
    def selected(self):
        return tuple(self._selected)
    
    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, value):
        if value == SELECT_MODE:
            self._render.colors['rigidbodycolor'] = (0.2, 1, 0.2, 0.1)
            self._render.colors['rigidbodybordercolor'] = (0, 1, 0, 0.5)
        elif value == MOVE_MODE:
            self._render.colors['rigidbodycolor'] = (1, 0.8, 0.3, 0.5)
            self._render.colors['rigidbodybordercolor'] = (1, 0.5, 0.2, 1)
        self._mode = value

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.RIGHT:
            self.move_camera(-dx, -dy)
        elif buttons == mouse.LEFT:
            if self.mode == SELECT_MODE:
                if self._selection:
                    self._selection[2] = x
                    self._selection[3] = y
                    self.select()
            elif self.mode == MOVE_MODE:
                self.move_selected(
                    x=dx / self._camera.zoom, 
                    y=dy / self._camera.zoom
                )
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y < 0:
            if self._camera.zoom > 0.05:
                self._camera.zoom -= 0.05
        elif scroll_y > 0:
            self._camera.zoom += 0.05
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.mode == SELECT_MODE and button == mouse.LEFT:
            self._selection = [x, y, x, y]

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            if self.mode == SELECT_MODE:
                self.select()
                self._selection = []
            elif self.mode == MOVE_MODE:
                self.mode = SELECT_MODE
    
    def resize(self, w, h):
        self._camera.w = w
        self._camera.h = h

    def select(self):
        if self._selection:
            self._selected.clear()
            x1, y1, x2, y2 = self._selection
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))
            zoom = self._camera.zoom
            for obj in self._objects:
                pos = obj.position * zoom
                x = pos[0] + self._camera.centerx + 60
                y = pos[1] + self._camera.centery
                if x1 < x < x2 and y1 < y < y2:
                    self._selected.append(obj)
    
    def add_object(self, *args, **kwargs):
        obj = RigidBody(*args, **kwargs)
        self._objects.append(obj)
    
    def delete_selected(self):
        while self._selected:
            obj = self._selected.pop()
            self._objects.remove(obj)
    
    def select_closer(self, x, y):
        point_x = (x - self._camera.centerx) / self._camera.zoom
        point_y = (y - self._camera.centery) / self._camera.zoom
        min_dist = 20 * self._camera.zoom
        closer = None
        
        for obj in self._objects:
            dist_x = point_x - obj.position[0]
            dist_y = point_y - obj.position[1]
            dist = (dist_x*dist_x + dist_y*dist_y)**0.5

            if dist < min_dist:
                min_dist = dist
                closer = obj
        
        self._selected.clear()
        if closer is not None:
            self._selected = [closer]
    
    def select_area(self, x1, y1, x2, y2):
        pass

    def move_camera(self, dx, dy):
        self._camera.x += dx
        self._camera.y += dy

    def move_selected(self, x, y):
        for obj in self.selected:
            obj.position += (x, y)

    def toggle_pause(self):
        self._running = not self._running
    
    def camera_to_home(self):
        self._camera.to_home()

    def draw_overlayer(self):
        zoom = self._camera.zoom

        for obj in self._selected:
            if self._camera.collide(obj):
                pos = obj.position * zoom
                objx = int(pos[0] + self._camera.centerx)
                objy = int(pos[1] + self._camera.centery)
                draw_circle(objx, objy, 25 * zoom, (1, 0.2, 0.2, 1))
        
        if self._selection:
            x1, y1, x2, y2 = self._selection
            rect = (x1, y1, x2, y1, x2, y2, x1, y2)

            gl.glColor4f(0.1, 0.2, 0.3, 0.2)
            pyglet.graphics.draw(4, gl.GL_QUADS, ('v2f', rect))
            gl.glColor4f(0.3, 0.5, 0.8, 0.5)
            pyglet.graphics.draw(4, gl.GL_LINE_LOOP, ('v2f', rect))
    
    def draw(self):
        self._render.draw_grid()
        self._render.draw_axes()
        for obj in self._objects:
            self._render.draw_object(obj)
        self.draw_overlayer()
    
    def update(self, dt):
        if self._running:
            self._update(dt)
