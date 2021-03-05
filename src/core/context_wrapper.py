from .context import Context
from utils import singleton
from core.camera import Camera
from core.rigidbody import RigidBody
from constants import *


class ContextWrapper(metaclass=singleton.Singleton):
    def __init__(self, w, h):
        self._context = Context()
        self._camera = Camera(0, 0, w, h)
        self._camera.set_active()
        self._running = False
        self._mode = SELECT_MODE
        self._selected = []
        self._ruler = None
        self._selection_area = None
        self._frames = []

    def get_ruler(self):
        return self._ruler
    
    def set_ruler(self, *args):
        self._ruler = args

    def get_objects(self):
        return self._context._objects

    def get_camera(self):
        return self._camera
    
    def get_selected(self):
        return tuple(self._selected)
    
    def get_mode(self):
        return self._mode

    def get_selection_area(self):
        return self._selection_area

    def set_selection_area(self, x1, y1, x2, y2):
        if x1 - x2 == 0 or y1 - y2 == 0:
            self.select_area = None
        else:
            self._selection_area = (x1, y1, x2, y2)
    
    def set_select_mode(self):
        self._mode = SELECT_MODE

    def set_move_mode(self):
        self._mode = MOVE_MODE

    def set_ruler_mode(self):
        self._mode = RULER_MODE
    
    def resize(self, w, h):
        self._camera.w = w
        self._camera.h = h

    def add_object(self, *args, **kwargs):
        obj = RigidBody(*args, **kwargs)
        self._context._objects.append(obj)
    
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
    
    def select_area(self):
        if self._selection_area is not None:
            x1, y1, x2, y2 = self._selection_area
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))
            
            zoom = self._camera.zoom
            for obj in self._objects:
                pos = obj.position * zoom
                x = pos[0] + self._camera.centerx
                y = pos[1] + self._camera.centery
                if x1 < x < x2 and y1 < y < y2:
                    self._selected.append(obj)

    def zoom_out(self, x, y):
        if self._camera.zoom > 0.05:
            self._camera.zoom *= 10/11
    
    def zoom_in(self, x, y):
        self._camera.zoom *= 11/10    
    
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

    def update(self, dt):
        if self._running:
            self._update(dt)
