import math

from core.camera import Camera


class Context:
    def __init__(self, x, y, w, h):
        self.w = w
        self.h = h
        self.camera = Camera(0, 0, w, h)
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
        min_dist = 20 * self.camera.zoom
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

    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)
