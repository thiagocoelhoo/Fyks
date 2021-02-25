from core.camera import Camera
from .context import Context
from core.rigidbody import RigidBody
from constants import *


class ContextWrapper:
    def __init__(self, w, h):
        self._context = Context()
        self._camera = Camera(0, 0, w, h)
        self._running = False
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
        self._mode = value

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
    
    def update(self, dt):
        if self._running:
            self._update(dt)
