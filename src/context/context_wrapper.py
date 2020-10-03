import pyglet
import pyglet.gl as gl
from pyglet.window import mouse

from core.camera import Camera
from core.render import Render, draw_circle
from .context import Context
from core.rigidbody import RigidBody


class ContextWrapper(Context):
    def __init__(self, w, h):
        super().__init__()
        self._camera = Camera(0, 0, w, h)
        self._render = Render(self._camera)
        self._running = True
        self._selection = []
        self._selected = []
    
    @property
    def selected(self):
        return tuple(self._selected)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.LEFT:
            self._camera.x -= dx
            self._camera.y -= dy
        elif buttons == mouse.RIGHT:
            if self._selection:
                self._selection[2] = x
                self._selection[3] = y
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y < 0:
            if self._camera.zoom > 0.05:
                self._camera.zoom -= 0.05
        elif scroll_y > 0:
            self._camera.zoom += 0.05
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.RIGHT:
            self._selection = [x, y, x, y]

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.RIGHT:
            self.select()
            self._selection = []
    
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
                x = obj.x * zoom + self._camera.centerx
                y = obj.y * zoom + self._camera.centery
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
            dist = ((point_x - obj.x)**2 + (point_y - obj.y)**2)**0.5
            if dist < min_dist:
                min_dist = dist
                closer = obj
        
        self._selected.clear()
        if closer is not None:
            self._selected = [closer]
    
    def move_camera(self, x, y):
        pass

    def select_area(self, x1, y1, x2, y2):
        pass

    def toggle_pause(self):
        self._running = not self._running
    
    def set_frame(self, frame):
        self._set_frame(frame)
    
    def draw_overlayer(self, x, y):
        zoom = self._camera.zoom

        for obj in self._selected:
            if self._camera.collide(obj):
                objx = int(obj.x * zoom + self._camera.centerx) + x
                objy = int(obj.y * zoom + self._camera.centery) + y
                draw_circle(
                    objx,
                    objy, 
                    25 * zoom,
                    (1, 0.2, 0.2, 1),
                )
        
        if self._selection:
            x1, y1, x2, y2 = self._selection
            rect = (x1, y1, x2, y1, x2, y2, x1, y2)

            gl.glColor4f(0.1, 0.2, 0.3, 0.2)
            pyglet.graphics.draw(
                4, gl.GL_QUADS,
                ('v2f', rect)
            )
            gl.glColor4f(0.3, 0.5, 0.8, 0.5)
            pyglet.graphics.draw(
                4, gl.GL_LINE_LOOP,
                ('v2f', rect)
            )
    
    def draw(self, x, y):
        self._render.draw_grid(x, y)
        self._render.draw_axes(x, y)
        for obj in self._objects:
            self._render.draw_object(obj, offset_x=x, offset_y=y)
        self.draw_overlayer(x, y)
    
    def update(self, dt):
        if self._running:
            self._update(dt)
    