import pyglet
import pyglet.gl as gl
from pyglet.window import mouse

from core.camera import Camera
from core.render import Render, draw_circle
from graphicutils import graphicutils
from .context import Context
from core.rigidbody import RigidBody


class ContextWrapper:
    def __init__(self, w, h):
        self.__context = Context(0, 0, w, h)
        self.__camera = Camera(0, 0, w, h)
        self.__render = Render(self.__camera)
        self.__running = True
        self.__selection = []
        self.__selected = []
    
    @property
    def selected(self):
        return tuple(self.__selected)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.LEFT:
            self.__camera.x -= dx
            self.__camera.y -= dy
        elif buttons == mouse.RIGHT:
            if self.__selection:
                self.__selection[2] = x
                self.__selection[3] = y
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y < 0:
            if self.__camera.zoom > 0.05:
                self.__camera.zoom -= 0.05
        elif scroll_y > 0:
            self.__camera.zoom += 0.05
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.RIGHT:
            self.__selection = [x, y, x, y]

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.RIGHT:
            self.select()
            self.__selection = []
    
    def resize(self, w, h):
        self.__camera.w = w
        self.__camera.h = h

    def select(self):
        if self.__selection:
            self.__selected.clear()
            x1, y1, x2, y2 = self.__selection
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))
            zoom = self.__camera.zoom
            for obj in self.__context.objects:
                x = obj.x * zoom + self.__camera.centerx
                y = obj.y * zoom + self.__camera.centery
                if x1 < x < x2 and y1 < y < y2:
                    self.__selected.append(obj)
    
    def add_object(self, *args, **kwargs):
        obj = RigidBody(*args, **kwargs)
        self.__context.objects.append(obj)
    
    def delete_selected(self):
        while self.__selected:
            obj = self.__selected.pop()
            self.__context.objects.remove(obj)
    
    def select_closer(self, x, y):
        point_x = (x - self.__camera.centerx) / self.__camera.zoom
        point_y = (y - self.__camera.centery) / self.__camera.zoom
        min_dist = 20 * self.__camera.zoom
        closer = None
        
        for obj in self.__context.objects:
            dist = ((point_x - obj.x)**2 + (point_y - obj.y)**2)**0.5
            if dist < min_dist:
                min_dist = dist
                closer = obj
        
        self.__selected.clear()
        if closer is not None:
            self.__selected = [closer]
    
    def move_camera(self, x, y):
        pass

    def select_area(self, x1, y1, x2, y2):
        pass

    def toggle_pause(self):
        self.__running = not self.__running
    
    def draw_overlayer(self):
        zoom = self.__camera.zoom

        for obj in self.__selected:
            if self.__camera.collide(obj):
                objx = int(obj.x * zoom + self.__camera.centerx)
                objy = int(obj.y * zoom + self.__camera.centery)
                draw_circle(
                    objx,
                    objy, 
                    25 * zoom,
                    (1, 0.2, 0.2, 1),
                )
        
        if self.__selection:
            x1, y1, x2, y2 = self.__selection
            gl.glColor4f(0.1, 0.2, 0.3, 0.2)
            rect = (x1, y1, x2, y1, x2, y2, x1, y2)
            pyglet.graphics.draw(
                4, gl.GL_QUADS,
                ('v2f', rect)
            )
            gl.glColor4f(0.3, 0.5, 0.8, 0.5)
            pyglet.graphics.draw(
                4, gl.GL_LINE_LOOP,
                ('v2f', rect)
            )
    
    def draw(self):
        self.__render.draw_grid()
        self.__render.draw_axes()
        for obj in self.__context.objects:
            self.__render.render(obj)
        self.draw_overlayer()
    
    def update(self, dt):
        if self.__running:
            self.__context.update(dt)
    