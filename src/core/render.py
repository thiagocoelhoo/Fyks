import pyglet
from pyglet import gl

import graphicutils as gu
from app import colors


def draw_lines(vertices):
    pyglet.graphics.draw(
        len(vertices) // 2,
        gl.GL_LINES,
        ('v2f', vertices),
    )


def draw_circle(x, y, r, color, mode=gl.GL_LINE_LOOP, resolution=32):
    gl.glColor4f(*color)
    gu.draw_circle(int(x), int(y), int(r), resolution, mode)


class Render:
    def __init__(self, camera):
        self.camera = camera
        self.colors = {
            'rigidbodycolor': (0.2, 1, 0.2, 0.1),
            'rigidbodybordercolor': (0, 1, 0, 0.5),
        }
    
    def draw_grid(self):
        size = int(30 * self.camera.zoom)
        if size > 0:
            gl.glColor3f(*colors.CONTEXT_GRID_COLOR)
            gu.draw_grid(
                self.camera.w,
                self.camera.h, 
                int(self.camera.centerx),
                int(self.camera.centery),
                size, 
                0,
                0
            )
    
    def draw_axes(self):
        center_x = int(self.camera.centerx)
        center_y = int(self.camera.centery)
        gl.glColor3f(1, 0, 0)
        gu.draw_arrow(20, 40, 40, 0)
        draw_lines((0, center_y, self.camera.w, center_y))

        gl.glColor3f(0, 1, 0)
        gu.draw_arrow(20, 40, 0, 40)
        draw_lines((center_x, 0, center_x, self.camera.h))

    def draw_path(self, obj):
        gl.glColor4f(1, 0.76, 0.12, 0.8)
        gl.glBegin(gl.GL_LINES)
        for x, y in obj.path[:100]:
            pos_x = int(x * self.camera.zoom + self.camera.centerx)
            pos_y = int(y * self.camera.zoom + self.camera.centery)
            gl.glVertex2d(pos_x, pos_y)
        gl.glEnd()
    
    def draw_object(self, obj):
        self.draw_path(obj)
        
        pos = (obj.position * self.camera.zoom)
        x = int(pos[0] + self.camera.centerx)
        y = int(pos[1] + self.camera.centery)

        gl.glColor4f(0, 1, 0, 1)
        for force in obj.forces:
            if any(force):
                w = int(force[0] * self.camera.zoom)
                h = int(force[1] * self.camera.zoom)
                gu.draw_arrow(x, y, w, h)

        gl.glColor4f(0.2, 0.5, 1, 1)
        if any(obj.velocity):
            w = int(obj.velocity[0] * self.camera.zoom)
            h = int(obj.velocity[1] * self.camera.zoom)
            gu.draw_arrow(x, y, w, h)

        gl.glColor4f(0.9, 0.29, 0.58, 1)
        if any(obj.acceleration):
            w = int(obj.acceleration[0] * self.camera.zoom)
            h = int(obj.acceleration[1] * self.camera.zoom)
            gu.draw_arrow(x, y, w, h)
        
        draw_circle(
            x,
            y, 
            20 * self.camera.zoom,
            self.colors['rigidbodycolor'],
            mode=gl.GL_POLYGON
        )
        draw_circle(
            x,
            y,
            20 * self.camera.zoom,
            self.colors['rigidbodybordercolor'],
        )
