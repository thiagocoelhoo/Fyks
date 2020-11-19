import math

import pyglet
import pyglet.gl as gl
from pyglet.window import mouse, key

import graphicutils as gu
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
        self._ruler = None
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
                    y=dy / self._camera.zoom)
            elif self.mode == RULER_MODE:
                x_ = (x - self._camera.centerx) / self._camera.zoom
                y_ = (y - self._camera.centery) / self._camera.zoom
                self._ruler[2] = x_
                self._ruler[3] = y_
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y < 0:
            if self._camera.zoom > 0.05:
                self._camera.zoom -= 0.05
        elif scroll_y > 0:
            self._camera.zoom += 0.05
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            if self.mode == SELECT_MODE:
                self._selection = [x, y, x, y]
            elif self.mode == RULER_MODE:
                x_ = (x - self._camera.centerx) / self._camera.zoom
                y_ = (y - self._camera.centery) / self._camera.zoom
                self._ruler = [x_, y_, x_, y_]

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            if self.mode == SELECT_MODE:
                self.select()
                self._selection = []
            else:
                # self.mode = SELECT_MODE
                pass
    
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
                x = pos[0] + self._camera.centerx
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

    def set_select_mode(self):
        self.mode = SELECT_MODE

    def set_move_mode(self):
        self.mode = MOVE_MODE

    def set_ruler_mode(self):
        self.mode = RULER_MODE

    def draw_overlayer(self):
        zoom = self._camera.zoom

        for obj in self._selected:
            if self._camera.collide(obj):
                pos = obj.position * zoom
                objx = int(pos[0] + self._camera.centerx)
                objy = int(pos[1] + self._camera.centery)
                draw_circle(objx, objy, 25 * zoom, (1, 0.2, 0.2, 1))
        
        # Draw selection area
        if self.mode == SELECT_MODE and self._selection:
            x1, y1, x2, y2 = self._selection
            rect = (x1, y1, x2, y1, x2, y2, x1, y2)

            gl.glColor4f(0.1, 0.2, 0.3, 0.2)
            pyglet.graphics.draw(4, gl.GL_QUADS, ('v2f', rect))
            gl.glColor4f(0.3, 0.5, 0.8, 0.5)
            pyglet.graphics.draw(4, gl.GL_LINE_LOOP, ('v2f', rect))
        
        # Draw ruler
        if self.mode == RULER_MODE and self._ruler is not None:
            x1 = int(self._ruler[0] * self._camera.zoom + self._camera.centerx)
            y1 = int(self._ruler[1] * self._camera.zoom + self._camera.centery)
            x2 = int(self._ruler[2] * self._camera.zoom + self._camera.centerx)
            y2 = int(self._ruler[3] * self._camera.zoom + self._camera.centery)
            
            gl.glColor4f(0.27, 0.63, 0.78, 0.8)
            gu.draw_dashed_line(x2, y2, x1, y1)
            gu.draw_circle(x1, y1, 4, 8, gl.GL_LINE_LOOP)
            gu.draw_circle(x2, y2, 4, 8, gl.GL_LINE_LOOP)

            size = math.hypot(
                self._ruler[2] - self._ruler[0],
                self._ruler[3] - self._ruler[1])
            
            label = pyglet.text.Label(
                font_name='verdana', 
                font_size=12,
                color=(255, 255, 255, 200))
            label.text = f'{size:.2f}m'
            label.x = (x1 + x2) // 2
            label.y = (y1 + y2) // 2
            label.draw()

    def draw(self):
        self._render.draw_grid()
        self._render.draw_axes()
        for obj in self._objects:
            self._render.draw_object(obj)
        self.draw_overlayer()
    
    def update(self, dt):
        if self._running:
            self._update(dt)
